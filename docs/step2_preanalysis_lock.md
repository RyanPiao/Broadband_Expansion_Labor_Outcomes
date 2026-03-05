# Step 2 Pre-Analysis Lock (Must-Fix Closure from `DAY1_review.md`)

This document is the formal Step-2 lock before modeling. It resolves all 8 must-fix items.

## 1) Locked panel sample specification
- **Unit:** county-year panel.
- **Years:** **2017-2023** (inclusive).
- **Geography:** 50 U.S. states + DC (state FIPS `<=56`), counties only.
- **Exclusions:** U.S. territories removed; invalid denominator rows (division by zero) become missing and are handled via analysis-specific complete-case filtering.
- **Boundary treatment:** fixed county FIPS key (`state_fips + county_fips`) as panel ID; no boundary re-aggregation in Stage X.

## 2) Locked treatment construction + harmonization rule
- **Intended policy treatment (target spec):** county share with fixed broadband availability >=100/20 Mbps.
- **Blocked component (this run):** harmonized Form 477 + BDC county availability series cannot be completed in Stage-X window due heavy geospatial/crosswalk integration.
- **Real-data fallback used (locked):** ACS household broadband subscription share:  
  `broadband_sub_share = B28002_004E / B28002_001E`.
- **Series-break rule (pre-registered for FCC integration):** include indicator `fcc_series_break_post_2022 = 1{year>=2022}` once FCC availability series is merged.

## 3) Locked outcome definitions
- **Primary outcome:** remote-work share (ACS 5-year):  
  `remote_work_share = B08006_017E / B08006_001E`.
- **Secondary outcome A:** digital employment share from ACS `C24030`:  
  selected info/finance/professional-scientific/management counts / `C24030_001E`.
- **Secondary outcome B (single wage/income metric):** log median household income:  
  `log_median_hh_income = log(B19013_001E)`.

## 4) Locked primary estimator details
- **Primary estimator:** county + year two-way fixed effects (TWFE), OLS with **state-clustered SE**.
- **Baseline equation:**
  \[
  Y_{ct} = \beta\,Broadband_{ct} + \theta_1 Unemp_{ct} + \theta_2 \log(Pop_{ct}) + \alpha_c + \lambda_t + \epsilon_{ct}
  \]
- **Event-study diagnostic:** event window `k \in {-3,-2,0,1,2,3}`, omitted period `k=-1`.

## 5) Locked diagnostic decision rules
- **Pre-trend gate:** event-study leads (`k=-3,-2`) each should have `p > 0.10`.
- **Treatment support gate:**
  - ever-treated county share >= 20%
  - treated cohorts >= 3
- **Primary sign gate:** remote-work baseline coefficient expected positive.

## 6) Baseline controls + policy overlays (enumerated)
- **Controls in baseline model (Step 4 active):**
  - unemployment rate (`B23025_005E/B23025_003E`)
  - log population (`log(B01003_001E)`)
- **Policy overlays (pre-specified for Stage+ continuation):**
  - state broadband grant activity indicator
  - state labor-market shock indicator
  - state-year macro pressure proxy
  These are listed now for lock compliance; not yet integrated in this Step2-Step4 execution.

## 7) Spillover sensitivity plan (pre-specified)
At minimum one spillover check is required in continuation analyses:
1. Adjacent-county exposure control, or
2. Leave-neighbor-out exclusion band.

For this Step4 baseline package, diagnostics remain within primary model scope; spillover checks are earmarked for next robustness cycle.

## 8) Step 2 QA checklist + fail-stop conditions
Implemented in `scripts/day2_ingest_build_panel.py` and written to `outputs/day2_qa_report.csv`.
Required checks:
1. Year set exactly 2017-2023
2. Unique `(county_id, year)` key (no duplicates)
3. County coverage per year >= 3100
4. Non-missing share >= 95% for all core variables
5. Rate/share bounded in [0,1]
6. Full panel coverage share >= 90%

If any check fails, the script raises an exception and halts downstream steps.
