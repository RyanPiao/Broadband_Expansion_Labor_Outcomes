#!/usr/bin/env python3
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
raw = ROOT / "data_raw"
out = ROOT / "data_analysis"
raw.mkdir(parents=True, exist_ok=True)
out.mkdir(parents=True, exist_ok=True)

series = {
    "IPG3344S": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=IPG3344S",
    "USINFO": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=USINFO",
    "PAYEMS": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=PAYEMS",
}

dfs = []
for sid, url in series.items():
    p = raw / f"{sid}.csv"
    df = pd.read_csv(url)
    df.to_csv(p, index=False)
    df.columns = ["date", sid]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df[sid] = pd.to_numeric(df[sid], errors="coerce")
    dfs.append(df.dropna(subset=["date"]))

panel = dfs[0]
for d in dfs[1:]:
    panel = panel.merge(d, on="date", how="inner")

panel = panel.sort_values("date").reset_index(drop=True)
for c in ["IPG3344S", "USINFO", "PAYEMS"]:
    panel[f"{c}_yoy"] = panel[c].pct_change(12) * 100.0

panel = panel.rename(columns={
    "IPG3344S_yoy": "chip_yoy",
    "USINFO_yoy": "software_emp_yoy",
    "PAYEMS_yoy": "payems_yoy",
})

panel.to_csv(out / "panel_monthly.csv", index=False)

summary = {
    "n_rows": int(len(panel)),
    "date_min": str(panel["date"].min().date()),
    "date_max": str(panel["date"].max().date()),
    "missing": {k: int(panel[k].isna().sum()) for k in panel.columns if k != "date"},
}
(ROOT / "outputs").mkdir(exist_ok=True)
with open(ROOT / "outputs/day2_panel_build_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(json.dumps(summary, indent=2))
