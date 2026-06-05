#!/usr/bin/env python3
"""
Option 1 - Link-failure hop-count penalty vs NoC size.

For each scheme we plot the *extra* hops caused by a single link failure:
    avg penalty  = failAvgHop   - avgHop
    max penalty  = MaxHopChange - avgHop      (MaxHopChange assumed = max hop
                                               count after failure)
A shaded band spans avg->max penalty for each scheme.

Usage:
    python hop_penalty.py [rl_double.csv] [hp_rl.csv] [output_dir]
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# ------------------------------------------------------------------ config
RL_CSV = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "RL_double_Stats_avgHop_Fail_Change.csv")
HP_CSV = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(
    "RL_HP_Stats_avgHop_Fail_Change.csv")

X_CSV = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(
    "RL_original_avgHop.csv"
)

OUTDIR = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(".")
OUTDIR.mkdir(parents=True, exist_ok=True)

# scheme -> (csv, display label, color)
SCHEMES = {
    "RL_double": (RL_CSV, "RL-double", "#2c7fb8"),   # blue
    "HP_RL":     (HP_CSV, "HP-RL",     "#d7301f"),   # red
}

mpl.rcParams.update({
    "font.family": "Liberation Sans",
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "axes.spines.top": False, "axes.spines.right": False,
})


def load(csv):
    df = pd.read_csv(csv)
    df.columns = [c.strip() for c in df.columns]
    df["avg_pen"] = df["failAvgHop"] - df["avgHop"]
    df["max_pen"] = df["MaxHopChange"] - df["avgHop"]
    return df


def load_x_curve(csv):
    df = pd.read_csv(csv)
    df.columns = [c.strip() for c in df.columns]
    if "NoCSize" not in df.columns:
        raise ValueError(f"'NoCSize' column not found in {csv}")
    if "avgHop" not in df.columns:
        raise ValueError(f"'avgHop' column not found in {csv}")
    df["NoCSize"] = pd.to_numeric(df["NoCSize"], errors="coerce")
    df["avgHop"] = pd.to_numeric(df["avgHop"], errors="coerce")
    df = df.dropna(subset=["NoCSize", "avgHop"])
    df = df.sort_values("NoCSize")
    
    return df



fig, ax = plt.subplots(figsize=(8.5, 5.2))

for label_key, (csv, label, color) in SCHEMES.items():
    d = load(csv)
    x = d["NoCSize"].values
    # shaded band: avg penalty -> max penalty
    ax.fill_between(x, d["avg_pen"], d["max_pen"],
                    color=color, alpha=0.15, zorder=1, linewidth=0)
    # average penalty (solid) and worst-case penalty (dashed)
    ax.plot(x, d["avg_pen"], color=color, lw=2.0, marker="o", ms=5,
            zorder=3, label=f"{label} - avg penalty")
    ax.plot(x, d["max_pen"], color=color, lw=2.0, ls="--", marker="s",
            ms=5, mfc="white", mec=color, zorder=3,
            label=f"{label} - max penalty")






ax.set_xlabel("RLNoC size", fontsize=12)
ax.set_ylabel("Extra hops after link failure  (\u0394 hops)", fontsize=12)
#ax.set_title("Link-failure hop-count penalty vs network size", fontsize=13, fontweight="bold", pad=10)
ax.set_xticks(load(RL_CSV)["NoCSize"].values)
ax.grid(axis="both", color="0.88", lw=0.7, zorder=0)
ax.set_axisbelow(True)
ax.margins(x=0.02)
ax.set_ylim(bottom=0)

ax.legend(frameon=False, ncol=2, fontsize=9.5,
          loc="upper center", bbox_to_anchor=(0.5, -0.13))

fig.tight_layout()
for ext in ("png", "pdf"):
    fig.savefig(OUTDIR / f"hop_penalty.{ext}", dpi=300, bbox_inches="tight")
print("wrote hop_penalty.png / .pdf to", OUTDIR)
