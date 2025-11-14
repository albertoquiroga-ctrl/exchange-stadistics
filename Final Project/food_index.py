#!/usr/bin/env python3
"""Fetch the Food Price Index dataset without requiring an R installation.

This script mirrors the outputs of the original `foodIndex.R` utility by
discovering the latest FAO release (preferred) or falling back to the
IMF/FRED monthly series when FAO is unavailable.  It writes:
  - data/ffpi_monthly.csv
  - data/ffpi_monthly.xlsx  (sheet 'data' plus a 'meta' sheet)
  - data/ffpi_readme.txt
"""

from __future__ import annotations

import argparse
import datetime as dt
import io
import os
import re
import textwrap
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Tuple
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests


START_YEAR_DEFAULT = 2010
FAO_PAGES = [
    "https://www.fao.org/worldfoodsituation/foodpricesindex/en/",
    "https://www.fao.org/worldfoodsituation/foodpricesindex/",
    "https://www.fao.org/worldfoodsituation/foodpricesindex",
]
FAO_REGEX = re.compile(r"(?i)(food[ _-]?price[ _-]?indices|ffpi).*\.(csv|xlsx?)$")
DATE_CANDIDATES = [
    "date",
    "month",
    "period",
    "time",
    "reference_month",
    "year_month",
]
SERIES_PATTERNS = {
    "ffpi_food": [r"^food$", r"food_price_index", r"fao_food", r"^ffpi$"],
    "ffpi_cereals": [r"cereal"],
    "ffpi_veg_oils": [r"veg", r"vegetable.*oil"],
    "ffpi_dairy": [r"dairy"],
    "ffpi_meat": [r"meat"],
    "ffpi_sugar": [r"sugar"],
}
USER_AGENT = "ffpi-fetch-python/1.0"


def log(message: str, *args: object) -> None:
    timestamp = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    text = message % args if args else message
    print(f"[{timestamp} UTC] {text}")


def clean_column(name: str) -> str:
    cleaned = re.sub(r"[^0-9a-z]+", "_", name.lower()).strip("_")
    return cleaned or "col"


def extract_links(html: str) -> Iterable[str]:
    return re.findall(r'href=["\']([^"\']+)["\']', html, flags=re.IGNORECASE)


def http_get(
    url: str,
    *,
    timeout: int = 30,
    max_attempts: int = 3,
) -> requests.Response:
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(
                url,
                headers={"User-Agent": USER_AGENT},
                timeout=timeout,
            )
            if response.status_code >= 200 and response.status_code < 300:
                return response
            last_exc = RuntimeError(
                f"{url} returned status {response.status_code}"
            )
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
        if attempt < max_attempts:
            time.sleep(0.75 * attempt)
    raise RuntimeError(f"Failed to GET {url}") from last_exc


def discover_fao_resource() -> str:
    for page in FAO_PAGES:
        log("Scanning FAO page: %s", page)
        try:
            resp = http_get(page)
        except Exception as exc:  # noqa: BLE001
            log("  - skipped (%s)", exc)
            continue
        links = extract_links(resp.text)
        matches = []
        for href in links:
            if FAO_REGEX.search(href or ""):
                matches.append(urljoin(page, href))
        if matches:
            matches = sorted(
                set(matches),
                key=lambda item: (not item.lower().endswith(".xlsx"), -len(item)),
            )
            chosen = matches[0]
            log("  - found FAO resource: %s", chosen)
            return chosen
    raise RuntimeError("Could not discover an FFPI download link from FAO pages.")


def parse_dates(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        dates = pd.to_datetime(
            series,
            unit="D",
            origin=pd.Timestamp("1899-12-30"),
            errors="coerce",
        )
    else:
        dates = pd.to_datetime(series, errors="coerce")
    dates = dates.dropna()
    if dates.empty:
        return dates
    return dates.dt.to_period("M").dt.to_timestamp()


def match_column(columns: Iterable[str], patterns: Iterable[str]) -> str | None:
    for pattern in patterns:
        compiled = re.compile(pattern, flags=re.IGNORECASE)
        for col in columns:
            if compiled.search(col):
                return col
    return None


def normalize_fao_table(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    cleaned_cols = [clean_column(str(col)) for col in df.columns]
    df.columns = cleaned_cols

    date_col = next((c for c in DATE_CANDIDATES if c in df.columns), df.columns[0])
    date_series = parse_dates(df[date_col])
    df = df.loc[date_series.index].copy()
    df["date"] = date_series
    df = df.dropna(subset=["date"])

    out = pd.DataFrame({"date": df["date"]})
    for target, patterns in SERIES_PATTERNS.items():
        col = match_column(df.columns, patterns)
        if col:
            out[target] = pd.to_numeric(df[col], errors="coerce")
        else:
            out[target] = pd.NA

    out = out.sort_values("date").drop_duplicates(subset="date").reset_index(drop=True)
    return out


def _infer_extension(url: str) -> str:
    path = urlparse(url).path
    suffix = Path(path).suffix.lower()
    if suffix.startswith("."):
        suffix = suffix[1:]
    return suffix or "csv"


@dataclass
class FetchResult:
    frame: pd.DataFrame
    source: str
    source_url: str
    retrieved_utc: str
    notes: str


def fetch_fao_ffpi(url: str, start_year: int) -> FetchResult:
    log("Downloading FAO FFPI file: %s", url)
    resp = http_get(url, timeout=60, max_attempts=4)
    extension = _infer_extension(url)
    content = io.BytesIO(resp.content)

    if extension in {"xls", "xlsx"}:
        raw_df = pd.read_excel(content)
    else:
        content.seek(0)
        raw_df = pd.read_csv(content)

    normalized = normalize_fao_table(raw_df)
    start_dt = dt.datetime(start_year, 1, 1)
    normalized = normalized[normalized["date"] >= pd.Timestamp(start_dt)]
    normalized = normalized.reset_index(drop=True)

    retrieved = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    normalized = normalized.assign(
        unit="Index (2014-2016=100)",
        base_period="2014-2016",
        source="FAO World Food Situation - Food Price Index",
        source_url=url,
        retrieved_utc=retrieved,
    )

    return FetchResult(
        frame=normalized,
        source="FAO World Food Situation - Food Price Index",
        source_url=url,
        retrieved_utc=retrieved,
        notes="Derived directly from the FAO Food Price Index download.",
    )


def fetch_fred_ffpi(start_year: int, api_key: str | None) -> FetchResult:
    base = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": "PFOODINDEXM",
        "observation_start": f"{start_year}-01-01",
        "frequency": "m",
        "file_type": "json",
        "sort_order": "asc",
    }
    if api_key:
        params["api_key"] = api_key
    log("Downloading FRED IMF food price index fallback.")
    request = requests.Request("GET", base, params=params).prepare()
    resp = http_get(request.url)
    payload = resp.json()
    observations = payload.get("observations", [])
    if not observations:
        raise RuntimeError("FRED response did not contain observations.")

    rows = []
    for obs in observations:
        value = obs.get("value")
        if value in {None, ".", ""}:
            continue
        try:
            numeric = float(value)
        except ValueError:
            continue
        rows.append(
            {
                "date": pd.to_datetime(obs["date"]),
                "ffpi_food": numeric,
                "ffpi_cereals": pd.NA,
                "ffpi_veg_oils": pd.NA,
                "ffpi_dairy": pd.NA,
                "ffpi_meat": pd.NA,
                "ffpi_sugar": pd.NA,
            }
        )

    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    retrieved = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    df = df.assign(
        unit="Index (2016=100)",
        base_period="2016",
        source="FRED (IMF Primary Commodity Prices, PFOODINDEXM)",
        source_url="https://fred.stlouisfed.org/series/PFOODINDEXM",
        retrieved_utc=retrieved,
    )

    notes = "Fallback series from FRED / IMF global food index (PFOODINDEXM)."
    if not api_key:
        notes += " No FRED API key detected; limited unauthenticated quota applies."

    return FetchResult(
        frame=df,
        source="FRED (IMF Primary Commodity Prices, PFOODINDEXM)",
        source_url="https://fred.stlouisfed.org/series/PFOODINDEXM",
        retrieved_utc=retrieved,
        notes=notes,
    )


def build_meta(result: FetchResult, fallback_used: bool) -> pd.DataFrame:
    frame = result.frame
    meta = [
        ("primary_source", result.source),
        ("source_url", result.source_url),
        ("retrieved_utc", result.retrieved_utc),
        ("rows", str(len(frame))),
        ("columns", ", ".join(frame.columns)),
        ("fallback_used", str(fallback_used)),
        ("notes", result.notes),
        ("generated_utc", dt.datetime.utcnow().isoformat() + "Z"),
        ("command", "python food_index.py"),
    ]
    return pd.DataFrame(meta, columns=["field", "value"])


def write_outputs(result: FetchResult, meta: pd.DataFrame, out_dir: Path) -> Tuple[Path, Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    frame = result.frame.copy()
    frame["date"] = pd.to_datetime(frame["date"]).dt.strftime("%Y-%m-%d")

    csv_path = out_dir / "ffpi_monthly.csv"
    frame.to_csv(csv_path, index=False)

    xlsx_path = out_dir / "ffpi_monthly.xlsx"
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        frame.to_excel(writer, index=False, sheet_name="data")
        meta.to_excel(writer, index=False, sheet_name="meta")

    readme_path = out_dir / "ffpi_readme.txt"
    readme_text = textwrap.dedent(
        f"""
        Food Price Index export generated on {dt.datetime.utcnow().isoformat()}Z

        Primary source : {result.source}
        Source URL     : {result.source_url}
        Rows exported  : {len(frame)}
        Outputs        : {csv_path.name}, {xlsx_path.name}

        Notes:
        {result.notes}
        """
    ).strip() + "\n"
    readme_path.write_text(readme_text, encoding="utf-8")

    return csv_path, xlsx_path, readme_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download monthly Food Price Index data without R."
    )
    parser.add_argument(
        "--fred-only",
        action="store_true",
        help="skip FAO discovery and use the FRED fallback directly",
    )
    parser.add_argument(
        "--start-year",
        type=int,
        default=START_YEAR_DEFAULT,
        help=f"Earliest year of data to keep (default {START_YEAR_DEFAULT}).",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data"),
        help="Directory where ffpi outputs will be written.",
    )
    parser.add_argument(
        "--fao-url",
        type=str,
        help="Optional explicit FAO download URL; skips discovery when provided.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    fred_key = os.getenv("FRED_API_KEY", "")
    result: FetchResult | None = None
    fallback_used = False

    if not args.fred_only:
        try:
            url = args.fao_url or discover_fao_resource()
            result = fetch_fao_ffpi(url, start_year=args.start_year)
        except Exception as exc:  # noqa: BLE001
            log("FAO fetch failed (%s).", exc)
            fallback_used = True

    if result is None:
        result = fetch_fred_ffpi(args.start_year, fred_key or None)
        fallback_used = True

    meta = build_meta(result, fallback_used=fallback_used)
    csv_path, xlsx_path, readme_path = write_outputs(result, meta, args.out_dir)
    log("Wrote %s", csv_path)
    log("Wrote %s", xlsx_path)
    log("Wrote %s", readme_path)


if __name__ == "__main__":
    main()
