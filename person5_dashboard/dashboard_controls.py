"""Accessible selection menus shared by the dashboard's pages.

A tracked Streamlit popover keeps the menu the same width as its trigger.
Choosing an option updates session state and closes the popover in one click.
"""

from collections.abc import Callable, Sequence
from html import escape
from typing import TypeVar

import streamlit as st

Choice = TypeVar("Choice", int, str)


def _select_option(selection_key: str, popover_key: str, value: Choice) -> None:
    """Update a menu choice before Streamlit reruns the script."""
    st.session_state[selection_key] = value
    st.session_state[popover_key] = False


def menu_select(
    label: str,
    options: Sequence[Choice],
    *,
    key: str,
    format_func: Callable[[Choice], str] = str,
) -> Choice:
    """Show a full-width, non-searchable selector that closes on selection.

    Guidance is presented in the page itself rather than via hover tooltips.
    Streamlit 1.55+ is required for tracked popover state.
    """
    if not options:
        raise ValueError("menu_select requires at least one option")

    if st.session_state.get(key) not in options:
        st.session_state[key] = options[0]

    popover_key = f"{key}_popover"
    st.markdown(
        f'<div class="ui-dropdown-label">{escape(label)}</div>',
        unsafe_allow_html=True,
    )

    # Streamlit makes a stretched popover at least as wide as its trigger.
    # Tracking the open state lets each option's callback close the panel.
    with st.popover(
        format_func(st.session_state[key]),
        key=popover_key,
        on_change="rerun",
        width="stretch",
    ):
        for index, option in enumerate(options):
            st.button(
                format_func(option),
                key=f"{key}_option_{index}",
                width="stretch",
                on_click=_select_option,
                args=(key, popover_key, option),
                type="primary" if option == st.session_state[key] else "secondary",
            )

    return st.session_state[key]
