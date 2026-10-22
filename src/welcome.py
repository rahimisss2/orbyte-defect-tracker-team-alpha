"""Shared presentation for the dashboard welcome banners."""

from html import escape

import streamlit as st


def render_welcome(title: str, kicker: str, description: str, key: str) -> None:
    with st.container(key=key):
        st.markdown(
            """
            <style>
            .orbyte-home-hero {
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
            .orbyte-home-hero::after {
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
            .orbyte-home-hero .hero-kicker {
              margin: 0 0 .5rem;
              color: #9bd2cb !important;
              font: 500 .65rem/1.4 var(--orbyte-mono) !important;
              letter-spacing: .14em;
              text-transform: uppercase;
            }
            .orbyte-home-hero h2 {
              max-width: 720px;
              margin: 0 0 .55rem;
              color: #f0f6f6 !important;
              font: 800 clamp(1.55rem, 3vw, 2.25rem)/1.12 var(--orbyte-display) !important;
              letter-spacing: -.045em !important;
            }
            .orbyte-home-hero .hero-copy {
              max-width: 650px;
              margin: 0;
              color: #c1d3d7 !important;
              font: 500 .88rem/1.6 var(--orbyte-display) !important;
            }
            @media (max-width: 767px) {
              .orbyte-home-hero { padding: 1.25rem 1.1rem; }
              .orbyte-home-hero::after { right: -6rem; opacity: .65; }
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<section class="orbyte-home-hero" aria-label="{escape(kicker)}">'
            f'<p class="hero-kicker">{escape(kicker)}</p>'
            f'<h2>{escape(title)}</h2>'
            f'<p class="hero-copy">{escape(description)}</p>'
            '</section>',
            unsafe_allow_html=True,
        )
