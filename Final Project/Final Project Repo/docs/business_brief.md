# Business brief — Food prices, energy, logistics and climate (2018–2025)

## 1. Business question

How do shipping costs, energy indicators and global temperature anomalies co-move with food price inflation month-by-month over 2018–2025?

The goal of this project is **not** to run regressions, but to curate a **clean, documented multi-source monthly dataset** that is ready for modeling and monitoring. The core deliverable is the dataset + documentation, not a forecasting model.

## 2. Decision to influence

Primary decisions this dataset should support (for a hypothetical policymaker / analyst):

- Monitoring: detect periods when food price inflation appears to be driven more by shipping vs energy vs climate vs FX.
- Scenario design: “What if” reasoning about future shocks (e.g. spike in freight costs, energy disruptions).
- Communication: provide clear, documented indicators that can be used in later slides and reports.

This team project aligns with the course brief: **dataset assembly and documentation, not causal inference or ML.**

## 3. Time period and grain

- Time period: Monthly observations from **January 2018 to (at least) November 2025**.
- Grain: **Each row = one calendar month**, identified by the first day of the month in `Date` (to be normalized to `YYYY-MM-01`).

## 4. Variables and roles (high level)

Response (primary KPI):

- `ffpi_food`: FAO Food Price Index – All food (monthly, index 2014–2016 = 100).

Key explanatory indicators:

- `ffpi_cereals`, `ffpi_veg_oils`, `ffpi_dairy`, `ffpi_meat`, `ffpi_sugar`: FAO sub-indices by food group.
- `bdi_price`: Baltic Dry Index (shipping costs / capacity tightness).
- `ffpi_Energy_Consumption `: Hong Kong electricity / energy consumption index.
- `Engergy Imported `: Level of imported energy (raw; needs documentation).
- `ipi_food`: Import Price Index for food into Hong Kong.
- `wpm_fish`: Wholesale price of local marine fish.

Climate indicators:

- `gat_land_ocean`: Global land-ocean temperature anomaly (°C vs baseline).
- `gat_land`, `gat_ocean`: Land-only and ocean-only anomalies.

FX indicators:

- `ffpi_USD/HKD_Rate`: USD/HKD exchange indicator (index or level).
- `USD/HKD Rate`: Rounded spot USD/HKD rate (≈ 7.8, probably redundant).

Retail indicators:

- `rs_Dairy_Products`: Retail sales in supermarkets for dairy etc.
- `rs_Fresh`: Retail sales in supermarkets for fresh / chilled foods.

(Full column-level definitions are in `data_dictionary.md`.)

## 5. Core KPIs

- Main KPI:  
  - Level and change of `ffpi_food`.
- Supporting KPIs:
  - Sub-indices: `ffpi_cereals`, `ffpi_veg_oils`, `ffpi_meat`, `ffpi_dairy`, `ffpi_sugar`.
  - Local food-related indicators: `ipi_food`, `wpm_fish`, `rs_Dairy_Products`, `rs_Fresh`.

## 6. “Segments” / breakdown dimensions

This dataset has **no cross-sectional customers or regions**. Segmentation is mainly:

- By **indicator family**: shipping vs energy vs climate vs FX vs local retail.
- By **time regime**:
  - Pre-COVID: 2018–2019.
  - COVID & supply-chain stress: approx. 2020–2022.
  - Recent period: 2023–2025.

These regimes will be used in Step 1D for “segment” / regime comparisons.

## 7. Constraints and scope

- Scope:
  - Assemble monthly series from multiple public sources.
  - Standardize date key and basic naming/units.
  - Document coverage, transformations, and caveats.
  - Produce data dictionary and basic insight drafts.

- Out of scope for this deliverable:
  - Regression models or ML.
  - Strong causal claims.
  - Use of proprietary/paywalled data.

- Practical constraints:
  - Series may start/stop at different dates → need common sample window.
  - Latest months may be provisional or missing for some sources.
  - No access to micro-level household or firm data; all indicators are aggregates.

## 8. Intended users

- Course instructors evaluating data quality, documentation and clarity.
- Future you (or classmates) who might reuse this dataset to:
  - Build forecasting models.
  - Study specific episodes (e.g. COVID supply-chain shock).
  - Prepare editorial-style charts and decks.
