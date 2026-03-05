# Step 2 (Tuesday) — Preanalysis Lock

## Primary specification (descriptive-associational)
Estimate correlation and simple OLS:

software_emp_yoy_t = a + b * chip_yoy_t + c * payems_yoy_t + e_t

## Lag specification
Also evaluate lead-lag correlations for chip_yoy vs software_emp_yoy at lags 0..6 months.

## Interpretation constraints
- This is not a causal identification design.
- Results are directional evidence for scheduling deeper causal work in Step 4+.
