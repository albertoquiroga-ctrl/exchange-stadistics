"""
Export the insight-validation conclusions and charts into data/derived for LLM use.

The script mirrors the computations from 04_insight_validation.ipynb:
- recompute regime windows and candidate insight stats,
- save time-series charts per insight,
- write Markdown + JSON + CSV summaries into data/derived/04_insight_validation.
Run it from anywhere inside the repo:
    python notebooks/export_insight_validation_artifacts.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import matplotlib.pyplot as plt
import pandas as pd

plt.style.use("seaborn-v0_8")

# Regime setup shared with the notebook
REGIME_ORDER = ["2018-2019", "2020-2022", "2023-2025"]
REGIME_COLORS: Dict[str, str] = {
    "2018-2019": "#d9ead3",
    "2020-2022": "#fce5cd",
    "2023-2025": "#d9d2e9",
}

# Candidate insights to validate and export
CANDIDATE_INSIGHTS: List[Dict[str, object]] = [
    {
        "id": "CI1",
        "title": "FFPI food level remains about 30 points higher after 2019",
        "kpi": "ffpi_food",
        "relevance_score": 5,
        "pairs": [("2018-2019", "2020-2022"), ("2018-2019", "2023-2025")],
    },
    {
        "id": "CI2",
        "title": "Veg oils index surged during the 2020-2022 stress window",
        "kpi": "ffpi_veg_oils",
        "relevance_score": 5,
        "pairs": [("2018-2019", "2020-2022"), ("2018-2019", "2023-2025")],
    },
    {
        "id": "CI3",
        "title": "Import price pressure (IPI food) stayed elevated through 2025",
        "kpi": "ipi_food",
        "relevance_score": 4,
        "pairs": [("2018-2019", "2023-2025"), ("2020-2022", "2023-2025")],
    },
]


def as_relative_posix(path: Path, anchor: Path) -> str:
    """Return a POSIX-style relative path when possible; fall back to absolute."""
    try:
        return path.relative_to(anchor).as_posix()
    except ValueError:
        return path.as_posix()


def locate_data_clean(start_dir: Path) -> Path:
    """Locate data_clean.(csv|parquet) walking up from the start directory."""
    rel_candidates = [
        Path("data") / "clean" / "data_clean.csv",
        Path("data") / "clean" / "data_clean.parquet",
        Path("Final Project") / "Final Project Repo" / "data" / "clean" / "data_clean.csv",
        Path("Final Project") / "Final Project Repo" / "data" / "clean" / "data_clean.parquet",
    ]
    for base in [start_dir, *start_dir.parents]:
        for rel in rel_candidates:
            candidate = (base / rel).resolve()
            if candidate.exists():
                return candidate
    raise FileNotFoundError("Could not find data/clean/data_clean.(csv|parquet)")


def assign_regime(ts: pd.Timestamp) -> str:
    year = ts.year
    if year <= 2019:
        return "2018-2019"
    if year <= 2022:
        return "2020-2022"
    return "2023-2025"


def load_frame(data_path: Path) -> pd.DataFrame:
    """Load the cleaned dataset and append the regime column."""
    if data_path.suffix == ".csv":
        df = pd.read_csv(data_path)
    else:
        df = pd.read_parquet(data_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["regime"] = df["date"].apply(assign_regime)
    df["regime"] = pd.Categorical(df["regime"], categories=REGIME_ORDER, ordered=True)
    return df


def ensure_output_dirs(data_path: Path) -> Tuple[Path, Path]:
    """Ensure data/derived/04_insight_validation and its figures dir exist."""
    data_dir = data_path.parent.parent
    export_dir = data_dir / "derived" / "04_insight_validation"
    fig_dir = export_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    return export_dir, fig_dir


def regime_windows(df: pd.DataFrame) -> List[Dict[str, object]]:
    meta = (
        df.groupby("regime", observed=False)["date"]
        .agg(start="min", end="max", rows="size")
        .reset_index()
    )
    return [
        {
            "regime": row.regime,
            "start_date": row.start.date().isoformat(),
            "end_date": row.end.date().isoformat(),
            "rows": int(row.rows),
        }
        for row in meta.itertuples(index=False)
    ]


def plot_series(df: pd.DataFrame, kpi: str, title: str, fig_path: Path) -> Path:
    """Plot KPI over time with shaded regimes and save as PNG."""
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(df["date"], df[kpi], color="#1f77b4", linewidth=1.5)
    ax.set_title(title)
    ax.set_ylabel(kpi)
    ax.set_xlabel("date")
    for reg, group in df.groupby("regime", observed=False):
        ax.axvspan(
            group["date"].min(),
            group["date"].max(),
            color=REGIME_COLORS.get(reg, "#f0f0f0"),
            alpha=0.2,
            label=reg,
        )
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), title="regime")
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(fig_path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return fig_path


def candidate_stats(
    df: pd.DataFrame, kpi: str, pairs: Iterable[Tuple[str, str]]
) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    """Compute per-regime stats and pairwise deltas for a KPI."""
    regime_stats = (
        df.groupby("regime", observed=False)[kpi]
        .agg(mean="mean", median="median", n_valid="count", n_missing=lambda s: int(s.isna().sum()))
        .reset_index()
    )
    regime_stats["mean"] = regime_stats["mean"].astype(float)
    regime_stats["median"] = regime_stats["median"].astype(float)

    pair_rows: List[Dict[str, object]] = []
    for base_reg, compare_reg in pairs:
        base_mean_series = regime_stats.loc[regime_stats["regime"] == base_reg, "mean"]
        compare_mean_series = regime_stats.loc[regime_stats["regime"] == compare_reg, "mean"]
        if base_mean_series.empty or compare_mean_series.empty:
            continue
        base_mean = float(base_mean_series.iloc[0])
        compare_mean = float(compare_mean_series.iloc[0])
        delta = compare_mean - base_mean
        ratio = compare_mean / base_mean if base_mean else None
        pair_rows.append(
            {
                "base_regime": base_reg,
                "compare_regime": compare_reg,
                "delta_mean": round(delta, 2),
                "ratio_mean": round(ratio, 2) if ratio is not None else None,
            }
        )

    regime_rows = [
        {
            "regime": row.regime,
            "mean": round(float(row.mean), 2) if pd.notna(row.mean) else None,
            "median": round(float(row.median), 2) if pd.notna(row.median) else None,
            "n_valid": int(row.n_valid),
            "n_missing": int(row.n_missing),
        }
        for row in regime_stats.itertuples(index=False)
    ]
    return regime_rows, pair_rows


def build_markdown(
    export_dir: Path,
    data_path: Path,
    windows: List[Dict[str, object]],
    insights: List[Dict[str, object]],
) -> str:
    """Construct a Markdown summary that is easy for LLMs to parse."""
    lines: List[str] = []
    lines.append("# Insight validation export")
    data_root = export_dir.parent.parent
    lines.append(f"- source_data: `{as_relative_posix(data_path, data_root)}`")
    lines.append(f"- figures_dir: `{as_relative_posix(export_dir / 'figures', data_root)}`")
    window_text = "; ".join(
        f"{w['regime']}: {w['start_date']} to {w['end_date']} (rows={w['rows']})"
        for w in windows
    )
    lines.append(f"- regime_windows: {window_text}")
    lines.append("")
    for insight in insights:
        lines.append(f"## {insight['id']} - {insight['title']}")
        lines.append(
            f"- kpi: `{insight['kpi']}` (relevance_score={insight['relevance_score']})"
        )
        lines.append(f"- figure: `{insight['figure']}`")
        sample_sizes = "; ".join(
            f"{r['regime']}: n={r['n_valid']}, missing={r['n_missing']}"
            for r in insight["regime_stats"]
        )
        lines.append(f"- sample_sizes: {sample_sizes}")
        for pair in insight["pair_deltas"]:
            lines.append(
                f"- delta {pair['compare_regime']} vs {pair['base_regime']}: "
                f"delta_mean={pair['delta_mean']}, ratio_mean={pair['ratio_mean']}"
            )
        lines.append(f"- conclusion: {insight['title']}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    start_dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    data_path = locate_data_clean(start_dir)
    df = load_frame(data_path)
    export_dir, fig_dir = ensure_output_dirs(data_path)

    windows = regime_windows(df)
    insight_records: List[Dict[str, object]] = []
    all_regime_rows: List[Dict[str, object]] = []
    all_pair_rows: List[Dict[str, object]] = []

    for insight in CANDIDATE_INSIGHTS:
        kpi = str(insight["kpi"])
        figure_path = fig_dir / f"{insight['id'].lower()}_{kpi}.png"
        plot_series(df, kpi, str(insight["title"]), figure_path)

        regime_rows, pair_rows = candidate_stats(df, kpi, insight["pairs"])
        all_regime_rows.extend(
            {**row, "insight_id": insight["id"], "kpi": kpi} for row in regime_rows
        )
        all_pair_rows.extend(
            {**row, "insight_id": insight["id"], "kpi": kpi} for row in pair_rows
        )

        insight_records.append(
            {
                "id": insight["id"],
                "title": insight["title"],
                "kpi": kpi,
                "relevance_score": insight["relevance_score"],
                "figure": str(figure_path.relative_to(export_dir.parent.parent).as_posix()),
                "regime_stats": regime_rows,
                "pair_deltas": pair_rows,
            }
        )

    markdown_body = build_markdown(export_dir, data_path, windows, insight_records)
    (export_dir / "insight_validation_summary.md").write_text(markdown_body, encoding="utf-8")

    payload = {
        "source_data": as_relative_posix(data_path, export_dir.parent.parent),
        "export_dir": as_relative_posix(export_dir, export_dir.parent.parent),
        "regime_windows": windows,
        "insights": insight_records,
    }
    (export_dir / "insight_validation_summary.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )

    if all_regime_rows:
        pd.DataFrame(all_regime_rows).to_csv(
            export_dir / "insight_regime_stats.csv", index=False
        )
    if all_pair_rows:
        pd.DataFrame(all_pair_rows).to_csv(
            export_dir / "insight_pair_deltas.csv", index=False
        )

    print(f"Saved LLM-ready artifacts to {export_dir}")


if __name__ == "__main__":
    main()
