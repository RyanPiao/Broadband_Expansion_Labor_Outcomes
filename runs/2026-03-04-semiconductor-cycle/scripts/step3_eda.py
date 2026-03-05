#!/usr/bin/env python3
from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data_analysis/panel_monthly.csv"
out = ROOT / "outputs"
out.mkdir(exist_ok=True)

df = pd.read_csv(p, parse_dates=["date"])
use = df[["date", "chip_yoy", "software_emp_yoy", "payems_yoy"]].dropna().copy()

# correlations and lag scan
corr = use[["chip_yoy", "software_emp_yoy", "payems_yoy"]].corr()
corr.to_csv(out / "day3_corr_matrix.csv")

lag_rows = []
for lag in range(0, 7):
    x = use["chip_yoy"].shift(lag)
    y = use["software_emp_yoy"]
    z = pd.concat([x, y], axis=1).dropna()
    c = z.iloc[:,0].corr(z.iloc[:,1]) if len(z) > 2 else np.nan
    lag_rows.append({"lag_months": lag, "corr_chip_to_software": c, "n": int(len(z))})
lag_df = pd.DataFrame(lag_rows)
lag_df.to_csv(out / "day3_lag_scan.csv", index=False)

# plot
plt.figure(figsize=(10,4))
plt.plot(use["date"], use["chip_yoy"], label="chip_yoy", alpha=0.9)
plt.plot(use["date"], use["software_emp_yoy"], label="software_emp_yoy", alpha=0.9)
plt.axhline(0, color="black", lw=0.8)
plt.legend()
plt.title("YoY Growth: Semiconductor Production vs Software Employment")
plt.tight_layout()
plt.savefig(out / "day3_growth_overlay.png", dpi=150)
plt.close()

summary = {
    "n_rows_eda": int(len(use)),
    "corr_chip_software": float(corr.loc["chip_yoy", "software_emp_yoy"]),
    "best_lag": int(lag_df.loc[lag_df["corr_chip_to_software"].abs().idxmax(), "lag_months"]),
    "best_lag_corr": float(lag_df["corr_chip_to_software"].abs().max()),
}
with open(out / "day3_eda_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(json.dumps(summary, indent=2))
