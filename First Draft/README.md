# Econ 7900 Team Project Package (v2)
**Title:** Drivers of Food Price Inflation: Building a Multi-source Monthly Dataset (2018–2025)  
**Course:** Econ 7900 Statistics for Data Science  
**Deliverables generated:** 2025-11-05T10:20:56.084552Z

## Contents
- `data/final_dataset_sample.csv` — sample dataset to illustrate schema and visuals.
- `data/data_dictionary.csv` — variables, units, definitions.
- `images/*.png` — example figures.
- `code/fetch_and_build_dataset.R` — reproducible script to fetch public data and build the full dataset locally.
- `docs/` — presentation slides (PPTX).

## Rebuild the full dataset locally
1. Install R (≥4.2) and the packages referenced in the script.
2. Run `code/fetch_and_build_dataset.R` to fetch and merge public monthly series into `data/final_dataset.csv`.
3. The script aligns dates to month start, standardizes names/units, and writes outputs.

## Notes
- The included CSV contains simulated values purely to demonstrate structure; rebuild locally for real data.
- No statistical modeling is performed, per the course brief.
