#!/usr/bin/env python3
"""Step 6: Reproducibility polish artifacts (manifest + run metadata)."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = PROJECT_ROOT / "outputs"
DOCS = PROJECT_ROOT / "docs"

KEY_ARTIFACTS = [
    "data_analysis/county_year_panel.csv",
    "outputs/day2_panel_build_summary.json",
    "outputs/day3_eda_summary_stats.csv",
    "outputs/day4_baseline_model_results.csv",
    "outputs/day4_event_study_results.csv",
    "outputs/day5_robustness_sensitivity.csv",
    "outputs/day5_limitations_register.csv",
    "docs/day5_robustness_limitations.md",
]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def package_snapshot() -> list[dict[str, str]]:
    req = PROJECT_ROOT / "requirements.txt"
    rows = []
    for line in req.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" in line:
            pkg, ver = line.split("==", 1)
        else:
            pkg, ver = line, "unpinned"
        rows.append({"package": pkg, "version_spec": ver})
    return rows


def git_commit() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT, text=True)
        return out.strip()
    except Exception:
        return "unknown"


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    manifest_rows = []
    missing_rows = []

    for rel in KEY_ARTIFACTS:
        p = PROJECT_ROOT / rel
        if p.exists():
            manifest_rows.append(
                {
                    "path": rel,
                    "bytes": p.stat().st_size,
                    "sha256": sha256_of(p),
                }
            )
        else:
            missing_rows.append({"path": rel, "status": "missing"})

    manifest = pd.DataFrame(manifest_rows)
    manifest.to_csv(OUTPUTS / "day6_artifact_manifest.csv", index=False)

    if missing_rows:
        pd.DataFrame(missing_rows).to_csv(OUTPUTS / "day6_missing_artifacts.csv", index=False)

    pd.DataFrame(package_snapshot()).to_csv(OUTPUTS / "day6_requirements_snapshot.csv", index=False)

    run_meta = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "git_head": git_commit(),
        "artifact_count": int(len(manifest_rows)),
        "missing_count": int(len(missing_rows)),
    }

    (OUTPUTS / "day6_run_metadata.json").write_text(json.dumps(run_meta, indent=2))

    print("Step6 reproducibility polish outputs written.")


if __name__ == "__main__":
    main()
