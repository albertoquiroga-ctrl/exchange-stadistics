# Refined hypotheses about drivers of food price inflation (FFPI)

Baseline context from the cleaned panel (2018–2025):
- Headline `ffpi_food` climbed from an average of ~95 in 2018–2019 to ~123 in 2020–2022 and ~125 in 2023–2025, with a 2022 peak (yearly mean ~145) before easing slightly. Segment counts by regime: 24 months (2018–2019), 36 months (2020–2022), 35 months (2023–2025).
- Strong co-movement with FAO sub-indices: `ffpi_veg_oils` (~0.95 correlation) and `ffpi_dairy`/`ffpi_cereals` (>0.87) track `ffpi_food`; shipping (`bdi_price`, ~0.42) is moderate; retail sales are inversely related (`rs_dairy_products` -0.47, `rs_fresh` -0.24); climate indicators show weak association (~0.1); energy fields remain all-null and unusable.

Hypotheses (5 marked **High priority** for deeper analysis):

| ID | KPI metric (formula) | Segments / comparisons | Time window | Why it matters | Priority |
| --- | --- | --- | --- | --- | --- |
| H1 | `ffpi_food` level and MoM % = `(ffpi_food / ffpi_food.shift(1) - 1) * 100` | Regime means: 2018–2019 vs 2020–2022 vs 2023–2025 | Full sample | Confirms whether stress-period surges (e.g., 2022 peak) materially lifted the baseline level for policy focus. | **High** |
| H2 | `ffpi_veg_oils` vs `ffpi_food` levels (corr/β) | Overall and by regime | Full sample | Veg oils show the tightest co-movement; quantifying their contribution highlights the most responsive driver to monitor. | **High** |
| H3 | `ffpi_cereals` share of variation in `ffpi_food` (corr and variance ratios) | Overall vs stress vs recent | 2018–2025 | Tests whether cereal shocks (notably 2020–2022 lift) still explain current FFPI volatility. | Explore |
| H4 | Lead–lag: `bdi_price` (lead 1–2 months) vs `ffpi_food` MoM % | Pre-COVID vs 2020–2022 vs 2023–2025 | 2018–2025 | Shipping tightened most in 2020–2022; evidence of leading effects would justify BDI as an early warning gauge. | **High** |
| H5 | Import pass-through: corr/β of `ipi_food` level vs `ffpi_food` level | Overall and by regime | 2018–2025 | Higher `ipi_food` during 2023–2025 coincides with elevated FFPI; gauges trade-cost pass-through strength. | **High** |
| H6 | Local demand dampening: `rs_dairy_products` and `rs_fresh` vs `ffpi_food` (corr, slopes) | Compare high-FFPI months vs others | 2018–2025 | Negative correlations suggest demand softness may offset price spikes; informs retail-facing policy messaging. | **High** |
| H7 | Sub-index divergence: gap `ffpi_veg_oils - ffpi_cereals` | Stress window (2020–2022) vs pre/post | 2018–2025 | Persistent gaps would signal differentiated supply shocks, useful for scenario planning. | Explore |
| H8 | Sugar momentum: `ffpi_sugar` YoY % vs `ffpi_food` YoY % | Overall and post-2022 | 2018–2025 | Sugar’s sharp rise in 2023–2025 may be a hidden driver of current FFPI stickiness. | Explore |
| H9 | Climate sensitivity: corr of `gat_land_ocean` with `ffpi_food` | Full sample; exclude IQR-flagged months | 2018–2025 | Weak baseline links need confirmation before deprioritizing climate signals in dashboards. | Explore |
| H10 | Outlier influence: mean `ffpi_food` in `flag_iqr_outlier` months vs others | Full sample | 2018–2025 | Tests whether flagged extremes materially skew averages, informing whether to winsorize or annotate. | Explore |
