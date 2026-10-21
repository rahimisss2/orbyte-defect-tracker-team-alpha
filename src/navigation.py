"""Premium native-button navigation, backed by Streamlit's existing routes."""

from pathlib import Path

import streamlit as st


def _prepare_transition() -> None:
    # Even selecting the current page should replay the requested entrance.
    st.session_state.pop("_orbyte_transition_page", None)

def _select_section(section: str) -> None:
    st.session_state["_orbyte_nav_section"] = section


def render_navigation(active_path: str) -> None:
    active_section = "MANAGER" if active_path in ("manager", "review") else "OPERATIONS"
    # Follow direct URLs and in-page shortcuts, but allow browsing the other
    # section without navigating away from the currently displayed page.
    if st.session_state.get("_orbyte_nav_route") != active_path:
        st.session_state["_orbyte_nav_section"] = active_section
        st.session_state["_orbyte_nav_route"] = active_path
    selected_section = st.session_state["_orbyte_nav_section"]

    with st.container(key="top-navigation"):
        st.image(str(Path(__file__).resolve().parent / "assets" / "orbyte-mark.svg"), width=150)
        st.caption("RETAIL CLAIMS OPERATIONS · LIVE WORKSPACE")
        with st.container(key="navigation-sections"):
            for column, section in zip(st.columns(2), ("OPERATIONS", "MANAGER")):
                with column:
                    st.button(
                        section,
                        key=f"section_{section.lower()}",
                        type="primary" if selected_section == section else "secondary",
                        width="stretch",
                        on_click=_select_section,
                        args=(section,),
                    )

        sections = {
            "OPERATIONS": [
                ("overview", "control_room", "", "Control Room", "🏢", "System overview and claim activity"),
                ("intake", "log_incident", "intake", "Log Incident", "📦", "Record defective deliveries"),
                ("audit", "audit_history", "audit", "Audit History", "📋", "Shared operations audit trail"),
            ],
            "MANAGER": [
                ("manager", "manager_dashboard", "manager", "Manager Dashboard", "📊", "Financial exposure and active claims"),
                ("review", "review_authorize", "review", "Review & Authorisation", "✍️", "Review drafts and authorize claims"),
            ],
        }
        pages = sections[selected_section]
        grid_key = "operations-nav" if selected_section == "OPERATIONS" else "manager-nav"
        st.caption("OPERATIONS" if selected_section == "OPERATIONS" else "MANAGER SECTION")
        with st.container(key=grid_key):
            for column, (screen, filename, path, label, icon, description) in zip(st.columns(len(pages)), pages):
                with column, st.container(key=f"nav-card-{screen}", border=True):
                    st.markdown(f'<div class="orbyte-nav-icon">{icon}</div>', unsafe_allow_html=True)
                    if st.button(
                        label,
                        key=f"nav_{screen}",
                        type="primary" if active_path == path else "secondary",
                        width="stretch",
                        on_click=_prepare_transition,
                    ):
                        st.switch_page(f"screens/{filename}.py")
                    st.caption(description)
