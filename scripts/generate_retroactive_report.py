#!/usr/bin/env python3
"""Rebuild the retroactive validation report from existing results.

`run_all.py` writes the report after every run; use this script to regenerate it
without re-running the analyses (e.g. after editing `report.py`).

Usage:
    python scripts/generate_retroactive_report.py               # full run
    python scripts/generate_retroactive_report.py --tag no_koponen2019

Reads:
    outputs/retroactive_validation[/<tag>]/all_results.json
    experiments/retroactive_validation/data/published_data.py

Writes:
    outputs/retroactive_validation[/<tag>]/Experiment_Report.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from experiments.retroactive_validation.report import write_report

BASE_DIR = ROOT / "outputs" / "retroactive_validation"


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild the retroactive validation report")
    parser.add_argument("--tag", default="full", help="Run tag (default: full)")
    args = parser.parse_args()

    results_dir = BASE_DIR if args.tag == "full" else BASE_DIR / args.tag
    results = json.loads((results_dir / "all_results.json").read_text(encoding="utf-8"))
    path = write_report(results, results_dir)
    text = path.read_text(encoding="utf-8")
    print(f"Report written to {path}")
    print(f"  Length: {len(text):,} characters, {text.count(chr(10)):,} lines")


if __name__ == "__main__":
    main()
