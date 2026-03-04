# Day 2 Data QA Checklist

This checklist is executed programmatically by `scripts/day2_ingest_build_panel.py`.

## Merge keys and structural checks
- [ ] Key exists: `county_id`, `year`
- [ ] `(county_id, year)` uniqueness (0 duplicates)
- [ ] Year set exactly `{2017,...,2023}`

## Coverage checks
- [ ] County count per year >= 3100
- [ ] Full panel county share >= 90%

## Core variable quality checks
For each of:
`remote_work_share`, `broadband_sub_share`, `digital_emp_share`, `log_median_hh_income`, `unemployment_rate`, `population`
- [ ] Non-missing share >= 95%

For share/rate variables:
- [ ] All non-missing values in [0,1]

## Fail-stop rule
If any check fails:
1. Write failing checks to `outputs/day2_qa_report.csv`
2. Raise error and stop pipeline (Day3-Day4 not run)
