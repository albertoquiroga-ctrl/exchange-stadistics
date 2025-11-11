# GOAL: Fetch FAO Food Price Index (FFPI) monthly data (and sub-indices) via FAO page link discovery.
# Fallback to IMF/FRED PFOODINDEXM if FAO fetch fails. Output CSV + XLSX with metadata.

# 0) Libraries: httr2 (or httr), rvest, xml2, jsonlite, readr, readxl, writexl, dplyr, tidyr, lubridate, stringr, janitor
# 1) Params: start_year <- 2010; use_fao <- TRUE; fred_api_key from Sys.getenv("FRED_API_KEY")
# 2) Function get_fao_ffpi_url():
#    - GET https://www.fao.org/worldfoodsituation/foodpricesindex/en
#    - Parse HTML and find the latest link whose href matches regex "(?i)(food[_-]?price[_-]?indices).*\\.(csv|xlsx?)"
#    - Return absolute URL and file extension.
# 3) Function fetch_fao_ffpi(url):
#    - Download to temp file; if xls/xlsx use readxl::read_excel, else readr::read_csv
#    - Clean names -> snake_case; find date column; pivot/rename columns to:
#        ffpi_food, ffpi_cereals, ffpi_veg_oils, ffpi_dairy, ffpi_meat, ffpi_sugar
#    - Parse month (e.g., "2025-10") to Date (first of month).
#    - Add unit="Index (2014–2016=100)", base_period="2014–2016",
#      source="FAO World Food Situation – FFPI", source_url=url, retrieved_utc=Sys.time()
#    - Return tibble
# 4) Function fetch_imf_fred_pfood():
#    - Use FRED observations endpoint: series_id=PFOODINDEXM; parse date/value -> ffpi_food
#    - unit="Index (2016=100)", base_period="2016",
#      source="IMF via FRED (PFOODINDEXM)", source_url="https://fred.stlouisfed.org/series/PFOODINDEXM"
# 5) main():
#    - Try FAO route if use_fao; if error or empty, log warning and use IMF route.
#    - Filter to date >= as.Date(paste0(start_year,"-01-01"))
#    - Arrange by date; distinct by date; sanity checks on ranges; stop() if catastrophic.
#    - Write CSV and XLSX (sheet1=data; sheet2=meta)
#    - Print a short summary.
