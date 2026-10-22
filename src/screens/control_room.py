import streamlit as st

from page_transition import show_page_transition
from views import control_room

show_page_transition("")

with st.container(key="control-room-home"):
    st.markdown(
        """
        <style>
        .st-key-control-room-home .st-key-kpi-grid [data-testid="stColumn"] {
          border-radius: 12px;
          border-color: rgba(99, 145, 159, .52);
          background:
            radial-gradient(ellipse at 100% 0%, rgba(66, 194, 178, .105), transparent 48%),
            linear-gradient(145deg, #213648, #1b2b3a);
          box-shadow: 0 14px 30px rgba(3, 10, 18, .24), 0 0 18px rgba(66, 194, 178, .045), inset 0 1px rgba(220, 246, 244, .055);
        }
        .st-key-control-room-home [data-testid="stButton"] button {
          min-height: 2.85rem;
          padding: .58rem 1.15rem;
          border: 1px solid #b7ff72;
          border-radius: 8px;
          background: linear-gradient(135deg, #a8f45c, #82db45);
          color: #13291b;
          box-shadow: 0 7px 20px rgba(109, 207, 61, .19), inset 0 1px rgba(246, 255, 226, .52);
          font-weight: 800;
          transition: transform .16s ease, background-color .16s ease, border-color .16s ease, box-shadow .16s ease;
        }
        .st-key-control-room-home [data-testid="stButton"] button p,
        .st-key-control-room-home [data-testid="stButton"] button [data-testid="stMarkdownContainer"] p {
          color: #13291b !important;
          font-weight: 800 !important;
        }
        .st-key-control-room-home [data-testid="stButton"] button:hover {
          transform: translateY(-2px);
          border-color: #d2ff9c;
          background: linear-gradient(135deg, #c0ff7e, #98ec5e);
          box-shadow: 0 10px 25px rgba(109, 207, 61, .27), inset 0 1px rgba(246, 255, 226, .68);
        }
        .st-key-control-room-home [data-testid="stButton"] button:active {
          transform: translateY(1px);
          background: #78cb3d;
          box-shadow: 0 3px 10px rgba(109, 207, 61, .17), inset 0 2px 5px rgba(37, 84, 27, .2);
        }
        .st-key-control-room-home [data-testid="stButton"] button:focus-visible {
          outline: 3px solid #c4ff8d;
          outline-offset: 4px;
        }
        @media (prefers-reduced-motion: reduce) {
          .st-key-control-room-home [data-testid="stButton"] button {
            transition: none;
          }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    control_room()
