# Step 4 Interpretation Notes

## Baseline model package
- Estimator: county/year TWFE (within transformation) with state-clustered SE.
- Treatment proxy: ACS broadband subscription share (`B28002_004E / B28002_001E`).
- Outcomes:
  1. `remote_work_share` (primary)
  2. `digital_emp_share`
  3. `log_median_hh_income`

## Main estimates (`outputs/day4_baseline_model_results.csv`)
- **Remote-work share:** coef = **-0.1093** (SE 0.0205, p<0.001), effect per +10pp broadband = **-0.0109**.
- **Digital employment share:** coef = -0.0039 (SE 0.0076, p=0.60), not statistically distinguishable from zero.
- **Log median HH income:** coef = **+0.4167** (SE 0.0415, p<0.001), effect per +10pp broadband = **+0.0417 log points**.

## Event-study diagnostics (`outputs/day4_event_study_results.csv`)
- Pre-period lead at **k=-3** is significant (p=0.0078), indicating potential pre-trend concerns.
- Most post-period coefficients are negative for remote-work share in this specification.

## Gate status (`outputs/day4_model_diagnostics.csv`)
- ❌ Pre-trend gate (k=-3,-2 p>0.10): **fail**
- ✅ Treatment-support share gate: **pass** (ever-treated share = 0.971)
- ✅ Treated cohorts gate: **pass** (7 cohorts)
- ❌ Primary sign gate (remote-work effect >0): **fail**

## Interpretation for Stage-X decisioning
1. This baseline package does **not** support a clean positive remote-work response under the current proxy-treatment design.
2. Income association is positive, but interpretation remains observational and sensitive to specification.
3. Given pre-trend failure and sign mismatch versus prior expectation, this should be treated as **diagnostic evidence**, not a final causal claim.
4. Highest-priority next step is to replace proxy treatment with harmonized FCC availability series and re-run diagnostics.
