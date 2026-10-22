"""The five native Streamlit pages, all backed by the same local claim records."""

import logging
from datetime import datetime
from decimal import Decimal

import streamlit as st

from database import amount, authorize_claim, create_claim, summarize


def rm(value):
    return f"RM {value:.2f}"


def claim_label(claim_id):
    return f"CLM-{claim_id[:8].upper()}"


def display_date(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d %b %Y, %H:%M UTC")
    except (TypeError, AttributeError, ValueError):
        return "Date unavailable"


def metric_cards(cards):
    with st.container(key="kpi-grid"):
        for column, (label, value, description) in zip(st.columns(4, gap="small"), cards):
            with column:
                st.metric(label, value)
                st.caption(description)


def control_room():
    stats = summarize(st.session_state["database"]["claims"])
    if st.button("Log an Incident", type="primary", icon=":material/add:"):
        st.switch_page("screens/log_incident.py")
    metric_cards([
        ("ALL CLAIMS", f"{stats['total_count']:02}", "Incidents in this workspace"),
        ("AWAITING REVIEW", f"{stats['pending_count']:02}", "Active pending discrepancies"),
        ("AUTHORIZED · DEMO", f"{stats['authorized_count']:02}", "Manager decisions recorded"),
        ("CLAIMED VALUE", rm(stats["total_value"]), "Total incident value logged"),
    ])


def submit_incident():
    try:
        claim = create_claim(
            st.session_state.get("incident_supplier"),
            st.session_state.get("incident_quantity"),
            st.session_state.get("incident_notes", ""),
        )
    except ValueError as error:
        st.session_state["flash"] = ("error", str(error))
    except OSError:
        logging.exception("Could not save incident")
        st.session_state["flash"] = ("error", "Incident could not be saved. Please try again.")
    else:
        st.session_state["incident_supplier"] = None
        st.session_state["incident_quantity"] = None
        st.session_state["incident_notes"] = ""
        st.session_state["flash"] = (
            "success",
            f"Incident {claim_label(claim['id'])} submitted. It is now waiting for manager review.",
        )


def log_incident():
    st.caption("Floor Worker Portal — record defective deliveries for manager review.")
    suppliers = st.session_state["database"]["suppliers"]
    with st.container(key="incident-form-panel", border=True):
        st.subheader("Log a delivery discrepancy")
        st.caption("Keep the original details. The manager can refine the claim letter.")
        supplier_name = st.selectbox(
            "Supplier", [entry["name"] for entry in suppliers],
            index=None, placeholder="Choose a supplier…", key="incident_supplier",
            persist_state="session", disabled=not suppliers,
        )
        supplier = next((entry for entry in suppliers if entry["name"] == supplier_name), None)
        if supplier:
            st.caption(f"{supplier['item']} · {rm(supplier['cost'])} / unit")
        elif not suppliers:
            st.warning("No suppliers are available in the local database.")
        quantity_column, estimate_column = st.columns(2)
        with quantity_column:
            quantity = st.number_input(
                "Affected quantity", min_value=1, max_value=100_000, value=None, step=1,
                placeholder="Units, e.g. 6", key="incident_quantity", persist_state="session",
            )
        with estimate_column:
            estimate = amount(Decimal(str(supplier["cost"])) * quantity) if supplier and quantity else Decimal("0.00")
            st.metric("Estimated loss", rm(estimate))
        st.text_area(
            "Raw incident notes", placeholder="Describe what happened in your own words…",
            height=140, max_chars=5_000, key="incident_notes", persist_state="session",
        )
        st.button(
            "Submit incident", type="primary", icon=":material/arrow_outward:",
            on_click=submit_incident, disabled=not suppliers,
        )


def manager_dashboard():
    stats = summarize(st.session_state["database"]["claims"])
    st.caption("Financial exposure and active discrepancy counts, calculated from the same claim records.")
    if st.button("Review & Authorisation", type="primary", icon=":material/arrow_outward:"):
        st.switch_page("screens/review_authorize.py")
    metric_cards([
        ("TOTAL CASH LEAKS", rm(stats["total_value"]), "Recorded defect losses across all claims"),
        ("PENDING EXPOSURE", rm(stats["pending_value"]), "Losses awaiting manager authorization"),
        ("AUTHORIZED VALUE · DEMO", rm(stats["authorized_value"]), "Approved locally, not recovered funds"),
        ("ACTIVE DISCREPANCIES", f"{stats['pending_count']:02}", "Pending claims requiring a decision"),
    ])


def record_authorization(claim_id):
    try:
        authorize_claim(
            claim_id,
            st.session_state.get(f"signature_{claim_id}", ""),
            st.session_state.get(f"letter_{claim_id}", ""),
        )
    except ValueError as error:
        st.session_state["flash"] = ("error", str(error))
    except OSError:
        logging.exception("Could not save authorization")
        st.session_state["flash"] = ("error", "Authorization could not be recorded. Please try again.")
    else:
        st.session_state.pop(f"signature_{claim_id}", None)
        st.session_state.pop(f"letter_{claim_id}", None)
        st.session_state["flash"] = ("success", "Manager authorization recorded locally for demo purposes only.")


def review_authorize():
    st.caption("Manager workspace — inspect the incident, edit the claim draft, then sign and authorize.")
    pending = sorted(
        (claim for claim in st.session_state["database"]["claims"] if claim["status"] == "pending_review"),
        key=lambda claim: claim["createdAt"], reverse=True,
    )
    if not pending:
        st.success("Review queue is clear.")
        st.caption("New floor incidents will appear here before any decision is recorded.")
        if st.button("Log an incident", icon=":material/add:"):
            st.switch_page("screens/log_incident.py")
        return
    st.subheader("Pending discrepancies")
    for claim in pending:
        with st.container(key=f"review-claim-{claim['id']}", border=True):
            st.subheader(claim_label(claim["id"]))
            st.caption(f"Submitted {display_date(claim['createdAt'])} · Pending review")
            facts, draft = st.columns([1, 1.5], gap="large")
            with facts:
                st.caption("SUPPLIER")
                st.text(claim["supplier"])
                st.caption("ITEM / UNIT COST")
                st.text(f"{claim['item']} · {rm(claim['unitCost'])}")
                st.caption("QUANTITY / CLAIMED VALUE")
                st.text(f"{claim['quantity']} units · {rm(claim['loss'])}")
                st.caption("FLOOR WORKER NOTES")
                st.text(claim["notes"] or "No additional notes.")
            with draft:
                st.text_area(
                    "Claim letter draft", value=claim.get("letter", ""),
                    height=310, max_chars=10_000, key=f"letter_{claim['id']}", persist_state="session",
                    help="Template-generated draft, editable before authorization. No external AI service is connected.",
                )
            st.text_input(
                "eSign · Manager full name", max_chars=160, key=f"signature_{claim['id']}",
                placeholder="Manager full name", persist_state="session",
            )
            st.caption("Authorization is recorded locally for demo purposes only.")
            st.button(
                "Authorize claim", type="primary", key=f"authorize_{claim['id']}",
                icon=":material/arrow_outward:", on_click=record_authorization, args=(claim["id"],),
            )


def audit_history():
    st.caption("The complete live audit trail, available to all operations staff.")
    claims = sorted(st.session_state["database"]["claims"], key=lambda claim: claim["createdAt"], reverse=True)
    st.subheader("Audit history")
    with st.container(key="audit-filters", border=True):
        search_column, status_column = st.columns([2, 1])
        with search_column:
            search = st.text_input(
                "Search claims", placeholder="Supplier, claim ID or item…",
                key="audit_search", persist_state="session",
            ).strip().casefold()
        with status_column:
            decision = st.selectbox(
                "Decision", ["All statuses", "Pending review", "Authorized · demo"],
                key="audit_decision", persist_state="session",
            )
        if search or decision != "All statuses":
            st.button("Clear filters", key="audit_clear", on_click=clear_audit_filters)

    if not claims:
        st.caption("0 RECORDS · Pending review / Authorized · demo")
        st.info("Nothing to audit yet. Submitted and authorized claims will be recorded here.")
        if st.button("Log an incident", icon=":material/add:"):
            st.switch_page("screens/log_incident.py")
        return

    visible_claims = [
        claim for claim in claims
        if (
            not search or any(
                search in str(value).casefold()
                for value in (claim["supplier"], claim["item"], claim_label(claim["id"]))
            )
        ) and (
            decision == "All statuses"
            or (decision == "Pending review" and claim["status"] == "pending_review")
            or (decision == "Authorized · demo" and claim["status"] == "authorized_demo")
        )
    ]
    st.caption(f"SHOWING {len(visible_claims)} OF {len(claims)} RECORDS · Pending review / Authorized · demo")
    if not visible_claims:
        st.info("No claims match these filters. Try another supplier, claim ID, item or decision.")
        return
    rows = [{
        "Claim ID": claim_label(claim["id"]),
        "Created": display_date(claim["createdAt"]),
        "Supplier": claim["supplier"],
        "Item": claim["item"],
        "Qty": claim["quantity"],
        "Claimed value": rm(claim["loss"]),
        "Decision": "Authorized · demo" if claim["status"] == "authorized_demo" else "Pending review",
        "Authorized by": claim.get("authorizedBy", "—"),
    } for claim in visible_claims]
    from audit_ui import render_audit_records

    render_audit_records(rows)
    with st.expander("Interactive table · sort and download"):
        st.dataframe(rows, hide_index=True, width="stretch")


def clear_audit_filters():
    st.session_state["audit_search"] = ""
    st.session_state["audit_decision"] = "All statuses"
