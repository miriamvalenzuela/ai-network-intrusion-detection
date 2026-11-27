"""Run from repository root: python -m unittest discover -s person5_dashboard/tests -v"""
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from person5_dashboard.dashboard_data import (
    OFFICIAL_TEST_ROWS, comparison_table, load_results, model_statistics, validate_predictions
)


def frame(truth=(0, 0, 1, 1), predicted=(0, 1, 0, 1)):
    return pd.DataFrame({"row_id": list(range(len(truth))), "y_true": truth, "y_pred": predicted})


class DashboardDataTests(unittest.TestCase):
    def test_confusion_counts_and_metrics(self):
        stats = model_statistics(frame())
        self.assertEqual((stats["True normal"], stats["False alarms"], stats["Missed attacks"], stats["Detected attacks"]), (1, 1, 1, 1))
        for metric in ["Accuracy", "Precision", "Recall", "F1", "False alarm rate"]:
            self.assertAlmostEqual(stats[metric], 0.5)

    def test_valid_schema(self):
        self.assertEqual(len(validate_predictions(frame())), 4)

    def test_missing_column_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "exactly these columns"):
            validate_predictions(frame().drop(columns="y_pred"))

    def test_shuffled_rows_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "original test order"):
            validate_predictions(frame().iloc[::-1].reset_index(drop=True))

    def test_invalid_labels_are_rejected(self):
        bad = frame()
        bad.loc[0, "y_pred"] = 2
        with self.assertRaisesRegex(ValueError, "only 0"):
            validate_predictions(bad)

    def test_incomplete_real_results_rejected(self):
        with self.assertRaisesRegex(ValueError, "official test rows"):
            validate_predictions(frame(), expected_rows=OFFICIAL_TEST_ROWS)

    def test_missing_files_do_not_crash(self):
        with tempfile.TemporaryDirectory() as temp:
            report = load_results(Path(temp))
            self.assertEqual(len(report.frames), 0)
            self.assertEqual(len(report.missing), 4)

    def test_mismatch_is_excluded_without_discarding_valid_model(self):
        with tempfile.TemporaryDirectory() as temp:
            a = frame()
            b = frame(truth=(0, 1, 1, 1))
            a.to_csv(Path(temp) / "p1.csv", index=False)
            b.to_csv(Path(temp) / "p2.csv", index=False)
            report = load_results(Path(temp))
            self.assertEqual(list(report.frames), [1])
            self.assertEqual(len(report.problems), 1)
            self.assertEqual(len(comparison_table(report.frames)), 1)

    def test_full_fake_result_accepts_real_row_count(self):
        big = pd.DataFrame({"row_id": range(OFFICIAL_TEST_ROWS), "y_true": [0]*OFFICIAL_TEST_ROWS, "y_pred": [0]*OFFICIAL_TEST_ROWS})
        self.assertEqual(len(validate_predictions(big, expected_rows=OFFICIAL_TEST_ROWS)), OFFICIAL_TEST_ROWS)


if __name__ == "__main__":
    unittest.main()
