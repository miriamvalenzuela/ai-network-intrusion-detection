"""Shared STARTER helpers, already provided so team members can work independently.

The final assignment still belongs to each person. This file only handles common
CSV loading, label-safe preprocessing, and the agreed prediction-file format.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
TRAIN_NAME = "UNSW_NB15_training-set.csv"
TEST_NAME = "UNSW_NB15_testing-set.csv"
DROP_COLUMNS = ("id", "label", "attack_cat")
CATEGORICAL_COLUMNS = ("proto", "service", "state")


def load_data(data_dir="data/raw"):
    """Read the original split and return (X_train, y_train, X_test, y_test, train, test)."""
    directory = Path(data_dir)
    if not directory.is_absolute():
        directory = ROOT / directory
    train_path = directory / TRAIN_NAME
    test_path = directory / TEST_NAME
    missing = [str(p) for p in (train_path, test_path) if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing dataset file(s):\n  " + "\n  ".join(missing)
            + "\nRun: python scripts/download_dataset.py\n"
            + "Or: python scripts/generate_sample_data.py (for a quick demo only)"
        )
    train = pd.read_csv(train_path, low_memory=False)
    test = pd.read_csv(test_path, low_memory=False)
    for name, frame in (("training", train), ("testing", test)):
        if "label" not in frame:
            raise ValueError(f"{name} CSV does not contain the required 'label' column")
    if set(train.columns) != set(test.columns):
        raise ValueError("Training and test CSV columns do not match")
    y_train = pd.to_numeric(train["label"], errors="raise").astype(int)
    y_test = pd.to_numeric(test["label"], errors="raise").astype(int)
    if not set(y_train.unique()).issubset({0, 1}) or not set(y_test.unique()).issubset({0, 1}):
        raise ValueError("Expected binary labels: 0=normal, 1=attack")
    X_train = train.drop(columns=list(DROP_COLUMNS), errors="ignore").copy()
    X_test = test.drop(columns=list(DROP_COLUMNS), errors="ignore").copy()
    if list(X_train.columns) != list(X_test.columns):
        X_test = X_test.reindex(columns=X_train.columns)
    X_train = X_train.replace([np.inf, -np.inf], np.nan)
    X_test = X_test.replace([np.inf, -np.inf], np.nan)
    print(f"Loaded {len(train):,} training rows and {len(test):,} testing rows from {directory}")
    return X_train, y_train, X_test, y_test, train, test


def preprocess_for(X, numeric_only=False):
    """Build a transformer. It is fitted on training records by each model pipeline."""
    categorical = [] if numeric_only else [c for c in CATEGORICAL_COLUMNS if c in X.columns]
    numeric = [c for c in X.columns if c not in categorical and pd.api.types.is_numeric_dtype(X[c])]
    if not numeric:
        raise ValueError("No numeric features found")
    transformers = [
        ("numeric", Pipeline([
            ("missing", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]), numeric)
    ]
    if categorical:
        transformers.append(("categorical", Pipeline([
            ("missing", SimpleImputer(strategy="most_frequent")),
            ("encode", OneHotEncoder(handle_unknown="ignore")),
        ]), categorical))
    return ColumnTransformer(transformers, remainder="drop")


def select_training_rows(X, y, max_rows=30000):
    """Pick a reproducible, stratified training subset, or all rows with max_rows=0."""
    if max_rows <= 0 or len(X) <= max_rows:
        return X, y
    chosen, _ = train_test_split(
        np.arange(len(y)), train_size=max_rows, stratify=y, random_state=42
    )
    print(f"Using {max_rows:,} of {len(X):,} training rows for a faster starter run.")
    return X.iloc[chosen], y.iloc[chosen]


def output_paths(data_dir, person_number, person_folder):
    """Synthetic runs go to ignored scratch/, never to final results/."""
    is_demo = Path(data_dir).name == "sample"
    if is_demo:
        csv_path = ROOT / "scratch" / "sample_results" / f"p{person_number}.csv"
        metric_path = ROOT / "scratch" / "sample_results" / f"p{person_number}_metrics.json"
    else:
        csv_path = ROOT / "results" / f"p{person_number}.csv"
        metric_path = ROOT / person_folder / "metrics.json"
    return csv_path, metric_path, is_demo


def save_results(y_test, predictions, data_dir, person_number, person_folder):
    """Export row_id,y_true,y_pred in unchanged test-set order and save metrics."""
    y_true = np.asarray(y_test, dtype=int)
    y_pred = np.asarray(predictions, dtype=int)
    if y_true.shape != y_pred.shape or not set(np.unique(y_pred)).issubset({0, 1}):
        raise ValueError("Predictions must be one 0 or 1 for every test row")
    csv_path, metric_path, is_demo = output_paths(data_dir, person_number, person_folder)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    metric_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({
        "row_id": np.arange(len(y_true), dtype=int),
        "y_true": y_true,
        "y_pred": y_pred,
    }).to_csv(csv_path, index=False)
    metrics = {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
        "training_data": "SYNTHETIC_SAMPLE_DO_NOT_REPORT" if is_demo else "UNSW_NB15",
        "test_rows": int(len(y_true)),
    }
    metric_path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(f"Predictions saved: {csv_path}")
    print(f"Metrics saved: {metric_path}")
    print("Metrics:", json.dumps(metrics, indent=2))
    if is_demo:
        print("DEMO ONLY: these results use synthetic data, not official UNSW-NB15 scores.")
    return metrics
