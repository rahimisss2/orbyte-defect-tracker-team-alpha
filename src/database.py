"""Local JSON persistence shared by every Orbyte page."""

import copy
import fcntl
import json
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from uuid import uuid4

DB_FILE = Path(__file__).resolve().parents[1] / "synthetic_db.json"
INITIAL_DATA = {
    "suppliers": [
        {"name": "Pak Ali Eggs Enterprise", "item": "Grade A Eggs (Per Board)", "cost": 15, "email": "pakali@supplier.com"},
        {"name": "Marigold Dairy Corp", "item": "Fresh Milk Box (Per Crate)", "cost": 45, "email": "accounts@marigold.com"},
        {"name": "Gombak Veggie WholeSale", "item": "Fresh Mustard Greens (Per KG)", "cost": 8.5, "email": "sales@gombakveggie.com"},
    ],
    "claims": [],
}


def _write_database(data):
    """Replace atomically so interrupted writes cannot truncate the database."""
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=DB_FILE.parent, delete=False) as temporary:
            temporary_path = Path(temporary.name)
            json.dump(data, temporary, ensure_ascii=False, indent=2)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_path, DB_FILE)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


@contextmanager
def _locked_database():
    # A separate lock file remains stable across atomic database replacements.
    with DB_FILE.with_suffix(".json.lock").open("a", encoding="utf-8") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            if not DB_FILE.exists():
                _write_database(copy.deepcopy(INITIAL_DATA))
            data = json.loads(DB_FILE.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or not isinstance(data.get("suppliers"), list) or not isinstance(data.get("claims"), list):
                raise ValueError("The local database has an invalid structure. Existing records have not been replaced.")
            yield data
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def read_database():
    with _locked_database() as data:
        return data


def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def amount(value):
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def claim_letter(supplier, quantity, notes, loss):
    return "\n".join([
        f"Dear Accounts Team at {supplier['name']},",
        "",
        "We are writing to report a delivery discrepancy from a recent order.",
        f"Our floor team recorded {quantity} unit{'' if quantity == 1 else 's'} of {supplier['item']} as defective.",
        f"Incident notes: {notes}" if notes else "",
        "",
        f"We request a credit note for RM {loss:.2f} to be reviewed against the upcoming invoice settlement.",
        "",
        "Please confirm receipt and verify this adjustment with your delivery team.",
        "",
        "Best regards,",
        "Manager, Orbyte Retail Hub Network",
    ])


def create_claim(supplier_name, quantity, notes):
    if isinstance(quantity, bool) or not isinstance(quantity, int) or not 1 <= quantity <= 100_000:
        raise ValueError("Quantity must be a whole number from 1 to 100,000.")
    notes = notes.strip() if isinstance(notes, str) else ""
    if not notes or len(notes) > 5_000:
        raise ValueError("Incident notes must contain 1 to 5,000 characters.")
    with _locked_database() as data:
        supplier = next((entry for entry in data["suppliers"] if entry["name"] == supplier_name), None)
        if supplier is None:
            raise ValueError("Choose a valid supplier.")
        loss = float(amount(Decimal(str(supplier["cost"])) * quantity))
        claim = {
            "id": str(uuid4()),
            "supplier": supplier["name"],
            "item": supplier["item"],
            "quantity": quantity,
            "unitCost": supplier["cost"],
            "loss": loss,
            "notes": notes,
            "letter": claim_letter(supplier, quantity, notes, loss),
            "status": "pending_review",
            "createdAt": timestamp(),
        }
        data["claims"].insert(0, claim)
        _write_database(data)
        return claim


def authorize_claim(claim_id, authorized_by, final_letter):
    authorized_by = authorized_by.strip() if isinstance(authorized_by, str) else ""
    final_letter = final_letter.strip() if isinstance(final_letter, str) else ""
    if not authorized_by or len(authorized_by) > 160:
        raise ValueError("Enter the manager's full name (160 characters or fewer).")
    if not final_letter or len(final_letter) > 10_000:
        raise ValueError("The reviewed letter must contain 1 to 10,000 characters.")
    with _locked_database() as data:
        claim = next((entry for entry in data["claims"] if entry["id"] == claim_id), None)
        if claim is None:
            raise ValueError("Claim not found.")
        if claim["status"] != "pending_review":
            raise ValueError("This claim has already been authorized.")
        claim.update(
            status="authorized_demo",
            authorizedBy=authorized_by,
            authorizedAt=timestamp(),
            finalLetter=final_letter,
        )
        _write_database(data)
        return claim


def summarize(claims):
    pending = [claim for claim in claims if claim["status"] == "pending_review"]
    authorized = [claim for claim in claims if claim["status"] == "authorized_demo"]
    return {
        "total_count": len(claims),
        "pending_count": len(pending),
        "authorized_count": len(authorized),
        "total_value": sum((amount(claim["loss"]) for claim in claims), Decimal("0.00")),
        "pending_value": sum((amount(claim["loss"]) for claim in pending), Decimal("0.00")),
        "authorized_value": sum((amount(claim["loss"]) for claim in authorized), Decimal("0.00")),
    }
