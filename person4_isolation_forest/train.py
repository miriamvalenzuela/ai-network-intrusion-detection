"""Person 4: anomaly detection trained ONLY on normal training records."""
from pathlib import Path
import sys
import argparse
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project_utils.core import load_data, preprocess_for, save_results


def main():
    parser = argparse.ArgumentParser(description="Person 4: Isolation Forest")
    parser.add_argument("--data-dir", default="data/raw")
    parser.add_argument("--max-train-rows", type=int, default=30000,
                        help="Maximum normal training rows; 0=use all normal rows")
    args = parser.parse_args()
    X_train, y_train, X_test, y_test, _, _ = load_data(args.data_dir)
    X_normal = X_train.loc[y_train == 0]
    if args.max_train_rows > 0 and len(X_normal) > args.max_train_rows:
        X_normal = X_normal.sample(n=args.max_train_rows, random_state=42)
        print(f"Using {len(X_normal):,} normal training rows for a faster starter run.")
    model = Pipeline([
        # Numeric-only is an intentional simplification for this anomaly detector.
        ("prepare", preprocess_for(X_normal, numeric_only=True)),
        ("detector", IsolationForest(
            n_estimators=100, contamination=0.02, random_state=42, n_jobs=-1
        )),
    ])
    print("Training Isolation Forest on normal traffic only...")
    model.fit(X_normal)
    # IsolationForest returns +1 for normal and -1 for an anomaly.
    # Our class-project output contract is 0=normal, 1=attack/suspicious.
    raw_predictions = model.predict(X_test)
    predictions = (raw_predictions == -1).astype(int)
    save_results(y_test, predictions, args.data_dir, 4, "person4_isolation_forest")
    # TODO: Discuss why anomalies do not always match labeled attacks.


if __name__ == "__main__":
    main()
