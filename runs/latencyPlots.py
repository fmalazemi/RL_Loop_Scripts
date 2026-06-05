#!/usr/bin/env python3
"""
Create an academic-style curve figure from N CSV files.

Each file should contain at least these columns:
  - Injection_rate
  - _avg_plat

The figure will contain N curves:
  X-axis: Injection rate
  Y-axis: Packet average latency

IDE-friendly usage:
1. Put this script anywhere you like.
2. Edit the USER SETTINGS section.
3. Manually write the full paths or relative paths of your CSV files.
4. Press Run in your IDE.

The script saves:
  - packet_latency_vs_injection_rate.png
  - packet_latency_vs_injection_rate.pdf
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# USER SETTINGS
# Edit this section only
# ============================================================

# Add your files here.
# You can use relative paths:
#   "rlBetaUniformOutput_with_headers.csv"
#
# Or full paths:
#   "/Users/fawaz/Desktop/hpRLNoC/RL_original_Runs/originalRLRuns_4x4/rlBetaUniformOutput_with_headers.csv"
#
# label: the name shown in the figure legend.
traffic = "Uniform"
NOC_SIZE = 16
MAIN_FOLDER = "./"
TRAFFIC_PATTERN = f"rlBeta{traffic}Output_with_headers.csv"
OUTPUT_FILE = f"{traffic}_{NOC_SIZE}.pdf"
TITLE = f"{traffic} {NOC_SIZE}x{NOC_SIZE}"
SUB_FOLDERS = ["RL_original_Runs", "RL_double_runs", "RL_HP_runs_improved", "RL_ONIONPLUS_runs"]
LABEL = ["O-RLNoC", "D-RLNoC", "RHP-RLNoC", "Onion+"]

DATA_FILES = []
for i in range(len(SUB_FOLDERS)):
  file = { "path": f"{SUB_FOLDERS[i]}/runs{NOC_SIZE}/{TRAFFIC_PATTERN}",
            "label": LABEL[i]
  }
  DATA_FILES.append(file)
  

  '''
DATA_FILES = [
    {
        "path": f"{MAIN_FOLDER}RL_original_Runs/runs4/rlBetaUniformOutput_with_headers.csv",
        "label": "O-RLNoC"
    },{
      "path": "/Users/fawaz/Desktop/hpRLNoC/RL_double_runs/runs4/rlBetaUniformOutput_with_headers.csv",
      "label": "D-RLNoC"
    },{
        "path": "/Users/fawaz/Desktop/hpRLNoC/RL_HP_runs/runs4/rlBetaUniformOutput_with_headers.csv",
        "label": "RHP-RLNoC"
    },

    # Add more files like this:
    # {
    #     "path": "another_file_with_headers.csv",
    #     "label": "Proposed Design"
    # },
    # {
    #     "path": "third_file_with_headers.csv",
    #     "label": "Baseline"
    # },
]'''

# Column names in your CSV files
X_COLUMN = "Injection_rate"
Y_COLUMN = "_avg_plat"

# Output figure names
OUTPUT_PNG = "packet_latency_vs_injection_rate.png"
OUTPUT_PDF = OUTPUT_FILE

# Figure text
FIGURE_TITLE = ""  # For papers, usually keep title empty and use the caption instead.
X_LABEL = "Injection Rate (packet/node/cycle)"
Y_LABEL = "Average Packet Latency (cycle)"

# Academic publishing style settings
FIGURE_WIDTH = 7.0
FIGURE_HEIGHT = 4.8
DPI = 600

FONT_SIZE = 70
LABEL_SIZE = 13
TICK_SIZE = 11
LEGEND_SIZE = 10

LINE_WIDTH = 2.0
MARKER_SIZE = 5

SHOW_GRID = True
USE_LOG_Y_AXIS = False

X_LIMITS = None
# Example:
# X_LIMITS = (0.0, 0.18)

Y_LIMITS = (0,200)
# Example:
# Y_LIMITS = (0, 200)

LEGEND_LOCATION = "upper left"


# ============================================================
# Program code
# Usually, you do not need to edit below this line
# ============================================================

def load_curve(file_info):
    file_path = Path(file_info["path"])
    label = file_info.get("label", file_path.stem)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)

    if X_COLUMN not in df.columns:
        raise ValueError(f"Column '{X_COLUMN}' was not found in {file_path}")

    if Y_COLUMN not in df.columns:
        raise ValueError(f"Column '{Y_COLUMN}' was not found in {file_path}")

    df[X_COLUMN] = pd.to_numeric(df[X_COLUMN], errors="coerce")
    df[Y_COLUMN] = pd.to_numeric(df[Y_COLUMN], errors="coerce")

    df = df.dropna(subset=[X_COLUMN, Y_COLUMN])

    if df.empty:
        raise ValueError(f"No valid numeric data found in {file_path}")

    df = df.sort_values(by=X_COLUMN)

    return df[X_COLUMN], df[Y_COLUMN], label


def apply_academic_style():
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "font.size": FONT_SIZE,
        "axes.labelsize": LABEL_SIZE,
        "xtick.labelsize": TICK_SIZE,
        "ytick.labelsize": TICK_SIZE,
        "legend.fontsize": LEGEND_SIZE,
        "axes.linewidth": 1.0,
        "lines.linewidth": LINE_WIDTH,
        "savefig.dpi": DPI,
        "savefig.bbox": "tight",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def create_figure():
    if not DATA_FILES:
        print("ERROR: DATA_FILES is empty.")
        print("Please add at least one file in the USER SETTINGS section.")
        return

    apply_academic_style()

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))

    markers = ["o", "s", "^", "D", "v", "P", "X", "*", "<", ">", "h", "p"]
    linestyles = ["-", "--", "-.", ":"]

    plotted = 0

    for i, file_info in enumerate(DATA_FILES):
        try:
            x, y, label = load_curve(file_info)

            marker = markers[i % len(markers)]
            linestyle = linestyles[(i // len(markers)) % len(linestyles)]

            ax.plot(
                x,
                y,
                label=label,
                marker=marker,
                linestyle=linestyle,
                linewidth=LINE_WIDTH,
                markersize=MARKER_SIZE,
                markerfacecolor="white",
                markeredgewidth=1.2,
            )

            print(f"Plotted: {file_info['path']} as '{label}'")
            plotted += 1

        except Exception as e:
            print(f"ERROR with file {file_info.get('path', 'UNKNOWN')}: {e}")

    if plotted == 0:
        print("No curves were plotted.")
        return

    ax.set_xlabel(X_LABEL)
    ax.set_ylabel(Y_LABEL)
    plt.title(TITLE, fontsize=13)
    if FIGURE_TITLE:
        ax.set_title(FIGURE_TITLE)

    if USE_LOG_Y_AXIS:
        ax.set_yscale("log")

    if X_LIMITS is not None:
        ax.set_xlim(X_LIMITS)

    if Y_LIMITS is not None:
        ax.set_ylim(Y_LIMITS)

    if SHOW_GRID:
        ax.grid(True, which="major", linestyle="--", linewidth=0.6, alpha=0.6)
        ax.grid(True, which="minor", linestyle=":", linewidth=0.4, alpha=0.4)
        ax.minorticks_on()

    ax.legend(
        loc=LEGEND_LOCATION,
        frameon=True,
        fancybox=False,
        edgecolor="black",
        framealpha=1.0,
    )

    fig.tight_layout()

    fig.savefig(OUTPUT_PNG, dpi=DPI)
    fig.savefig(OUTPUT_PDF)

    print()
    print("Figure created successfully.")
    #print(f"PNG saved as: {OUTPUT_PNG}")
    print(f"PDF saved as: {OUTPUT_PDF}")

    #plt.show()


if __name__ == "__main__":
    create_figure()
  