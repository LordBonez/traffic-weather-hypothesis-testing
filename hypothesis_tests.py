"""Rain/dry hypothesis testing from a team project (April 2026).

This repository focuses on Section 2, hypothesis testing.
Original team project: https://github.com/Gurdeep2005/CS301_project
October 2026 packaging adds a CLI, validation and repeatable tests.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

def analyze(frame, alpha=0.05):
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    columns = ["total_vol", "precipitation (mm)"]
    missing = set(columns) - set(frame.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    values = frame[columns].apply(pd.to_numeric, errors="coerce")
    if not np.isfinite(values.to_numpy()).all() or (values < 0).any().any():
        raise ValueError("Traffic and precipitation values must be finite, nonnegative numbers")
    log_volume = np.log1p(values["total_vol"])
    rainy = values["precipitation (mm)"] > 0
    rain, dry = log_volume[rainy], log_volume[~rainy]
    if len(rain) < 2 or len(dry) < 2:
        raise ValueError("Each rain/dry group needs at least two observations")
    t = stats.ttest_ind(rain, dry, equal_var=False)
    f = stats.f_oneway(rain, dry)
    if not all(np.isfinite(x) for x in (t.statistic, t.pvalue, f.statistic, f.pvalue)):
        raise ValueError("The data do not support finite test statistics (check within-group variation)")
    return {
        "rows": int(len(values)), "rainy_hours": int(len(rain)), "dry_hours": int(len(dry)),
        "response": "log1p(total_vol)", "alpha": float(alpha),
        "welch_t_test": {"statistic": float(t.statistic), "p_value": float(t.pvalue),
                         "reject_equal_means": bool(t.pvalue < alpha)},
        "one_way_anova": {"statistic": float(f.statistic), "p_value": float(f.pvalue),
                          "reject_equal_means": bool(f.pvalue < alpha)},
    }

def main():
    parser = argparse.ArgumentParser(description="Compare log traffic volume between rainy and dry hours.")
    parser.add_argument("--csv", type=Path, required=True, help="Path to merged_traffic_weather.csv")
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--output", type=Path, help="Optional JSON result path")
    args = parser.parse_args()
    try:
        result = analyze(pd.read_csv(args.csv), args.alpha)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Error: {exc}\n")
    text = json.dumps(result, indent=2, allow_nan=False)
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
