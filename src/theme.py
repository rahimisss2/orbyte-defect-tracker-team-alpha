"""Orbyte's native Streamlit theme; loaded before the five native pages."""

import streamlit as st


def apply_theme() -> None:
    """Inject the compact navy-and-teal Orbyte visual system."""
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
            radial-gradient(ellipse at 100% 0%, rgba(42, 132, 124, .10), transparent 34%),
            radial-gradient(ellipse at 0% 100%, rgba(35, 108, 115, .07), transparent 38%),
            linear-gradient(135deg, #111c2a 0%, #172332 52%, #1a2938 100%);
        }
        [data-testid="stHeader"] {
          background: rgba(13, 25, 38, .60);
          border-bottom: 1px solid rgba(149, 177, 188, .13);
          backdrop-filter: blur(12px);
        }
        [data-testid="stToolbar"] { right: 1rem; }
        [data-testid="stMainBlockContainer"] {
          max-width: 1440px;
          padding: 3.9rem clamp(1rem, 3vw, 2.7rem) 1.5rem;
        }

        h1, h2, h3, h4 {
          color: #f0f5f6;
          font-family: var(--orbyte-display);
          letter-spacing: -.045em;
        }
        h1 {
          font-weight: 800;
          font-size: clamp(1.9rem, 3.2vw, 2.65rem);
          line-height: 1.08;
          margin: .1rem 0 .25rem;
        }
        [data-testid="stMarkdownContainer"] h1 {
          color: #f0f5f6 !important;
          font-family: var(--orbyte-display) !important;
          font-size: clamp(1.9rem, 3.2vw, 2.65rem) !important;
          font-weight: 800 !important;
          letter-spacing: -.045em !important;
          line-height: 1.08 !important;
        }
        h2 { font-weight: 700; font-size: 1.28rem; }
        h3 { font-weight: 700; font-size: 1.05rem; }
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4 {
          color: #f0f5f6 !important;
          font-family: var(--orbyte-display) !important;
          font-weight: 700 !important;
          letter-spacing: -.035em !important;
          line-height: 1.35 !important;
        }
        [data-testid="stMarkdownContainer"] h2 { font-size: 1.28rem !important; }
        [data-testid="stMarkdownContainer"] h3 { font-size: 1.05rem !important; }
        p, label, [data-testid="stCaptionContainer"] { color: var(--orbyte-soft); }
        [data-testid="stMarkdownContainer"] p {
          color: var(--orbyte-soft) !important;
          font-family: var(--orbyte-display) !important;
          font-size: .84rem !important;
          line-height: 1.55 !important;
        }
        [data-testid="stMarkdownContainer"] p.orbyte-eyebrow {
          margin: 0 0 .32rem !important;
          color: #a8c4c6 !important;
          font-family: var(--orbyte-mono) !important;
          font-size: .61rem !important;
          font-weight: 500 !important;
          letter-spacing: .13em !important;
          line-height: 1.3 !important;
        }
        [data-testid="stCaptionContainer"] {
          font-size: .81rem;
          line-height: 1.55;
        }
        [data-testid="stCaptionContainer"] p {
          color: var(--orbyte-soft) !important;
          font-family: var(--orbyte-display) !important;
          font-size: .81rem !important;
          font-weight: 500 !important;
          line-height: 1.55 !important;
        }
        [data-testid="stVerticalBlock"] { gap: .8rem; }
        [data-testid="stElementContainer"] { margin-bottom: 0; }
        [data-testid="stMarkdownContainer"] p { margin-bottom: .45rem; }
        .orbyte-topline {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 12px;
          margin: 0 0 .7rem;
          color: #afc1c6;
          font: 500 .68rem var(--orbyte-mono);
          letter-spacing: .025em;
        }
        .orbyte-topline .crumb { color: #d4e1e3; }
        .orbyte-topline .slash { color: #789197; padding: 0 .45rem; }
        .orbyte-live {
          display: inline-flex;
          align-items: center;
          gap: 7px;
          color: #b7d6d2;
          font: 500 .61rem var(--orbyte-mono);
          letter-spacing: .07em;
          white-space: nowrap;
        }
        .orbyte-live::before {
          content: "";
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: #78d0a2;
          box-shadow: 0 0 0 3px rgba(120, 208, 162, .11);
        }
        .orbyte-eyebrow {
          margin: 0 0 .32rem;
          color: #a8c4c6;
          font: 500 .61rem var(--orbyte-mono);
          letter-spacing: .13em;
        }

        /* Streamlit navigation and its expand/collapse controls remain native. */
        [data-testid="stSidebar"] {
          background: linear-gradient(165deg, #0c2b31 0%, #102a32 48%, #122832 100%);
          border-right: 1px solid rgba(123, 185, 185, .16);
          box-shadow: 12px 0 34px rgba(3, 11, 18, .12);
        }
        [data-testid="stSidebar"] > div:first-child { background: transparent; }
        [data-testid="stSidebar"] [data-testid="stLogo"] {
          padding: .6rem .85rem .2rem;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #c2d5d8; }
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
          color: #afc6c8;
          font-size: .68rem;
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
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: .38rem; }
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] { padding-top: .25rem; }
        [data-testid="stSidebar"] [data-testid="stNavSectionHeader"] {
          color: #a8c1c3 !important;
          font: 500 .64rem var(--orbyte-mono) !important;
          letter-spacing: .09em !important;
          text-transform: uppercase;
        }
        [data-testid="stSidebar"] [data-testid="stNavSectionHeader"] p {
          color: #a8c1c3 !important;
          font: 500 .64rem/1.5 var(--orbyte-mono) !important;
          letter-spacing: .09em !important;
        }
        [data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] p {
          color: inherit !important;
          font: 600 .84rem/1.5 var(--orbyte-display) !important;
        }
        [data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] {
          color: #c2d5d8 !important;
          font-family: var(--orbyte-display) !important;
          font-size: .84rem !important;
          font-weight: 600 !important;
        }
        [data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][aria-current="page"] {
          color: #f3fffd !important;
          background: #1d4147 !important;
          box-shadow: inset 2px 0 var(--orbyte-teal);
        }

        /* Bordered native containers: compact raised panels from the old workspace. */
        [data-testid="stVerticalBlockBorderWrapper"] {
          background: linear-gradient(145deg, rgba(29, 45, 61, .97), rgba(26, 41, 56, .97));
          border: 1px solid #364a5b;
          border-radius: 9px;
          box-shadow: 0 12px 30px rgba(3, 11, 19, .16);
        }
        .st-key-incident-form-panel,
        [class*="st-key-review-claim-"] {
          background: linear-gradient(145deg, #1d2d3d, #1a2938);
          border: 1px solid #364a5b;
          border-radius: 9px;
          box-shadow: 0 12px 30px rgba(3, 11, 19, .16);
          padding: 1.1rem;
        }
        [data-testid="stText"] {
          color: var(--orbyte-soft);
          font-family: var(--orbyte-display);
          font-size: .84rem;
          line-height: 1.6;
        }
        [data-testid="stMetric"] {
          min-height: 102px;
          padding: .82rem .95rem .72rem;
          background: linear-gradient(145deg, #213244, #1b2a39);
          border: 1px solid #394d5e;
          border-radius: 9px;
          box-shadow: 0 8px 20px rgba(3, 10, 18, .1);
          transition: transform .18s ease, border-color .18s ease;
        }
        [data-testid="stMetric"]:hover { border-color: #4b716f; transform: translateY(-2px); }
        [data-testid="stMetricLabel"] {
          color: #c0cdd2;
          font: 500 .64rem var(--orbyte-mono);
          letter-spacing: .065em;
          text-transform: uppercase;
        }
        [data-testid="stMetricLabel"] label,
        [data-testid="stMetricLabel"] p,
        [data-testid="stMetricLabel"] > div {
          color: #c0cdd2 !important;
          font: 500 .64rem/1.45 var(--orbyte-mono) !important;
          letter-spacing: .065em;
          text-transform: uppercase;
        }
        [data-testid="stMetric"] [data-testid="stMetricLabel"] p {
          color: #c0cdd2 !important;
          font-family: var(--orbyte-mono) !important;
          font-size: .64rem !important;
          font-weight: 500 !important;
          line-height: 1.45 !important;
          letter-spacing: .065em !important;
          text-transform: uppercase !important;
        }
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] > div,
        [data-testid="stMetricValue"] p {
          color: var(--orbyte-teal-light) !important;
          font-family: var(--orbyte-mono) !important;
          font-size: clamp(1.25rem, 2vw, 1.75rem) !important;
          font-weight: 500 !important;
          line-height: 1.2 !important;
          font-variant-numeric: tabular-nums;
          overflow-wrap: anywhere;
        }
        [data-testid="stMetricDelta"] { font-size: .72rem; }
        .st-key-kpi-grid [data-testid="stHorizontalBlock"] {
          display: grid;
          grid-template-columns: repeat(4, minmax(0, 1fr));
          gap: .8rem;
        }
        .st-key-kpi-grid [data-testid="stColumn"] {
          width: 100% !important;
          min-width: 0 !important;
          padding: .82rem;
          background: linear-gradient(145deg, #213244, #1b2a39);
          border: 1px solid #394d5e;
          border-radius: 9px;
          box-shadow: 0 8px 20px rgba(3, 10, 18, .1);
        }
        .st-key-kpi-grid [data-testid="stMetric"] {
          min-height: 82px;
          padding: 0;
          background: none;
          border: 0;
          box-shadow: none;
          transform: none;
        }
        .st-key-kpi-grid [data-testid="stMetricValue"],
        .st-key-kpi-grid [data-testid="stMetricValue"] > div,
        .st-key-kpi-grid [data-testid="stMetricValue"] p {
          color: #e6f2f1 !important;
          font-family: var(--orbyte-display) !important;
          font-size: clamp(1.2rem, 1.8vw, 1.65rem) !important;
          font-weight: 700 !important;
          letter-spacing: -.035em;
        }
        .st-key-kpi-grid [data-testid="stCaptionContainer"] {
          color: #b3c2c8;
          font-size: .7rem;
          line-height: 1.45;
        }
        .st-key-kpi-grid [data-testid="stCaptionContainer"] p {
          color: #b3c2c8 !important;
          font-family: var(--orbyte-display) !important;
          font-size: .7rem !important;
          font-weight: 500 !important;
          line-height: 1.45 !important;
        }

        [data-testid="stAlert"] {
          border-radius: 7px;
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
          border-radius: 6px;
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
        [data-testid="stTextArea"] textarea::placeholder { color: #a6b6bb; opacity: 1; }
        [data-testid="stWidgetLabel"] p {
          color: #d8e3e5 !important;
          font-family: var(--orbyte-display) !important;
          font-size: .85rem !important;
          font-weight: 600 !important;
          line-height: 1.45 !important;
        }
        [data-testid="stButton"] button,
        [data-testid="stFormSubmitButton"] button {
          min-height: 2.55rem;
          padding: .48rem .9rem;
          border: 1px solid #43c2b2;
          border-radius: 7px;
          background: #35a998;
          color: #062821;
          font-family: var(--orbyte-display);
          font-size: .82rem;
          font-weight: 700;
          transition: transform .18s ease, background-color .18s ease, border-color .18s ease;
        }
        [data-testid="stButton"] button p,
        [data-testid="stFormSubmitButton"] button p,
        [data-testid="stButton"] button [data-testid="stMarkdownContainer"] p,
        [data-testid="stFormSubmitButton"] button [data-testid="stMarkdownContainer"] p {
          margin: 0 !important;
          color: #062821 !important;
          font-family: var(--orbyte-display) !important;
          font-size: .82rem !important;
          font-weight: 700 !important;
          line-height: 1.25 !important;
          letter-spacing: 0 !important;
        }
        [data-testid="stButton"] button:hover,
        [data-testid="stFormSubmitButton"] button:hover {
          background: #50c4b2;
          border-color: #6bd6c7;
          transform: translateY(-1px);
        }
        [data-testid="stButton"] button:focus-visible,
        [data-testid="stFormSubmitButton"] button:focus-visible,
        input:focus-visible, textarea:focus-visible, [role="combobox"]:focus-visible,
        [data-testid="stSidebar"] button:focus-visible,
        [data-testid="stSidebar"] a:focus-visible {
          outline: 3px solid #66dfce;
          outline-offset: 3px;
        }
        [data-testid="stButton"] button:disabled,
        [data-testid="stFormSubmitButton"] button:disabled { opacity: .62; }

        [data-testid="stDataFrame"] { border: 1px solid #3d5261; border-radius: 8px; overflow: hidden; }
        [data-testid="stDataFrame"] [role="columnheader"] {
          color: #c2cfd2;
          font-family: var(--orbyte-mono);
          font-size: .68rem;
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
          .st-key-kpi-grid [data-testid="stHorizontalBlock"] { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }
        @media (max-width: 767px) {
          [data-testid="stMainBlockContainer"] { padding: 3.8rem 1rem 1.4rem; }
          [data-testid="stMetric"] { min-height: 92px; padding: .75rem; }
          h1 { font-size: clamp(1.8rem, 7vw, 2.4rem); }
          [data-testid="stMarkdownContainer"] h1 {
            font-size: clamp(1.8rem, 7vw, 2.4rem) !important;
          }
          .st-key-kpi-grid [data-testid="stHorizontalBlock"] { gap: .6rem; }
          .st-key-kpi-grid [data-testid="stColumn"] { padding: .72rem; }
        }
        @media (max-width: 560px) {
          .st-key-kpi-grid [data-testid="stHorizontalBlock"] { grid-template-columns: minmax(0, 1fr); }
          .st-key-kpi-grid [data-testid="stMetric"] { min-height: 74px; }
          .st-key-kpi-grid [data-testid="stMetricValue"],
          .st-key-kpi-grid [data-testid="stMetricValue"] > div,
          .st-key-kpi-grid [data-testid="stMetricValue"] p { font-size: 1.45rem !important; }
          [data-testid="stSidebar"] [data-testid="stSidebarNav"] { padding-bottom: .8rem; }
          .orbyte-topline { font-size: .61rem; }
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
