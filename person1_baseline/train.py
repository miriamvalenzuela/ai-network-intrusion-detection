"""Person 1: supervised baseline using Logistic Regression."""
from pathlib import Path
import sys
import argparse
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project_utils.core import load_data, preprocess_for, select_training_rows, save_results


def main():
    parser = argparse.ArgumentParser(description="Person 1: Logistic Regression baseline")
    parser.add_argument("--data-dir", default="data/raw")
    parser.add_argument("--max-train-rows", type=int, default=30000,
                        help="Training subset size; 0=use all training rows")
    args = parser.parse_args()
    X_train, y_train, X_test, y_test, _, _ = load_data(args.data_dir)
    X_train, y_train = select_training_rows(X_train, y_train, args.max_train_rows)
    model = Pipeline([
        ("prepare", preprocess_for(X_train)),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])
    print("Training Logistic Regression model...")
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    save_results(y_test, predictions, args.data_dir, 1, "person1_baseline")
    # TODO: Try another training size and explain what changes in your README.


if __name__ == "__main__":
    main()
