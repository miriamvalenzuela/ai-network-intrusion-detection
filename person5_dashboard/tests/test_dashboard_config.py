"""Static checks for the dashboard's public title and selector wiring."""

import unittest
from pathlib import Path

APP = (Path(__file__).resolve().parents[1] / "app.py").read_text(encoding="utf-8")


class DashboardConfigTests(unittest.TestCase):
    def test_every_choice_uses_shared_popover_selector(self):
        self.assertEqual(APP.count("menu_select("), 5)
        self.assertNotIn("st.selectbox(", APP)
        self.assertNotIn("st.dataframe(", APP)

    def test_title_updated(self):
        self.assertIn('page_title="AI Network Intrusion Detection Dashboard"', APP)
        self.assertIn('"Overview": ("AI Network Intrusion Detection Dashboard"', APP)


if __name__ == "__main__":
    unittest.main()
