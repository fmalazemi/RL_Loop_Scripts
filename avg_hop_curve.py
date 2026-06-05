#!/usr/bin/env python3
"""
Average hop count vs NoC size - LINE graph sized for a two-column
manuscript (IEEE/ACM single-column width ~3.5 in).

Curves:
    Optimal (Manhattan)  [optimal_avgHop.csv]
    D-RLNoC              [RL_double_Stats_avgHop_Fail_Change.csv]
    RHP-RLNoC            [HP_RL_Stats_avgHop_Fail_Change.csv]
    O-RLNoC              [RL_original_avgHop_Fail_Change.csv]

Usage:
    python avg_hop_curve.py [output_dir]
"""
import sys
from pathlib import Path

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

UP = Path(".")
OUTDIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
OUTDIR.mkdir(parents=True, exist_ok=True)

# label -> (csv, color, linestyle, marker, open_marker?)
CURVES = [
  ("Manhatten (Optimal)", UP / "optimal_avgHop.csv",                    "#f0a500", "-", "D", False),
  ("O-RLNoC",            UP / "RL_Stats.csv",     "#d7301f", "-",  "s", False),
  # Additional curves
  ("Onion+",            UP / "OINIONPlus_Stats.csv",                    "#1a9850", "-",  "v", False),
  ("D-RLNoC",            UP / "RL_double_Stats.csv", "#2c7fb8", "-",  "o", False),
  ("RHP-RLNoC",          UP / "HP_RL_Stats.csv",     "#444444", "-",  "^", False),
]

# ---- manuscript-scale rcParams (single column ~3.5") ---- 
mpl.rcParams.update({
    "font.family": "Liberation Sans",
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "font.size": 8,
    "axes.labelsize": 8,
    "axes.titlesize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.7,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "lines.linewidth": 1.3,
    "lines.markersize": 3.2,
})


def load(csv):
    df = pd.read_csv(csv)
    df.columns = [c.strip() for c in df.columns]
    return df


fig, ax = plt.subplots(figsize=(3.5, 2.7))   # IEEE single-column width

xticks = None
for label, csv, color, ls, mk, openm in CURVES:
    d = load(csv)
    xticks = d["NoCSize"].values
    ax.plot(d["NoCSize"], d["HopCount"], color=color, ls=ls,
            marker=mk, mec=color, mew=0.8,
            mfc=("white" if openm else color),
            label=label, zorder=3)

ax.set_xlabel("RLNoC size")
ax.set_ylabel("Average hop count")
ax.set_xticks(xticks[::2])      # every other size to avoid crowding
ax.set_ylim(bottom=0)
ax.grid(axis="both", color="0.9", lw=0.5, zorder=0)
ax.set_axisbelow(True)
ax.margins(x=0.02)

ax.legend(frameon=True, ncol=1, loc="upper left",
          handlelength=2.0, borderaxespad=0.5, labelspacing=0.3,
          fancybox=False, edgecolor="0.4", framealpha=1.0,
          borderpad=0.5).get_frame().set_linewidth(0.7)

fig.tight_layout(pad=0.4)
for ext in ("png", "pdf"):
    fig.savefig(OUTDIR / f"avg_hop_curve.{ext}", dpi=600, bbox_inches="tight")
print("wrote avg_hop_curve.png / .pdf to", OUTDIR)