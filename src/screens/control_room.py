import streamlit as st

from page_transition import show_page_transition
from views import control_room

show_page_transition("")

with st.container(key="control-room-home"):
    st.markdown(
        """
        <style>
        .st-key-control-room-home .orbyte-home-hero {
          position: relative;
          isolation: isolate;
          overflow: hidden;
          margin: 0 0 1.05rem;
          padding: clamp(1.35rem, 3vw, 2.35rem);
          border: 1px solid rgba(105, 173, 177, .32);
          border-radius: 16px;
          background:
            radial-gradient(ellipse at 92% 8%, rgba(66, 194, 178, .19), transparent 36%),
            radial-gradient(ellipse at 5% 100%, rgba(54, 111, 130, .18), transparent 43%),
            linear-gradient(118deg, #172b3b 0%, #1d3846 54%, #1a3240 100%);
          box-shadow: 0 18px 42px rgba(3, 11, 19, .24), inset 0 1px rgba(231, 250, 247, .08);
        }
        .st-key-control-room-home .orbyte-home-hero::after {
          position: absolute;
          z-index: -1;
          top: -3.5rem;
          right: -2.5rem;
          width: 14rem;
          height: 14rem;
          border: 1px solid rgba(129, 208, 199, .13);
          border-radius: 50%;
          box-shadow: 0 0 0 1.7rem rgba(129, 208, 199, .035), 0 0 0 3.4rem rgba(129, 208, 199, .025);
          content: "";
        }
        .st-key-control-room-home .orbyte-home-hero .hero-kicker {
          margin: 0 0 .5rem;
          color: #9bd2cb !important;
          font: 500 .65rem/1.4 var(--orbyte-mono) !important;
          letter-spacing: .14em;
          text-transform: uppercase;
        }
        .st-key-control-room-home .orbyte-home-hero h2 {
          max-width: 720px;
          margin: 0 0 .55rem;
          color: #f0f6f6 !important;
          font: 800 clamp(1.55rem, 3vw, 2.25rem)/1.12 var(--orbyte-display) !important;
          letter-spacing: -.045em !important;
        }
        .st-key-control-room-home .orbyte-home-hero .hero-copy {
          max-width: 650px;
          margin: 0;
          color: #c1d3d7 !important;
          font: 500 .88rem/1.6 var(--orbyte-display) !important;
        }
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
        @media (max-width: 767px) {
          .st-key-control-room-home .orbyte-home-hero {
            padding: 1.25rem 1.1rem;
          }
          .st-key-control-room-home .orbyte-home-hero::after {
            right: -6rem;
            opacity: .65;
          }
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
    st.markdown(
        """
        <section class="orbyte-home-hero" aria-label="Control room overview">
          <p class="hero-kicker">Operations overview</p>
          <h2>Welcome to your Control Room</h2>
          <p class="hero-copy">A high-level overview of delivery incidents and claim activity. All operations staff can view the current system summary.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    control_room()
