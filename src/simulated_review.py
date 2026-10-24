"""Deterministic demo assistance, never presented as live generative AI."""

from decimal import Decimal

from ai_review import ContextualReview
from database import amount


def simulate_review(context):
    """Demo heuristics, not production claims policy or an approval decision."""
    incident = context["incident"]
    supplier = context["supplier_metrics"]
    loss = amount(incident["financial_loss"])
    pending = amount(supplier["pending_exposure"])
    total = amount(supplier["total_recorded_loss"])
    count = supplier["recorded_incidents"]
    supplier_name = str(incident["supplier_name"])[:200]
    item_name = str(incident["item"])[:200]
    notes = incident.get("incident_notes", "").casefold()
    safety_flag = any(term in notes for term in (
        "expired", "contaminated", "mould", "mold", "spoiled", "rotten",
    ))

    if safety_flag:
        urgency, recommendation = "Critical", "Full Refund"
        rule = (
            "The notes contain a potential food-safety keyword. This is an unverified "
            "text flag, not a confirmed safety finding; inspect the evidence immediately."
        )
    elif loss >= Decimal("500") or (count >= 3 and pending >= Decimal("250")):
        urgency, recommendation = "High", "Full Refund"
        rule = (
            "Demo rule: incident loss is at least RM 500, or at least three recorded "
            "supplier incidents have combined pending exposure of RM 250 or more."
        )
    elif loss >= Decimal("100") or count >= 3:
        urgency, recommendation = "Medium", "Partial Claim"
        rule = (
            "Demo rule: incident loss is at least RM 100 or the supplier has at least "
            "three recorded incidents. Verify the recoverable amount before proposing a partial credit."
        )
    else:
        urgency, recommendation = "Low", "Supplier Warning"
        rule = (
            "Demo rule: below the financial and recurrence escalation thresholds. "
            "Request corrective action while preserving the recorded claim for manager review."
        )

    action = {
        "Full Refund": f"Please review a full credit or refund of the recorded RM {loss:.2f}, subject to verification.",
        "Partial Claim": "Please review a proportionate credit after verifying the affected stock and recoverable value; no partial amount has been calculated.",
        "Supplier Warning": "Please investigate this discrepancy and propose corrective action, with any credit adjustment remaining subject to verification.",
    }[recommendation]
    return ContextualReview(
        risk_assessment=(
            f"For supplier {supplier_name}, the incident records {incident['affected_quantity']} affected units and RM {loss:.2f} "
            f"in loss. This supplier has {count} recorded incidents totalling RM {total:.2f}, "
            f"with RM {pending:.2f} pending exposure. These are logged losses, not recovered funds. "
            "Delivery volume and supporting evidence are not available here, so a defect rate "
            "or confirmed supplier fault cannot be established. "
            + ("The notes contain a possible safety concern requiring verification." if safety_flag else
               "Review the incident notes and delivery evidence before deciding liability.")
        ),
        urgency=urgency,
        recommendation=recommendation,
        rationale=rule + " This is a simulated recommendation; the manager makes the final decision.",
        claim_paragraph=(
            f"Our records show {incident['affected_quantity']} affected units of {item_name} "
            f"from {supplier_name}, with a recorded discrepancy value of RM {loss:.2f}. "
            f"{action} Please check the incident notes against your delivery records and "
            "confirm the appropriate resolution with our team."
        ),
    )
