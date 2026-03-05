# Day 2 (Tuesday) — Data Extraction Spec

## Sources (public)
All pulled from FRED CSV endpoints (no API key required):
- https://fred.stlouisfed.org/graph/fredgraph.csv?id=IPG3344S
- https://fred.stlouisfed.org/graph/fredgraph.csv?id=USINFO
- https://fred.stlouisfed.org/graph/fredgraph.csv?id=PAYEMS

## Pipeline steps
1. Download each series to `data_raw/`
2. Parse date column and numeric value
3. Inner-join by month
4. Construct growth variables:
   - `chip_yoy` = YoY % change in `IPG3344S`
   - `software_emp_yoy` = YoY % change in `USINFO`
   - `payems_yoy` = YoY % change in `PAYEMS`
5. Export analysis panel to `data_analysis/panel_monthly.csv`

## QA checks
- No duplicate dates
- Missingness summary by variable
- Date overlap window recorded
- Sample size reported in run summary
