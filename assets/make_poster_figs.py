"""Plots for a poster, drawn at the size at which they are printed.

Copy this file to <poster>/figures/make_poster_figs.py and replace the three demo functions by
the paper's plots. Read the same result files as the paper's plotting code: same data and same
normalisation as the paper, and only sizes, fonts, labels and legends change. A paper figure
scaled up to poster size keeps its 8pt labels in proportion and its thin lines; redrawing it at
print size is what makes it readable from two metres.

    python3 figures/make_poster_figs.py        # writes fig_*_poster.pdf and a small PNG preview

Rules that the demos follow (the reasons are in references/figures.md of the skill):
  - figsize is the printed size in cm; the poster includes the PDF without rescaling it much;
  - tick labels 22pt, axis labels 26pt, titles of small multiples 28pt, legends 22pt;
  - words in labels and legends are the poster's own terms, never a synonym from the code;
  - one curve needs no legend: the axis label names it, and a reference line carries its label;
  - several curves keep a legend, and marker shapes and dashes differ, so that colour is never
    the only way to tell them apart;
  - plots that sit in one row get the same height, which lets their x-axes align on the poster;
  - everything stays vector (rasterise only a scatter with a huge number of points).
"""
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
CM = 1 / 2.54
SCALE = 1.0                       # same value as \posterfontscale in poster.tex
TICK, LABEL, TITLE, LEG = (round(s * SCALE) for s in (22, 26, 28, 22))
ROW_H = 18                        # height in cm of the plots that share the bottom row

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "Nimbus Sans", "DejaVu Sans"],
    "mathtext.fontset": "custom",
    "mathtext.rm": "sans", "mathtext.it": "sans:italic", "mathtext.bf": "sans:bold",
    "axes.linewidth": 1.4,
    "xtick.major.width": 1.4, "ytick.major.width": 1.4,
    "xtick.major.size": 7, "ytick.major.size": 7,
    "xtick.minor.size": 4, "ytick.minor.size": 4,
})


def save(fig, name):
    """Vector PDF for the poster and a small PNG to look at."""
    fig.savefig(os.path.join(HERE, name + ".pdf"), bbox_inches="tight", pad_inches=0.05)
    fig.savefig(os.path.join(HERE, name + ".png"), bbox_inches="tight", pad_inches=0.05, dpi=60)
    plt.close(fig)
    print("saved", name)


def demo_main():
    """Small multiples with one shared legend above them (for example one panel per dataset)."""
    rng = np.random.RandomState(0)
    names = ["Dataset A", "Dataset B", "Dataset C", "Dataset D"]
    baselines = {"Baseline 1": dict(marker="s", color="C1"), "Baseline 2": dict(marker="^", color="C2"),
                 "Baseline 3": dict(marker="D", color="C3")}
    fig, axes = plt.subplots(1, 4, figsize=(60 * CM, ROW_H * CM))
    for ax, name in zip(axes, names):
        x = np.linspace(0.6, 1.0, 9)
        y = 0.03 * (x - 0.6) ** 2 / 0.16 * rng.uniform(0.6, 1.4)
        ax.plot(x, y, "o-", color="C0", lw=4, ms=9, zorder=10)
        for k, st in enumerate(baselines.values()):
            xb = rng.uniform(0.75, 0.98)
            ax.scatter(xb, np.interp(xb, x, y) * rng.uniform(1.4, 2.4) + 0.004 * k, marker=st["marker"],
                       color=st["color"], s=260, zorder=15, edgecolors="black", linewidths=1.3)
        # 1e-2 printed as x10^-2, in the same font as the tick labels
        ax.ticklabel_format(style="sci", axis="y", scilimits=(0, 0), useMathText=True)
        ax.yaxis.get_offset_text().set_fontsize(TICK - 2)
        ax.set_title(name, fontsize=TITLE, fontweight="bold", pad=34)
        ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=4))
        ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=4))
        ax.tick_params(labelsize=TICK)
        ax.grid(True, alpha=0.3, lw=1)
        ax.set_xlabel("quantity on the x-axis", fontsize=LABEL)
    axes[0].set_ylabel("quantity on the y-axis\n(its unit or variant)", fontsize=LABEL)
    handles = [Line2D([0], [0], color="C0", marker="o", lw=4, ms=11, label="Our method")]
    for label, st in baselines.items():
        handles.append(Line2D([0], [0], color=st["color"], marker=st["marker"], lw=0, ms=15,
                              markeredgecolor="black", markeredgewidth=1.3, label=label))
    fig.legend(handles=handles, loc="upper center", ncol=len(handles), fontsize=LEG + 2, frameon=False,
               bbox_to_anchor=(0.5, 1.02), columnspacing=2.0, handlelength=2.0)
    fig.tight_layout(rect=(0, 0, 1, 0.86), w_pad=2.0)
    save(fig, "fig_main_poster")


def demo_second():
    """One curve and a reference line: no legend, the line carries its own label."""
    ts = np.arange(2, 22)
    ns = 2 ** ts
    limit = (1 + np.sqrt(2)) / 2
    ratio = limit + 0.46 * 0.62 ** (ts - 2)
    fig, ax = plt.subplots(figsize=(30 * CM, ROW_H * CM))
    ax.plot(ns, ratio, "o-", color="C0", lw=4, ms=11, zorder=3)
    ax.axhline(limit, color="red", ls="--", lw=3, zorder=2)
    ax.text(ns[-1], limit + 0.025, r"limit $\approx 1.207$", fontsize=LEG + 2, ha="right", va="bottom", color="black")
    ax.set_xscale("log", base=2)
    shown = [t for t in ts if t % 3 == 2]
    ax.set_xticks([2 ** t for t in shown])
    ax.set_xticklabels([f"$2^{{{t}}}$" for t in shown])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_ylim(1.0, 1.75)
    ax.set_xlabel(r"number of items $n$", fontsize=LABEL)
    ax.set_ylabel("ratio to the lower bound", fontsize=LABEL)
    ax.tick_params(labelsize=TICK)
    ax.grid(True, alpha=0.3, lw=1)
    fig.tight_layout()
    save(fig, "fig_second_poster")


def demo_runtime():
    """Log-log runtime with four curves: legend in the empty corner, headroom so it clears the data."""
    ns = np.array([1e2, 3e2, 1e3, 3e3, 1e4, 3e4, 1e5, 3e5])
    fig, ax = plt.subplots(figsize=(38 * CM, ROW_H * CM))
    kw = dict(lw=4, ms=11)
    ax.plot(ns[:5], 4e-8 * ns[:5] ** 2.4, "s--", color="C1", label="variant one, naive scan", **kw)
    ax.plot(ns, 6e-9 * ns ** 2, "o-", color="C3", label="variant one (heap)", **kw)
    ax.plot(ns, 2e-9 * ns ** 2, "v-", color="C2", label="variant two (linked list)", **kw)
    big = np.append(ns, [1e6, 3e6])
    ax.errorbar(big, 4e-7 * big ** 1.25, yerr=1.5e-7 * big ** 1.25, fmt="D-", color="C4", capsize=6, capthick=2,
                label="variant one, easy input (heap)", **kw)
    ax.set_xscale("log")
    ax.set_yscale("log")
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi * 60)                       # headroom for the legend
    ax.yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=100))
    ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_xlabel(r"number of items $n$", fontsize=LABEL)
    ax.set_ylabel("wall-clock time (s)", fontsize=LABEL)
    ax.tick_params(labelsize=TICK)
    ax.grid(True, which="major", alpha=0.3, lw=1)
    ax.legend(fontsize=LEG, loc="upper left", frameon=False, handlelength=2.2)
    fig.tight_layout()
    save(fig, "fig_runtime_poster")


if __name__ == "__main__":
    demo_main()
    demo_second()
    demo_runtime()
