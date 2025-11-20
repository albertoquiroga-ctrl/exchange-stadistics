# Hypotheses about drivers of food price inflation (FFPI)

Each hypothesis lists the KPI metric, segments to compare, relevant time window, and why the relationship matters for the business decision (monitoring drivers of food price inflation and scenario design).

| ID | KPI metric (formula) | Segments / comparisons | Time window | Why it matters |
| --- | --- | --- | --- | --- |
| H1 | `ffpi_food` MoM % = `(ffpi_food / ffpi_food.shift(1) - 1) * 100` | Regimes: 2018–2019 vs 2020–2022 vs 2023–2025 | Full sample | Shows whether headline food inflation accelerated during stress periods, informing which regime to emphasize in monitoring. |
| H2 | Correlation between `ffpi_food` level and `ipi_food` level | Full sample; contrast stress period vs other months | 2018–2025 | Import prices are a plausible pass-through driver; higher co-movement in stress months would support focusing on trade costs. |
| H3 | Lead–lag: `ffpi_food` MoM vs `bdi_price` level (lead 1–2 months) | Compare pre-COVID vs stress vs recent regimes | 2018–2025 | Shipping tightness may precede food price spikes; evidence would justify using BDI as an early warning indicator. |
| H4 | Contribution of sub-indices: volatility of `ffpi_veg_oils` vs `ffpi_cereals` vs `ffpi_meat` (std dev of MoM %) | Regime comparison | 2018–2025 | Identifies which food groups drive overall FFPI volatility, guiding which sub-index to highlight in narratives. |
| H5 | Gap: `ffpi_veg_oils` - `ffpi_cereals` (level difference) | Stress window vs pre-COVID | 2018–2022 focus | Persistent gaps would suggest differentiated supply shocks, useful for scenario design (e.g., oilseed shortages). |
| H6 | Local retail signals: correlation of `ffpi_food` level with `rs_dairy_products` and `rs_fresh` | Regime comparison | 2018–2025 | Tests whether global price pressure is mirrored in local retail indicators, informing messaging for policymakers. |
| H7 | FX resilience: variance of `ffpi_food` when `ffpi_usd_hkd_rate` is above vs below median | Full sample | 2018–2025 | If variance is similar, it supports deprioritizing FX as a driver, simplifying monitoring dashboards. |
| H8 | Climate sensitivity: correlation of `ffpi_food` level with `gat_land_ocean` | Full sample; exclude flagged IQR outliers | 2018–2025 | Even weak associations help decide whether to track climate anomalies in monthly briefings. |
| H9 | Outlier impact: average `ffpi_food` level in months flagged by `flag_iqr_outlier` vs non-flagged months | Full sample | 2018–2025 | Checks whether high-impact months drive the mean; informs whether to footnote or winsorize for dashboards. |
| H10 | Data completeness stress test: compare results of H2–H4 with and without all-null energy columns dropped | Full sample | 2018–2025 | Ensures conclusions are robust to current energy-data gaps; highlights need to re-parse energy fields or exclude them. |

High-priority hypotheses for next-step testing: **H2**, **H3**, **H4**, **H5**, **H6**.
