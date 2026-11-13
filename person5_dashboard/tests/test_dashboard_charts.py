"""Verify that chart/table HTML preserves numeric scores and accessibility labels."""
import unittest
import pandas as pd
from person5_dashboard.dashboard_charts import comparison_table_html, matrix_chart_html, score_chart_html


class ChartTests(unittest.TestCase):
    def setUp(self):
        self.scores = pd.DataFrame([
            {"Model": "Logistic Regression", "Accuracy": .75, "Precision": 1.0, "Recall": .5,
             "F1": 2/3, "False alarms": 0, "Missed attacks": 2},
            {"Model": "Random Forest", "Accuracy": .875, "Precision": .8, "Recall": 1.0,
             "F1": 8/9, "False alarms": 1, "Missed attacks": 0},
        ])

    def test_bars_have_accessible_labels_and_values(self):
        html = score_chart_html(self.scores, "Recall")
        self.assertIn('role="progressbar"', html)
        self.assertIn('aria-label="Random Forest: Recall"', html)
        self.assertIn('100.0%', html)
        self.assertIn('50.0%', html)

    def test_rejects_incorrect_metric(self):
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            score_chart_html(self.scores, "DoesNotExist")

    def test_comparison_table_has_column_headers(self):
        html = comparison_table_html(self.scores)
        self.assertIn('<th scope="col">F1-score</th>', html)
        self.assertIn('Random Forest', html)
        self.assertIn('87.5%', html)

    def test_confusion_matrix_correctly_positions_counts(self):
        html = matrix_chart_html({"True normal": 6, "False alarms": 0,
                                  "Missed attacks": 2, "Detected attacks": 4})
        self.assertIn('aria-label="Confusion matrix', html)
        self.assertIn('<th scope="row">Attack</th>', html)
        self.assertIn('Missed attacks', html)
        self.assertIn('<strong>2</strong>', html)
        self.assertIn('Detected attacks', html)

    def test_html_escapes_model_names(self):
        malicious = self.scores.copy()
        malicious.loc[0, "Model"] = '<img src=x onerror=alert(1)>'
        html = comparison_table_html(malicious)
        self.assertNotIn('<img', html)
        self.assertIn('&lt;img', html)

if __name__ == "__main__":
    unittest.main()
