"""Native Streamlit manager recommendation layer, isolated per incident/session."""

import streamlit as st

from ai_review import (
    AIReviewError, MODEL, context_fingerprint, generate_review,
    incident_context, insert_paragraph,
)


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


def render_ai_panel(claim, claims):
    claim_id = claim["id"]
    context = incident_context(claim, claims)
    fingerprint = context_fingerprint(context)
    review_key = f"ai_review_{claim_id}"
    with st.container(key=f"ai-context-{claim_id}", border=True):
        st.markdown("#### Context-Aware AI Recommendation")
        st.caption(
            f"Live Gemini · {MODEL} · Clicking Generate sends this incident's supplier, "
            "item, notes and loss metrics to Google. No signature or supplier email is sent."
        )
        if st.button("Generate AI Contextual Review", key=f"generate_ai_{claim_id}"):
            with st.spinner("Analyzing supplier risk and claim context…"):
                try:
                    result = generate_review(context)
                except AIReviewError as error:
                    st.error(str(error))
                else:
                    st.session_state[review_key] = result.model_dump()
                    st.session_state[f"ai_context_{claim_id}"] = fingerprint
        result = st.session_state.get(review_key)
        if result:
            stale = st.session_state.get(f"ai_context_{claim_id}") != fingerprint
            if stale:
                st.warning("Incident or exposure metrics have changed. Generate a new review before inserting it.")
            st.markdown("**Business risk assessment**")
            st.text(result["risk_assessment"])
            st.markdown(f"**Urgency: {result['urgency']} · {result['recommendation']}**")
            st.text(result["rationale"])
            st.markdown("**Suggested claim paragraph**")
            st.text(result["claim_paragraph"])
            st.button(
                "Insert AI paragraph into draft", key=f"insert_ai_{claim_id}",
                disabled=stale, on_click=apply_ai_paragraph,
                args=(claim_id, claim.get("letter", "")),
            )
            if error := st.session_state.get(f"ai_insert_error_{claim_id}"):
                st.error(error)
        st.caption(
            "AI advice may be inaccurate. Verify the evidence and edit the draft before signing. "
            "Generating or inserting advice does not authorize a claim or change its recorded value."
        )
