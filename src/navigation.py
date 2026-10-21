"""Premium native-button navigation, backed by Streamlit's existing routes."""

from pathlib import Path

import streamlit as st


def _prepare_transition() -> None:
    # Even selecting the current page should replay the requested entrance.
    st.session_state.pop("_orbyte_transition_page", None)


def render_navigation(active_path: str) -> None:
    with st.container(key="top-navigation"):
        st.image(str(Path(__file__).resolve().parent / "assets" / "orbyte-mark.svg"), width=150)
        st.caption("RETAIL CLAIMS OPERATIONS · LIVE WORKSPACE")
        operations = [
            ("overview", "", "Control Room", "🏢", "System overview and claim activity"),
            ("intake", "intake", "Log Incident", "📦", "Record defective deliveries"),
            ("audit", "audit", "Audit History", "📋", "Shared operations audit trail"),
        ]
        with st.container(key="operations-nav"):
            for column, (screen, path, label, icon, description) in zip(st.columns(3), operations):
                with column, st.container(key=f"nav-card-{screen}", border=True):
                    st.markdown(f'<div class="orbyte-nav-icon">{icon}</div>', unsafe_allow_html=True)
                    if st.button(
                        label,
                        key=f"nav_{screen}",
                        type="primary" if active_path == path else "secondary",
                        width="stretch",
                        on_click=_prepare_transition,
                    ):
                        st.switch_page(f"screens/{screen}.py")
                    st.caption(description)

        with st.expander("Manager section", expanded=active_path in ("manager", "review")):
            for column, (path, label) in zip(st.columns(2), [
                ("manager", "Manager Dashboard"),
                ("review", "Review & Authorisation"),
            ]):
                with column:
                    if st.button(
                        label,
                        key=f"nav_{path}",
                        type="primary" if active_path == path else "secondary",
                        width="stretch",
                        on_click=_prepare_transition,
                    ):
                        st.switch_page(f"screens/{path}.py")
