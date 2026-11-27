"""Regression tests for full-width, auto-closing selectors."""

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
        self.popover_kwargs = {}
        self.buttons = []
        self.labels = []

    def markdown(self, text, **kwargs):
        self.labels.append(text)

    @contextmanager
    def popover(self, label, **kwargs):
        self.popover_kwargs = {"label": label, **kwargs}
        yield

    def button(self, text, **kwargs):
        self.buttons.append({"text": text, **kwargs})
        return False


def load_controls(fake_streamlit):
    spec = importlib.util.spec_from_file_location("controls_under_test", CONTROLS_PATH)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, {"streamlit": fake_streamlit}):
        spec.loader.exec_module(module)
    return module


class MenuTests(unittest.TestCase):
    def setUp(self):
        self.fake = FakeStreamlit()
        self.controls = load_controls(self.fake)

    def test_empty_options_rejected(self):
        with self.assertRaisesRegex(ValueError, "at least one"):
            self.controls.menu_select("Choose", [], key="empty")

    def test_uses_stretched_tracked_popover(self):
        self.controls.menu_select("Select model", [1, 2], key="model")
        self.assertEqual(self.fake.popover_kwargs["width"], "stretch")
        self.assertEqual(self.fake.popover_kwargs["key"], "model_popover")
        self.assertEqual(self.fake.popover_kwargs["on_change"], "rerun")
        self.assertNotIn("help", self.fake.popover_kwargs)

    def test_options_are_regular_full_width_buttons(self):
        self.controls.menu_select("Model", [1, 2], key="model")
        self.assertEqual(len(self.fake.buttons), 2)
        self.assertTrue(all(button["width"] == "stretch" for button in self.fake.buttons))
        self.assertEqual(self.fake.buttons[0]["type"], "primary")
        self.assertEqual(self.fake.buttons[1]["type"], "secondary")

    def test_click_updates_choice_and_closes_popover(self):
        self.controls.menu_select("Model", [1, 2], key="model")
        button = self.fake.buttons[1]
        button["on_click"](*button["args"])
        self.assertEqual(self.fake.session_state["model"], 2)
        self.assertIs(self.fake.session_state["model_popover"], False)
        self.assertEqual(self.controls.menu_select("Model", [1, 2], key="model"), 2)
        self.assertEqual(self.fake.popover_kwargs["label"], "2")

    def test_choice_resets_when_option_is_missing(self):
        self.fake.session_state["model"] = 999
        self.assertEqual(self.controls.menu_select("Model", [1, 2], key="model"), 1)

    def test_custom_labels_and_escaped_heading(self):
        self.controls.menu_select("<Choose>", [2], key="model", format_func=lambda value: f"Model {value}")
        self.assertEqual(self.fake.popover_kwargs["label"], "Model 2")
        self.assertIn("&lt;Choose&gt;", self.fake.labels[0])


if __name__ == "__main__":
    unittest.main()
