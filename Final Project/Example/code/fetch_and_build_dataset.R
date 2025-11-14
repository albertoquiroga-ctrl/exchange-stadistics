# fetch_and_build_dataset.R (v2)
suppressPackageStartupMessages({
  library(readr); library(dplyr); library(tidyr)
  library(lubridate); library(stringr); library(janitor)
})

to_month_start <- function(x) floor_date(as_date(x), unit = "month")

src <- list(
  fao_fpi = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/FAO%20Food%20Price%20Index%20(FPI)%20-%20FAO/FAO%20Food%20Price%20Index%20(FPI)%20-%20FAO.csv",
  brent   = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv",
  bdi     = "https://raw.githubusercontent.com/datasets/bdi/master/data/bdi.csv",
  temp    = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/NOAA%20Global%20Temperature%20Anomalies/NOAA%20Global%20Temperature%20Anomalies.csv",
  fx      = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/FRED%20-%20Exchange%20Rates/FRED%20-%20Exchange%20Rates.csv"
)

fao <- read_csv(src$fao_fpi, show_col_types = FALSE) %>%
  clean_names() %>% rename(date = time) %>%
  mutate(date = to_month_start(date)) %>%
  select(date, fao_food_price_index = value) %>% arrange(date)

energy <- read_csv(src$brent, show_col_types = FALSE)
brent <- energy %>% filter(country == "World") %>%
  transmute(date = to_month_start(as.Date(paste0(year, "-", if_else(!is.na(month), sprintf("%02d", month), "01"), "-01"))),
            brent_crude_usd = oil_price) %>% filter(!is.na(brent_crude_usd)) %>% arrange(date)

bdi <- read_csv(src$bdi, show_col_types = FALSE) %>%
  clean_names() %>% mutate(date = to_month_start(date)) %>%
  group_by(date) %>% summarize(baltic_dry_index = round(mean(value, na.rm = TRUE))) %>% ungroup()

temp <- read_csv(src$temp, show_col_types = FALSE) %>%
  clean_names() %>% mutate(date = to_month_start(date)) %>%
  select(date, global_temp_anomaly_c = anomaly) %>% arrange(date)

fx <- read_csv(src$fx, show_col_types = FALSE) %>%
  clean_names() %>% filter(str_detect(indicator, "HKD|DEXHKUS|HKD/US")) %>%
  mutate(date = to_month_start(date)) %>% group_by(date) %>%
  summarize(fx_hkd_per_usd = mean(value, na.rm = TRUE)) %>% ungroup()

df <- fao %>% full_join(brent, by = "date") %>%
  full_join(bdi, by = "date") %>% full_join(temp, by = "date") %>%
  full_join(fx, by = "date") %>% arrange(date) %>%
  filter(date >= as.Date("2018-01-01"), date <= as.Date("2025-09-01")) %>%
  mutate(covid_period = as.integer(date >= as.Date("2020-03-01") & date <= as.Date("2022-06-01")),
         supply_chain_peak = as.integer(date >= as.Date("2021-06-01") & date <= as.Date("2022-03-01")))

dir.create("../data", showWarnings = FALSE, recursive = TRUE)
write_csv(df, "../data/final_dataset.csv")
message("Wrote ../data/final_dataset.csv with ", nrow(df), " rows and ", ncol(df), " columns.")
