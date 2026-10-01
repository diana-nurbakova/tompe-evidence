"""Evidence ledger: synthesis of Analyses 1-4.

Replaces the former category-by-analysis convergence table. That table needed a
per-category value from every source, which the verified data no longer supply
(see `published_data.py`, rule 2). The ledger instead records one entry per
finding, with the basis it rests on, and counts findings by direction. No
convergence ratio or binomial test is computed: findings with different bases
and measures are not exchangeable draws.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, List, Optional

# Direction of a finding relative to the analysis prediction
SUPPORT = "support"
AGAINST = "against"
MIXED = "mixed"
UNINFORMATIVE = "uninformative"
DIRECTIONS = [SUPPORT, MIXED, AGAINST, UNINFORMATIVE]

# What the finding rests on
NUMERIC_TEST = "numeric test"            # inferential statistic on verified values
NUMERIC_DESCRIPTIVE = "numeric descriptive"  # verified values compared, no test
QUALITATIVE = "qualitative"              # direction stated by the source, no values
BASES = [NUMERIC_TEST, NUMERIC_DESCRIPTIVE, QUALITATIVE]


def finding(
    analysis: str,
    source: str,
    claim: str,
    direction: str,
    basis: str,
    source_location: str,
    detail: Optional[Dict] = None,
) -> Dict:
    """Build one ledger entry."""
    assert direction in DIRECTIONS, direction
    assert basis in BASES, basis
    return {
        "analysis": analysis,
        "source": source,
        "claim": claim,
        "direction": direction,
        "basis": basis,
        "source_location": source_location,
        "detail": detail or {},
    }


def summarise(analyses: Dict[str, Dict]) -> Dict:
    """Collect findings from every analysis and count them by direction and basis."""
    findings: List[Dict] = []
    for result in analyses.values():
        findings.extend(result.get("findings", []))

    by_analysis = {}
    for name, result in analyses.items():
        fs = result.get("findings", [])
        by_analysis[name] = {
            "status": result.get("status", "run"),
            "n_findings": len(fs),
            "by_direction": {d: sum(f["direction"] == d for f in fs) for d in DIRECTIONS},
            "sources": sorted({f["source"] for f in fs}),
        }

    cross = Counter((f["direction"], f["basis"]) for f in findings)
    return {
        "experiment": "EvidenceLedger",
        "findings": findings,
        "by_analysis": by_analysis,
        "by_direction_and_basis": {
            d: {b: cross[(d, b)] for b in BASES} for d in DIRECTIONS
        },
        "n_findings": len(findings),
        "n_distinct_sources": len({f["source"] for f in findings}),
        "note": ("Counts of findings, not of independent tests. A source can "
                 "contribute more than one finding, and to more than one analysis."),
    }
