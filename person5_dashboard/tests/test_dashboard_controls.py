"""Check menu selection state without launching a Streamlit server."""

import importlib.util
import sys
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

CONTROLS_PATH = Path(__file__).resolve().parents[1] / "dashboard_controls.py"


class FakeStreamlit:
    def __init__(self):
        self.session_state = {}
        self.click_key = None
        self.trigger = None
        self.labels = []

    def markdown(self, text, **kwargs):
        self.labels.append(text)

    @contextmanager
    def popover(self, label, **kwargs):
        self.trigger = label
        yield

    def button(self, label, *, key, on_click, args, **kwargs):
        if key == self.click_key:
            on_click(*args)


def load_controls(fake_streamlit):
    spec = importlib.util.spec_from_file_location("dashboard_controls_under_test", CONTROLS_PATH)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, {"streamlit": fake_streamlit}):
        spec.loader.exec_module(module)
    return module


class MenuTests(unittest.TestCase):
    def setUp(self):
        self.fake = FakeStreamlit()
        self.controls = load_controls(self.fake)

    def test_requires_a_choice(self):
        with self.assertRaisesRegex(ValueError, "at least one"):
            self.controls.menu_select("Select", [], key="empty")

    def test_defaults_to_first_option(self):
        selected = self.controls.menu_select("Model", [1, 2], key="model", format_func=str)
        self.assertEqual(selected, 1)
        self.assertEqual(self.fake.trigger, "1")

    def test_click_updates_selection_without_text_input(self):
        self.fake.click_key = "model_choice_1"
        selected = self.controls.menu_select("Model", [1, 2], key="model")
        self.assertEqual(selected, 2)
        self.assertEqual(self.fake.session_state["model"], 2)

    def test_unavailable_model_resets_to_first(self):
        self.fake.session_state["model"] = 99
        selected = self.controls.menu_select("Model", [1, 2], key="model")
        self.assertEqual(selected, 1)

    def test_label_escaped_before_html_render(self):
        self.controls.menu_select("Select <model>", [1], key="model")
        self.assertIn("Select &lt;model&gt;", self.fake.labels[0])


if __name__ == "__main__":
    unittest.main()
