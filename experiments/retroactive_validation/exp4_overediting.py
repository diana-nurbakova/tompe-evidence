"""Analysis 4: Over-editing as misdirected ToM.

Prediction: unnecessary edits concentrate on low-ToM dimensions (S1-S2), where
a well-developed machine model raises false alarms; they are rare at higher
ToM levels. Tested as a negative Kendall tau between ToM rank and the rate at
which edits of each type were unnecessary.

The edit type 'deleted' has two defensible assignments (S2 or S4; see
`published_data.MAPPING_SENSITIVITY`). Both are always reported; S2, the
encoded assignment, is primary.
"""

from __future__ import annotations

from typing import Dict, List

from scipy import stats

from .data import published_data as pd
from .evidence_ledger import (
    AGAINST, MIXED, NUMERIC_DESCRIPTIVE, NUMERIC_TEST, QUALITATIVE, SUPPORT,
    UNINFORMATIVE, finding,
)
from .tom_mapping import SKILL_TO_TOM_RANK

ANALYSIS = "Analysis 4"
DELETED_MAPPINGS = ("S2", "S4")


def _is_deletion(edit_type: str) -> bool:
    return edit_type.lower().startswith("delet")


def rate_by_rank(src: Dict, deleted_skill: str) -> Dict:
    """Kendall tau between ToM rank and unnecessary rate, for one mapping."""
    rows = []
    for m in src["measures"]:
        skill = deleted_skill if _is_deletion(m["edit_type"]) else m["skill"]
        rows.append({"edit_type": m["edit_type"], "skill": skill,
                     "tom_rank": SKILL_TO_TOM_RANK[skill],
                     "unnecessary_rate": m["unnecessary_rate"],
                     **({"total": m["total"]} if "total" in m else {})})
    tau, p = stats.kendalltau([r["tom_rank"] for r in rows],
                              [r["unnecessary_rate"] for r in rows])
    return {"deleted": deleted_skill, "n": len(rows),
            "kendall_tau": round(float(tau), 4), "p_value": round(float(p), 4),
            "per_type": rows}


def analyze_rates(src: Dict) -> List[Dict]:
    runs = {d: rate_by_rank(src, d) for d in DELETED_MAPPINGS}
    primary = runs["S2"]
    signs = {r["kendall_tau"] < 0 for r in runs.values()}
    direction = SUPPORT if signs == {True} else AGAINST if signs == {False} else MIXED
    taus = ", ".join(f"deleted={d}: tau={r['kendall_tau']:+.3f}, p={r['p_value']:.3f}"
                     for d, r in runs.items())
    return [finding(
        ANALYSIS, src["source"],
        f"Unnecessary-edit rate falls with ToM rank ({taus}); not significant "
        "under either mapping. Ranks span S2-S4 only.",
        direction, NUMERIC_TEST, src["source_location"],
        {"measure": src["measure"], "mappings": runs,
         "significant_at_05": primary["p_value"] < 0.05},
    )]


def analyze_de_almeida(src: Dict) -> List[Dict]:
    agg = src["aggregate"]
    return [finding(
        ANALYSIS, src["source"],
        f"Preferential changes were {agg['EN-PT-BR']['preferential']}% (EN-PT-BR) "
        f"to {agg['EN-FR']['preferential']}% (EN-FR) of recorded items; the most "
        "experienced translators made the most preferential changes.",
        MIXED, NUMERIC_DESCRIPTIVE, src["source_location"],
        {"aggregate": agg, "note": src["note"]},
    )]


def analyze_koponen_2015() -> List[Dict]:
    d = pd.DELETED["Koponen2015.performance_by_session"]
    return [finding(
        ANALYSIS, "Koponen2015", d["replacement"],
        UNINFORMATIVE, QUALITATIVE,
        "Koponen (2015), thematic analysis of reflective essays",
        {"why_uninformative": "Over-editing is reported, but not by error type, "
                              "so it does not bear on where over-editing concentrates."},
    )]


def run_all(sources: List[Dict]) -> Dict:
    findings = []
    for src in sources:
        if src["source"] in ("KoponenSalmi2017", "Koponen2019"):
            findings.extend(analyze_rates(src))
        elif src["source"] == "DeAlmeida2013":
            findings.extend(analyze_de_almeida(src))
    findings.extend(analyze_koponen_2015())

    tested = [f for f in findings if f["basis"] == NUMERIC_TEST]
    return {
        "experiment": "Analysis4_OverEditing",
        "prediction": ("Unnecessary edits concentrate on low-ToM types; negative "
                       "tau between ToM rank and unnecessary-edit rate"),
        "status": "run",
        "findings": findings,
        "not_counted": {k: v for k, v in pd.UNVERIFIED.items()
                        if k in ("NitzkeGros2020", "MellingerShreve2016")},
        "mapping_sensitivity": pd.MAPPING_SENSITIVITY,
        "interpretation": (
            f"{sum(f['direction'] == SUPPORT for f in tested)}/{len(tested)} sources "
            "with per-type rates show the predicted negative tau under both "
            "mappings; none is significant. Nitzke & Gros and Mellinger & Shreve "
            "are not counted until verified."),
    }
