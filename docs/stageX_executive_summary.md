# Executive Summary — Broadband Expansion and Local Labor-Market Adjustment in the Remote-Work Era

## Abstract
This report evaluates how county-level broadband expansion relates to remote work, digital employment, and income in the U.S. (2017–2023).
Using public ACS county-year data and a fixed-effects/event-study design, this study builds a transparent workflow for ingestion, modeling, robustness checks, and reproducibility packaging.
Results are informative but mixed: income associations are positive and precise, while remote-work estimates are negative with pre-trend warnings, so causal claims remain constrained.

## 2) Why this question matters
Broadband policy is commonly justified as a labor-market inclusion and productivity lever. Decision-makers need credible evidence on whether expanded broadband access shifts remote-work participation, digital job intensity, and local incomes. Better causal evidence improves infrastructure targeting, workforce planning, and evaluation of public subsidy programs.

## 3) Data used (Public Real/Synthetic + provenance)
- **Public real data (active):** U.S. Census ACS 5-year county-year pulls (2017-2023), via `https://api.census.gov/data/{year}/acs/acs5`.
- **Treatment used in this study:** household broadband subscription share (`B28002_004E / B28002_001E`).
- **Outcomes:** remote-work share (`B08006_017E / B08006_001E`), digital employment share (ACS `C24030` mapping), log median household income (`log(B19013_001E)`).
- **Provenance artifacts:** `outputs/day2_source_manifest.csv` (year-level URLs + access timestamps), `outputs/day2_qa_report.csv` (all QA checks passed).
- **Synthetic data:** Not used.
- **Blocked component:** harmonized historical FCC Form 477/BDC county availability series (deferred).

## 4) Method in plain English + estimand + identification assumptions
**Plain-English approach:**
1. Build a county-year panel with locked variable definitions and QA fail-stops.
2. Estimate county and year fixed-effects models with state-clustered SE.
3. Interpret treatment coefficient as association between broadband share shifts and outcome shifts within counties over time.
4. Run event-study leads/lags to check pre-trends and dynamic patterns.
5. Stress-test baseline estimates across pre-registered sensitivity specifications.

**Estimand (baseline FE):**
- For each outcome \(Y_{ct}\): coefficient \(\beta\) on `broadband_sub_share` in
  \(Y_{ct} = \beta Broadband_{ct} + controls + county\ FE + year\ FE + \epsilon_{ct}\).
- Practical scale: effect of a +10 percentage-point broadband increase is \(0.1\times\beta\).

**Identification assumptions:**
- Conditional parallel trends after fixed effects and controls (unemployment, log population).
- No dominant unobserved county-time shocks that jointly move subscription share and outcomes.
- Proxy validity: subscription share tracks the underlying infrastructure exposure of interest.
- Stable measurement framework (with explicit acknowledgment of post-2022 FCC series-break risk for future integration).

## 5) Key findings (3-5 bullets)
- **Data quality and coverage are strong:** all Step-2 QA gates pass; coverage is ~3,142-3,144 counties/year, full-panel share 0.994 (`outputs/day2_qa_report.csv`).
- **Baseline remote-work estimate is negative:** coef = **-0.1093** (SE 0.0205, p=1.05e-07), implying **-0.0109** for a +10pp broadband increase (`outputs/day4_baseline_model_results.csv`).
- **Income association is positive and precise:** coef = **+0.4167** (SE 0.0415, p=9.05e-24), implying **+0.0417 log points** per +10pp broadband (`outputs/day4_baseline_model_results.csv`).
- **Event-study pre-trend concern remains:** lead at k=-3 is significant (p=0.0078), failing pre-trend gate (`outputs/day4_event_study_results.csv`, `outputs/day4_model_diagnostics.csv`).
- **Robustness is mostly sign-consistent but not invariant:** 7/8 specs keep baseline sign; first-difference flips positive, highlighting specification sensitivity (`outputs/day5_robustness_sensitivity.csv`).

## 6) Robustness summary
- Robustness package ran 8 pre-specified specifications; all have p<0.10, and 88% preserve baseline sign/magnitude range around ~-0.011 per +10pp.
- Placebo future-treatment estimate remains negative and significant, which is directionally concerning for strict causal interpretation under this proxy treatment.
- First-difference sign reversal indicates non-trivial dependence on estimator choice.
- Combined with pre-trend failure, robustness results support a **diagnostic/associational** reading rather than a finalized causal claim.

## 7) What we can/cannot claim (limitations)
**We can claim:**
- The public-data pipeline and reproducibility package are complete and auditable.
- There is a stable empirical association between broadband subscription share and outcomes, with opposite signs across remote work (negative) and income (positive).

**We cannot claim (yet):**
- A definitive causal effect of infrastructure availability on remote-work participation in this run.
- That subscription-share treatment is equivalent to true provider availability exposure.
- Household-level mechanisms or short-run dynamics (county-year ACS 5-year smoothing limits temporal granularity).

## 8) Practical implications
- Do not use these remote-work coefficients alone to justify broadband policy impact on telework adoption.
- Treat current output as a high-quality diagnostic baseline and prioritize treatment-measure upgrade before policy inference.
- Income results are promising but should be interpreted as provisional until identification diagnostics improve with true availability data.

## 9) Reproducibility steps
```bash
cd /Users/openclaw/.openclaw/workspace/projects/te-research-lab-weekX
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_day2_day7.py
```
Component-level reproduction option:
```bash
python scripts/day2_ingest_build_panel.py
python scripts/day3_eda.py
python scripts/day4_baseline_model.py
python scripts/day5_robustness_sensitivity.py
python scripts/day6_reproducibility_polish.py
python scripts/day7_weekly_recap.py
```

## 10) Evidence links + citations + next-stage plan
**Core evidence links:**
- Design/spec/QA: `docs/day2_preanalysis_lock.md`, `docs/day2_data_extraction_spec.md`, `docs/day2_data_qa_checklist.md`
- Exploration + baseline interpretation: `docs/day3_eda_note.md`, `docs/day4_interpretation_notes.md`
- Robustness + limitations: `docs/day5_robustness_limitations.md`, `outputs/day5_robustness_sensitivity.csv`, `outputs/day5_limitations_register.csv`
- Reproducibility: `docs/day6_reproducibility_runbook.md`, `outputs/day6_artifact_manifest.csv`, `outputs/day6_run_metadata.json`
- Study recap: `docs/day7_weekly_recap.md`

**Citations (data/methods):**
- U.S. Census Bureau ACS API documentation: https://api.census.gov/data.html
- Callaway, B., & Sant'Anna, P. H. C. (2021). Difference-in-Differences with multiple time periods. *Journal of Econometrics*.
- Sun, L., & Abraham, S. (2021). Estimating dynamic treatment effects in event studies with heterogeneous treatment effects. *Journal of Econometrics*.

**Next-stage plan:**
1. Integrate harmonized FCC Form-477/BDC county availability treatment and re-estimate all core models.
2. Re-run event-study diagnostics with modern staggered-adoption estimators and tighter cohort comparability.
3. Execute pre-registered spillover sensitivity (adjacent-county exposure control or leave-neighbor-out band).
4. Add policy-overlay controls (state broadband grants and labor-market shocks) and reassess sign stability.
