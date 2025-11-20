# Data quality notes — Combined dataset

## Main data quality risks
- Dataset spans 96 rows and 19 columns (monthly 2018-01 to 2025-11); one row has a missing `Date` with all indicators empty and should be removed to avoid carrying null-only data.
- `ffpi_energy_consumption` and `energy_imported` failed to parse and are 100% missing after cleaning (96 nulls each), so they are unusable unless we re-parse the raw strings with more aggressive delimiter stripping.
- Core FFPI and climate indicators each have 2–4 missing values concentrated in late 2025, so the most recent months are incomplete and should be treated cautiously.
- `usd_hkd_rate` is constant at 7.8 across the sample and redundant with `ffpi_usd_hkd_rate`.
- Twelve months are flagged by the IQR outlier detector (mostly 2019–2020 spikes/dips); they are retained but warrant review in analysis.

## Confirmed cleaning steps to keep
- Parse `Date` to monthly datetime (`YYYY-MM-01`) and normalize column names to snake_case (e.g., `ffpi_energy_consumption`, `energy_imported`, `usd_hkd_rate`).
- Remove thousand separators and stray spaces from numeric strings (e.g., `bdi_price`, energy measures, retail sales) before float conversion.
- Drop the fully empty final row (missing `Date` and indicators) to maintain a clean 95-month panel.
- Keep the duplicate check (0 duplicates found) and retain rows while appending `flag_iqr_outlier` and `flag_negative_values` boolean columns for downstream filtering instead of hard deletions.
- Save the cleaned table to `data/cleaned.csv` for reuse in the baseline EDA and later steps.

## Columns to drop or derive for analysis
- Exclude `usd_hkd_rate` from modeling and visuals because it is constant and redundant.
- If the energy columns remain all-null after retrying stricter parsing, drop them from analysis; otherwise rerun cleaning to recover numeric values.
- Derive month/year helper fields from `date` if needed for grouping, and use the flag columns to optionally filter outliers rather than deleting them.
