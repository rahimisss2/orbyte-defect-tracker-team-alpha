"""A short, shared entrance indicator for native Streamlit pages."""

import time

import streamlit as st


def show_page_transition(page_path: str) -> None:
    """Show once per page change, not on ordinary widget reruns."""
    if st.session_state.get("_orbyte_transition_page") == page_path:
        return

    progress = st.progress(0, text="Loading page…")
    try:
        for value in range(5, 101, 5):
            time.sleep(0.015)
            progress.progress(value, text="Loading page…")
    finally:
        progress.empty()

    st.session_state["_orbyte_transition_page"] = page_path
