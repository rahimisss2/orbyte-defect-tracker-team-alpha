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
        with patch.object(ai_review.st, "secrets", {"GEMINI_API_KEY": "test-only"}), patch.dict(os.environ, {"GEMINI_API_KEY": "environment-test-only"}):
            self.assertEqual(ai_review.get_api_key(), "test-only")
        with patch.object(ai_review.st, "secrets") as secrets, patch.dict(os.environ, {"GEMINI_API_KEY": "env-test-only"}):
            secrets.__getitem__.side_effect = FileNotFoundError("No Streamlit secrets file")
            with self.assertRaisesRegex(ai_review.AIReviewError, "not configured"):
                ai_review.get_api_key()
        with patch.object(ai_review.st, "secrets", {}), patch.dict(os.environ, {"GEMINI_API_KEY": "env-test-only"}):
            with self.assertRaisesRegex(ai_review.AIReviewError, "not configured"):
                ai_review.get_api_key()
        for invalid in ("", "   ", None, 123):
            with self.subTest(invalid=invalid), patch.object(ai_review.st, "secrets", {"GEMINI_API_KEY": invalid}):
                with self.assertRaises(ai_review.AIReviewError):
                    ai_review.get_api_key()
        with patch.object(ai_review.st, "secrets", {}), patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ai_review.AIReviewError, "not configured"):
                ai_review.generate_review({})

    def test_calls_requested_model_with_schema(self):
        with patch.object(ai_review, "get_api_key", return_value="test-only"), patch.object(ai_review.genai, "Client") as client:
            generate = client.return_value.__enter__.return_value.models.generate_content
            generate.return_value = SimpleNamespace(text=json.dumps(REVIEW))
            result = ai_review.generate_review({"incident": {"supplier_name": "Test"}})
            self.assertEqual(result.model_dump(), REVIEW)
            self.assertEqual(generate.call_args.kwargs["model"], "gemini-flash-latest")
            schema = generate.call_args.kwargs["config"].response_schema
            self.assertEqual(schema, ai_review.RESPONSE_SCHEMA)
            self.assertEqual(set(schema.required), set(REVIEW))
            self.assertIsNone(schema.additional_properties)
            self.assertIsNone(schema.properties["claim_paragraph"].max_length)
            self.assertEqual(schema.properties["urgency"].enum, ["Low", "Medium", "High", "Critical"])
            self.assertEqual(client.call_args.kwargs["http_options"].timeout, 60_000)

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

    def test_gateway_timeout_is_safe_and_not_automatically_retried(self):
        with patch.object(ai_review, "get_api_key", return_value="test-only"), patch.object(ai_review.genai, "Client") as client:
            generate = client.return_value.__enter__.return_value.models.generate_content
            generate.side_effect = ai_review.errors.ServerError(
                504, {"error": {"message": "sensitive-provider-message"}}
            )
            with self.assertRaisesRegex(ai_review.AIReviewError, "HTTP 504") as raised:
                ai_review.generate_review({})
            self.assertIsInstance(raised.exception, ai_review.AIGatewayTimeout)
            self.assertNotIn("sensitive-provider-message", str(raised.exception))
            generate.assert_called_once()


class SimulationTests(unittest.TestCase):
    def context(self, loss="25.50", count=1, pending="25.50", notes="Damaged on delivery"):
        return {
            "incident": {
                "supplier_name": "Test supplier", "item": "Vegetables", "affected_quantity": 3,
                "financial_loss": loss, "incident_notes": notes,
            },
            "supplier_metrics": {
                "recorded_incidents": count, "total_recorded_loss": "750.50",
                "pending_exposure": pending,
            },
        }

    def test_demo_rules_are_contextual_and_do_not_invent_partial_amounts(self):
        from simulated_review import simulate_review
        cases = [
            ({}, "Low", "Supplier Warning"),
            ({"loss": "100"}, "Medium", "Partial Claim"),
            ({"loss": "500"}, "High", "Full Refund"),
            ({"count": 3, "pending": "250"}, "High", "Full Refund"),
            ({"count": 3}, "Medium", "Partial Claim"),
            ({"notes": "Expired stock reported"}, "Critical", "Full Refund"),
        ]
        for kwargs, urgency, recommendation in cases:
            with self.subTest(kwargs=kwargs):
                context = self.context(**kwargs)
                original = json.dumps(context, sort_keys=True)
                review = simulate_review(context)
                self.assertEqual((review.urgency, review.recommendation), (urgency, recommendation))
                self.assertIn("simulated recommendation", review.rationale)
                self.assertIn("Test supplier", review.claim_paragraph)
                self.assertEqual(json.dumps(context, sort_keys=True), original)
                if recommendation == "Partial Claim":
                    self.assertIn("no partial amount has been calculated", review.claim_paragraph)

    def test_only_confirmed_504_and_enabled_page_use_fallback(self):
        import ai_panel
        context = self.context()
        with patch.object(ai_panel, "generate_review", side_effect=ai_review.AIGatewayTimeout("HTTP 504")) as generate:
            result, source = ai_panel.request_review(context, allow_simulated_fallback=True)
            self.assertEqual(source, "simulated")
            self.assertIsInstance(result, ai_review.ContextualReview)
            generate.assert_called_once()
            with self.assertRaises(ai_review.AIGatewayTimeout):
                ai_panel.request_review(context, allow_simulated_fallback=False)
        for message in ("Gemini is not configured.", "Invalid response", "Permission denied"):
            with patch.object(ai_panel, "generate_review", side_effect=ai_review.AIReviewError(message)), patch.object(ai_panel, "simulate_review") as simulate:
                with self.assertRaises(ai_review.AIReviewError):
                    ai_panel.request_review(context, allow_simulated_fallback=True)
                simulate.assert_not_called()


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

    def test_504_fallback_stays_labelled_and_can_be_reviewed_inserted_and_signed(self):
        import ai_panel
        claim_id = self.claim["id"]
        original = self.path.read_bytes()
        with patch.object(ai_panel, "generate_review", side_effect=ai_review.AIGatewayTimeout("HTTP 504")) as generate:
            app = self.app()
            app.text_area(key=f"letter_{claim_id}").input("Manager edits.\n\nBest regards,\nManager").run()
            app.button(key=f"generate_ai_{claim_id}").click().run()
            self.assertFalse(app.exception)
            self.assertFalse(app.error)
            self.assertTrue(any("SIMULATED FALLBACK" in item.value for item in app.warning))
            self.assertFalse(any("LIVE GEMINI RESPONSE" in item.value for item in app.caption))
            self.assertEqual(app.session_state[f"ai_source_{claim_id}"], "simulated")
            self.assertEqual(self.path.read_bytes(), original)
            app.button(key=f"insert_ai_{claim_id}").click().run()
            letter = app.text_area(key=f"letter_{claim_id}").value
            self.assertIn("Manager edits.", letter)
            self.assertIn("Gombak Veggie WholeSale", letter)
            self.assertIn("RM 25.50", letter)
            self.assertTrue(any("SIMULATED FALLBACK" in item.value for item in app.warning))
            self.assertEqual(self.path.read_bytes(), original)
            app.button(key=f"authorize_{claim_id}").click().run()
            self.assertTrue(app.error)  # A simulated recommendation cannot bypass eSign.
            app.text_input(key=f"signature_{claim_id}").input("Test Manager").run()
            app.button(key=f"authorize_{claim_id}").click().run()
            self.assertFalse(app.exception)
            approved = database.read_database()["claims"][0]
            self.assertEqual(approved["status"], "authorized_demo")
            self.assertEqual(approved["finalLetter"], letter)
            self.assertEqual(approved["loss"], self.claim["loss"])
            generate.assert_called_once()

    def test_live_success_replaces_simulation_provenance(self):
        import ai_panel
        claim_id = self.claim["id"]
        with patch.object(ai_panel, "generate_review", side_effect=[
            ai_review.AIGatewayTimeout("HTTP 504"), ai_review.ContextualReview(**REVIEW),
        ]):
            app = self.app()
            app.button(key=f"generate_ai_{claim_id}").click().run()
            self.assertEqual(app.session_state[f"ai_source_{claim_id}"], "simulated")
            app.button(key=f"generate_ai_{claim_id}").click().run()
            self.assertEqual(app.session_state[f"ai_source_{claim_id}"], "live")
            self.assertFalse(any("SIMULATED FALLBACK" in item.value for item in app.warning))
            self.assertTrue(any("LIVE GEMINI RESPONSE" in item.value for item in app.caption))


if __name__ == "__main__":
    unittest.main()
