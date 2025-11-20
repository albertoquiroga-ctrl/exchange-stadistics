# Baseline EDA code snippets (pandas + matplotlib/plotly)

These cells align with the business brief (monitor food price drivers across shipping, energy, climate, FX and local retail) and the EDA plan. They assume the cleaned monthly panel at `data/clean/data_clean.parquet` (CSV fallback `data/cleaned.csv`) with `date` parsed as a monthly timestamp and outlier flags retained. Energy columns now parse to numeric; the code still drops them if they are fully empty.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")
plt.style.use("seaborn-v0_8")
```

## Load and prep

```python
parquet_path = Path("Final Project/Final Project Repo/data/clean/data_clean.parquet")
csv_fallback = Path("Final Project/Final Project Repo/data/cleaned.csv")

if parquet_path.exists():
    df = pd.read_parquet(parquet_path)
elif csv_fallback.exists():
    df = pd.read_csv(csv_fallback, parse_dates=["date"])
else:
    raise FileNotFoundError("No cleaned dataset found.")

# Drop constant or all-null columns flagged in data-quality notes
null_cols = [c for c in ["ffpi_energy_consumption", "energy_imported"] if c in df.columns and df[c].isna().all()]
const_cols = [c for c in df.columns if df[c].nunique(dropna=False) == 1]
cols_to_drop = [c for c in null_cols + const_cols if c in df.columns]
df = df.drop(columns=cols_to_drop)

# Helper fields
df = df.assign(
    year=df["date"].dt.year,
    month=df["date"].dt.month,
    regime=pd.cut(
        df["date"],
        bins=pd.to_datetime([
            "2017-12-31", "2019-12-31", "2022-12-31", "2025-12-31"
        ]),
        labels=["2018-2019 (pre-COVID)", "2020-2022 (stress)", "2023-2025 (recent)"]
    ),
)
```

## Univariate distributions — key KPIs & drivers

```python
kpi_cols = [
    "ffpi_food", "ffpi_cereals", "ffpi_veg_oils", "ffpi_meat", "ffpi_dairy", "ffpi_sugar",
    "ipi_food", "wpm_fish", "bdi_price"
]

fig, axes = plt.subplots(nrows=len(kpi_cols), ncols=2, figsize=(12, 4 * len(kpi_cols)))
for i, col in enumerate(kpi_cols):
    sns.histplot(df[col], kde=True, ax=axes[i, 0], color="#2a9d8f")
    axes[i, 0].set_title(f"Distribution of {col}")
    sns.boxplot(x=df[col], ax=axes[i, 1], color="#e76f51")
    axes[i, 1].set_title(f"Boxplot of {col}")
plt.tight_layout()
plt.show()
```

## Time-series plots — overall KPIs

```python
# Levels
level_cols = ["ffpi_food", "ffpi_cereals", "ffpi_veg_oils", "ffpi_meat", "ffpi_dairy", "ffpi_sugar"]
fig = px.line(df, x="date", y=level_cols, title="FAO food indices over time")
fig.update_layout(legend_title_text="Index")
fig.show()

# Month-on-month change
for col in level_cols:
    df[f"mom_{col}"] = df[col].pct_change() * 100

mom_cols = [f"mom_{c}" for c in level_cols]
fig = px.line(df, x="date", y=mom_cols, title="MoM % change — FAO indices")
fig.update_yaxes(title_text="MoM %")
fig.show()
```

## Segment size plots — regime counts and missingness

```python
# Regime counts (segment sizes)
regime_counts = df.groupby("regime").size().reset_index(name="months")
fig = px.bar(regime_counts, x="regime", y="months", title="Months per regime (segment size)")
fig.update_layout(xaxis_title="Regime", yaxis_title="Number of months")
fig.show()

# Missingness per column
missing = df.isna().sum().reset_index(name="missing_rows").rename(columns={"index": "column"})
fig = px.bar(missing, x="column", y="missing_rows", title="Missing values per column")
fig.update_layout(xaxis_tickangle=45)
fig.show()
```

## Optional: time-series by driver family

```python
# Shipping and import prices
fig = px.line(df, x="date", y=["bdi_price", "ipi_food"], title="Shipping & import price indicators")
fig.show()

# Climate anomalies
climate_cols = [c for c in ["gat_land_ocean", "gat_land", "gat_ocean"] if c in df.columns]
if climate_cols:
    fig = px.line(df, x="date", y=climate_cols, title="Global temperature anomalies")
    fig.show()

# Local retail indicators
retail_cols = [c for c in ["rs_dairy_products", "rs_fresh", "wpm_fish"] if c in df.columns]
fig = px.line(df, x="date", y=retail_cols, title="Local retail/wholesale indicators")
fig.show()
```

## Outlier overlay on FFPI

```python
fig = px.line(df, x="date", y="ffpi_food", title="FFPI with IQR outlier flags")
outliers = df[df["flag_iqr_outlier"]]
fig.add_scatter(x=outliers["date"], y=outliers["ffpi_food"], mode="markers", 
                marker=dict(color="red", size=9), name="IQR outlier")
fig.show()
```
```
