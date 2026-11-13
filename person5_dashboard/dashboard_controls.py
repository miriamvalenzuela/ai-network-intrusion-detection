"""Small, accessible controls used by the model evaluation dashboard.

Unlike Streamlit's searchable selectbox, the menu below uses real buttons.
It is suitable for the project's short, fixed lists of choices.
"""

from collections.abc import Callable, Sequence
from html import escape
from typing import TypeVar

import streamlit as st

Choice = TypeVar("Choice", int, str)


def _save_choice(key: str, value: Choice) -> None:
    """Update the selection before Streamlit reruns the application."""
    st.session_state[key] = value


def menu_select(
    label: str,
    options: Sequence[Choice],
    *,
    key: str,
    format_func: Callable[[Choice], str] = str,
    help_text: str | None = None,
) -> Choice:
    """Display a non-searchable dropdown menu with an accessible button trigger.

    The selected value is stored under ``key`` in Streamlit session state.
    If available models change, an unavailable selection resets safely.
    """
    if not options:
        raise ValueError("menu_select requires at least one option")

    if st.session_state.get(key) not in options:
        st.session_state[key] = options[0]

    selected = st.session_state[key]
    st.markdown(
        f'<div class="ui-dropdown-label">{escape(label)}</div>',
        unsafe_allow_html=True,
    )

    # st.popover renders a button trigger rather than a searchable input.
    with st.popover(
        format_func(selected),
        help=help_text or label,
        use_container_width=True,
    ):
        for index, option in enumerate(options):
            option_label = format_func(option)
            displayed_label = f"\u2713  {option_label}" if option == selected else option_label
            st.button(
                displayed_label,
                key=f"{key}_choice_{index}",
                use_container_width=True,
                on_click=_save_choice,
                args=(key, option),
            )

    return st.session_state[key]
