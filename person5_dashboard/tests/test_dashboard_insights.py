"""Verify model explanations are derived from scores, not fabricated."""

import unittest

import pandas as pd

from person5_dashboard.dashboard_insights import insights_html


class InsightTests(unittest.TestCase):
    def setUp(self):
        self.table = pd.DataFrame([
            {"Model": "Random Forest", "F1": .923, "Recall": 1.0, "Precision": .857,
             "True normal": 5, "False alarms": 1, "Missed attacks": 0, "Detected attacks": 6},
            {"Model": "Logistic Regression", "F1": .8, "Recall": 2/3, "Precision": 1.0,
             "True normal": 6, "False alarms": 0, "Missed attacks": 2, "Detected attacks": 4},
        ])

    def test_notes_tradeoff_and_uses_real_counts(self):
        text = insights_html(self.table, demo=True)
        self.assertIn("12.3 percentage points", text)
        self.assertIn("missed 0 of 6 labeled attacks", text)
        self.assertIn("16.7% false alarm rate", text)
        self.assertIn("missed 2 attacks", text)

    def test_demo_flag_is_explicit(self):
        self.assertIn("fabricated examples", insights_html(self.table, demo=True))
        self.assertNotIn("fabricated examples", insights_html(self.table, demo=False))

    def test_single_model_does_not_invent_comparison(self):
        text = insights_html(self.table.head(1), demo=False)
        self.assertIn("Only one model is available", text)

    def test_no_models_is_safe(self):
        self.assertIn("Add a valid results file", insights_html(self.table.head(0), demo=False))

    def test_escapes_untrusted_model_names(self):
        dangerous = self.table.copy()
        dangerous.loc[0, "Model"] = '<img src=x onerror=alert(1)>'
        text = insights_html(dangerous, demo=True)
        self.assertNotIn('<img', text)
        self.assertIn('&lt;img', text)


if __name__ == "__main__":
    unittest.main()
