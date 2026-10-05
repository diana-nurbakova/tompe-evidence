"""Figures for the retroactive validation analyses.

F5  Analysis 2: NMT error change by ToM level, and omission visibility.
F7  Analysis 4: unnecessary-edit rate by ToM rank, both 'deleted' mappings.

Only verified numeric values are plotted. Qualitative findings appear in the
evidence ledger table, not in figures.

Sized for a two-column IEEE page: F5 spans both columns (7.0 in), F7 fits one
column (3.4 in). Each figure is written as PDF (for \\includegraphics) and PNG.
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
SURFACE = "white"

# ToM group -> slot: low (S1-S2), meaning (S3), author/reader (S4+)
SKILL_SLOT = {"S1": 0, "S2": 0, "S3": 1, "S4": 2, "S5": 2, "S6": 2, "S7": 2}
GROUP_LABEL = ["S1–S2 (machine, form)", "S3 (machine, meaning)", "S4+ (author / reader)"]

# Source key -> citation as the bibliography gives it. Every key that reaches
# visible text goes through this map; a missing key raises rather than leaking.
DISPLAY_NAME = {
    "KoponenSalmi2017":    "Koponen & Salmi (2017)",
    "Koponen2019":         "Koponen et al. (2019)",
    "Bentivogli2018":      "Bentivogli et al. (2018)",
    "VanBrussel2018":      "Van Brussel et al. (2018)",
    "Yamada2019":          "Yamada (2019)",
    "Popovic2018":         "Popović (2018)",
    "DeAlmeida2013":       "de Almeida (2013)",
    "NitzkeGros2020":      "Nitzke & Gros (2020)",
    "MellingerShreve2016": "Mellinger & Shreve (2016)",
}

# Base fonts at final print size (DejaVu Sans covers Latin Extended-A, so "ć" renders)
FONT_FULL_WIDTH = {
    "font.family": "DejaVu Sans",
    "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "legend.fontsize": 7.5,
}
FONT_COLUMN = {
    "font.family": "DejaVu Sans",
    "font.size": 7, "axes.titlesize": 8, "axes.labelsize": 7,
    "xtick.labelsize": 6.5, "ytick.labelsize": 6.5, "legend.fontsize": 6.5,
}


def _style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK_2)
    ax.tick_params(colors=INK_2)
    ax.grid(axis="x", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def _save(fig, path: Path) -> Path:
    """Write the figure as vector PDF and 300 dpi PNG; return the PDF path."""
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.02, facecolor=SURFACE)
    fig.savefig(path.with_suffix(".png"), dpi=300, bbox_inches="tight", pad_inches=0.02, facecolor=SURFACE)
    plt.close(fig)
    return path.with_suffix(".pdf")


def figure_f5_fluency(exp2: Dict, output_dir: Path) -> Path:
    """Analysis 2: relative NMT error change per category, plus omission visibility."""
    bent = next(f for f in exp2["findings"]
                if f["source"] == "Bentivogli2018" and "per_pair" in f["detail"])
    vb = next(f for f in exp2["findings"]
              if f["source"] == "VanBrussel2018" and "categories" in f["detail"])
    vis = next(f for f in exp2["findings"]
               if f["source"] == "VanBrussel2018" and "content_word_share" in f["detail"])

    # One bold heading row per source, then its categories (change None marks a heading)
    rows = [(DISPLAY_NAME[bent["source"]], None, None)]  # (label, change, skill)
    for pair, d in bent["detail"]["per_pair"].items():
        for c in d["categories"]:
            rows.append((f"{pair[:2].upper()}–{pair[2:].upper()}: {c['category'].lower()}",
                         c["change"], c["skill"]))
    rows.append((DISPLAY_NAME[vb["source"]], None, None))
    for c in vb["detail"]["categories"]:
        rows.append((c["category"].replace("_", " "), c["change"], c["skill"]))

    with plt.rc_context(FONT_FULL_WIDTH):
        fig, (ax1, ax2) = plt.subplots(
            1, 2, figsize=(7.0, 3.2), gridspec_kw={"width_ratios": [2.6, 1]},
            layout="constrained", facecolor=SURFACE)

        # Clip the one extreme value (semantically unrelated, +389%): the bar stops at
        # `clip` with a break mark across it, and its true value is labelled inside the axes.
        clip = 1.2
        ys = range(len(rows))[::-1]
        for y, (label, change, skill) in zip(ys, rows):
            if change is None:
                continue
            shown = max(min(change, clip), -1)
            ax1.barh(y, shown, height=0.62, color=SLOT[SKILL_SLOT[skill]])
            if change > clip:
                for dx in (-0.10, -0.06):
                    ax1.plot([clip + dx - 0.02, clip + dx + 0.02], [y - 0.42, y + 0.42],
                             color=SURFACE, linewidth=1.6, solid_capstyle="butt")
            ax1.text(shown + (0.03 if shown >= 0 else -0.03), y, f"{change:+.0%}", va="center",
                     ha="left" if shown >= 0 else "right", fontsize=7, color=INK_2)
        ax1.set_yticks(list(ys))
        ax1.set_yticklabels([r[0] for r in rows], color=INK)
        for tick, (_, change, _) in zip(ax1.get_yticklabels(), rows):
            if change is None:
                tick.set_fontweight("bold")
        for tick, (_, change, _) in zip(ax1.yaxis.get_major_ticks(), rows):
            if change is None:
                tick.tick1line.set_visible(False)
        ax1.axvline(0, color=INK_2, linewidth=0.8)
        ax1.set_xlim(-1.35, clip + 0.4)
        ax1.set_ylim(-0.6, len(rows) - 0.4)
        ax1.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
        ax1.set_xlabel("Relative error change, NMT vs PBMT (negative = fewer errors)",
                       color=INK_2)
        ax1.set_title("NMT removes form errors more than meaning errors", color=INK, loc="left")
        _style(ax1)

        systems = ["RBMT", "PBMT", "NMT"]
        vals = [vis["detail"][s] for s in systems]
        ax2.bar(systems, vals, width=0.55, color=SLOT[2])
        for x, v in enumerate(vals):
            ax2.text(x, v + 0.02, f"{v:.0%}", ha="center", fontsize=7, color=INK)
        ax2.set_ylim(0, 0.85)
        ax2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
        ax2.set_title("Omissions with no trace\nin the target", color=INK, loc="left")
        ax2.set_xlabel(f"{DISPLAY_NAME[vis['source']]},\nTable 6", color=INK_2)
        _style(ax2)
        ax2.grid(axis="x", visible=False)
        ax2.grid(axis="y", color=GRID, linewidth=0.6)

        handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in SLOT]
        fig.legend(handles, GROUP_LABEL, loc="outside lower center", ncol=3, frameon=False,
                   labelcolor=INK_2)
        return _save(fig, output_dir / "F5_fluency_paradox.png")


def _tau_note(tested) -> str:
    """Figure-level statement of the rank correlations under both 'deleted' mappings."""
    stats = [(f["detail"]["mappings"]["S2"], f["detail"]["mappings"]["S4"]) for f in tested]
    key = lambda s: (round(s[0]["kendall_tau"], 2), round(s[0]["p_value"], 2),
                     round(s[1]["kendall_tau"], 2), round(s[1]["p_value"], 2))
    fmt = lambda m: f"τ = {m['kendall_tau']:+.2f} (p = {m['p_value']:.2f})"
    if len(tested) > 1 and len({key(s) for s in stats}) == 1:
        s2, s4 = stats[0]
        return (f"Identical rank correlation in both studies: the two samples produce the "
                f"same ordering of edit types. {fmt(s2)} treating deletions as S2; "
                f"{fmt(s4)} treating them as S4.")
    return " ".join(f"{DISPLAY_NAME[f['source']]}: {fmt(s2)} treating deletions as S2; "
                    f"{fmt(s4)} as S4." for f, (s2, s4) in zip(tested, stats))


def figure_f7_overediting(exp4: Dict, output_dir: Path) -> Path:
    """Analysis 4: unnecessary-edit rate by edit type, ordered by ToM rank.

    One panel per study, stacked so the two orderings sit one above the other.
    The rank statistics are stated once, below both panels.
    """
    tested = [f for f in exp4["findings"] if "mappings" in f["detail"]]
    with plt.rc_context(FONT_COLUMN):
        # Last row is an empty axes that holds the legend and the statistics note
        fig, axes = plt.subplots(len(tested) + 1, 1, figsize=(3.4, 1.45 * len(tested) + 1.15),
                                 height_ratios=[1] * len(tested) + [0.78],
                                 layout="constrained", facecolor=SURFACE, squeeze=False)
        axes, key_ax = axes[:-1, 0], axes[-1, 0]

        for ax, f in zip(axes, tested):
            primary = f["detail"]["mappings"]["S2"]
            rows = sorted(primary["per_type"], key=lambda r: (r["tom_rank"], -r["unnecessary_rate"]))
            for x, r in enumerate(rows):
                ax.bar(x, r["unnecessary_rate"], width=0.6, color=SLOT[SKILL_SLOT[r["skill"]]],
                       hatch="//" if r["edit_type"].lower().startswith("delet") else None,
                       edgecolor=SURFACE, linewidth=0)
                ax.text(x, r["unnecessary_rate"] + 0.02, f"{r['unnecessary_rate']:.0%}",
                        ha="center", fontsize=6.5, color=INK)
            ax.set_xticks(range(len(rows)))
            ax.set_xticklabels([f"{textwrap.fill(r['edit_type'], 12, break_long_words=False)}"
                                f"\n{r['skill']}" for r in rows], color=INK)
            ax.set_title(DISPLAY_NAME[f["source"]], color=INK, loc="left")
            ax.set_ylim(0, 0.95)
            ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
            _style(ax)
            ax.grid(axis="x", visible=False)
            ax.grid(axis="y", color=GRID, linewidth=0.6)
            ax.set_ylabel("Judged unnecessary", color=INK_2)

        handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in SLOT]
        handles.append(plt.Rectangle((0, 0), 1, 1, facecolor=SLOT[0], hatch="//",
                                     edgecolor=SURFACE, linewidth=0))
        key_ax.axis("off")
        key_ax.legend(handles, GROUP_LABEL + ["Deletions (S2; S4 alternative)"],
                      loc="upper center", ncol=2, frameon=False, labelcolor=INK_2,
                      columnspacing=1.0, handlelength=1.4, borderaxespad=0)
        key_ax.text(0.5, 0.0, textwrap.fill(_tau_note(tested), 68), transform=key_ax.transAxes,
                    ha="center", va="bottom", fontsize=6.5, color=INK, linespacing=1.3)
        return _save(fig, output_dir / "F7_overediting.png")
