"""Color tokens for the Streamlit presentation layer.

Only color values differ between themes. The layout rules live in theme.css so
light and dark mode remain visually consistent and easy to maintain.
"""

from pathlib import Path

CSS_PATH = Path(__file__).with_name("theme.css")

COLORS = {
    "Light": {
        "canvas": "#F5F6F8", "surface": "#FFFFFF", "surface_alt": "#F9FAFC",
        "sidebar": "#FFFFFF", "text": "#202535", "muted": "#667185",
        "subtle": "#8791A1", "border": "#E4E8EE", "blue": "#455BB1",
        "blue_soft": "#EDF1FC", "blue_text": "#304792",
        "track": "#EEF1F6", "bar": "#86A8BF",
        "teal": "#18859C", "green": "#83B89E", "orange": "#F3B34E",
        "coral": "#F06D64", "good_bg": "#EAF6F2", "bad_bg": "#FFF1ED",
        "note_bg": "#EFF5FB", "focus": "#405BC6", "shadow": "rgba(23, 36, 65, .025)",
    },
    "Dark": {
        "canvas": "#131923", "surface": "#1C2532", "surface_alt": "#222D3B",
        "sidebar": "#171F2A", "text": "#EFF3FA", "muted": "#B1BCCD",
        "subtle": "#9CAAC0", "border": "#354253", "blue": "#90A9FF",
        "blue_soft": "#2B3750", "blue_text": "#C1D0FF",
        "track": "#364456", "bar": "#779FB9",
        "teal": "#4BB7CC", "green": "#6FB99E", "orange": "#F0BB68",
        "coral": "#F38C82", "good_bg": "#253F39", "bad_bg": "#473538",
        "note_bg": "#25364A", "focus": "#B9CBFF", "shadow": "rgba(0, 0, 0, .10)",
    },
}


def build_theme_css(theme: str) -> str:
    """Return one token declaration followed by the shared stylesheet."""
    if theme not in COLORS:
        raise ValueError(f"Unknown theme: {theme}")

    tokens = "\n".join(f"--ui-{name.replace('_', '-')}: {value};" for name, value in COLORS[theme].items())
    return f":root {{\n{tokens}\n}}\n" + CSS_PATH.read_text(encoding="utf-8")
