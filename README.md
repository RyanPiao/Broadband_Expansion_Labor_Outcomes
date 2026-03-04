# Tech-Econ Weekly Lab Run (Week X)
## Broadband Expansion × Labor Outcomes

This repository now contains a **fresh Day2-Day4 execution** built on the approved Day-1 framing.

## Scope completed in this run
- ✅ **Day 2**: ingestion/spec lock/QA + initial data artifacts
- ✅ **Day 3**: EDA notebook + exploratory outputs
- ✅ **Day 4**: baseline FE model + event-study diagnostics + interpretation notes
- ⛔ Days 5-7 are intentionally out of scope for this run.

---

## Day-1 must-fix closure (applied first)
All must-fix items from `DAY1_review.md` were locked before modeling:
- `docs/day2_preanalysis_lock.md`
- `docs/day2_data_extraction_spec.md`
- `docs/day2_data_qa_checklist.md`

---

## Data used
### Public real data (active)
- U.S. Census ACS 5-year API (county-year, 2017-2023)

### Blocked component and fallback
- **Blocked:** historical FCC Form-477 + BDC harmonized county availability build in this run window.
- **Fallback used:** ACS broadband subscription share (`B28002_004E / B28002_001E`) as treatment proxy.
- **Synthetic data:** not used.

---

## Repository structure

```text
.
├── README.md
├── PLAN.md
├── DAY1_problem_framing.md
├── DAY1_review.md
├── requirements.txt
├── data_raw/
├── data_intermediate/
├── data_analysis/
├── docs/
│   ├── day2_preanalysis_lock.md
│   ├── day2_data_extraction_spec.md
│   ├── day2_data_qa_checklist.md
│   ├── day3_eda_note.md
│   └── day4_interpretation_notes.md
├── notebooks/
│   ├── day3_eda.ipynb
│   └── day4_baseline_model.ipynb
├── outputs/
└── scripts/
    ├── day2_ingest_build_panel.py
    ├── day3_eda.py
    ├── day4_baseline_model.py
    └── run_day2_day4.py
```

---

## Reproducibility

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_day2_day4.py
```

---

## Key outputs by day

### Day 2
- `data_raw/day2_acs_raw_2017_2023.csv`
- `data_intermediate/day2_county_year_panel.csv`
- `data_analysis/county_year_panel.csv`
- `outputs/day2_source_manifest.csv`
- `outputs/day2_qa_report.csv`
- `outputs/day2_missingness_by_variable.csv`
- `outputs/day2_sample_by_year.csv`
- `outputs/day2_panel_build_summary.json`

### Day 3
- `notebooks/day3_eda.ipynb`
- `outputs/day3_eda_summary_stats.csv`
- `outputs/day3_eda_missingness.csv`
- `outputs/day3_eda_yearly_means.csv`
- `outputs/day3_eda_correlation_matrix.csv`
- `outputs/day3_eda_treatment_support.csv`
- `outputs/day3_eda_trends.png`
- `outputs/day3_eda_broadband_distribution.png`
- `outputs/day3_eda_correlation_heatmap.png`
- `docs/day3_eda_note.md`

### Day 4
- `notebooks/day4_baseline_model.ipynb`
- `outputs/day4_baseline_model_results.csv`
- `outputs/day4_event_study_results.csv`
- `outputs/day4_event_study_plot.png`
- `outputs/day4_model_diagnostics.csv`
- `outputs/day4_model_sample_support.csv`
- `docs/day4_interpretation_notes.md`
