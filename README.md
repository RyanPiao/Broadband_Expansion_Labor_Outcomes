# Tech-Econ Weekly Lab Run (Week X)
## Broadband Expansion × Labor Outcomes

This repository now contains the **full Step 2-Step 7 continuation** for the approved Step-1 framing.

## Start here (primary single-page overview)
- **Executive summary:** [`docs/weekX_executive_summary.md`](docs/weekX_executive_summary.md)
- Website abstract source: [`docs/weekX_website_abstract.md`](docs/weekX_website_abstract.md)

## Scope completed in this run

### Executive summary
- `docs/weekX_executive_summary.md`

- ✅ **Step 2**: ingestion/spec lock/QA + analysis-ready county-year panel
- ✅ **Step 3**: EDA notebook + exploratory outputs
- ✅ **Step 4**: baseline FE model + event-study diagnostics
- ✅ **Step 5**: robustness/sensitivity package + limitations register
- ✅ **Step 6**: reproducibility polish (manifest, requirements snapshot, runbook)
- ✅ **Step 7**: weekly recap report suitable for website research summary

---

## Step-1 must-fix closure (applied before modeling)
- `docs/step2_preanalysis_lock.md`
- `docs/step2_data_extraction_spec.md`
- `docs/step2_data_qa_checklist.md`

---

## Data used
### Public real data (active)
- U.S. Census ACS 5-year API (county-year, 2017-2023)

### Blocked component and fallback
- **Blocked in Week-X:** harmonized historical FCC Form-477/BDC county availability panel.
- **Fallback used:** ACS household broadband subscription share (`B28002_004E / B28002_001E`) as treatment proxy.
- **Synthetic data:** not used.

---

## Repository structure

```text
.
├── README.md
├── PLAN.md
├── STEP1_problem_framing.md
├── STEP1_review.md
├── requirements.txt
├── data_raw/
├── data_intermediate/
├── data_analysis/
├── docs/
│   ├── step2_*.md
│   ├── step3_eda_note.md
│   ├── step4_interpretation_notes.md
│   ├── step5_robustness_limitations.md
│   ├── step6_reproducibility_runbook.md
│   ├── step6_reproducibility_checklist.md
│   └── step7_weekly_recap.md
├── notebooks/
├── outputs/
└── scripts/
    ├── step2_ingest_build_panel.py
    ├── step3_eda.py
    ├── step4_baseline_model.py
    ├── step5_robustness_sensitivity.py
    ├── step6_reproducibility_polish.py
    ├── step7_weekly_recap.py
    ├── run_day2_day4.py
    └── run_day2_day7.py
```

---

## Reproducibility

### Full rerun
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_day2_day7.py
```

### Reproducibility package outputs
- `outputs/step6_artifact_manifest.csv`
- `outputs/step6_requirements_snapshot.csv`
- `outputs/step6_run_metadata.json`
- `docs/step6_reproducibility_runbook.md`

---

## Step 5-Step 7 core artifacts

### Step 5 (robustness/sensitivity + limitations)
- `outputs/step5_robustness_sensitivity.csv`
- `outputs/step5_limitations_register.csv`
- `docs/step5_robustness_limitations.md`

### Step 6 (reproducibility polish)
- `outputs/step6_artifact_manifest.csv`
- `outputs/step6_requirements_snapshot.csv`
- `outputs/step6_run_metadata.json`
- `docs/step6_reproducibility_runbook.md`
- `docs/step6_reproducibility_checklist.md`

### Step 7 (weekly recap)
- `docs/step7_weekly_recap.md`
- `outputs/step7_website_summary.txt`
- `outputs/step7_recap_metadata.json`
