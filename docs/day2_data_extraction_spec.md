# Day 2 Data Extraction Spec

## Objective
Construct a reproducible county-year panel for 2017-2023 using **public real** Census ACS data.

## Source system
- **API:** Census ACS 5-year endpoint
- **Template:** `https://api.census.gov/data/{year}/acs/acs5`
- **Years:** 2017, 2018, 2019, 2020, 2021, 2022, 2023
- **Geography query:** `for=county:*`

## Raw variables requested
- `B08006_001E`, `B08006_017E` (remote-work)
- `B28002_001E`, `B28002_004E` (broadband subscription)
- `B19013_001E` (median household income)
- `B23025_003E`, `B23025_005E` (unemployment control)
- `B01003_001E` (population control)
- `C24030_001E`, `C24030_013E`, `C24030_040E`, `C24030_015E`, `C24030_042E`, `C24030_018E`, `C24030_045E`, `C24030_019E`, `C24030_046E` (digital industry employment)

## Derived fields
- `county_id = state_fips + county_fips`
- `remote_work_share = B08006_017E / B08006_001E`
- `broadband_sub_share = B28002_004E / B28002_001E`
- `digital_emp_share = digital_emp_count / C24030_001E`
- `unemployment_rate = B23025_005E / B23025_003E`
- `log_median_hh_income = log(B19013_001E)` if positive
- `fcc_series_break_post_2022 = 1{year>=2022}` (locked forward-compatibility indicator)

## Inclusion/exclusion filters
- Keep states with `state_fips <= 56` (50 states + DC).
- Drop impossible shares (outside [0,1]) by setting to missing.
- Keep all rows through ingestion; model scripts apply complete-case filtering by specification.

## Output files (Day 2)
- `data_raw/day2_acs_raw_2017_2023.csv`
- `data_intermediate/day2_county_year_panel.csv`
- `data_analysis/county_year_panel.csv`
- `outputs/day2_source_manifest.csv`
- `outputs/day2_qa_report.csv`
- `outputs/day2_missingness_by_variable.csv`
- `outputs/day2_sample_by_year.csv`
- `outputs/day2_panel_build_summary.json`

## Blocker and fallback statement
- **Blocked component:** historical FCC availability harmonization (Form 477 + BDC).
- **Fallback used:** ACS subscription share as treatment proxy.
- **Synthetic use:** none in Day2-Day4 pipeline.
