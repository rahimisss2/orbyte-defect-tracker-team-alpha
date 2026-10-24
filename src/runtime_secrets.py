"""Bridge Replit Secrets into Streamlit's native in-memory secrets store."""

import os

import streamlit as st


def configure_replit_secrets():
    """Run at startup; never write, log, return, or session-cache the credential.

    Replit injects secrets as environment variables. Streamlit 1.66.1 supplies a
    thread-safe programmatic merge API, so clients can read only st.secrets.
    Capture the injected value before loading file-based secrets, which can
    promote their own values to the environment.
    """
    injected_key = os.environ.get("GEMINI_API_KEY")
    if isinstance(injected_key, str) and injected_key.strip():
        st.secrets.load_if_toml_exists()
        st.secrets.merge_programmatic_secrets({"GEMINI_API_KEY": injected_key})
