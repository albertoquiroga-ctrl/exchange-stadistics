# Insight drafts

## Insight 1
- **Insight_label:** Veg oils index remained ~40% below pre-2019 levels even in 2023–2025, underscoring incomplete post-shock recovery.
- **KPI_definition:** Mean veg oils index level (index points), computed as `avg(ffpi_veg_oils)` for each regime.
- **Segments_compared:** Regimes 2018–2019 vs 2023–2025.
- **Time_window:** Jan 2018–Dec 2019 vs Jan 2023–Nov 2025.
- **Evidence_summary:** 2018–2019 average vs 2023–2025 average shows a ~55-point drop (~39% lower; ratio ≈0.61) with N=24 vs 34 and p≈2.5e-21.
- **Robustness_caveats:** Highly significant with balanced samples, but sensitive to late-2025 monthly updates and potential index revisions.
- **Why_hypothesis:** Hypothesis—structural supply shifts (e.g., biodiesel demand, weather shocks) and slower demand normalization kept veg oil prices from fully rebounding.
- **Relevance_score:** 5

## Insight 2
- **Insight_label:** Veg oils plunged by ~43% from 2018–2019 to 2020–2022, highlighting the sharp COVID-era reset.
- **KPI_definition:** Mean veg oils index level (index points), computed as `avg(ffpi_veg_oils)` for each regime.
- **Segments_compared:** Regimes 2018–2019 vs 2020–2022.
- **Time_window:** Jan 2018–Dec 2019 vs Jan 2020–Dec 2022.
- **Evidence_summary:** ~65-point decline (~43% lower; ratio ≈0.57) with N=24 vs 36; p≈2.6e-10.
- **Robustness_caveats:** Large effect with strong significance; may mask intra-period volatility and commodity-mix changes.
- **Why_hypothesis:** Hypothesis—pandemic-driven demand shocks and supply chain constraints compressed veg oil prices relative to pre-COVID peaks.
- **Relevance_score:** 5

## Insight 3
- **Insight_label:** Overall FAO food price index levels fell ~22–23% after 2019, signaling a sustained step-down.
- **KPI_definition:** Mean FFPI food level (index points), computed as `avg(ffpi_food)` for each regime.
- **Segments_compared:** Regimes 2018–2019 vs 2020–2022, and 2018–2019 vs 2023–2025.
- **Time_window:** Jan 2018–Dec 2019 vs Jan 2020–Dec 2022 vs Jan 2023–Nov 2025.
- **Evidence_summary:** Drops of ~27–29 points (~22–23% lower; ratios ≈0.77) with N=24 vs 36/34; p-values <1e-8.
- **Robustness_caveats:** Strong significance and decent sample sizes; KPI duplicated across hypotheses, and later regime still open to late-2025 revisions.
- **Why_hypothesis:** Hypothesis—post-pandemic supply normalization and lower energy/shipping costs eased global food prices.
- **Relevance_score:** 5

## Insight 4
- **Insight_label:** Imported food price index declined 7–12% in 2023–2025 versus prior regimes, indicating easing import cost pressures.
- **KPI_definition:** Mean IPI food level (index points), computed as `avg(ipi_food)` for each regime.
- **Segments_compared:** 2018–2019 vs 2023–2025, and 2020–2022 vs 2023–2025.
- **Time_window:** Jan 2018–Dec 2019 vs Jan 2020–Dec 2022 vs Jan 2023–Nov 2025.
- **Evidence_summary:** ~12-point drop (~12% lower) vs pre-COVID and ~7.6-point drop (~7.6% lower) vs COVID period; N=24/36/33 with p<1e-15.
- **Robustness_caveats:** Very significant despite modest Ns; susceptible to import-weight revisions and exchange-rate swings.
- **Why_hypothesis:** Hypothesis—cooling freight rates and improved supply chains lowered import costs for food products.
- **Relevance_score:** 4

## Insight 5
- **Insight_label:** Correlation between imported and overall food prices flipped negative during 2020–2022 before reverting positive, suggesting unstable pass-through dynamics.
- **KPI_definition:** Correlation of IPI food vs FFPI food levels, computed as `corr(ipi_food, ffpi_food)` within each regime.
- **Segments_compared:** Regimes 2018–2019 vs 2020–2022 vs 2023–2025.
- **Time_window:** Jan 2018–Dec 2019 vs Jan 2020–Dec 2022 vs Jan 2023–Nov 2025.
- **Evidence_summary:** Correlation shifted from moderately positive in 2018–2019 (~+0.37) to negative (~-0.88) in 2020–2022, then back positive (~+0.37) in 2023–2025; Ns 24–36, p-values not available.
- **Robustness_caveats:** Correlations lack p-values and may be unstable due to small samples and autocorrelation; treat as directional.
- **Why_hypothesis:** Hypothesis—temporary policy or logistics shocks broke the usual import-to-retail price pass-through, later normalizing as supply chains stabilized.
- **Relevance_score:** 3

# Top_insights_to_pursue
1) **Veg oils remained ~40% below pre-2019 by 2023–2025 (Insight 1):** Combines large, highly significant effect with clear executive relevance for supply and pricing decisions; stable N and tight ratio.
2) **Veg oils plunged ~43% during 2020–2022 vs pre-COVID (Insight 2):** Highlights shock period dynamics and recovery gap; strong p-value and substantial magnitude suit storyboard on volatility.
3) **Overall FFPI food step-down of ~22–23% post-2019 (Insight 3):** Broad KPI with significant, consistent declines across regimes, ideal for headline charting and policy framing.
