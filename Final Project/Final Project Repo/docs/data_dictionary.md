# Data dictionary — Combined monthly dataset

| name | type | description | unit | example_values |
| --- | --- | --- | --- | --- |
| Date | date (YYYY-MM-01) | Calendar month of observation; first day of month used as timestamp. Currently stored as string `DD/MM/YYYY` and should be parsed to a proper date. | month | 01/01/2018 |
| ffpi_food | numeric (float) | Composite index of international prices for a representative basket of food commodities (FAO Food Price Index – all food). | Index (2014–2016 = 100) | 96.7 |
| ffpi_cereals | numeric (float) | Index of international prices for major cereal commodities (wheat, rice, coarse grains). | Index (2014–2016 = 100) | 95.2 |
| ffpi_veg_oils | numeric (float) | Index of international prices for key vegetable oils and oilseeds. | Index (2014–2016 = 100) | 98.25 |
| ffpi_dairy | numeric (float) | Index of international prices for dairy products (e.g. milk, cheese, butter). | Index (2014–2016 = 100) | 106.0 |
| ffpi_meat | numeric (float) | Index of international prices for meat products. | Index (2014–2016 = 100) | 95.3 |
| ffpi_sugar | numeric (float) | Index of international prices for sugar. | Index (2014–2016 = 100) | 87.2 |
| bdi_price | numeric (float) | Baltic Dry Index (BDI): composite index of charter rates for bulk carriers, proxy for global shipping costs and capacity tightness. Stored as string with commas, should be cleaned to numeric. | Index (points) | 1,152.00 |
| gat_land_ocean | numeric (float) | Global land and ocean average temperature anomaly relative to a historical baseline. | Degrees Celsius anomaly | 0.84 |
| gat_land | numeric (float) | Global land average temperature anomaly relative to a historical baseline. | Degrees Celsius anomaly | 1.44 |
| gat_ocean | numeric (float) | Global ocean average temperature anomaly relative to a historical baseline. | Degrees Celsius anomaly | 0.58 |
| ffpi_Energy_Consumption  | numeric (float) | Index of energy/electricity consumption in Hong Kong. Stored as string with spaces; should be cleaned to numeric. | Index (2014–2016 = 100) | 10 954 |
| Engergy Imported  | numeric (float) | Approximate level of imported energy for Hong Kong (volume or value). Stored as string with spaces; must be cleaned and documentation checked against the original source. | Level (unit TBD) | 29 787 |
| ffpi_USD/HKD_Rate | numeric (float) | USD/HKD exchange indicator used in the FAO-aligned dataset (check whether this is an index or the level rate; values ≈ 7.75–7.85). | Index / level (TBD; confirm) | 7.821 |
| USD/HKD Rate | numeric (float) | Rounded spot exchange rate of USD to HKD (HKD per USD). Constant at 7.8 in this dataset; likely redundant sanity check. | HKD per USD | 7.8 |
| ipi_food | numeric (float) | Import Price Index for food (Trade Index Numbers by end-use category – imports, food). | Index (base year per Census & Statistics Dept table; check source) | 86.8 |
| rs_Dairy_Products | numeric (float) | Value of retail sales in supermarkets of dairy products and eggs, non-alcoholic drinks, rice and noodles, and other foods. | HKD (nominal; per Census & Statistics Dept table) | 1957.0 |
| rs_Fresh | numeric (float) | Value of retail sales in supermarkets of fresh/chilled meat, fish, seafood, fruit, vegetables, and frozen food. | HKD (nominal; per Census & Statistics Dept table) | 961.0 |
| wpm_fish | numeric (float) | Wholesale price index / reference figure for local marine fish (proxy for fresh food supply-side costs). | HKD per kg (approx; confirm in source) | 36.3 |
