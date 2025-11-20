# Segment scoreboard (top 20 rows)

|KPI|segment_dimension|segment_A|segment_B|diff|ratio|N_A|N_B|p_value|hypothesis|abs_diff|ratio_deviation|n_min|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Veg oils level|regime|2018-2019|2020-2022|-65.19013888888894|0.567388286821891|24|36|2.5886752786713807e-10|H2|65.19013888888894|0.432611713178109|24|
|Veg oils level|regime|2018-2019|2023-2025|-55.15629901960783|0.6078635454349023|24|34|2.5225033963498042e-21|H2|55.15629901960783|0.3921364545650977|24|
|FFPI Food level|regime|2018-2019|2023-2025|-29.207843137254898|0.7654764153913974|24|34|1.1214197424818075e-38|H1|29.207843137254898|0.2345235846086025|24|
|FFPI Food level|regime|2018-2019|2023-2025|-29.207843137254898|0.7654764153913974|24|34|1.1214197424818075e-38|H2|29.207843137254898|0.2345235846086025|24|
|FFPI Food level|regime|2018-2019|2020-2022|-27.438888888888897|0.7765057242409158|24|36|2.6112389800951884e-09|H1|27.438888888888897|0.2234942757590842|24|
|FFPI Food level|regime|2018-2019|2020-2022|-27.438888888888897|0.7765057242409158|24|36|2.6112389800951884e-09|H2|27.438888888888897|0.2234942757590842|24|
|IPI food level|regime|2018-2019|2023-2025|-12.259848484848476|0.8774238017330184|24|33|6.421113040906194e-47|H5|12.259848484848476|0.1225761982669816|24|
|Veg oils level|regime|2020-2022|2023-2025|10.03383986928111|1.0713360842179616|36|34|0.2208392833236798|H2|10.03383986928111|0.0713360842179615|34|
|IPI food level|regime|2020-2022|2023-2025|-7.609848484848484|0.9239153487244745|36|33|8.69866010321172e-16|H5|7.609848484848484|0.0760846512755256|33|
|IPI food level|regime|2018-2019|2020-2022|-4.649999999999992|0.9496798629272252|24|36|8.453697705682769e-10|H5|4.649999999999992|0.0503201370727747|24|
|FFPI Food level|regime|2020-2022|2023-2025|-1.7689542483660006|0.9857962298213574|36|34|0.6203042097949634|H1|1.7689542483660006|0.0142037701786426|34|
|FFPI Food level|regime|2020-2022|2023-2025|-1.7689542483660006|0.9857962298213574|36|34|0.6203042097949634|H2|1.7689542483660006|0.0142037701786426|34|
|Corr(IPI food, FFPI food)|regime|2020-2022|2023-2025|1.248779372375059|-2.0595598153175274|36|33|nan|H5|1.248779372375059|3.0595598153175274|33|
|FFPI Food MoM %|regime|2020-2022|2023-2025|0.976739940438921|-5.983501621199842|36|35|0.1312410526840752|H1|0.976739940438921|6.983501621199842|35|
|Corr(IPI food, FFPI food)|regime|2018-2019|2020-2022|-0.879662147649159|-0.0464409507551872|24|36|nan|H5|0.879662147649159|1.0464409507551873|24|
|Corr(RS fresh, FFPI food)|high_ffpi_flag|True|False|0.7601986096730349|-0.6924614877519337|24|69|nan|H6|0.7601986096730349|1.6924614877519335|24|
|Corr(BDI lead1, FFPI MoM%)|regime|2018-2019|2020-2022|-0.7210449135078576|-1.2455028280724052|23|36|nan|H4|0.7210449135078576|2.2455028280724054|23|
|FFPI Food MoM %|regime|2018-2019|2020-2022|-0.6465003924112271|0.2274836657279048|23|36|0.3382595111549344|H1|0.6465003924112271|0.7725163342720952|23|
|Corr(BDI lead2, FFPI MoM%)|regime|2018-2019|2020-2022|-0.5641075137528988|-1.3889519134358668|23|36|nan|H4|0.5641075137528988|2.388951913435867|23|
|Corr(BDI lead1, FFPI MoM%)|regime|2018-2019|2023-2025|-0.4434133539846689|-9.199352953484738|23|34|nan|H4|0.4434133539846689|10.199352953484738|23|

## Quick observations (from top rows)

- Veg oils index fell sharply from 2018–2019 to both 2020–2022 and 2023–2025, with ratios near 0.57–0.61.
- Overall FFPI food levels dropped ~22–23% when comparing 2018–2019 to 2020–2022/2023–2025, with strong significance.
- IPI food levels also trended down across regimes, though with smaller (~5–12%) declines.
- Correlations between IPI food and FFPI food flipped signs across regimes, suggesting instability in the relationship.
- Lead correlations between BDI and FFPI food MoM weakened substantially after 2018–2019, indicating shipping-price link erosion.

## Candidate insights (needs business validation)

1. **Veg oils collapse post-2019**  
   - **KPI & formula:** Mean veg oils index level (`avg(ffpi_veg_oils)`) by regime; compare 2018–2019 vs 2020–2022.  
   - **Segments:** Regimes 2018–2019 vs 2020–2022.  
   - **Magnitude:** ~65-point drop (~43% lower, ratio 0.57).  
   - **Time window:** Regime averages over Jan 2018–Dec 2019 vs Jan 2020–Dec 2022.  
   - **Robustness:** Strong p-value (<1e-9) and decent N (24 vs 36), but may mask intra-regime volatility.  
   - **Relevance_score:** 5.

2. **Veg oils remain below pre-COVID despite partial rebound**  
   - **KPI & formula:** Mean veg oils index level by regime; compare 2018–2019 vs 2023–2025.  
   - **Segments:** Regimes 2018–2019 vs 2023–2025.  
   - **Magnitude:** ~55-point drop (~39% lower, ratio 0.61).  
   - **Time window:** Jan 2018–Dec 2019 vs Jan 2023–Nov 2025.  
   - **Robustness:** Extremely significant (p≈2.5e-21); moderate N (24 vs 34). Trend sensitive to final 2025 months.  
   - **Relevance_score:** 5.

3. **Modest veg-oils recovery after 2022**  
   - **KPI & formula:** Mean veg oils index level by regime; compare 2020–2022 vs 2023–2025.  
   - **Segments:** Regimes 2020–2022 vs 2023–2025.  
   - **Magnitude:** +10 points (~7% increase, ratio 1.07).  
   - **Time window:** Jan 2020–Dec 2022 vs Jan 2023–Nov 2025.  
   - **Robustness:** p≈0.22 (not statistically strong); N similar (36 vs 34). Use cautiously as a directional hint.  
   - **Relevance_score:** 3.

4. **Overall food price index stepped down ~22–23%**  
   - **KPI & formula:** Mean FFPI food level (`avg(ffpi_food)`) by regime; compare 2018–2019 vs later regimes.  
   - **Segments:** 2018–2019 vs 2020–2022, and 2018–2019 vs 2023–2025.  
   - **Magnitude:** -27 to -29 points (~22–23% lower, ratios 0.77 and 0.77).  
   - **Time window:** Jan 2018–Dec 2019 vs the two later regimes.  
   - **Robustness:** Very strong p-values (<1e-8), reasonable N (24 vs 34–36). Possible double-counting since KPI repeated for H1/H2 hypotheses.  
   - **Relevance_score:** 5.

5. **Imported food prices soften, especially recently**  
   - **KPI & formula:** Mean IPI food level (`avg(ipi_food)`) by regime.  
   - **Segments:** 2018–2019 vs 2023–2025, and 2020–2022 vs 2023–2025.  
   - **Magnitude:** ~12-point drop vs pre-COVID (~12% lower) and ~7.6-point drop vs COVID period (~7.6% lower).  
   - **Time window:** Jan 2018–Dec 2019, Jan 2020–Dec 2022, Jan 2023–Nov 2025.  
   - **Robustness:** Extremely low p-values (<1e-15); Ns 24–36. Potential sensitivity to import-weight revisions.  
   - **Relevance_score:** 4.

6. **FFPI month-over-month movements stabilized post-2020**  
   - **KPI & formula:** Average FFPI food MoM % change (`avg(ffpi_food_mom_pct)`) by regime.  
   - **Segments:** 2018–2019 vs 2020–2022 vs 2023–2025.  
   - **Magnitude:** -0.65 ppts from 2018–2019 to 2020–2022 (ratio 0.23); +0.98 ppts from 2020–2022 to 2023–2025 (ratio -5.98, implying sign flip).  
   - **Time window:** Same regime windows as above.  
   - **Robustness:** p-values ~0.13–0.34 (weak); small Ns (23–36). Treat as suggestive of volatility changes, not definitive.  
   - **Relevance_score:** 2.

7. **Shipping–food inflation link weakened sharply**  
   - **KPI & formula:** Correlation between BDI (lead 1–2 months) and FFPI food MoM (`corr(bdi_price_{t-1/2}, ffpi_food_mom)`), by regime.  
   - **Segments:** 2018–2019 vs 2020–2022 vs 2023–2025.  
   - **Magnitude:** Correlations drop ~0.56–0.72 between 2018–2019 and 2020–2022; additional ~0.36–0.44 drop vs 2023–2025 (ratios imply large relative swings).  
   - **Time window:** Regime averages over Jan 2018–Nov 2025 with specified leads.  
   - **Robustness:** No p-values; Ns 23–36. Correlation estimates may be unstable with small samples and autocorrelation.  
   - **Relevance_score:** 3.

8. **IPI–FFPI correlation flipped sign after 2019**  
   - **KPI & formula:** Correlation between IPI food and FFPI food levels (`corr(ipi_food, ffpi_food)`) by regime.  
   - **Segments:** 2018–2019 vs 2020–2022 vs 2023–2025.  
   - **Magnitude:** Shifts from moderately positive (~+0.37) in 2018–2019 to negative (~-0.88) in 2020–2022, then back positive (~+0.37) in 2023–2025; ratio swings >2x.  
   - **Time window:** Regime-specific correlations Jan 2018–Nov 2025.  
   - **Robustness:** No p-values; Ns 24–36. Correlations sensitive to overlapping shocks and possible non-stationarity.  
   - **Relevance_score:** 3.
