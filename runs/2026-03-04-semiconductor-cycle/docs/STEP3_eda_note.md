# Step 3 (Wednesday) — EDA Note

This note summarizes outputs from `scripts/day3_eda.py`.

## Deliverables
- `outputs/day3_corr_matrix.csv`
- `outputs/day3_lag_scan.csv`
- `outputs/day3_growth_overlay.png`
- `outputs/day3_eda_summary.json`

## Step 3 readout (executed)
- Contemporaneous correlation (`chip_yoy`, `software_emp_yoy`): **0.3534**.
- Strongest lag association (0..6 months): **lag 3**, |corr| = **0.3860**.
- Sign is positive and directionally consistent with Step 1 hypothesis.

## Next suggestion
Move to Step 4 with baseline regression + lag specification using Newey-West or HAC errors for serial correlation robustness.