"""Theme and accessible presentation regression tests."""

import unittest

from person5_dashboard.dashboard_charts import kpi_grid_html, outcome_overview_html
from person5_dashboard.dashboard_theme import build_theme_css


class PresentationTests(unittest.TestCase):
    def test_light_and_dark_styles_have_identical_component_rules(self):
        light = build_theme_css("Light")
        dark = build_theme_css("Dark")
        self.assertIn("--ui-canvas: #F5F6F8", light)
        self.assertIn("--ui-canvas: #131923", dark)
        self.assertIn(".ui-kpi-grid", light)
        self.assertIn(".ui-kpi-grid", dark)

    def test_unknown_theme_rejected(self):
        with self.assertRaises(ValueError):
            build_theme_css("Unknown")

    def test_kpi_escapes_text(self):
        html = kpi_grid_html([("<test>", "85%", "Example")])
        self.assertIn("&lt;test&gt;", html)
        self.assertNotIn("<test>", html)

    def test_donut_counts_sum_to_total_and_have_text_labels(self):
        stats = {
            "True normal": 6,
            "Detected attacks": 4,
            "False alarms": 0,
            "Missed attacks": 2,
        }
        html = outcome_overview_html(stats, "Logistic Regression")
        self.assertIn("12", html)
        self.assertIn("Missed attacks: 2", html)
        self.assertIn("Detected attacks", html)
        self.assertIn("conic-gradient(", html)

    def test_outcome_escapes_model_name(self):
        html = outcome_overview_html({
            "True normal": 1, "Detected attacks": 1,
            "False alarms": 0, "Missed attacks": 0,
        }, "<img>")
        self.assertIn("&lt;img&gt;", html)
        self.assertNotIn("<img>", html)


if __name__ == "__main__":
    unittest.main()
