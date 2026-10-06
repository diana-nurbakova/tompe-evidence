"""Retroactive validation experiment orchestrator.

Runs the analyses that the verified source data support and produces:
- JSON results (per-analysis + evidence ledger)
- Figures F5 (Analysis 2; full-width and single-column stacked) and F7 (Analysis 4)
- The detailed results report (Experiment_Report.md, via report.py)

Analyses 3 (expertise) and 3b (development) are withdrawn: no verified source
provides data for them (see `data/published_data.py`, EXPERIMENT_SOURCES).

Usage:
    python -m experiments.retroactive_validation.run_all
    python -m experiments.retroactive_validation.run_all --exclude Koponen2019 --tag no_koponen2019
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from experiments.retroactive_validation.data import published_data as pd
from experiments.retroactive_validation import exp1_difficulty_ordering as exp1
from experiments.retroactive_validation import exp2_fluency_paradox as exp2
from experiments.retroactive_validation import exp4_overediting as exp4
from experiments.retroactive_validation import evidence_ledger as ledger
from experiments.retroactive_validation import visualizations as viz
from experiments.retroactive_validation import report


BASE_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "retroactive_validation"

WITHDRAWN = {
    "Analysis 3": "Expertise: no inferential source survives verification.",
    "Analysis 3b": "Development: Koponen (2015) contains no per-type or per-session data.",
}


def all_sources() -> dict:
    """Every verified source record in the data module, keyed by source name."""
    return {v["source"]: v for v in vars(pd).values()
            if isinstance(v, dict) and "source" in v and "verified" in v}


def sources_for(analysis_key: str, exclude: list[str]) -> list[dict]:
    """Verified records named for an analysis in EXPERIMENT_SOURCES."""
    records = all_sources()
    names = [entry.split(" (")[0] for entry in pd.EXPERIMENT_SOURCES[analysis_key]]
    return [records[n] for n in names if n in records and n not in exclude]


def print_summary(results: dict):
    sep = "=" * 70
    print(f"\n{sep}\nRETROACTIVE VALIDATION -- RESULTS [{results['metadata']['tag']}]\n{sep}")
    for key in ["analysis1", "analysis2", "analysis4"]:
        r = results[key]
        print(f"\n  {r['experiment']}\n  Prediction: {r['prediction']}\n  >> {r['interpretation']}")
    for name, why in WITHDRAWN.items():
        print(f"\n  {name}: WITHDRAWN. {why}")
    print(f"\n  Ledger: {results['ledger']['n_findings']} findings from "
          f"{results['ledger']['n_distinct_sources']} sources")
    for d, row in results["ledger"]["by_direction_and_basis"].items():
        print(f"    {d:<14}" + "  ".join(f"{b}: {row[b]}" for b in ledger.BASES))
    print(sep)


def run(exclude: list[str] | None = None, tag: str = "full",
        output_dir: Path | None = None) -> dict:
    """Run all analyses with optional source exclusion.

    Args:
        exclude: Source names to exclude (e.g. ["Koponen2019"]).
        tag: Label for this run variant (used in metadata and output path).
        output_dir: Override output directory. Defaults to
            outputs/retroactive_validation/ (full) or .../<tag>/.
    """
    exclude = exclude or []
    if output_dir is None:
        output_dir = BASE_OUTPUT_DIR / tag if tag != "full" else BASE_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    a2_sources = sources_for("analysis_2_fluency", exclude)
    a4_sources = sources_for("analysis_4_overediting", exclude)

    print("[1/4] Analysis 1: difficulty ordering (qualitative only)...")
    a1 = exp1.run_all()
    if exclude:
        a1["findings"] = [f for f in a1["findings"] if f["source"] not in exclude]
    print(f"[2/4] Analysis 2: fluency paradox ({len(a2_sources)} sources)...")
    a2 = exp2.run_all(a2_sources)
    print(f"[3/4] Analysis 4: over-editing ({len(a4_sources)} sources)...")
    a4 = exp4.run_all(a4_sources)
    print("[4/4] Evidence ledger...")
    summary = ledger.summarise({"Analysis 1": a1, "Analysis 2": a2, "Analysis 4": a4})

    results = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "data_version": "published_data.py verified 2026-10",
            "tag": tag,
            "excluded_sources": exclude,
            "withdrawn_analyses": WITHDRAWN,
            "source_counts": {"analysis2": len(a2_sources), "analysis4": len(a4_sources)},
        },
        "analysis1": a1,
        "analysis2": a2,
        "analysis4": a4,
        "ledger": summary,
    }

    results_path = output_dir / "all_results.json"
    results_path.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\nResults saved to {results_path}")

    print("\nGenerating figures and report...")
    print(f"  F5: {viz.figure_f5_fluency(a2, output_dir)}")
    print(f"  F5 (stacked): {viz.figure_f5_fluency_stacked(a2, output_dir)}")
    print(f"  F7: {viz.figure_f7_overediting(a4, output_dir)}")
    print(f"  {report.write_report(results, output_dir)}")

    print_summary(results)
    return results


def main():
    parser = argparse.ArgumentParser(description="Retroactive validation experiments")
    parser.add_argument("--exclude", nargs="+", default=[],
                        help="Source names to exclude (e.g. Koponen2019)")
    parser.add_argument("--tag", default=None,
                        help="Label for this run variant (default: no_<sources> or full)")
    args = parser.parse_args()
    if args.tag is None:
        args.tag = ("no_" + "_".join(n.lower() for n in args.exclude)) if args.exclude else "full"
    run(exclude=args.exclude, tag=args.tag)


if __name__ == "__main__":
    main()
