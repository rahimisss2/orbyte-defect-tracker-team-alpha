"""AI tests use mocks and temporary databases; never call Google."""

import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import ai_review
import database
from streamlit.testing.v1 import AppTest

REVIEW = {
    "risk_assessment": "Repeated damaged stock may increase supplier leakage; delivery volume is unknown.",
    "urgency": "High",
    "recommendation": "Full Refund",
    "rationale": "Review the documented loss promptly, subject to delivery evidence.",
    "claim_paragraph": "Please review the three damaged units and the recorded RM 25.50 adjustment against your delivery evidence.",
}


class ReviewServiceTests(unittest.TestCase):
    def test_secure_credentials_and_missing_key(self):
        with patch.object(ai_review.st, "secrets", {"GEMINI_API_KEY": "test-only"}):
            self.assertEqual(ai_review.get_api_key(), "test-only")
        with patch.object(ai_review.st, "secrets", {}), patch.dict(os.environ, {"GEMINI_API_KEY": "env-test-only"}):
            self.assertEqual(ai_review.get_api_key(), "env-test-only")
        with patch.object(ai_review.st, "secrets", {}), patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ai_review.AIReviewError, "not configured"):
                ai_review.generate_review({})

    def test_calls_requested_model_with_schema(self):
        with patch.object(ai_review, "get_api_key", return_value="test-only"), patch.object(ai_review.genai, "Client") as client:
            generate = client.return_value.__enter__.return_value.models.generate_content
            generate.return_value = SimpleNamespace(text=json.dumps(REVIEW))
            result = ai_review.generate_review({"incident": {"supplier_name": "Test"}})
            self.assertEqual(result.model_dump(), REVIEW)
            self.assertEqual(generate.call_args.kwargs["model"], "gemini-2.5-flash")
            schema = generate.call_args.kwargs["config"].response_schema
            self.assertEqual(schema, ai_review.RESPONSE_SCHEMA)
            self.assertEqual(set(schema.required), set(REVIEW))
            self.assertIsNone(schema.additional_properties)
            self.assertIsNone(schema.properties["claim_paragraph"].max_length)
            self.assertEqual(schema.properties["urgency"].enum, ["Low", "Medium", "High", "Critical"])
            self.assertEqual(client.call_args.kwargs["http_options"].timeout, 20_000)

    def test_invalid_and_failed_responses_are_sanitized(self):
        with patch.object(ai_review, "get_api_key", return_value="test-only"), patch.object(ai_review.genai, "Client") as client:
            generate = client.return_value.__enter__.return_value.models.generate_content
            generate.return_value = SimpleNamespace(text='{"urgency":"Unknown"}')
            with self.assertRaisesRegex(ai_review.AIReviewError, "invalid review"):
                ai_review.generate_review({})
            generate.side_effect = RuntimeError("sensitive-provider-message")
            with self.assertRaises(ai_review.AIReviewError) as raised:
                ai_review.generate_review({})
            self.assertNotIn("sensitive-provider-message", str(raised.exception))

    def test_paragraph_insertion_preserves_edits_and_is_idempotent(self):
        letter = "Manager's own edits.\n\nBest regards,\nManager"
        updated = ai_review.insert_paragraph(letter, REVIEW["claim_paragraph"])
        self.assertTrue(updated.startswith("Manager's own edits."))
        self.assertLess(updated.index(REVIEW["claim_paragraph"]), updated.index("Best regards,"))
        self.assertEqual(ai_review.insert_paragraph(updated, REVIEW["claim_paragraph"]), updated)
        revised = ai_review.insert_paragraph(updated, "Revised paragraph.", REVIEW["claim_paragraph"])
        self.assertNotIn(REVIEW["claim_paragraph"], revised)
        with self.assertRaises(ai_review.AIReviewError):
            ai_review.insert_paragraph("x" * 9999, "Too long")

    def test_retired_model_is_reported_without_provider_payload(self):
        with patch.object(ai_review, "get_api_key", return_value="test-only"), patch.object(ai_review.genai, "Client") as client:
            generate = client.return_value.__enter__.return_value.models.generate_content
            generate.side_effect = ai_review.errors.ClientError(
                404, {"error": {"message": "Model no longer available; sensitive-provider-message"}}
            )
            with self.assertRaisesRegex(ai_review.AIReviewError, "no longer available") as raised:
                ai_review.generate_review({})
            self.assertNotIn("sensitive-provider-message", str(raised.exception))


class ReviewWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.path = Path(self.temporary.name) / "synthetic_db.json"
        self.override = patch.object(database, "DB_FILE", self.path)
        self.override.start()
        database.read_database()
        self.claim = database.create_claim("Gombak Veggie WholeSale", 3, "Three KG damaged during unloading.")

    def tearDown(self):
        self.override.stop()
        self.temporary.cleanup()

    def app(self):
        app = AppTest.from_file(str(ROOT / "src/main.py"), default_timeout=20).run()
        return app.switch_page("screens/review_authorize.py").run()

    def test_context_is_minimal_and_metrics_are_real(self):
        approved = database.create_claim("Gombak Veggie WholeSale", 2, "Different private notes")
        database.authorize_claim(approved["id"], "Private Signature", "Reviewed")
        context = ai_review.incident_context(self.claim, database.read_database()["claims"])
        self.assertEqual(context["incident"]["financial_loss"], "25.50")
        self.assertEqual(context["supplier_metrics"]["total_recorded_loss"], "42.50")
        self.assertEqual(context["supplier_metrics"]["pending_exposure"], "25.50")
        serialized = json.dumps(context)
        self.assertNotIn("Private Signature", serialized)
        self.assertNotIn("Different private notes", serialized)
        self.assertNotIn("@", serialized)

    def test_generate_insert_edit_sign_and_authorize(self):
        import ai_panel
        claim_id = self.claim["id"]
        original = self.path.read_bytes()
        with patch.object(ai_panel, "generate_review", return_value=ai_review.ContextualReview(**REVIEW)) as generate:
            app = self.app()
            generate.assert_not_called()
            app.text_area(key=f"letter_{claim_id}").input("Manager edit.\n\nBest regards,\nManager").run()
            app.button(key=f"generate_ai_{claim_id}").click().run()
            generate.assert_called_once()
            self.assertEqual(self.path.read_bytes(), original)
            self.assertEqual(app.text_area(key=f"letter_{claim_id}").value, "Manager edit.\n\nBest regards,\nManager")
            self.assertTrue(any("Context-Aware AI Recommendation" in item.value for item in app.markdown))
            app.button(key=f"insert_ai_{claim_id}").click().run()
            self.assertIn(REVIEW["claim_paragraph"], app.text_area(key=f"letter_{claim_id}").value)
            app.button(key=f"insert_ai_{claim_id}").click().run()
            self.assertEqual(app.text_area(key=f"letter_{claim_id}").value.count(REVIEW["claim_paragraph"]), 1)
            self.assertEqual(self.path.read_bytes(), original)
            app.button(key=f"authorize_{claim_id}").click().run()
            self.assertTrue(app.error)  # Signature remains mandatory.
            app.text_input(key=f"signature_{claim_id}").input("Test Manager").run()
            app.button(key=f"authorize_{claim_id}").click().run()
            self.assertFalse(app.exception)
            approved = database.read_database()["claims"][0]
            self.assertEqual(approved["status"], "authorized_demo")
            self.assertIn(REVIEW["claim_paragraph"], approved["finalLetter"])
            self.assertEqual(approved["loss"], self.claim["loss"])
            generate.assert_called_once()

    def test_missing_credentials_keeps_draft_and_database_unchanged(self):
        import ai_panel
        original = self.path.read_bytes()
        with patch.object(ai_panel, "generate_review", side_effect=ai_review.AIReviewError("Gemini is not configured.")):
            app = self.app()
            app.button(key=f"generate_ai_{self.claim['id']}").click().run()
            self.assertTrue(app.error)
            self.assertFalse(app.exception)
            self.assertEqual(self.path.read_bytes(), original)
            self.assertEqual(app.text_area(key=f"letter_{self.claim['id']}").value, self.claim["letter"])
            self.assertTrue(app.button(key=f"authorize_{self.claim['id']}"))


if __name__ == "__main__":
    unittest.main()
