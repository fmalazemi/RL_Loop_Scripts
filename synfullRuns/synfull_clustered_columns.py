#!/usr/bin/env python3
"""
Generate two clustered (grouped) column figures from the NoC benchmark sheet:
  1. raw metric values
  2. values normalized relative to O-RLNoC (O-RLNoC == 1.0 baseline)

Usage:
    python clustered_columns.py [path_to_xlsx] [output_dir]
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# ---------------------------------------------------------------- config
N = 4
FILE_NAME = f"synfull{N}.xlsx"
ADD_LEGENDS = False # If you have multiple figures, keep legends for the last figure. 
XLSX = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(FILE_NAME)
OUTDIR = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")
OUTDIR.mkdir(parents=True, exist_ok=True)

SCHEMES = ["D-RLNoC", "RHP-RLNoC", "Onion+", "O-RLNoC"]
BASELINE = "O-RLNoC"                 # normalization reference
COLORS = {"D-RLNoC": "#2c7fb8",     # blue
          "RHP-RLNoC": "#f0a500",   # amber
          "O-RLNoC": "#d7301f",
  "Onion+": "black"}     # red
METRIC = "Metric"                   # <-- rename to your real metric + unit
BAR_W = 0.16                        # width of each bar
GAP_BEFORE_AVG = 1.6                # extra space before the Average group
ANNOTATE = False                    # set True for per-bar value labels
Y_NBINS = 5                          # max number of y-axis tick intervals

mpl.rcParams.update({
    "font.family": "Liberation Sans",   # Arial-metric substitute
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "axes.spines.top": False, "axes.spines.right": False,
})

# ---------------------------------------------------------------- data
df = pd.read_excel(XLSX)
df.columns = [c.strip() for c in df.columns]
df["workload"] = df["workload"].str.strip()
df = df.set_index("workload")[SCHEMES]

labels = list(df.index)             # 16 benchmarks + 'Average' at the end
# x positions with a gap before the trailing Average group
x = np.arange(len(labels), dtype=float)
if labels[-1].lower() == "average":
    x[-1] += GAP_BEFORE_AVG

norm = df.div(df[BASELINE], axis=0)  # normalized relative to O-RLNoC


# ---------------------------------------------------------------- plotting
def grouped_bar(data, ylabel, title, fname, baseline_line=None):
    if ADD_LEGENDS:
      fig, ax = plt.subplots(figsize=(13, 3.7))
    else:
      fig, ax = plt.subplots(figsize=(13, 2.3))
    offsets = (np.arange(len(SCHEMES)) - (len(SCHEMES) - 1) / 2) * BAR_W
    for off, scheme in zip(offsets, SCHEMES):
        bars = ax.bar(x + off, data[scheme].values, BAR_W,
                      label=scheme, color=COLORS[scheme],
                      edgecolor="white", linewidth=0.4, zorder=3)
        if ANNOTATE:
            ax.bar_label(bars, fmt="%.2f", padding=2, fontsize=6, rotation=90)

    if baseline_line is not None:
        pass #ax.axhline(baseline_line, color="black", lw=1.0, ls="--", zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=9)
    # emphasize the Average tick
    if labels[-1].lower() == "average":
        ax.get_xticklabels()[-1].set_fontweight("bold")
        ax.get_xticklabels()[-1].set_fontstyle("italic")
    ax.set_yticks([0, 0.5, 1.0])
    ax.set_ylabel(ylabel, fontsize=8)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=0)
    ax.margins(x=0.01)
    ax.grid(axis="y", color="0.85", lw=0.7, zorder=0)
    ax.set_axisbelow(True)
    #ax.yaxis.set_major_locator(MaxNLocator(nbins=Y_NBINS))   # fewer y ticks
    ax.set_yticks([0, 0.5, 1.0])
  
    if ADD_LEGENDS:
      ax.legend(frameon=False, ncol=len(SCHEMES), fontsize=16, loc="upper center", bbox_to_anchor=(0.5, -0.62))
    #ax.legend(frameon=False, ncol=1, fontsize=10,
    #              loc="upper center", bbox_to_anchor=(1.01, 0.5))
  
    fig.tight_layout()
    for ext in ["pdf"]: #("png", "pdf"):
        fig.savefig(OUTDIR / f"{fname}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


# Figure 1: raw values
grouped_bar(
    df,
    ylabel= METRIC,
    title= "NoC schemes per benchmark (raw values)",
    fname= f"synfull{N}_normalized_raw",
)

# Figure 2: normalized to O-RLNoC
# headroom so the 1.0 baseline bars + lower bars are readable
grouped_bar(
    norm,
    ylabel= f"Normalized to {BASELINE}",
    title= f"{N}x{N}",
    fname= f"synfull{N}_normalized",
    baseline_line=1.0,
)

print("wrote:",
      *(str(OUTDIR / f"{FILE_NAME}_{k}.{e}")
        for k in ("raw", "normalized") for e in ["pdf"]), sep="\n  ")