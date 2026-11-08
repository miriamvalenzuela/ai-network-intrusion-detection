"""Person 1: data exploration and two simple training-data figures."""
from pathlib import Path
import sys
import argparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from project_utils.core import load_data


def main():
    parser = argparse.ArgumentParser(description="Person 1: inspect data and save charts")
    parser.add_argument("--data-dir", default="data/raw")
    args = parser.parse_args()
    _, _, _, _, train, test = load_data(args.data_dir)
    demo = Path(args.data_dir).name == "sample"
    out = (ROOT / "scratch" / "sample_analysis") if demo else (ROOT / "person1_baseline" / "figures")
    out.mkdir(parents=True, exist_ok=True)
    counts = train["label"].value_counts().reindex([0, 1], fill_value=0)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.bar(["Normal (0)", "Attack (1)"], counts.to_numpy())
    ax.set_title("Training-data label counts")
    ax.set_ylabel("Rows")
    fig.tight_layout()
    fig.savefig(out / "class_counts.png", dpi=130)
    plt.close(fig)

    top_missing = train.isna().mean().sort_values(ascending=False).head(8) * 100
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.barh(top_missing.index[::-1], top_missing.iloc[::-1])
    ax.set_xlabel("Percent missing")
    ax.set_title("Training features with most missing values")
    fig.tight_layout()
    fig.savefig(out / "missing_values.png", dpi=130)
    plt.close(fig)

    summary = [
        "# Dataset Summary" + (" (SYNTHETIC DEMO - not final results)" if demo else ""),
        "", "- Dataset: UNSW-NB15 prepared train/test split" if not demo else "- Dataset: made-up data for testing only",
        f"- Training rows: {len(train):,}",
        f"- Testing rows: {len(test):,}",
        f"- Training normal records: {int(counts[0]):,}",
        f"- Training attack records: {int(counts[1]):,}",
        f"- Columns: {len(train.columns)}", "",
        "TODO: Explain what a traffic record represents, which columns are useful, and what you noticed.",
    ]
    (out.parent / ("dataset_summary_demo.md" if demo else "dataset_summary.md")).write_text(
        "\n".join(summary) + "\n", encoding="utf-8"
    )
    print(f"Saved summary and charts to: {out.parent}")


if __name__ == "__main__":
    main()
