#!/usr/bin/env python3

import pandas as pd
from pathlib import Path




def main(traffic, N, BASELINE):
    CSV_FILE = Path(f"{traffic}_{N}_figure_data.csv")
    X_COL = "Injection_rate"
    
    
    df = pd.read_csv(CSV_FILE)
    df.columns = [c.strip() for c in df.columns]

    if BASELINE not in df.columns:
        raise ValueError(f"Baseline column '{BASELINE}' not found.")

    if X_COL not in df.columns:
        raise ValueError(f"Column '{X_COL}' not found.")

    # Sort by injection rate, then take the lowest injection rate
    df = df.sort_values(X_COL)
    zero_load = df.iloc[0]

    baseline_value = zero_load[BASELINE]
    injection_rate = zero_load[X_COL]

    #print(f"Zero-load injection rate: {injection_rate}")
    print("="*20)
    #print("NoC Size = {N}x{N}")
    print(f"Traffic Pattern: {traffic}")
    print(f"Baseline: {BASELINE} = {baseline_value:.5f}")
    for scheme in df.columns:
        if scheme in [X_COL]:
            continue
        scheme_value = zero_load[scheme]

        improvement = ((baseline_value - scheme_value) / baseline_value) * 100

        print(f"{scheme}: {scheme_value:.5f} ({improvement:+.2f}% vs {BASELINE})")
        






if __name__ == "__main__":
    T = ["Shuffle", "Uniform", "Bitrev", "Bitcomp"]
    N = 16
    BASELINE = "O-RLNoC"
    #print("NoC 4x4")
    for t in T:
        main(t, N, BASELINE)