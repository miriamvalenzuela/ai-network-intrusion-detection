"""Person 3: linear Support Vector Machine intrusion classifier."""
from pathlib import Path
import sys
import argparse
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project_utils.core import load_data, preprocess_for, select_training_rows, save_results


def main():
    parser = argparse.ArgumentParser(description="Person 3: linear SVM")
    parser.add_argument("--data-dir", default="data/raw")
    parser.add_argument("--max-train-rows", type=int, default=30000,
                        help="Training subset size; 0=use all training rows")
    args = parser.parse_args()
    X_train, y_train, X_test, y_test, _, _ = load_data(args.data_dir)
    X_train, y_train = select_training_rows(X_train, y_train, args.max_train_rows)
    model = Pipeline([
        ("prepare", preprocess_for(X_train)),
        ("classifier", LinearSVC(C=0.5, class_weight="balanced", max_iter=5000, dual="auto")),
    ])
    print("Training linear SVM model...")
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    save_results(y_test, predictions, args.data_dir, 3, "person3_svm")
    # TODO: Try different C values; consider training time and convergence warnings.


if __name__ == "__main__":
    main()
