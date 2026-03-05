# Day 5 — Robustness/Sensitivity + Limitations

## Robustness and sensitivity summary
- Specifications run: **8**
- Specs with same sign as baseline: **88%**
- Specs with p-value < 0.10: **8 / 8**
- Baseline effect (+10pp broadband on remote-work share): **-0.0110**

## Spec table (remote-work outcome)

| spec | coef | p_value | effect_10pp | n_obs |
|---|---:|---:|---:|---:|
| baseline_replication | -0.1095 | 5.559e-08 | -0.0110 | 21999 |
| exclude_2020 | -0.1105 | 5.165e-08 | -0.0110 | 18856 |
| full_panel_only | -0.1124 | 3.095e-08 | -0.0112 | 21930 |
| winsorized_treatment_1_99 | -0.1174 | 1.741e-08 | -0.0117 | 21999 |
| lagged_treatment_l1 | -0.1048 | 1.83e-05 | -0.0105 | 18846 |
| placebo_future_treatment_f1 | -0.0974 | 3.437e-10 | -0.0097 | 18846 |
| add_series_break_control | -0.1127 | 2.653e-08 | -0.0113 | 21999 |
| first_difference | 0.1364 | 1.366e-27 | 0.0136 | 18845 |

## Limitations register (Week-1)
- **Pre-trend warning in event-study leads** (high): Lead p-values: 0.008, 0.780
- **Primary coefficient sign is negative for remote-work outcome** (high): Baseline coef=-0.1095, p=5.559e-08
- **ACS subscription proxy may not equal infrastructure availability** (high): Treatment uses household subscription share (B28002) rather than provider availability coverage.
- **County-level aggregates and ACS 5-year smoothing** (medium): Panel is county-year with rolling ACS 5-year estimates.

## Week-2 implications
1. Prioritize treatment-measure upgrade (FCC availability harmonization).
2. Re-run with modern staggered-adoption estimators and stronger comparability restrictions.
3. Treat this week's remote-work estimates as directional diagnostics, not final causal claims.
