"""Analysis 2: Fluency paradox as ToM-selective detection impairment.

Prediction: NMT's fluency gain reduces low-ToM errors (S1-S2) more than
high-ToM errors (S3+), and leaves post-editors less able to catch what remains.

Operationalisation for per-category error data: each high-ToM category's
relative NMT error change is compared with the mean low-ToM change. The source
supports the prediction if every high-ToM category falls less than the
low-ToM categories, contradicts it if none does, and is mixed otherwise. This
counts direction-consistent comparisons; it is not a significance test.
"""

from __future__ import annotations

from typing import Dict, List

import numpy as np

from .data import published_data as pd
from .evidence_ledger import (
    AGAINST, MIXED, NUMERIC_DESCRIPTIVE, SUPPORT, finding,
)
from .tom_mapping import SKILL_TO_TOM_RANK, is_low_tom

ANALYSIS = "Analysis 2"


def _relative_change(new: float, old: float) -> float:
    """(new - old) / old. Negative = fewer errors under the newer system."""
    return (new - old) / old if old else float("inf")


def _direction_verdict(categories: List[Dict]) -> Dict:
    """Compare each high-ToM category's change against the mean low-ToM change."""
    low = [c["change"] for c in categories if is_low_tom(c["skill"])]
    low_mean = float(np.mean(low))
    comparisons = []
    for c in categories:
        if is_low_tom(c["skill"]):
            continue
        comparisons.append({
            "category": c["category"],
            "skill": c["skill"],
            "change": c["change"],
            "consistent": c["change"] > low_mean,  # fell less (or rose) than low-ToM
        })
    n_ok = sum(c["consistent"] for c in comparisons)
    if n_ok == len(comparisons):
        direction = SUPPORT
    elif n_ok == 0:
        direction = AGAINST
    else:
        direction = MIXED
    return {
        "low_tom_mean_change": round(low_mean, 4),
        "comparisons": comparisons,
        "n_consistent": n_ok,
        "n_comparisons": len(comparisons),
        "direction": direction,
    }


def analyze_bentivogli(src: Dict) -> List[Dict]:
    """Relative error reduction, NMT vs PBMT, per HTER error class and pair."""
    out = []
    per_pair = {}
    for pair in ["EnDe", "EnFr"]:
        cats = [{"category": m["error_class"], "skill": m["skill"],
                 "change": m[f"reduction_{pair}"] / 100} for m in src["measures"]]
        per_pair[pair] = {"categories": cats, **_direction_verdict(cats)}
    dirs = {v["direction"] for v in per_pair.values()}
    direction = dirs.pop() if len(dirs) == 1 else MIXED
    out.append(finding(
        ANALYSIS, src["source"],
        "NMT reduced word-order and morphology errors (S2) more than lexical "
        "errors (S3), in both language pairs.",
        direction, NUMERIC_DESCRIPTIVE, src["source_location"],
        {"per_pair": per_pair, "caveat": src["note"]},
    ))

    share = src["lexical_share_of_residual_errors"]
    out.append(finding(
        ANALYSIS, src["source"],
        "Lexical errors' share of residual errors rises from PBMT to NMT "
        f"(EnDe {share['EnDe']['PBMT']}% -> {share['EnDe']['NMT']}%, "
        f"EnFr {share['EnFr']['PBMT']}% -> {share['EnFr']['NMT']}%).",
        SUPPORT, NUMERIC_DESCRIPTIVE, share["source_location"],
        {"note": share["note"]},
    ))
    return out


def analyze_van_brussel(src: Dict, baseline: str = "PBMT") -> List[Dict]:
    """Annotated error counts, NMT vs a baseline system, per category."""
    counts = src["error_counts"]
    cats = []
    for name, c in counts.items():
        if not isinstance(c, dict) or "skill" not in c:
            continue
        cats.append({
            "category": name, "skill": c["skill"],
            "tom_rank": SKILL_TO_TOM_RANK[c["skill"]],
            "baseline": c[baseline], "NMT": c["NMT"],
            "change": round(_relative_change(c["NMT"], c[baseline]), 4),
        })
    verdict = _direction_verdict(cats)
    off = [c["category"] for c in verdict["comparisons"] if not c["consistent"]]
    out = [finding(
        ANALYSIS, src["source"],
        f"Error counts NMT vs {baseline}: grammar (S2) fell "
        f"{-verdict['low_tom_mean_change']:.0%}; "
        f"{verdict['n_consistent']}/{verdict['n_comparisons']} high-ToM categories "
        f"fell less or rose" + (f" (exception: {', '.join(off)})." if off else "."),
        verdict["direction"], NUMERIC_DESCRIPTIVE, counts["source_location"],
        {"baseline": baseline, "categories": cats, **verdict},
    )]

    vis = src["omission_visibility"]
    out.append(finding(
        ANALYSIS, src["source"],
        f"Omissions with no trace in the target: RBMT {vis['RBMT']:.0%}, "
        f"PBMT {vis['PBMT']:.0%}, NMT {vis['NMT']:.0%}. In NMT, fluency no longer "
        "signals that source content is missing.",
        SUPPORT, NUMERIC_DESCRIPTIVE, vis["source_location"],
        {k: vis[k] for k in ["RBMT", "PBMT", "NMT", "content_word_share",
                             "words_per_omission", "note"]},
    ))
    return out


def analyze_yamada(src: Dict) -> List[Dict]:
    """Aggregate correction rate of major errors, SMT+PE vs NMT+PE."""
    agg = src["aggregate"]
    smt, nmt = agg["SMT_PE"]["correction_rate"], agg["NMT_PE"]["correction_rate"]
    return [finding(
        ANALYSIS, src["source"],
        f"Students corrected {smt:.1%} of major errors in SMT output but "
        f"{nmt:.0%} in NMT output.",
        SUPPORT if nmt < smt else AGAINST, NUMERIC_DESCRIPTIVE,
        agg["source_location"],
        {"SMT_PE": agg["SMT_PE"], "NMT_PE": agg["NMT_PE"],
         "raw_output_quality": src["raw_output_quality"]["note"],
         "caveat": "Aggregate only; no per-type correction rates."},
    )]


def analyze_koponen_2019(src: Dict) -> List[Dict]:
    """Overlooked necessary corrections: system totals only."""
    o = src["overlooked"]
    return [finding(
        ANALYSIS, src["source"],
        f"Overlooked necessary corrections: NMT {o['NMT']['pct_of_unedited']}%, "
        f"SMT {o['SMT']['pct_of_unedited']}%, RBMT {o['RBMT']['pct_of_unedited']}% "
        "of unedited words. NMT has the fewest.",
        AGAINST, NUMERIC_DESCRIPTIVE, o["source_location"],
        {s: o[s] for s in ["NMT", "SMT", "RBMT"]} | {"note": o["note"]},
    )]


ANALYZERS = {
    "Bentivogli2018": analyze_bentivogli,
    "VanBrussel2018": analyze_van_brussel,
    "Yamada2019": analyze_yamada,
    "Koponen2019": analyze_koponen_2019,
}


def run_all(sources: List[Dict]) -> Dict:
    findings = []
    for src in sources:
        if src["source"] in ANALYZERS:
            findings.extend(ANALYZERS[src["source"]](src))

    # Secondary: Van Brussel against RBMT instead of PBMT (reported, not counted)
    vb = next((s for s in sources if s["source"] == "VanBrussel2018"), None)
    secondary = analyze_van_brussel(vb, baseline="RBMT")[0] if vb else None

    n = {d: sum(f["direction"] == d for f in findings) for d in (SUPPORT, MIXED, AGAINST)}
    return {
        "experiment": "Analysis2_FluencyParadox",
        "prediction": ("NMT reduces low-ToM errors more than high-ToM errors, and "
                       "post-editors catch fewer of the errors that remain"),
        "status": "run",
        "findings": findings,
        "secondary": {"VanBrussel2018_vs_RBMT": secondary},
        "interpretation": (f"{n[SUPPORT]} supporting, {n[MIXED]} mixed and "
                           f"{n[AGAINST]} contrary findings from "
                           f"{len({f['source'] for f in findings})} sources. "
                           "No finding rests on an inferential test."),
    }
