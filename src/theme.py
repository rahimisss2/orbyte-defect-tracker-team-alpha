"""Orbyte's Streamlit visual system.

Call :func:`apply_theme` near the start of the app, after ``st.set_page_config``.
The styles intentionally target Streamlit's public ``data-testid`` hooks and
leave its native navigation, sidebar controls, and error surfaces intact.
"""

import streamlit as st


def apply_theme() -> None:
    """Inject the Orbyte dark navy and teal theme into the current Streamlit page."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

        :root {
          color-scheme: dark;
          --orbyte-canvas: #101a27;
          --orbyte-raised: #152232;
          --orbyte-surface: #1b2a3a;
          --orbyte-surface-high: #223345;
          --orbyte-ink: #e8f0f2;
          --orbyte-soft: #c4d1d5;
          --orbyte-muted: #a1b2b9;
          --orbyte-line: #314354;
          --orbyte-line-strong: #496070;
          --orbyte-teal: #42c2b2;
          --orbyte-teal-light: #8fe2d3;
          --orbyte-green: #78d0a2;
          --orbyte-amber: #e4b76d;
          --orbyte-display: "Manrope", sans-serif;
          --orbyte-mono: "DM Mono", monospace;
        }

        html, body, [data-testid="stAppViewContainer"] {
          color: var(--orbyte-ink);
          font-family: var(--orbyte-display);
          -webkit-font-smoothing: antialiased;
        }
        [data-testid="stAppViewContainer"] {
          background:
            radial-gradient(ellipse at 100% 0%, rgba(42, 132, 124, .075), transparent 34%),
            radial-gradient(ellipse at 0% 100%, rgba(35, 108, 115, .055), transparent 38%),
            linear-gradient(135deg, #111c2a 0%, #172332 52%, #1a2938 100%);
        }
        [data-testid="stHeader"] {
          background: rgba(13, 25, 38, .56);
          border-bottom: 1px solid rgba(149, 177, 188, .14);
          backdrop-filter: blur(12px);
        }
        [data-testid="stToolbar"] { right: 1rem; }
        [data-testid="stMainBlockContainer"] {
          max-width: 1440px;
          padding: 5rem clamp(1rem, 3.4vw, 3rem) 2.5rem;
        }

        h1, h2, h3, h4 {
          color: #f0f5f6;
          font-family: var(--orbyte-display);
          letter-spacing: -.045em;
        }
        h1 {
          font-weight: 800;
          font-size: clamp(2rem, 3.8vw, 3.05rem);
          line-height: 1.08;
          margin-bottom: .35rem;
        }
        h2 { font-weight: 700; }
        p, label, [data-testid="stCaptionContainer"] {
          color: var(--orbyte-soft);
        }
        [data-testid="stCaptionContainer"] {
          font-size: .92rem;
          line-height: 1.65;
        }

        /* Native sidebar stays fully usable, including Streamlit's own controls. */
        [data-testid="stSidebar"] {
          background: linear-gradient(165deg, #0c2b31 0%, #102a32 48%, #122832 100%);
          border-right: 1px solid rgba(123, 185, 185, .16);
          box-shadow: 12px 0 34px rgba(3, 11, 18, .12);
        }
        [data-testid="stSidebar"] > div:first-child {
          background: transparent;
        }
        .orbyte-brand {
          color: #e8f0f2;
          font: 800 1.8rem var(--orbyte-display);
          letter-spacing: -.06em;
          margin: .4rem 0 .6rem;
        }
        .orbyte-brand span { color: var(--orbyte-teal); }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
          color: #c2d5d8;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong {
          color: #a8c1c3;
          font: 500 .68rem var(--orbyte-mono);
          letter-spacing: .09em;
        }
        [data-testid="stSidebar"] a {
          color: #c2d5d8;
          border-radius: 7px;
          transition: background-color .18s ease, color .18s ease, transform .18s ease;
        }
        [data-testid="stSidebar"] a:hover {
          color: #f3fffd;
          background: rgba(167, 226, 221, .1);
          transform: translateX(2px);
        }
        [data-testid="stSidebar"] a[aria-current="page"] {
          color: #f3fffd;
          background: #1d4147;
          box-shadow: inset 2px 0 var(--orbyte-teal);
        }
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
          gap: .45rem;
        }

        /* Native bordered containers become calm, legible working surfaces. */
        [data-testid="stVerticalBlockBorderWrapper"] {
          background: linear-gradient(145deg, rgba(29, 45, 61, .96), rgba(26, 41, 56, .96));
          border: 1px solid #364a5b;
          border-radius: 10px;
          box-shadow: 0 14px 36px rgba(3, 11, 19, .18);
        }
        [data-testid="stMetric"] {
          min-height: 112px;
          padding: 1rem 1.05rem .85rem;
          background: linear-gradient(145deg, #213244, #1b2a39);
          border: 1px solid #394d5e;
          border-radius: 9px;
          box-shadow: 0 8px 20px rgba(3, 10, 18, .1);
          transition: transform .18s ease, border-color .18s ease;
        }
        [data-testid="stMetric"]:hover {
          border-color: #4b716f;
          transform: translateY(-2px);
        }
        [data-testid="stMetricLabel"] {
          color: #c0cdd2;
          font: 500 .68rem var(--orbyte-mono);
          letter-spacing: .065em;
          text-transform: uppercase;
        }
        [data-testid="stMetricValue"] {
          color: var(--orbyte-teal-light);
          font-family: var(--orbyte-mono);
          font-size: clamp(1.45rem, 2.2vw, 2rem);
          font-weight: 500;
          font-variant-numeric: tabular-nums;
        }
        [data-testid="stMetricDelta"] { font-size: .78rem; }
        .st-key-kpi-grid [data-testid="stHorizontalBlock"] {
          display: grid;
          grid-template-columns: repeat(4, minmax(0, 1fr));
          gap: 1rem;
        }
        .st-key-kpi-grid [data-testid="stColumn"] {
          width: 100% !important;
          min-width: 0 !important;
          padding: 1.1rem;
          background: linear-gradient(145deg, #213244, #1b2a39);
          border: 1px solid #394d5e;
          border-radius: 9px;
          box-shadow: 0 8px 20px rgba(3, 10, 18, .1);
        }
        .st-key-kpi-grid [data-testid="stMetric"] {
          padding: 0;
          min-height: 90px;
          background: none;
          border: 0;
          box-shadow: none;
          transform: none;
        }
        .st-key-kpi-grid [data-testid="stMetricValue"] {
          font-family: var(--orbyte-display);
          font-size: clamp(1.25rem, 1.9vw, 1.8rem);
          font-weight: 700;
          letter-spacing: -.035em;
        }

        [data-testid="stAlert"] {
          border-radius: 8px;
          border: 1px solid #53616c;
          background: #24323e;
          color: #d1dcdf;
        }
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stNumberInput"] input,
        [data-testid="stSelectbox"] [data-baseweb="select"] > div {
          color: #e7f0f1;
          background: #142331;
          border-color: #496070;
          border-radius: 7px;
          font-family: var(--orbyte-display);
          transition: border-color .16s ease, box-shadow .16s ease, background-color .16s ease;
        }
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus,
        [data-testid="stNumberInput"] input:focus,
        [data-testid="stSelectbox"] [data-baseweb="select"]:focus-within > div {
          border-color: #5bcabd;
          box-shadow: 0 0 0 3px rgba(65, 194, 178, .18);
          background: #182b38;
        }
        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder {
          color: #a6b6bb;
          opacity: 1;
        }
        [data-testid="stWidgetLabel"] p {
          color: #d8e3e5;
          font-weight: 600;
        }
        [data-testid="stButton"] button,
        [data-testid="stFormSubmitButton"] button {
          min-height: 2.7rem;
          padding: .55rem 1rem;
          border: 1px solid #43c2b2;
          border-radius: 7px;
          background: #35a998;
          color: #062821;
          font-family: var(--orbyte-display);
          font-weight: 700;
          transition: transform .18s ease, background-color .18s ease, border-color .18s ease;
        }
        [data-testid="stButton"] button:hover,
        [data-testid="stFormSubmitButton"] button:hover {
          background: #50c4b2;
          border-color: #6bd6c7;
          transform: translateY(-1px);
        }
        [data-testid="stButton"] button:focus-visible,
        [data-testid="stFormSubmitButton"] button:focus-visible,
        input:focus-visible, textarea:focus-visible, [role="combobox"]:focus-visible {
          outline: 3px solid #66dfce;
          outline-offset: 3px;
        }

        [data-testid="stDataFrame"] {
          border: 1px solid #3d5261;
          border-radius: 8px;
          overflow: hidden;
        }
        [data-testid="stDataFrame"] [role="columnheader"] {
          color: #c2cfd2;
          font-family: var(--orbyte-mono);
          font-size: .72rem;
        }
        [data-testid="stDataFrame"] [role="gridcell"] {
          color: #d0dadd;
          font-variant-numeric: tabular-nums;
        }
        [data-testid="stDataFrame"] [role="row"]:hover [role="gridcell"] {
          background: rgba(111, 178, 173, .07);
        }
        [data-testid="stSpinner"] > div { border-top-color: var(--orbyte-teal); }
        hr { border-color: rgba(149, 177, 188, .2); }

        @media (max-width: 1150px) {
          .st-key-kpi-grid [data-testid="stHorizontalBlock"] {
            grid-template-columns: repeat(2, minmax(0, 1fr));
          }
        }
        @media (max-width: 767px) {
          [data-testid="stMainBlockContainer"] {
            padding: 4.6rem 1rem 2rem;
          }
          [data-testid="stMetric"] {
            min-height: 98px;
            padding: .85rem;
          }
          h1 { font-size: clamp(1.85rem, 8vw, 2.55rem); }
        }
        @media (max-width: 600px) {
          .st-key-kpi-grid [data-testid="stHorizontalBlock"] {
            grid-template-columns: minmax(0, 1fr);
          }
          .st-key-kpi-grid [data-testid="stMetricValue"] { font-size: 1.8rem; }
        }
        @media (prefers-reduced-motion: reduce) {
          *, *::before, *::after {
            animation-duration: .01ms !important;
            animation-iteration-count: 1 !important;
            scroll-behavior: auto !important;
            transition-duration: .01ms !important;
          }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
