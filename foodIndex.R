# get_ffpi.R
# ------------------------------------------------------------
# GOAL
#   Fetch monthly Food Price Index for use as the dependent variable.
#   Preferred: FAO Food Price Index (FFPI) with sub-indices.
#   Fallback : IMF Food Price Index via FRED (series: PFOODINDEXM).
#
# OUTPUT (created under ./data):
#   - data/ffpi_monthly.csv
#   - data/ffpi_monthly.xlsx   (sheet1=data, sheet2=meta)
#   - data/ffpi_readme.txt
#
# USAGE
#   Rscript get_ffpi.R
#   or source("get_ffpi.R"); main()
#
# NOTES
#   - For FRED fallback, set environment variable FRED_API_KEY if you have one.
#   - This script aims to be robust to FAO link/name changes by discovering the
#     latest resource link from the FFPI landing page.
# ------------------------------------------------------------

suppressPackageStartupMessages({
  library(httr2)
  library(rvest)
  library(xml2)
  library(readr)
  library(readxl)
  library(writexl)
  library(dplyr)
  library(tibble)
  library(tidyr)
  library(lubridate)
  library(stringr)
  library(janitor)
  library(jsonlite)
})

# ----------------------------- Config -----------------------------
cfg <- list(
  out_dir     = "data",
  start_year  = 2010L,
  use_fao     = TRUE,
  fred_key    = Sys.getenv("32a2f393619ea98accfcc46e875e706f ", ""),
  # FAO landing pages to try (FAO keeps changing paths/tails)
  fao_pages = c(
    "https://www.fao.org/worldfoodsituation/foodpricesindex/en/",
    "https://www.fao.org/worldfoodsituation/foodpricesindex/",
    "https://www.fao.org/worldfoodsituation/foodpricesindex"
  ),
  # Regex to find a current file with indices (CSV/XLS/XLSX)
  fao_regex   = "(?i)(food[ _-]?price[ _-]?indices|FFPI).*\\.(csv|xlsx?)$",
  # FRED endpoint for IMF global food index (monthly, 2016=100)
  fred_series = "PFOODINDEXM"
)

# Ensure output dir
dir.create(cfg$out_dir, showWarnings = FALSE, recursive = TRUE)

# ----------------------------- Helpers -----------------------------

message2 <- function(...) cat(sprintf("[%s] %s\n", format(now(tzone = "UTC")), sprintf(...)))

get_html_safely <- function(url, tries = 3, backoff = 0.75) {
  for (i in seq_len(tries)) {
    resp <- tryCatch(
      request(url) |> req_user_agent("ffpi-fetch/1.0") |> req_perform(),
      error = function(e) e
    )
    if (inherits(resp, "error")) {
      Sys.sleep(backoff * i)
      next
    }
    if (resp_status(resp) >= 200 && resp_status(resp) < 300) {
      return(read_html(resp_body_string(resp)))
    }
    Sys.sleep(backoff * i)
  }
  stop("Failed to retrieve HTML from: ", url)
}

absolute_url <- function(href, base) {
  if (!length(href) || is.na(href) || href == "") return(NA_character_)
  if (grepl("^https?://", href, ignore.case = TRUE)) return(href)
  # resolve relative
  url <- tryCatch(xml2::url_absolute(href, base), error = function(e) NA_character_)
  if (is.na(url)) return(NA_character_) else url
}

# Parse a wide FAO table into standard schema
normalize_fao_table <- function(tbl_raw) {
  # Clean names, try to find a date-like column
  df <- janitor::clean_names(tbl_raw)

  # Candidate date col names
  date_candidates <- c("date", "month", "period", "time", "reference_month", "year_month")
  date_col <- intersect(date_candidates, names(df))
  if (length(date_col) == 0) {
    # Fallback: assume first column is a month label
    date_col <- names(df)[1]
  }

  # Lowercase column names for matching
  nm <- names(df)

  # Map likely sub-index columns
  match_col <- function(patterns) {
    idx <- which(Reduce(`|`, lapply(patterns, function(p) grepl(p, nm, ignore.case = TRUE))))
    if (length(idx)) nm[idx[1]] else NA_character_
  }

  col_food      <- match_col(c("^food$", "food price index", "fao food", "^ffpi$"))
  col_cereals   <- match_col(c("cereal"))
  col_veg_oils  <- match_col(c("vegetable", "veg[ ._-]?oil"))
  col_dairy     <- match_col(c("dairy"))
  col_meat      <- match_col(c("meat"))
  col_sugar     <- match_col(c("sugar"))

  # Start assembling
  out <- tibble(
    date = df[[date_col]]
  )

  # Parse date: handle "YYYY-MM", "YYYY Mmm", "Mmm YYYY", numeric Excel dates, etc.
  if (inherits(out$date, "Date")) {
    # ok
  } else if (is.numeric(out$date)) {
    # Possibly Excel serial
    origin <- as.Date("1899-12-30")
    out$date <- origin + as.integer(out$date)
  } else {
    # Character parsing
    out$date <- as.character(out$date)
    # Common patterns
    out$date <- coalesce(
      suppressWarnings(as.character(ym(out$date))),
      suppressWarnings(as.character(ymd(out$date))),
      suppressWarnings(as.character(parse_date_time(out$date, orders = c("Y-m", "Y-m-d", "b-Y", "Y-b", "b Y", "Y b"))))
    )
    out$date <- as.Date(out$date)
  }

  # Coerce to month start
  out$date <- floor_date(out$date, unit = "month")

  num <- function(x) suppressWarnings(as.double(x))

  add_if <- function(df_out, src, name) {
    if (!is.na(src) && src %in% names(df)) {
      df_out[[name]] <<- num(df[[src]])
    } else {
      df_out[[name]] <<- NA_real_
    }
  }

  add_if(out, col_food,     "ffpi_food")
  add_if(out, col_cereals,  "ffpi_cereals")
  add_if(out, col_veg_oils, "ffpi_veg_oils")
  add_if(out, col_dairy,    "ffpi_dairy")
  add_if(out, col_meat,     "ffpi_meat")
  add_if(out, col_sugar,    "ffpi_sugar")

  out <- out |>
    arrange(date) |>
    distinct(date, .keep_all = TRUE)

  out
}

# ----------------------------- FAO route -----------------------------

discover_fao_resource <- function() {
  for (pg in cfg$fao_pages) {
    message2("Scanning FAO page: %s", pg)
    html <- tryCatch(get_html_safely(pg), error = function(e) NULL)
    if (is.null(html)) next

    links <- html |>
      html_elements("a[href]") |>
      html_attr("href") |>
      unique()

    # Filter by regex
    hits <- links[grepl(cfg$fao_regex, links, perl = TRUE)]
    hits_abs <- vapply(hits, absolute_url, FUN.VALUE = character(1), base = pg)
    hits_abs <- unique(na.omit(hits_abs))

    if (length(hits_abs)) {
      # Heuristic: prefer xlsx over csv, and the one with latest-looking name
      xlsx_first <- c(
        hits_abs[grepl("\\.xlsx?$", hits_abs, ignore.case = TRUE)],
        hits_abs[grepl("\\.csv$", hits_abs, ignore.case = TRUE)]
      )
      # choose the longest or most "recent-looking"
      chosen <- xlsx_first[order(nchar(xlsx_first), decreasing = TRUE)][1]
      message2("Found FAO resource: %s", chosen)
      return(chosen)
    }
  }
  stop("Could not discover a FAO FFPI resource link from landing pages.")
}

fetch_fao_ffpi <- function(url) {
  message2("Downloading FAO file: %s", url)
  tf <- tempfile(fileext = tools::file_ext(url))
  # Download with retries
  req <- request(url) |> req_user_agent("ffpi-fetch/1.0")
  resp <- req_perform(req)
  if (resp_status(resp) < 200 || resp_status(resp) >= 300) {
    stop("FAO download failed with status: ", resp_status(resp))
  }
  bin <- resp_body_raw(resp)
  writeBin(bin, tf)

  ext <- tolower(tools::file_ext(url))
  raw_tbl <- NULL
  if (ext %in% c("xls", "xlsx")) {
    # Try first sheet, fallback to sheet 1 explicitly
    raw_tbl <- suppressWarnings(readxl::read_excel(tf))
  } else if (ext %in% c("csv")) {
    raw_tbl <- suppressWarnings(readr::read_csv(tf, show_col_types = FALSE))
  } else {
    # Try reading as CSV by default
    raw_tbl <- suppressWarnings(readr::read_csv(tf, show_col_types = FALSE))
  }

  if (!is.data.frame(raw_tbl) || nrow(raw_tbl) == 0) {
    stop("FAO file read returned no rows.")
  }

  norm <- normalize_fao_table(raw_tbl)

  # Add metadata
  norm <- norm |>
    mutate(
      unit        = "Index (2014-2016=100)",
      base_period = "2014-2016",
      source      = "FAO World Food Situation - Food Price Index",
      source_url  = url,
      retrieved_utc = format(Sys.time(), tz = "UTC", usetz = TRUE)
    )

  norm
}

# ----------------------------- FRED fallback -----------------------------

fetch_fred_ffpi <- function(start_year = cfg$start_year, api_key = cfg$fred_key) {
  message2("Fetching FRED fallback series: %s", cfg$fred_series)

  params <- list(
    series_id = cfg$fred_series,
    file_type = "json",
    observation_start = sprintf("%s-01-01", start_year)
  )
  if (nzchar(api_key)) {
    params$api_key <- api_key
  }

  req <- request("https://api.stlouisfed.org/fred/series/observations")
  req <- do.call(req_url_query, c(list(req), params))
  resp <- req_perform(req)
  if (resp_status(resp) < 200 || resp_status(resp) >= 300) {
    stop("FRED request failed with status: ", resp_status(resp))
  }

  dat <- resp_body_json(resp, simplifyVector = TRUE)
  obs <- dat$observations
  if (is.null(obs) || !nrow(obs)) {
    stop("FRED response did not include observations.")
  }

  tbl <- tibble::as_tibble(obs) |>
    transmute(
      date = as.Date(date),
      ffpi_food = suppressWarnings(as.numeric(value))
    ) |>
    filter(!is.na(date), !is.na(ffpi_food)) |>
    mutate(
      ffpi_cereals = NA_real_,
      ffpi_veg_oils = NA_real_,
      ffpi_dairy = NA_real_,
      ffpi_meat = NA_real_,
      ffpi_sugar = NA_real_,
      unit = "Index (2016=100)",
      base_period = "2016",
      source = "FRED (IMF Primary Commodity Prices, PFOODINDEXM)",
      source_url = "https://fred.stlouisfed.org/series/PFOODINDEXM",
      retrieved_utc = format(Sys.time(), tz = "UTC", usetz = TRUE)
    )

  tbl
}

# ----------------------------- Outputs -----------------------------

first_value <- function(x) {
  x <- x[!is.na(x)]
  if (!length(x)) return("")
  as.character(x[1])
}

build_meta <- function(tbl, fallback_used) {
  tibble(
    field = c(
      "rows",
      "columns",
      "unit",
      "base_period",
      "source",
      "source_url",
      "retrieved_utc",
      "fallback_used",
      "generated_utc",
      "command"
    ),
    value = c(
      as.character(nrow(tbl)),
      paste(names(tbl), collapse = ", "),
      first_value(tbl$unit),
      first_value(tbl$base_period),
      first_value(tbl$source),
      first_value(tbl$source_url),
      first_value(tbl$retrieved_utc),
      if (isTRUE(fallback_used)) "TRUE" else "FALSE",
      format(Sys.time(), tz = "UTC", usetz = TRUE),
      "Rscript foodIndex.R"
    )
  )
}

write_outputs <- function(data_tbl, meta_tbl, out_dir = cfg$out_dir) {
  dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

  csv_path <- file.path(out_dir, "ffpi_monthly.csv")
  readr::write_csv(data_tbl, csv_path)

  xlsx_path <- file.path(out_dir, "ffpi_monthly.xlsx")
  writexl::write_xlsx(list(data = data_tbl, meta = meta_tbl), xlsx_path)

  readme_path <- file.path(out_dir, "ffpi_readme.txt")
  fallback_flag <- meta_tbl$value[match("fallback_used", meta_tbl$field)]
  if (length(fallback_flag) == 0 || is.na(fallback_flag)) {
    fallback_flag <- "FALSE"
  }
  notes_line <- if (identical(fallback_flag, "TRUE")) {
    "FRED fallback was used because the FAO route failed."
  } else {
    "FAO download succeeded."
  }
  summary_lines <- c(
    sprintf("Food Price Index export generated on %s", format(Sys.time(), tz = "UTC", usetz = TRUE)),
    sprintf("Primary source : %s", first_value(data_tbl$source)),
    sprintf("Source URL     : %s", first_value(data_tbl$source_url)),
    sprintf("Rows exported  : %s", nrow(data_tbl)),
    sprintf("Fallback used  : %s", fallback_flag),
    sprintf("Outputs        : %s, %s", basename(csv_path), basename(xlsx_path)),
    "",
    "Notes:",
    notes_line
  )
  writeLines(summary_lines, con = readme_path)

  invisible(list(csv = csv_path, xlsx = xlsx_path, readme = readme_path))
}

# ----------------------------- Main -----------------------------

main <- function() {
  start_cutoff <- as.Date(sprintf("%s-01-01", cfg$start_year))
  data_tbl <- NULL
  fallback_used <- FALSE

  if (isTRUE(cfg$use_fao)) {
    data_tbl <- tryCatch({
      url <- discover_fao_resource()
      fetch_fao_ffpi(url)
    }, error = function(e) {
      message2("FAO fetch failed: %s", conditionMessage(e))
      NULL
    })
  }

  if (is.null(data_tbl)) {
    fallback_used <- TRUE
    data_tbl <- fetch_fred_ffpi(start_year = cfg$start_year, api_key = cfg$fred_key)
  }

  if (!"date" %in% names(data_tbl)) {
    stop("Resulting table is missing a 'date' column.")
  }

  data_tbl <- data_tbl |>
    mutate(date = as.Date(date)) |>
    arrange(date) |>
    distinct(date, .keep_all = TRUE) |>
    filter(date >= start_cutoff)

  if (!nrow(data_tbl)) {
    stop("No rows remaining after filtering by start_year.")
  }

  meta_tbl <- build_meta(data_tbl, fallback_used = fallback_used)
  paths <- write_outputs(data_tbl, meta_tbl, out_dir = cfg$out_dir)

  message2("Wrote %s", paths$csv)
  message2("Wrote %s", paths$xlsx)
  message2("Wrote %s", paths$readme)
}

if (identical(environment(), globalenv()) && !interactive()) {
  main()
}
