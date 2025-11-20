# Data quality notes – Combined dataset

## Main data quality risks
- Dataset now spans 95 rows and 20 columns (monthly 2018-01 to 2025-11) after dropping the null-only final row; the latest month (2025-11) is still mostly missing across KPIs.
- Energy fields (`ffpi_energy_consumption`, `energy_imported`) successfully parse to numeric after removing spaces/commas but each has 2 missing values.
- Core FFPI and climate indicators each have 1–3 missing values, concentrated in late 2025, so the freshest months remain incomplete.
- `usd_hkd_rate` is constant at 7.8 and removed; `ffpi_usd_hkd_rate` is retained.
- Seventeen months are flagged by the IQR outlier detector (kept for transparency); no negative values remain.

## Confirmed cleaning steps to keep
- Parse `Date` to monthly datetime (`YYYY-MM-01`), normalize column names to snake_case, and trim internal whitespace in string fields.
- Remove commas/spaces from numeric strings (shipping, energy, FX, retail) before float conversion; drop any fully empty rows.
- Drop columns that are all-null or constant (e.g., `usd_hkd_rate`) while keeping outlier/negative flags instead of deleting rows.
- Save cleaned outputs to `data/clean/data_clean.parquet` (primary) and `data/clean/data_clean.csv`, with a legacy copy at `data/cleaned.csv` for existing notebooks.

## Columns to drop or derive for analysis
- `usd_hkd_rate` is already removed; energy columns remain usable after parsing and should be kept.
- Derive month/year/regime helpers from `date` as needed for grouping, and optionally filter outliers using the flag columns rather than hard deletions.
