"""Person 2: Random Forest intrusion classifier."""
from pathlib import Path
import sys
import argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project_utils.core import load_data, preprocess_for, select_training_rows, save_results


def main():
    parser = argparse.ArgumentParser(description="Person 2: Random Forest")
    parser.add_argument("--data-dir", default="data/raw")
    parser.add_argument("--max-train-rows", type=int, default=30000,
                        help="Training subset size; 0=use all training rows")
    args = parser.parse_args()
    X_train, y_train, X_test, y_test, _, _ = load_data(args.data_dir)
    X_train, y_train = select_training_rows(X_train, y_train, args.max_train_rows)
    model = Pipeline([
        ("prepare", preprocess_for(X_train)),
        ("classifier", RandomForestClassifier(
            n_estimators=100, max_depth=18, min_samples_leaf=2,
            class_weight="balanced_subsample", random_state=42, n_jobs=-1
        )),
    ])
    print("Training Random Forest model...")
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    save_results(y_test, predictions, args.data_dir, 2, "person2_random_forest")
    # TODO: Experiment with n_estimators or max_depth and explain the result.


if __name__ == "__main__":
    main()
