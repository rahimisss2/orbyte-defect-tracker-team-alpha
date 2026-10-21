"""Orbyte Smart-Defect Tracker — run with streamlit run src/main.py."""

import logging
from html import escape
from pathlib import Path

import streamlit as st

from database import read_database
from theme import apply_theme

st.set_page_config(
    page_title="Orbyte · Smart-Defect Tracker",
    page_icon=":material/inventory_2:",
    layout="wide",
    initial_sidebar_state="auto",
)
apply_theme()
st.logo(str(Path(__file__).resolve().parent / "assets" / "orbyte-mark.svg"), size="large")

try:
    st.session_state["database"] = read_database()
except (OSError, ValueError) as error:
    logging.exception("Could not load Orbyte's local database")
    st.error(f"Could not load the local workspace: {error}")
    st.stop()

page = st.navigation({
    "OPERATIONS": [
        st.Page("screens/overview.py", title="Control room", icon=":material/dashboard:", default=True),
        st.Page("screens/intake.py", title="Log incident", icon=":material/add:", url_path="intake"),
        st.Page("screens/audit.py", title="Audit history", icon=":material/list_alt:", url_path="audit"),
    ],
    "MANAGER SECTION": [
        st.Page("screens/manager.py", title="Manager dashboard", icon=":material/trending_up:", url_path="manager"),
        st.Page("screens/review.py", title="Review & authorize", icon=":material/task_alt:", url_path="review"),
    ],
}, expanded=True)

with st.sidebar:
    st.divider()
    st.caption("Hub operations · Local demo workspace")
    pending = sum(claim["status"] == "pending_review" for claim in st.session_state["database"]["claims"])
    st.caption(f"{pending} pending {'discrepancy' if pending == 1 else 'discrepancies'}")
    st.caption("ORBYTE SYSTEMS")

st.markdown(
    (
        '<div class="orbyte-topline"><span><span class="crumb">Orbyte</span>'
        f'<span class="slash">/</span>{escape(page.title)}</span>'
        '<span class="orbyte-live">LIVE WORKSPACE</span></div>'
        '<p class="orbyte-eyebrow">RETAIL CLAIMS OPERATIONS</p>'
    ),
    unsafe_allow_html=True,
)
st.title(page.title)
st.info(
    "Demo workspace. No email is actually sent and no external supplier invoice is held. "
    "The Manager Section separates workflows; it does not enforce sign-in or access permissions."
)

flash = st.session_state.pop("flash", None)
if flash:
    level, message = flash
    getattr(st, level)(message)

page.run()
st.divider()
st.caption("ORBYTE SMART-DEFECT TRACKER · PRECISION IN EVERY HANDOFF")
