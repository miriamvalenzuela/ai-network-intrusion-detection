"""Verify that model results can be compared safely in the dashboard."""
from pathlib import Path
import argparse
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
COLUMNS = ["row_id", "y_true", "y_pred"]


def validate_file(path):
    df = pd.read_csv(path)
    if df.columns.tolist() != COLUMNS:
        raise ValueError(f"{path.name}: expected columns exactly {COLUMNS}, got {df.columns.tolist()}")
    if not df["row_id"].equals(pd.Series(range(len(df)), name="row_id")):
        raise ValueError(f"{path.name}: row_id must be 0..N-1 in original test order")
    for col in ("y_true", "y_pred"):
        if df[col].isna().any() or not df[col].isin([0, 1]).all():
            raise ValueError(f"{path.name}: {col} must contain only 0 and 1")
    return df


def main():
    parser = argparse.ArgumentParser(description="Validate all available prediction CSV files")
    parser.add_argument("--results-dir", default="results")
    args = parser.parse_args()
    folder = Path(args.results_dir)
    if not folder.is_absolute():
        folder = ROOT / folder
    baseline = None
    seen = 0
    for i in range(1, 5):
        path = folder / f"p{i}.csv"
        if not path.exists():
            print(f"p{i}.csv: not yet submitted")
            continue
        frame = validate_file(path)
        if baseline is not None:
            if not frame[["row_id", "y_true"]].equals(baseline[["row_id", "y_true"]]):
                raise ValueError(f"p{i}.csv has different row order or true labels")
        else:
            baseline = frame
        print(f"p{i}.csv: OK, {len(frame):,} rows")
        seen += 1
    if not seen:
        print("No results yet. This is normal during Week 1.")
    else:
        print(f"Validated {seen} prediction file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
