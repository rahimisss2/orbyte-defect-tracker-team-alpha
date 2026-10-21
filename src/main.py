"""Orbyte Smart-Defect Tracker — run with streamlit run src/main.py."""

import logging
from html import escape

import streamlit as st

from database import read_database
from navigation import render_navigation
from page_transition import show_page_transition
from theme import apply_theme

st.set_page_config(
    page_title="Orbyte · Smart-Defect Tracker",
    page_icon=":material/inventory_2:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(
    """
    <style>
    .main .block-container,
    [data-testid="stMainBlockContainer"] {
        animation: fadeIn ease 1s;
        -webkit-animation: fadeIn ease 1s;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @-webkit-keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @media (prefers-reduced-motion: reduce) {
        .main .block-container,
        [data-testid="stMainBlockContainer"] {
            animation: none !important;
            -webkit-animation: none !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)
apply_theme()
st.markdown(
    """
    <style>
    @media (max-width: 767px) {
        .st-key-top-navigation {
            padding: .55rem;
        }
        .st-key-operations-nav [data-testid="stHorizontalBlock"] {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: .5rem;
        }
        .st-key-operations-nav [data-testid="stColumn"] {
            width: 100% !important;
            min-width: 0 !important;
        }
        .st-key-nav-card-overview,
        .st-key-nav-card-intake,
        .st-key-nav-card-audit {
            min-width: 0;
            min-height: 0;
            padding: .55rem;
        }
        .st-key-nav-card-overview [data-testid="stButton"] button,
        .st-key-nav-card-intake [data-testid="stButton"] button,
        .st-key-nav-card-audit [data-testid="stButton"] button {
            height: auto;
            min-height: 2.4rem;
            padding: .4rem .45rem;
            white-space: normal;
        }
        .st-key-nav-card-overview [data-testid="stButton"] button p,
        .st-key-nav-card-intake [data-testid="stButton"] button p,
        .st-key-nav-card-audit [data-testid="stButton"] button p {
            white-space: normal !important;
            overflow-wrap: anywhere;
            text-overflow: clip;
        }
        .st-key-kpi-grid [data-testid="stHorizontalBlock"] {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: .5rem;
        }
        .st-key-kpi-grid [data-testid="stColumn"] {
            width: 100% !important;
            min-width: 0 !important;
            padding: .55rem;
        }
        .st-key-kpi-grid [data-testid="stMetric"] {
            min-width: 0;
            min-height: 70px;
        }
        .st-key-kpi-grid [data-testid="stMetricValue"],
        .st-key-kpi-grid [data-testid="stMetricValue"] > div,
        .st-key-kpi-grid [data-testid="stMetricValue"] p {
            min-width: 0;
            max-width: 100%;
            font-size: clamp(.88rem, 4.6vw, 1.2rem) !important;
            white-space: normal !important;
            overflow: visible !important;
            overflow-wrap: anywhere;
            text-overflow: clip !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
}, position="hidden")

render_navigation(page.url_path)
show_page_transition(page.url_path)

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
