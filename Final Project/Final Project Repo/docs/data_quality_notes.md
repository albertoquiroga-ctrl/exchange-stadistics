# Data quality notes — Combined dataset

## Snapshot

- Rows: 96  
- Columns: 19  
- Time span:
  - `Date` non-missing from 2018-01-01 to 2025-10-01.
  - One row (index 95) has `Date` and all indicators missing.
- No duplicated rows detected.

## Missingness

- `Date`: 1 missing (final row).
- Core FFPI indices (`ffpi_*`): 2 missing values each, concentrated in the last months (2025).
- Climate anomalies (`gat_*`): 4 missing values in late 2025.
- Energy indicators (`ffpi_Energy_Consumption `, `Engergy Imported `): ~3 missing each, mostly at the tail.
- FX:
  - `ffpi_USD/HKD_Rate`: 1 missing towards the end.
  - `USD/HKD Rate`: no missing but constant at 7.8.
- Local indicators (`ipi_food`, `rs_Dairy_Products`, `rs_Fresh`, `wpm_fish`): a few missing values in late 2025.

## Structural issues

- `Date` is stored as string `"DD/MM/YYYY"`, not as a proper date.
- `bdi_price`, `ffpi_Energy_Consumption `, and `Engergy Imported ` are stored as strings with commas or spaces and must be parsed to numeric.
- Column names include:
  - Trailing spaces: `ffpi_Energy_Consumption `, `Engergy Imported `.
  - Typo: `Engergy Imported `.
  - Slash and space in `USD/HKD Rate`.
- `USD/HKD Rate` is constant over time (7.8) and seems redundant with `ffpi_USD/HKD_Rate`.

## Cleaning decisions (proposed)

1. **Drop the fully empty last row** (index 95) after confirming it is not a placeholder for future data.
2. **Parse `Date`** as monthly date (`YYYY-MM-01`) using day-first parsing of the original string.
3. **Convert string numerics to floats**:
   - Remove commas and spaces from `bdi_price`, `ffpi_Energy_Consumption `, `Engergy Imported ` before casting to numeric.
4. **Standardize column names** (either in code or via a mapping):
   - Strip trailing spaces.
   - Optionally rename to snake_case (e.g. `energy_consumption_index`, `energy_imports`).
5. **Common sample window**:
   - For comparisons and correlations, use the intersection where `ffpi_food` and each driver are both non-missing.
   - For 2018-01 to 2025-10 you will still have some missing values in certain drivers; decide whether to:
     - carry NAs through in plots, or
     - restrict to months where all core variables are present, depending on the analysis.
6. **Redundant FX variable**:
   - Keep `ffpi_USD/HKD_Rate` as the main FX indicator.
   - Either drop `USD/HKD Rate` from analysis or mark it as a constant reference series.

## Risks / caveats

- Latest months (2025) are incomplete for several series and should be treated as provisional.  
- Differences in original base years and units mean that only *standardized* versions (e.g. z-scores or indexed to a common base) should be visually compared on the same axis.  
- Climate anomalies have small numeric variation in this period; they may be more useful as context than as main “drivers” in the short sample.
