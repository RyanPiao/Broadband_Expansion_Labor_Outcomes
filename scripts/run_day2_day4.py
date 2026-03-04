#!/usr/bin/env python3
"""Run Day2-Day4 pipeline in order."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

STEPS = [
    "scripts/day2_ingest_build_panel.py",
    "scripts/day3_eda.py",
    "scripts/day4_baseline_model.py",
]


def main() -> None:
    for step in STEPS:
        print(f"\n=== Running {step} ===")
        subprocess.run([sys.executable, str(PROJECT_ROOT / step)], check=True)
    print("\nDay2-Day4 pipeline complete.")


if __name__ == "__main__":
    main()
