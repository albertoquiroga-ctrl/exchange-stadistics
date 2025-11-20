# Insight validation export
- source_data: `clean/data_clean.csv`
- figures_dir: `derived/04_insight_validation/figures`
- regime_windows: 2018-2019: 2018-01-01 to 2019-12-01 (rows=24); 2020-2022: 2020-01-01 to 2022-12-01 (rows=36); 2023-2025: 2023-01-01 to 2025-11-01 (rows=35)

## CI1 - FFPI food level remains about 30 points higher after 2019
- kpi: `ffpi_food` (relevance_score=5)
- figure: `derived/04_insight_validation/figures/ci1_ffpi_food.png`
- sample_sizes: 2018-2019: n=24, missing=0; 2020-2022: n=36, missing=0; 2023-2025: n=34, missing=1
- delta 2020-2022 vs 2018-2019: delta_mean=27.44, ratio_mean=1.29
- delta 2023-2025 vs 2018-2019: delta_mean=29.21, ratio_mean=1.31
- conclusion: FFPI food level remains about 30 points higher after 2019

## CI2 - Veg oils index surged during the 2020-2022 stress window
- kpi: `ffpi_veg_oils` (relevance_score=5)
- figure: `derived/04_insight_validation/figures/ci2_ffpi_veg_oils.png`
- sample_sizes: 2018-2019: n=24, missing=0; 2020-2022: n=36, missing=0; 2023-2025: n=34, missing=1
- delta 2020-2022 vs 2018-2019: delta_mean=65.19, ratio_mean=1.76
- delta 2023-2025 vs 2018-2019: delta_mean=55.16, ratio_mean=1.65
- conclusion: Veg oils index surged during the 2020-2022 stress window

## CI3 - Import price pressure (IPI food) stayed elevated through 2025
- kpi: `ipi_food` (relevance_score=4)
- figure: `derived/04_insight_validation/figures/ci3_ipi_food.png`
- sample_sizes: 2018-2019: n=24, missing=0; 2020-2022: n=36, missing=0; 2023-2025: n=33, missing=2
- delta 2023-2025 vs 2018-2019: delta_mean=12.26, ratio_mean=1.14
- delta 2023-2025 vs 2020-2022: delta_mean=7.61, ratio_mean=1.08
- conclusion: Import price pressure (IPI food) stayed elevated through 2025
