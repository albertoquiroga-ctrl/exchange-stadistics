# EDA plan — Insight discovery for food prices, energy, logistics & climate

## Section 1 — Data audit & cleaning

**Questions to answer**

1. Do all series cover the same monthly window?  
2. Are there missing months or entire rows?  
3. Which columns are stored as strings but should be numeric?  
4. Are there obvious outliers or regime breaks that look like data errors?

**Tables / plots**

- Table: row/column counts; coverage start/end per variable.  
- Table: missing values by variable.  
- Table: basic summary stats (mean, sd, min, max) for each numeric column.  
- Diagnostic plot: indicator coverage over time (stacked bars of “non-missing” counts per month).

**Decision levers informed**

- Whether to restrict analysis to a common sample window.  
- Whether to drop the fully missing last row and/or last months for certain indicators.  
- Whether to drop redundant variables (e.g. `USD/HKD Rate`).

---

## Section 2 — Baseline univariate & time-series analysis

**Questions to answer**

1. How has `ffpi_food` evolved over 2018–2025 (level and volatility)?  
2. How do the sub-indices (`ffpi_cereals`, `ffpi_veg_oils`, …) differ in level and variability?  
3. How have shipping (BDI), energy, climate and FX indicators evolved over the same period?

**Tables / plots**

- Line chart: `ffpi_food` over time.  
- Line chart: FAO sub-indices in one panel (normalized to 2018-01 = 100 if needed).  
- Line charts: `bdi_price`, `ffpi_Energy_Consumption`, `ipi_food`, `gat_land_ocean`, `ffpi_USD/HKD_Rate`.  
- Table: summary stats for each series (mean, sd, min, max, count).

**Decision levers informed**

- Which series are most volatile / interesting.  
- Whether some indicators are flat or redundant (e.g. constant FX series).  
- Which time windows deserve later emphasis (e.g. 2020–2022 shock).

---

## Section 3 — Co-movement and correlation scan

**Questions to answer**

1. How strongly does `ffpi_food` correlate with each driver (BDI, energy, climate, FX, import prices, fish prices)?  
2. Are there obvious lead–lag patterns (e.g. BDI leading food prices by a few months)?  
3. Are local HK indicators (`ipi_food`, retail sales, fish prices) more tightly linked to FFPI than climate indices?

**Tables / plots**

- Correlation matrix: `ffpi_food` vs all drivers (contemporaneous).  
- Optional: cross-correlation plots for `ffpi_food` vs `bdi_price` and `ffpi_food` vs `ipi_food` for small lags (−6 to +6 months).  
- Scatterplots: FFPI vs BDI; FFPI vs IPI FOOD; FFPI vs temperature anomaly.

**Decision levers informed**

- Prioritization of variables for later visual stories.  
- Whether to treat climate anomalies as background context vs primary explanatory story.  
- Whether FX or import prices matter more for FFPI in this sample.

---

## Section 4 — Regime / episode comparison

**Questions to answer**

1. How do average FFPI levels differ across regimes:
   - Pre-COVID (2018–2019)  
   - COVID & supply-chain stress (2020–2022)  
   - Recent period (2023–2025)
2. How do BDI, energy consumption/imports, temperature anomalies and local prices behave across these regimes?  
3. Are some relationships (e.g. FFPI vs BDI) stronger in specific regimes?

**Tables / plots**

- Table: regime-wise means and standard deviations for FFPI and key drivers.  
- Bar chart: average FFPI by regime.  
- Bar chart: average BDI by regime.  
- Line chart with shaded backgrounds for regimes.

**Decision levers informed**

- Which regime differences are worth turning into “insight stories”.  
- Whether your final slide should emphasize “shock vs normal times” differences.

---

## Section 5 — Candidate insight harvesting

**Questions to answer**

1. Which 6–8 relationships look both non-obvious and actionable (for narrative purposes)?  
2. Which of those have enough data (no tiny sample segments) to be credible?  
3. Which 2–3 are strong enough to build a main chart and slide around?

**Tables / plots**

- “Scoreboard” table ranking candidate relationships by:
  - effect size (difference or correlation),  
  - data coverage,  
  - rough stability over time.

**Decision levers informed**

- Selection of the 2–3 **Top_insights_to_pursue** that feed into visual design (Step 2) and chart/slide work.
