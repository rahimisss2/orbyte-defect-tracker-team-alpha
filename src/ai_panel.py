"""Native Streamlit manager recommendation layer, isolated per incident/session."""

import streamlit as st

from ai_review import (
    AIGatewayTimeout, AIReviewError, MODEL, context_fingerprint, generate_review,
    incident_context, insert_paragraph,
)
from simulated_review import simulate_review


def request_review(context, *, allow_simulated_fallback=False):
    """Never mask missing credentials, invalid responses, or non-504 failures."""
    try:
        return generate_review(context), "live"
    except AIGatewayTimeout:
        if not allow_simulated_fallback:
            raise
        return simulate_review(context), "simulated"


def apply_ai_paragraph(claim_id, original_letter):
    review = st.session_state.get(f"ai_review_{claim_id}")
    if not review:
        return
    try:
        st.session_state[f"letter_{claim_id}"] = insert_paragraph(
            st.session_state.get(f"letter_{claim_id}", original_letter),
            review["claim_paragraph"],
            st.session_state.get(f"ai_inserted_{claim_id}", ""),
        )
    except AIReviewError as error:
        st.session_state[f"ai_insert_error_{claim_id}"] = str(error)
    else:
        st.session_state[f"ai_inserted_{claim_id}"] = review["claim_paragraph"]
        st.session_state.pop(f"ai_insert_error_{claim_id}", None)


def render_ai_panel(claim, claims, *, allow_simulated_fallback=False):
    claim_id = claim["id"]
    context = incident_context(claim, claims)
    fingerprint = context_fingerprint(context)
    review_key = f"ai_review_{claim_id}"
    with st.container(key=f"ai-context-{claim_id}", border=True):
        st.markdown("#### Context-Aware AI Recommendation")
        st.caption(
            f"Gemini · {MODEL} · Clicking Generate sends this incident's supplier, "
            "item, notes and loss metrics to Google. No signature or supplier email is sent."
        )
        if allow_simulated_fallback:
            st.caption("If Gemini returns HTTP 504, a clearly labelled simulated rules-based review will be shown instead.")
        if st.button("Generate AI Contextual Review", key=f"generate_ai_{claim_id}"):
            with st.spinner("Analyzing supplier risk and claim context…"):
                try:
                    result, source = request_review(
                        context, allow_simulated_fallback=allow_simulated_fallback,
                    )
                except AIReviewError as error:
                    st.error(str(error))
                else:
                    st.session_state[review_key] = result.model_dump()
                    st.session_state[f"ai_context_{claim_id}"] = fingerprint
                    st.session_state[f"ai_source_{claim_id}"] = source
        result = st.session_state.get(review_key)
        if result:
            simulated = st.session_state.get(f"ai_source_{claim_id}") == "simulated"
            if simulated:
                st.warning(
                    "SIMULATED FALLBACK · Gemini returned HTTP 504. This is deterministic "
                    "rules-based demo assistance, NOT live generative AI. Manager review is required."
                )
            else:
                st.caption(f"LIVE GEMINI RESPONSE · {MODEL}")
            stale = st.session_state.get(f"ai_context_{claim_id}") != fingerprint
            if stale:
                st.warning("Incident or exposure metrics have changed. Generate a new review before inserting it.")
            st.markdown("**Business risk assessment**")
            st.text(result["risk_assessment"])
            st.markdown(f"**Urgency: {result['urgency']} · {result['recommendation']}**")
            st.text(result["rationale"])
            st.markdown("**Suggested claim paragraph**")
            st.text(result["claim_paragraph"])
            if st.button(
                "Insert simulated paragraph into draft" if simulated else "Insert AI paragraph into draft",
                key=f"insert_ai_{claim_id}",
                disabled=stale,
            ):
                # This panel renders before the draft widget. Save its keyed
                # state now, then send a fresh render to the browser immediately.
                apply_ai_paragraph(claim_id, claim.get("letter", ""))
                st.rerun()
            if error := st.session_state.get(f"ai_insert_error_{claim_id}"):
                st.error(error)
        st.caption(
            "AI advice may be inaccurate. Verify the evidence and edit the draft before signing. "
            "Generating or inserting advice does not authorize a claim or change its recorded value."
        )
