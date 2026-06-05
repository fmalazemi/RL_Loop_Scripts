#!/usr/bin/env python3
"""
Add headers + Injection_rate column to one or more data files.

IDE-friendly usage:
1. Put this script in the same folder as your header file and data files.
2. Edit the USER SETTINGS section below.
3. Press Run in your IDE.

No command-line arguments are needed.

The script creates one output CSV per data file:
  originalFileName_with_headers.csv

It adds:
  - Injection_rate as the first column
  - Injection_rate at line i = (i + 1) * 0.005
"""

import csv
from pathlib import Path

FOLDER_NAMES = [
  "RL_original_Runs",
  "RL_HP_runs",
  "RL_HP_runs_improved",
  "RL_double_runs",
  "RL_ONION_runs",
  "RL_original_Runs"
]


# ============================================================
# USER SETTINGS
# Edit only this section
# ============================================================

# Put your header file name here
HEADER_FILE = "bookSim_output_headers.csv"

# Put your data file names here
DATA_FILES = [
    "rlBetaUniformOutput",
    "rlBeta4HotspotOutput",
    "rlBetaAsymmetricOutput",
    "rlBetaBitCompOutput",
    "rlBetaBitrevOutput",
    "rlBetaShuffleOutput",
    "rlBetaTransposeOutput",
    "rlBeta6HotspotOutput",
    "rlBeta8HotspotOutput",
    "rlBeta10HotspotOutput",
    "rlBeta12HotspotOutput",
    "rlBeta14HotspotOutput",
    "rlBetaZ16HotspotOutput",
    "rlBetaTornadoOutput"
]



# Injection rate formula:
# line i => (i + 1) * INJECTION_STEP
INJECTION_STEP = 0.005

# Output suffix
OUTPUT_SUFFIX = "_with_headers.csv"

# If True, the script stops when a row has the wrong number of columns.
# If False, it skips bad rows and continues.
STRICT_MODE = True


# ============================================================
# Program code
# Usually, you do not need to edit below this line
# ============================================================

def read_headers(header_file):
    """
    Read headers from a CSV header file.

    Empty cells are ignored. This handles trailing commas and cases
    where the final header appears on a second line.
    """
    headers = []

    with header_file.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)

        for row in reader:
            for cell in row:
                name = cell.strip()
                if name:
                    headers.append(name)

    return headers


def read_data_rows(data_file):
    """
    Read a tab-separated data file.

    Empty lines are ignored.
    Empty trailing columns caused by a final tab are removed.
    """
    rows = []

    with data_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            values = line.split("\t")

            while values and values[-1] == "":
                values.pop()

            rows.append(values)

    return rows


def make_output_file(data_file):
    """
    Example:
      rlBetaUniformOutput -> rlBetaUniformOutput_with_headers.csv
      data.txt            -> data_with_headers.csv
    """
    return data_file.with_name(data_file.stem + OUTPUT_SUFFIX)


def process_one_file(header_file, data_file):
    headers = read_headers(header_file)
    data_rows = read_data_rows(data_file)

    if not headers:
        raise ValueError("The header file does not contain any headers.")

    if not data_rows:
        raise ValueError("The data file is empty.")

    expected_columns = len(headers)
    valid_rows = []

    for line_index, row in enumerate(data_rows):
        if len(row) != expected_columns:
            message = (
                f"Column mismatch in file '{data_file}' at data line {line_index}. "
                f"Expected {expected_columns} columns, but found {len(row)} columns."
            )

            if STRICT_MODE:
                raise ValueError(message)
            else:
                print("WARNING:", message)
                print("Skipping this line.")
                continue

        valid_rows.append(row)

    if not valid_rows:
        raise ValueError(f"No valid rows found in file '{data_file}'.")

    output_file = make_output_file(data_file)

    with output_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["Injection_rate"] + headers)

        for i, row in enumerate(valid_rows):
            injection_rate = (i + 1) * INJECTION_STEP
            writer.writerow([f"{injection_rate:.3f}"] + row)

    return output_file, len(valid_rows), len(headers) + 1


def main():
    print("=" * 70)
    print("Add Headers + Injection_rate Column")
    print("=" * 70)
    print()

    header_file = Path(HEADER_FILE)

    if not header_file.exists():
        print(f"ERROR: Header file not found: {header_file}")
        print("Check HEADER_FILE in the USER SETTINGS section.")
        return

    if not DATA_FILES:
        print("ERROR: DATA_FILES list is empty.")
        print("Add one or more data filenames in the USER SETTINGS section.")
        return

    print(f"Header file: {header_file}")
    print(f"Number of data files: {len(DATA_FILES)}")
    print()

    success_count = 0
    for folder in FOLDER_NAMES:
      for i in [4,6,8,10,12,14,16]:
        for file_name in DATA_FILES:
            data_file = Path(f"{folder}/runs{i}/{file_name}")
    
            print("-" * 70)
            print(f"Processing: {data_file}")
    
            if not data_file.exists():
                print(f"ERROR: Data file not found: {data_file}")
                print("Skipping this file.")
                continue
    
            try:
                output_file, rows_written, columns_written = process_one_file(
                    header_file=header_file,
                    data_file=data_file
                )
    
                print("Done.")
                print(f"Output file    : {output_file}")
                print(f"Rows written   : {rows_written}")
                print(f"Columns written: {columns_written}")
                success_count += 1
    
            except Exception as e:
                print("ERROR:")
                print(e)

    print()
    print("=" * 70)
    print(f"Finished. Successfully processed {success_count} file(s).")
    print("=" * 70)


if __name__ == "__main__":
    main()
  