# Hypotheses about drivers of food price inflation (FFPI)

For each hypothesis:

- KPI: metric on `ffpi_food` or related index.
- Segments / regimes: time periods or indicator families.
- Priority: subjective 1–5 (5 = high priority for later analysis).

---

## H1 — Import price index and food price index move together

- KPI: `ffpi_food` level and monthly change.
- Driver: `ipi_food` (import price index for food).
- Claim: Higher import price index is associated with higher FAO food price index in the same month.
- Segment / regime: Full sample 2018–2025.
- Priority: **5 (high)**.

## H2 — Shipping costs (BDI) co-move with FFPI

- KPI: `ffpi_food` level.
- Driver: `bdi_price` (after cleaning to numeric).
- Claim: Months with high BDI levels tend to have higher FFPI, reflecting supply-chain tightness.
- Segment / regime: Full sample; check 2018–2019 vs 2020–2022.
- Priority: **4 (high)**.

## H3 — Local marine fish prices as a proxy for fresh food pressures

- KPI: `wpm_fish` and `ffpi_food` levels.
- Claim: Higher wholesale marine fish prices are associated with higher global food price index, albeit more weakly.
- Segment / regime: Full sample; pay attention to 2020–2022.
- Priority: **3 (medium)**.

## H4 — Energy consumption index and FFPI

- KPI: `ffpi_food` level.
- Driver: `ffpi_Energy_Consumption`.
- Claim: Higher energy consumption is moderately associated with higher FFPI, reflecting activity and energy-related costs.
- Segment / regime: Full sample; compare pre- and post-COVID.
- Priority: **3 (medium)**.

## H5 — Energy imports as a stress indicator

- KPI: `ffpi_food` level.
- Driver: `Engergy Imported` (once properly cleaned).
- Claim: Lower imported energy (e.g. constraints) is associated with higher FFPI.
- Segment / regime: Supply-chain stress period vs other months.
- Priority: **2 (low–medium)** (data quality risk).

## H6 — Global temperature anomalies and FFPI

- KPI: `ffpi_food` level.
- Driver: `gat_land_ocean`.
- Claim: In this short window, climate anomalies show at most a weak contemporaneous link with FFPI, but may shape long-term trend.
- Segment / regime: Full sample; optional.
- Priority: **2 (low–medium)**.

## H7 — FX: stronger USD vs HKD and food prices

- KPI: `ffpi_food` level.
- Driver: `ffpi_USD/HKD_Rate` (interpretation to be confirmed).
- Claim: Changes in USD/HKD around ~7.8 have limited explanatory power for FFPI in this sample.
- Segment / regime: Full sample.
- Priority: **1 (low)**.

## H8 — Dairy and fresh retail series as local demand proxies

- KPI: `rs_Dairy_Products`, `rs_Fresh` levels.
- Driver: Time and FFPI.
- Claim: Periods of elevated FFPI coincide with some upward movement in local HK retail food sales, but the relationship may be weak or lagged.
- Segment / regime: Full sample; compare regimes.
- Priority: **3 (medium)**.

## H9 — Sub-indices diverge: vegetable oils vs cereals

- KPI: Differences between `ffpi_veg_oils` and `ffpi_cereals`.
- Claim: Vegetable oil prices show stronger spikes than cereals around specific periods (e.g. 2020–2022), making them a candidate for storytelling.
- Segment / regime: Pre-COVID vs COVID vs recent.
- Priority: **4 (high)**.

## H10 — Regime shift: FFPI pre- vs post-COVID

- KPI: Average `ffpi_food` level by regime.
- Claim: Mean FFPI is noticeably higher in the COVID and post-COVID period than in 2018–2019.
- Segment / regime:
  - Pre-COVID: 2018–2019  
  - COVID/supply chain stress: 2020–2022  
  - Recent: 2023–2025
- Priority: **5 (high)**.

---

## High-priority hypotheses to take into 1D

Marking as **high priority** for the segmentation / effect-size scan:

- **H1** – Import price index vs FFPI.  
- **H2** – Shipping costs (BDI) vs FFPI.  
- **H9** – Divergence of vegetable oils vs cereals.  
- **H10** – Regime shift in FFPI pre- vs post-COVID.  
- **H8** – Local retail food indicators vs regimes (as a weaker but narratively useful angle).
