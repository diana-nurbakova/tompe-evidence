"""Figures for the retroactive validation analyses.

F5  Analysis 2: NMT error change by ToM level, and omission visibility.
F7  Analysis 4: unnecessary-edit rate by ToM rank, both 'deleted' mappings.

Only verified numeric values are plotted. Qualitative findings appear in the
evidence ledger table, not in figures.
"""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Dict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Validated default categorical slots, fixed order (dataviz reference palette)
SLOT = ["#2a78d6", "#eb6834", "#1baf7a"]
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
SURFACE = "#fcfcfb"

# ToM group -> slot: low (S1-S2), meaning (S3), author/reader (S4+)
SKILL_SLOT = {"S1": 0, "S2": 0, "S3": 1, "S4": 2, "S5": 2, "S6": 2, "S7": 2}
GROUP_LABEL = ["S1–S2 (machine, form)", "S3 (machine, meaning)", "S4+ (author / reader)"]


def _style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK_2)
    ax.tick_params(colors=INK_2, labelsize=8)
    ax.grid(axis="x", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def _group_legend(fig):
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in SLOT]
    fig.legend(handles, GROUP_LABEL, loc="lower center", ncol=3, frameon=False,
               fontsize=8, labelcolor=INK_2, bbox_to_anchor=(0.5, -0.02))


def figure_f5_fluency(exp2: Dict, output_dir: Path) -> Path:
    """Analysis 2: relative NMT error change per category, plus omission visibility."""
    bent = next(f for f in exp2["findings"]
                if f["source"] == "Bentivogli2018" and "per_pair" in f["detail"])
    vb = next(f for f in exp2["findings"]
              if f["source"] == "VanBrussel2018" and "categories" in f["detail"])
    vis = next(f for f in exp2["findings"]
               if f["source"] == "VanBrussel2018" and "content_word_share" in f["detail"])

    rows = []  # (label, change, skill)
    for pair, d in bent["detail"]["per_pair"].items():
        for c in d["categories"]:
            rows.append((f"Bentivogli {pair[:2]}–{pair[2:]}: {c['category']}", c["change"], c["skill"]))
    for c in vb["detail"]["categories"]:
        rows.append((f"Van Brussel: {c['category'].replace('_', ' ')}", c["change"], c["skill"]))

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(10, 4.6), gridspec_kw={"width_ratios": [2.3, 1]}, facecolor=SURFACE)

    # Clip the one extreme value (semantically unrelated, +389%) and label it
    clip = 1.2
    ys = range(len(rows))[::-1]
    for y, (label, change, skill) in zip(ys, rows):
        shown = max(min(change, clip), -1)
        ax1.barh(y, shown, height=0.62, color=SLOT[SKILL_SLOT[skill]])
        txt = f"{change:+.0%}" + (" →" if change > clip else "")
        ax1.text(shown + (0.03 if shown >= 0 else -0.03), y, txt, va="center",
                 ha="left" if shown >= 0 else "right", fontsize=7, color=INK_2)
    ax1.set_yticks(list(ys))
    ax1.set_yticklabels([r[0] for r in rows], fontsize=7.5, color=INK)
    ax1.axvline(0, color=INK_2, linewidth=0.8)
    ax1.set_xlim(-1.15, clip + 0.35)
    ax1.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax1.set_xlabel("Relative error change, NMT vs PBMT (negative = fewer errors)",
                   fontsize=8, color=INK_2)
    ax1.set_title("NMT removes form errors more than meaning errors",
                  fontsize=9.5, color=INK, loc="left")
    _style(ax1)

    systems = ["RBMT", "PBMT", "NMT"]
    vals = [vis["detail"][s] for s in systems]
    ax2.bar(systems, vals, width=0.55, color=SLOT[2])
    for x, v in enumerate(vals):
        ax2.text(x, v + 0.02, f"{v:.0%}", ha="center", fontsize=8, color=INK)
    ax2.set_ylim(0, 0.85)
    ax2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax2.set_title("Omissions with no trace in the target\n(Van Brussel et al., Table 6)",
                  fontsize=9.5, color=INK, loc="left")
    _style(ax2)
    ax2.grid(axis="x", visible=False)
    ax2.grid(axis="y", color=GRID, linewidth=0.6)

    _group_legend(fig)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    path = output_dir / "F5_fluency_paradox.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    return path


def figure_f7_overediting(exp4: Dict, output_dir: Path) -> Path:
    """Analysis 4: unnecessary-edit rate by edit type, ordered by ToM rank."""
    tested = [f for f in exp4["findings"] if "mappings" in f["detail"]]
    fig, axes = plt.subplots(1, len(tested), figsize=(4.4 * len(tested), 3.8),
                             sharey=True, facecolor=SURFACE)
    axes = axes if len(tested) > 1 else [axes]

    for ax, f in zip(axes, tested):
        primary = f["detail"]["mappings"]["S2"]
        rows = sorted(primary["per_type"], key=lambda r: (r["tom_rank"], -r["unnecessary_rate"]))
        for x, r in enumerate(rows):
            ax.bar(x, r["unnecessary_rate"], width=0.6, color=SLOT[SKILL_SLOT[r["skill"]]],
                   hatch="//" if r["edit_type"].lower().startswith("delet") else None,
                   edgecolor=SURFACE, linewidth=0)
            ax.text(x, r["unnecessary_rate"] + 0.015, f"{r['unnecessary_rate']:.0%}",
                    ha="center", fontsize=7.5, color=INK)
        ax.set_xticks(range(len(rows)))
        ax.set_xticklabels([f"{textwrap.fill(r['edit_type'], 11, break_long_words=False)}\n{r['skill']}" for r in rows],
                           fontsize=7, color=INK)
        alt = f["detail"]["mappings"]["S4"]
        ax.set_title(f"{f['source']}\n"
                     f"τ = {primary['kendall_tau']:+.2f} (p = {primary['p_value']:.2f}); "
                     f"deleted→S4: τ = {alt['kendall_tau']:+.2f} (p = {alt['p_value']:.2f})",
                     fontsize=8, color=INK, loc="left")
        ax.set_ylim(0, 0.95)
        ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
        _style(ax)
        ax.grid(axis="x", visible=False)
        ax.grid(axis="y", color=GRID, linewidth=0.6)
    axes[0].set_ylabel("Edits of this type judged unnecessary", fontsize=8, color=INK_2)

    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in SLOT]
    handles.append(plt.Rectangle((0, 0), 1, 1, facecolor=SLOT[0], hatch="//",
                                 edgecolor=SURFACE, linewidth=0))
    fig.legend(handles, GROUP_LABEL + ["Deletions (S2; S4 alternative)"],
               loc="lower center", ncol=4, frameon=False, fontsize=8,
               labelcolor=INK_2, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    path = output_dir / "F7_overediting.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    return path
