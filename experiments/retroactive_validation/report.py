"""Detailed results report for the retroactive validation analyses.

Every figure in the report is read from the results dict or from the data
module at generation time; no result is typed into the prose. `run_all.py`
calls `write_report` after each run, and `scripts/generate_retroactive_report.py`
rebuilds the report from an existing `all_results.json`.
"""

from __future__ import annotations

import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import matplotlib
import numpy
import scipy

from .data import published_data as pd
from .tom_mapping import MQM_TO_SKILL, SKILL_ORDER, SKILL_TO_TOM_RANK, TOM_LEVEL_LABELS

REPORT_NAME = "Experiment_Report.md"

PUBLICATION = (
    "Diana Nurbakova and Liana Ermakova. 2026. *When Fluency Masks Failure: A Theory "
    "of Mind Model of Error Detection in Machine Translation Post-Editing.* In "
    "Proceedings of the IEEE/WIC International Conference on Web Intelligence and "
    "Intelligent Agent Technology (WI-IAT 2026)."
)

SKILL_NAMES = {"S1": "Surface", "S2": "Grammar", "S3": "Meaning", "S4": "Completeness",
               "S5": "Terminology", "S6": "Pragmatic", "S7": "Discourse"}


def _p(p: float | None) -> str:
    if p is None:
        return "—"
    return "< 0.001" if p < 0.001 else f"{p:.3f}"


def _pct(x: float) -> str:
    return "new (from 0)" if x == float("inf") else f"{x:+.0%}"


def _participants(n) -> str:
    if isinstance(n, dict):
        return ", ".join(f"{v} {k}" for k, v in n.items())
    return "—" if n is None else str(n)


def _cell(s) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def _findings(results: Dict, analysis_key: str) -> List[Dict]:
    return results[analysis_key]["findings"]


def _verified_sources() -> List[Dict]:
    return sorted((v for v in vars(pd).values()
                   if isinstance(v, dict) and "source" in v and "verified" in v),
                  key=lambda s: s["source"])


class _Writer:
    def __init__(self):
        self.lines: List[str] = []

    def __call__(self, s: str = ""):
        self.lines.append(s)

    def table(self, header: List[str], rows: List[List]):
        self("| " + " | ".join(header) + " |")
        self("|" + "---|" * len(header))
        for r in rows:
            self("| " + " | ".join(_cell(c) for c in r) + " |")
        self()

    def text(self) -> str:
        return "\n".join(self.lines)


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

def _header(w: _Writer, results: Dict):
    meta = results["metadata"]
    w("# Retroactive Validation of the ToM Framework for Post-Editing")
    w()
    w("Detailed results report. Generated from `all_results.json` and "
      "`data/published_data.py`; do not edit by hand.")
    w()
    w(f"- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    w(f"- **Run timestamp:** {meta['timestamp']}")
    w(f"- **Data version:** {meta['data_version']}")
    w(f"- **Tag:** `{meta['tag']}`")
    w(f"- **Excluded sources:** {', '.join(meta['excluded_sources']) or 'none'}")
    w(f"- **Publication:** {PUBLICATION}")
    w()
    w("---")
    w()


def _summary(w: _Writer, results: Dict):
    led = results["ledger"]
    w("## 1. Summary")
    w()
    rows = []
    for name, a in led["by_analysis"].items():
        d = a["by_direction"]
        rows.append([name, a["status"], d["support"], d["mixed"], d["against"],
                     d["uninformative"], ", ".join(a["sources"])])
    for name, why in results["metadata"]["withdrawn_analyses"].items():
        rows.append([name, "withdrawn", "", "", "", "", why])
    w.table(["Analysis", "Status", "Support", "Mixed", "Against", "Uninformative", "Sources"], rows)

    tested = [f for f in led["findings"] if f["basis"] == "numeric test"]
    n_sig = sum(1 for f in tested if f["detail"].get("significant_at_05"))
    w(f"- {led['n_findings']} findings from {led['n_distinct_sources']} distinct sources.")
    w(f"- {len(tested)} findings rest on an inferential test; {n_sig} of them "
      "reach p < 0.05.")
    w("- Analysis 1 (difficulty ordering) is withdrawn: no verified source reports "
      "detection difficulty by error type. It is still run (Section 5) but its "
      "findings are not counted in the ledger.")
    w("- Paper numbering: repository Analysis 2 is the paper's Analysis 1 (fluency "
      "paradox); repository Analysis 4 is the paper's Analysis 2 (over-editing).")
    for k in ["analysis2", "analysis4"]:
        w(f"- **{results[k]['experiment']}**: {results[k]['interpretation']}")
    w()
    w("---")
    w()


def _data_revision(w: _Writer):
    w("## 2. Data Revision (2026-10)")
    w()
    w("The source data were re-extracted from the full texts in October 2026. The "
      "earlier encoding required every source to yield per-category numbers on a "
      "comparable scale; where a source did not report in that shape, values were "
      "filled in. The verified module enforces three rules:")
    w()
    w("1. **No value without provenance.** Every numeric value names its table or page "
      "and the measure the source actually reports.")
    w("2. **Qualitative findings stay qualitative.** A direction reported without "
      "per-category figures is counted as a finding, never used as input to a "
      "correlation.")
    w("3. **Deletions are recorded.** Every dropped encoding is listed below with the reason.")
    w()
    w("### 2.1 Withdrawn encodings")
    w()
    w.table(["Encoding", "Was", "Reason", "Replacement (in `published_data.py`)"],
            [[k, v["was"], v["reason"], v["replacement"]] for k, v in pd.DELETED.items()])
    w("Results produced from the earlier encoding (the former convergence table, "
      "the Analysis 1 rank correlations, Analyses 3 and 3b) are superseded and "
      "should not be cited. They remain in the git history for audit.")
    w()
    w("---")
    w()


def _framework(w: _Writer):
    w("## 3. Framework: MQM-to-ToM Mapping")
    w()
    by_skill = {s: [c for c, sk in MQM_TO_SKILL.items() if sk == s] for s in SKILL_ORDER}
    w.table(["Skill", "ToM level", "Rank", "MQM categories"],
            [[f"{s} {SKILL_NAMES[s]}", TOM_LEVEL_LABELS[s], SKILL_TO_TOM_RANK[s],
              ", ".join(by_skill[s])] for s in SKILL_ORDER])
    w("- Ordinal scale: S1=1, S2=2, S3=3, S4=S5=S6=4 (tied), S7=5.")
    w("- Low-ToM = S1–S2; high-ToM = S3 and above.")
    w(f"- Mapping sensitivity: {pd.MAPPING_SENSITIVITY['issue']} Both assignments "
      "are reported for Analysis 4.")
    w()
    w("---")
    w()


def _sources(w: _Writer, results: Dict):
    w("## 4. Sources")
    w()
    w("### 4.1 Verified sources")
    w()
    rows = []
    for s in _verified_sources():
        pairs = s.get("language_pairs") or [s.get("language_pair", "—")]
        measure = (s.get("measure") or s.get("error_counts", {}).get("measure")
                   or s.get("aggregate", {}).get("measure") or "—")
        rows.append([s["source"], s["citation"], ", ".join(pairs),
                     _participants(s.get("n_participants")), measure])
    w.table(["Source", "Citation", "Pairs", "Participants", "Measure"], rows)

    w("### 4.2 Assignment to analyses")
    w()
    w.table(["Analysis", "Sources"],
            [[k, ", ".join(v) or "none (withdrawn)"] for k, v in pd.EXPERIMENT_SOURCES.items()])

    w("### 4.3 Not verified, not counted")
    w()
    w.table(["Source", "Status"], [[k, v] for k, v in pd.UNVERIFIED.items()])
    w("---")
    w()


def _ledger_rows(findings: List[Dict]) -> List[List]:
    return [[f["source"], f["direction"], f["basis"], f["claim"], f["source_location"]]
            for f in findings]


LEDGER_HEADER = ["Source", "Direction", "Basis", "Finding", "Location"]


def _analysis1(w: _Writer, results: Dict):
    a = results["analysis1"]
    w("## 5. Analysis 1: ToM Ordering vs. Detection Difficulty (withdrawn)")
    w()
    w(f"**Prediction.** {a['prediction']}.")
    w()
    w("**Status.** Withdrawn; findings below are kept for audit and not counted in "
      "the ledger. "
      f"{results['metadata']['withdrawn_analyses'].get('Analysis 1', '')} "
      "The rank correlations reported previously rested on values withdrawn in "
      "Section 2.1 (Daems fixation ranks, Yamada per-type correction rates, Popović "
      "category rates, Temnikova ranks).")
    w()
    w.table(LEDGER_HEADER, _ledger_rows(a["findings"]))
    w(f"**Interpretation.** {a['interpretation']}")
    w()
    w("---")
    w()


def _analysis2(w: _Writer, results: Dict):
    a = results["analysis2"]
    w("## 6. Analysis 2: Fluency Paradox")
    w()
    w(f"**Prediction.** {a['prediction']}.")
    w()
    w("**Method.** For sources with verified per-category error data, each high-ToM "
      "category's relative error change under NMT is compared with the mean low-ToM "
      "change. A source supports the prediction if every high-ToM category fell less "
      "than the low-ToM categories (or rose), contradicts it if none did, and is mixed "
      "otherwise. Aggregate and qualitative findings are recorded with the direction "
      "the source reports. No inferential test is applied: per-category counts from "
      "one corpus are not independent observations.")
    w()
    w("### 6.1 Findings")
    w()
    w.table(LEDGER_HEADER, _ledger_rows(a["findings"]))

    bent = next((f for f in a["findings"] if "per_pair" in f["detail"]), None)
    if bent:
        w("### 6.2 Bentivogli et al. (2018): relative error change, NMT vs PBMT")
        w()
        rows = []
        for pair, d in bent["detail"]["per_pair"].items():
            for c in d["categories"]:
                rows.append([pair, c["category"], c["skill"], _pct(c["change"])])
        w.table(["Pair", "Error class", "Skill", "Change"], rows)
        w(f"Caveat: {bent['detail']['caveat']}")
        w()

    vb = next((f for f in a["findings"] if "categories" in f["detail"]), None)
    if vb:
        w("### 6.3 Van Brussel et al. (2018): error counts by category")
        w()
        sec = a["secondary"]["VanBrussel2018_vs_RBMT"]
        rbmt = {c["category"]: c for c in sec["detail"]["categories"]} if sec else {}
        rows = []
        for c in vb["detail"]["categories"]:
            r = rbmt.get(c["category"])
            rows.append([c["category"], c["skill"], r["baseline"] if r else "—",
                         c["baseline"], c["NMT"], _pct(c["change"]),
                         _pct(r["change"]) if r else "—"])
        w.table(["Category", "Skill", "RBMT", "PBMT", "NMT", "NMT vs PBMT", "NMT vs RBMT"], rows)
        w(f"Against PBMT (primary): {vb['direction']}. Against RBMT (secondary, not "
          f"counted): {sec['direction'] if sec else '—'}.")
        w()

    w(f"**Interpretation.** {a['interpretation']}")
    w()
    against = [f for f in a["findings"] if f["direction"] == "against"]
    for f in against:
        note = f["detail"].get("note")
        if note:
            w(f"*Contrary evidence ({f['source']}).* {note}")
            w()
    w("---")
    w()


def _withdrawn(w: _Writer, results: Dict):
    w("## 7. Withdrawn Analyses")
    w()
    for name, why in results["metadata"]["withdrawn_analyses"].items():
        w(f"- **{name}.** {why}")
    w()
    w("---")
    w()


def _analysis4(w: _Writer, results: Dict):
    a = results["analysis4"]
    w("## 8. Analysis 4: Over-Editing as Misdirected ToM")
    w()
    w(f"**Prediction.** {a['prediction']}.")
    w()
    w("**Method.** For sources reporting the rate at which edits of each type were "
      "unnecessary, Kendall's τ-b between ToM rank and that rate (two-sided p). "
      "Deletions are assigned to S2 (primary) and to S4 (alternative); both are reported.")
    w()
    w("### 8.1 Findings")
    w()
    w.table(LEDGER_HEADER, _ledger_rows(a["findings"]))

    w("### 8.2 Rank correlations under both mappings")
    w()
    rows = []
    for f in a["findings"]:
        for d, m in f["detail"].get("mappings", {}).items():
            rows.append([f["source"], f"deleted = {d}", m["n"],
                         f"{m['kendall_tau']:+.3f}", _p(m["p_value"])])
    w.table(["Source", "Mapping", "n", "τ", "p"], rows)

    w("### 8.3 Per-type unnecessary-edit rates")
    w()
    rows = []
    for f in a["findings"]:
        m = f["detail"].get("mappings", {}).get("S2")
        if not m:
            continue
        for r in m["per_type"]:
            rows.append([f["source"], r["edit_type"], r["skill"], f"{r['unnecessary_rate']:.0%}",
                         r.get("total", "—")])
    w.table(["Source", "Edit type", "Skill (primary)", "Unnecessary", "Edits"], rows)
    w(f"Note: {pd.MAPPING_SENSITIVITY['note']} Ranks span S2–S4 only; neither source "
      "has S1, S5–S7 categories.")
    w()
    w(f"**Interpretation.** {a['interpretation']}")
    w()
    w("---")
    w()


def _ledger(w: _Writer, results: Dict):
    led = results["ledger"]
    w("## 9. Evidence Ledger")
    w()
    w("The ledger replaces the former category-by-analysis convergence table and its "
      "convergence ratio. Findings differ in basis and measure, so they are counted, "
      "not pooled, and no ratio or binomial test is computed.")
    w()
    bases = list(next(iter(led["by_direction_and_basis"].values())).keys())
    w.table(["Direction"] + bases + ["Total"],
            [[d] + [row[b] for b in bases] + [sum(row.values())]
             for d, row in led["by_direction_and_basis"].items()])
    w(led["note"])
    w()
    multi = {}
    for f in led["findings"]:
        multi.setdefault(f["source"], set()).add(f["analysis"])
    shared = [s for s, an in multi.items() if len(an) > 1]
    if shared:
        w(f"Sources contributing to more than one analysis: {', '.join(sorted(shared))}.")
        w()
    w("---")
    w()


def _limitations(w: _Writer, results: Dict):
    led = results["ledger"]
    tested = [f for f in led["findings"] if f["basis"] == "numeric test"]
    w("## 10. Limitations")
    w()
    w(f"- Only {len(tested)} findings rest on an inferential test, and none reaches "
      "significance. The retrospective evidence is directional, not confirmatory."
      if not any(f["detail"].get("significant_at_05") for f in tested) else
      f"- {len(tested)} findings rest on an inferential test.")
    w("- The difficulty gradient (Analysis 1) has no quantitative support in the "
      "verified literature and is withdrawn; it is tested on the WMT 2020 MQM "
      "annotations instead (`tom_validation`).")
    w("- Measures differ between sources and are not commensurable; directions are "
      "compared, magnitudes are not.")
    w("- Nitzke & Gros (2020) and Mellinger & Shreve (2016) are excluded pending "
      "verification; Stasimioti & Sosoni (2021) contributes no data.")
    w("- The direction rule in Analysis 2 counts consistent comparisons; it does not "
      "weight categories by size.")
    w()
    w("---")
    w()


def _reproducibility(w: _Writer, results: Dict):
    w("## 11. Outputs and Reproducibility")
    w()
    w.table(["File", "Contents"], [
        ["`all_results.json`", "Structured results for every analysis and the ledger"],
        ["`ledger_counts.tex`", "Ledger headline counts as `\\newcommand` macros; the paper `\\input`s it"],
        [f"`{REPORT_NAME}`", "This report"],
        ["`F5_fluency_paradox.pdf` (+ `.png`)", "Analysis 2: relative error change by category; omission visibility"],
        ["`F5_fluency_paradox_stacked.pdf` (+ `.png`)", "Same as F5, panels stacked for single-column width"],
        ["`F7_overediting.pdf` (+ `.png`)", "Analysis 4: unnecessary-edit rate by edit type, both mappings"],
    ])
    w("```bash")
    w("python -m experiments.retroactive_validation.run_all            # full run, writes this report")
    w("python -m experiments.retroactive_validation.run_all --exclude Koponen2019   # sensitivity")
    w("python scripts/generate_retroactive_report.py                    # rebuild report from JSON")
    w("```")
    w()
    w(f"Environment at generation: Python {platform.python_version()}, SciPy "
      f"{scipy.__version__}, NumPy {numpy.__version__}, Matplotlib {matplotlib.__version__}.")
    w()


def build_report(results: Dict) -> str:
    w = _Writer()
    _header(w, results)
    _summary(w, results)
    _data_revision(w)
    _framework(w)
    _sources(w, results)
    _analysis1(w, results)
    _analysis2(w, results)
    _withdrawn(w, results)
    _analysis4(w, results)
    _ledger(w, results)
    _limitations(w, results)
    _reproducibility(w, results)
    return w.text()


def write_report(results: Dict, output_dir: Path) -> Path:
    path = output_dir / REPORT_NAME
    path.write_text(build_report(results), encoding="utf-8")
    return path
