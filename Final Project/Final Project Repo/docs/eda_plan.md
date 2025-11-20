# EDA Plan — Food prices, logistics, energy, climate (2018–2025)

1. **Business problem restated**  
   Build a clean, monthly panel (2018–2025) that links global food price inflation (`ffpi_food`) with shipping costs, energy use/imports, climate anomalies, FX, and local retail/wholesale indicators so policymakers can monitor which drivers dominate in different periods and craft “what-if” scenarios (e.g., freight spikes, energy shocks, climate swings).

2. **Core KPIs**  
   - Primary: Level and monthly change of `ffpi_food`.  
   - Supporting: `ffpi_cereals`, `ffpi_veg_oils`, `ffpi_meat`, `ffpi_dairy`, `ffpi_sugar`, `ipi_food`, `wpm_fish`, `rs_Dairy_Products`, `rs_Fresh`, `bdi_price`, `ffpi_Energy_Consumption`, `Engergy Imported`, `gat_land_ocean` (plus land/ocean splits), `ffpi_USD/HKD_Rate` and (for redundancy check) `USD/HKD Rate`.

3. **EDA & insight-discovery plan (in order)**  
   3.1 **Data audit & cleaning checks**  
   - Questions:  
     - Do all indicators share a consistent monthly date key (`YYYY-MM-01`) and window?  
     - Which columns need type fixes (strings with commas/spaces → numeric)?  
     - Where are missing months/values; any duplicated months or empty trailing rows?  
     - Are there obvious unit/scaling issues or outliers that look like data errors?  
   - Tables/plots:  
     - Coverage table: start/end date, non-missing count per variable.  
     - Missingness heatmap by month/variable; duplicate-month check.  
     - Summary stats (mean, sd, min/max, unique count) by variable.  
     - Outlier diagnostics (boxplots or z-score flags) per series.  
   - Decision levers:  
     - Define common analysis window; decide on forward-fill vs leave-missing.  
     - Choose variables to drop/retain (e.g., constant `USD/HKD Rate`).  
     - Flag transformations (comma/space removal, date parsing) and unit notes for documentation.

   3.2 **Baseline univariate & time-series trends**  
   - Questions:  
     - How do levels and month-on-month changes of `ffpi_food` evolve?  
     - Which FAO sub-indices drive overall volatility, and how do local HK indicators behave?  
     - Are shipping (BDI), energy, climate, and FX series trending or mean-reverting?  
   - Tables/plots:  
     - Line charts for each indicator family; optionally rebased to 2018-01=100.  
     - MoM and YoY change charts for `ffpi_food` and key drivers.  
     - Distribution plots (histograms/density) for level and change series.  
   - Decision levers:  
     - Identify which series show informative movement vs noise/flatness.  
     - Highlight time windows/episodes worth deeper focus (e.g., 2020–2022 shocks).  
     - Determine which change metrics (MoM vs YoY) to report for monitoring.

   3.3 **Segment/regime comparisons & hypothesis testing**  
   - Questions:  
     - How do averages/volatility differ across regimes: 2018–2019, 2020–2022, 2023–2025?  
     - Are shifts in FFPI mirrored by BDI, energy, climate, or FX changes in each regime?  
     - Do local HK indicators (`ipi_food`, `wpm_fish`, retail sales) diverge from global FFPI in specific periods?  
   - Tables/plots:  
     - Regime summary table (mean, sd) for KPIs and drivers.  
     - Bar/interval charts of regime means with confidence intervals.  
     - Line charts with shaded regime bands.  
     - Simple tests: t-tests or nonparametric comparisons of regime means; variance ratio checks.  
   - Decision levers:  
     - Decide whether to frame insights as “shock vs normal” contrasts.  
     - Prioritize regimes for storytelling and scenario stress points.  
     - Assess credibility of regime differences before highlighting them.

   3.4 **Co-movement, lead–lag, and dependence scan**  
   - Questions:  
     - Which drivers co-move most with `ffpi_food` contemporaneously?  
     - Are there lead–lag effects (e.g., BDI or energy leading FFPI by 1–6 months)?  
     - Are relationships stable across regimes or concentrated in specific episodes?  
   - Tables/plots:  
     - Correlation matrix and pairwise scatterplots (levels and changes).  
     - Cross-correlation functions for `ffpi_food` vs `bdi_price`, `ipi_food`, `ffpi_Energy_Consumption`.  
     - Rolling correlation/β plots over time windows.  
   - Decision levers:  
     - Select driver variables to feature in monitoring dashboards.  
     - Choose candidate lead indicators for “early warning” messaging.  
     - Decide whether climate or FX signals are strong enough to keep.

   3.5 **Stress episodes & anomaly checks (context-specific)**  
   - Questions:  
     - What happens around known shocks (COVID onset 2020, supply-chain crunch 2021, energy spikes 2022)?  
     - Do anomalies coincide with data issues (e.g., sudden zeros from reporting)?  
     - Are provisional recent months materially different from historical ranges?  
   - Tables/plots:  
     - Event-window line charts for key dates/shocks with annotations.  
     - Outlier flag tables tied to event windows.  
     - Range comparison of latest 6–12 months vs historical percentiles.  
   - Decision levers:  
     - Whether to exclude or footnote anomalous months.  
     - Which episodes to emphasize in insights and scenarios.  
     - Guidance on data freshness and provisional caveats.

   3.6 **Candidate insight harvesting & prioritization**  
   - Questions:  
     - Which relationships are strong, non-obvious, and well-supported by data coverage?  
     - Which 2–3 insights best explain FFPI movements (shipping vs energy vs local factors)?  
     - Which visuals will be most persuasive for policymakers?  
   - Tables/plots:  
     - Scoring table ranking candidate relationships by effect size, stability, and coverage.  
     - Shortlist chart drafts: top correlations/lead indicators; regime mean contrasts.  
   - Decision levers:  
     - Final selection of insight narratives and charts.  
     - Recommendations for monitoring metrics (what to track monthly).  
     - Documentation priorities for the clean dataset (notes on variable relevance).
