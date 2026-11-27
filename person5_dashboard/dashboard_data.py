"""Validation and evaluation for the Person 5 dashboard.

Pure Python functions live here so they can be tested without Streamlit.
The app compares existing predictions; it does not train models.
"""
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

MODEL_NAMES = {
    1: "Logistic Regression",
    2: "Random Forest",
    3: "Linear SVM",
    4: "Isolation Forest",
}
REQUIRED_COLUMNS = ["row_id", "y_true", "y_pred"]
OFFICIAL_TEST_ROWS = 82_332


@dataclass
class LoadReport:
    frames: dict[int, pd.DataFrame] = field(default_factory=dict)
    missing: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)


def validate_predictions(df: pd.DataFrame, source: str = "Prediction file", expected_rows: int | None = None) -> pd.DataFrame:
    """Validate a model's original, ordered binary predictions.

    Returns a copy with integer labels. Raises ValueError with a user-facing fix.
    """
    if list(df.columns) != REQUIRED_COLUMNS:
        raise ValueError(f"{source}: use exactly these columns, in this order: {', '.join(REQUIRED_COLUMNS)}.")
    if df.empty:
        raise ValueError(f"{source}: file contains no prediction rows.")
    if expected_rows is not None and len(df) != expected_rows:
        raise ValueError(
            f"{source}: found {len(df):,} rows, but real results must contain all "
            f"{expected_rows:,} official test rows. Re-run the model on the entire test set."
        )
    ids = df["row_id"]
    if ids.isna().any() or not np.array_equal(ids.to_numpy(), np.arange(len(df))):
        raise ValueError(f"{source}: row_id must be 0, 1, 2 ... in original test order (no missing or shuffled rows).")
    for label in ("y_true", "y_pred"):
        if df[label].isna().any() or not df[label].isin([0, 1]).all():
            raise ValueError(f"{source}: {label} must contain only 0 (normal) and 1 (attack).")

    clean = df.copy()
    for col in REQUIRED_COLUMNS:
        clean[col] = clean[col].astype("int64")
    return clean


def load_results(directory: Path, *, real: bool = False) -> LoadReport:
    """Load valid p1..p4 files and safely exclude incompatible ones."""
    report = LoadReport()
    reference: pd.DataFrame | None = None
    for number, name in MODEL_NAMES.items():
        path = directory / f"p{number}.csv"
        if not path.is_file():
            report.missing.append(name)
            continue
        try:
            frame = pd.read_csv(path)
            frame = validate_predictions(frame, path.name, OFFICIAL_TEST_ROWS if real else None)
            if reference is not None and not frame[["row_id", "y_true"]].equals(reference[["row_id", "y_true"]]):
                raise ValueError(
                    f"{path.name}: ground-truth labels do not match other loaded model files. "
                    "Every model must predict the same test rows in the same order."
                )
            if reference is None:
                reference = frame
            report.frames[number] = frame
        except (OSError, ValueError, pd.errors.ParserError, UnicodeError) as exc:
            report.problems.append(f"{name} ({path.name}): {exc}")
    return report


def model_statistics(df: pd.DataFrame) -> dict:
    """Binary classification scores with attack (1) as the positive class."""
    truth, predictions = df["y_true"], df["y_pred"]
    tn, fp, fn, tp = confusion_matrix(truth, predictions, labels=[0, 1]).ravel()
    return {
        "Accuracy": float(accuracy_score(truth, predictions)),
        "Precision": float(precision_score(truth, predictions, zero_division=0)),
        "Recall": float(recall_score(truth, predictions, zero_division=0)),
        "F1": float(f1_score(truth, predictions, zero_division=0)),
        "False alarm rate": float(fp / (fp + tn)) if (fp + tn) else 0.0,
        "True normal": int(tn),
        "False alarms": int(fp),
        "Missed attacks": int(fn),
        "Detected attacks": int(tp),
        "Rows": int(len(df)),
    }


def comparison_table(frames: dict[int, pd.DataFrame]) -> pd.DataFrame:
    """One row per available model, preserving numeric scores for charting."""
    records = []
    for number, df in frames.items():
        records.append({"Model number": number, "Model": MODEL_NAMES[number], **model_statistics(df)})
    if not records:
        return pd.DataFrame()
    return pd.DataFrame(records).sort_values(["F1", "Recall"], ascending=False).reset_index(drop=True)
