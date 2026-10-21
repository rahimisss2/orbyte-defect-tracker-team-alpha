"""Run with python -m unittest discover -s tests -v. Never writes real records."""

import concurrent.futures
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import database
from streamlit.testing.v1 import AppTest


class IsolatedDatabase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.path = Path(self.temporary.name) / "synthetic_db.json"
        self.override = patch.object(database, "DB_FILE", self.path)
        self.override.start()
        database.read_database()

    def tearDown(self):
        self.override.stop()
        self.temporary.cleanup()

    def incident(self):
        return database.create_claim("Gombak Veggie WholeSale", 3, "Three KG damaged during unloading.")


class DatabaseTests(IsolatedDatabase):
    def test_existing_database_is_read_without_reformatting_or_loss(self):
        original = (ROOT / "synthetic_db.json").read_bytes()
        self.path.write_bytes(original)
        data = database.read_database()
        self.assertEqual(data, json.loads(original))
        self.assertEqual(self.path.read_bytes(), original)

    def test_new_workspace_and_claim_calculation(self):
        self.assertEqual(len(database.read_database()["suppliers"]), 3)
        claim = self.incident()
        self.assertEqual(claim["loss"], 25.5)
        self.assertEqual(claim["unitCost"], 8.5)
        self.assertEqual(claim["quantity"], 3)
        self.assertEqual(claim["status"], "pending_review")
        self.assertIn("RM 25.50", claim["letter"])
        self.assertEqual(database.read_database()["claims"][0], claim)
        summary = database.summarize([claim])
        self.assertEqual(summary["pending_count"], 1)
        self.assertEqual(summary["total_value"], database.amount(25.5))

    def test_invalid_incidents_do_not_write_records(self):
        original = self.path.read_bytes()
        for quantity in (None, 0, -1, 1.5, 100_001, True, "3"):
            with self.subTest(quantity=quantity), self.assertRaises(ValueError):
                database.create_claim("Pak Ali Eggs Enterprise", quantity, "Broken.")
        for supplier, notes in (("Unknown supplier", "Broken."), ("Pak Ali Eggs Enterprise", ""), ("Pak Ali Eggs Enterprise", " ")):
            with self.assertRaises(ValueError):
                database.create_claim(supplier, 1, notes)
        with self.assertRaises(ValueError):
            database.create_claim("Pak Ali Eggs Enterprise", 1, "x" * 5_001)
        self.assertEqual(self.path.read_bytes(), original)

    def test_authorization_validation_and_duplicate_protection(self):
        claim = self.incident()
        for signature, letter in (("", claim["letter"]), ("x" * 161, claim["letter"]), ("Test Manager", ""), ("Test Manager", "x" * 10_001)):
            with self.assertRaises(ValueError):
                database.authorize_claim(claim["id"], signature, letter)
        approved = database.authorize_claim(claim["id"], "  Test Manager  ", "  Reviewed credit-note request  ")
        self.assertEqual(approved["authorizedBy"], "Test Manager")
        self.assertEqual(approved["finalLetter"], "Reviewed credit-note request")
        self.assertEqual(approved["status"], "authorized_demo")
        self.assertIn("authorizedAt", approved)
        original = self.path.read_bytes()
        with self.assertRaises(ValueError):
            database.authorize_claim(claim["id"], "Other Manager", "Another letter")
        with self.assertRaises(ValueError):
            database.authorize_claim("not-found", "Test Manager", "Reviewed letter")
        self.assertEqual(self.path.read_bytes(), original)
        summary = database.summarize(database.read_database()["claims"])
        self.assertEqual(summary["pending_count"], 0)
        self.assertEqual(summary["authorized_count"], 1)
        self.assertEqual(summary["authorized_value"], database.amount(25.5))

    def test_simultaneous_submissions_do_not_lose_records(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as workers:
            claims = list(workers.map(lambda _: self.incident(), range(12)))
        saved = database.read_database()["claims"]
        self.assertEqual(len(saved), 12)
        self.assertEqual({claim["id"] for claim in saved}, {claim["id"] for claim in claims})

    def test_corrupt_database_is_not_silently_reset(self):
        self.path.write_text('{"claims":', encoding="utf-8")
        with self.assertRaises(ValueError):
            database.read_database()
        self.assertEqual(self.path.read_text(encoding="utf-8"), '{"claims":')


class StreamlitTests(IsolatedDatabase):
    def test_custom_navigation_and_current_page_replay(self):
        with patch("page_transition.time") as clock:
            sleep = clock.sleep
            app = self.app()
            before = sleep.call_count
            app.button(key="nav_overview").click().run()
            self.assertEqual(app.title[0].value, "Control room")
            self.assertEqual(sleep.call_count - before, 20)
            for screen, filename, title in [
                ("intake", "log_incident", "Log incident"),
                ("audit", "audit_history", "Audit history"),
                ("manager", "manager_dashboard", "Manager dashboard"),
                ("review", "review_authorize", "Review & authorize"),
                ("overview", "control_room", "Control room"),
            ]:
                section = "manager" if screen in ("manager", "review") else "operations"
                app.button(key=f"section_{section}").click().run()
                before = sleep.call_count
                app.button(key=f"nav_{screen}").click().run()
                self.assertFalse(app.exception)
                self.assertEqual(app.title[0].value, title)
                self.assertEqual(sleep.call_count - before, 20)
                app.switch_page(f"screens/{filename}.py").run()
            self.assertEqual(database.read_database()["claims"], [])

    def test_section_switch_shows_only_related_pages_without_leaving_current_page(self):
        app = self.app()
        def visible_page_buttons():
            return {button.key for button in app.button if button.key and button.key.startswith("nav_")}
        self.assertEqual(visible_page_buttons(), {"nav_overview", "nav_intake", "nav_audit"})
        app.button(key="section_manager").click().run()
        self.assertEqual(visible_page_buttons(), {"nav_manager", "nav_review"})
        self.assertEqual(app.title[0].value, "Control room")
        app.run()
        self.assertEqual(visible_page_buttons(), {"nav_manager", "nav_review"})
        app.button(key="nav_manager").click().run()
        self.assertEqual(app.title[0].value, "Manager dashboard")
        app.switch_page("screens/manager_dashboard.py").run()
        app.button(key="section_operations").click().run()
        self.assertEqual(visible_page_buttons(), {"nav_overview", "nav_intake", "nav_audit"})
        self.assertEqual(app.title[0].value, "Manager dashboard")
        app.switch_page("screens/review_authorize.py").run()
        self.assertEqual(visible_page_buttons(), {"nav_manager", "nav_review"})

    def app(self):
        app = AppTest.from_file(str(ROOT / "src/main.py"), default_timeout=20).run()
        self.assertFalse(app.exception)
        return app

    def button(self, app, label):
        return next(button for button in app.button if button.label == label)

    def test_worker_to_manager_to_audit_with_persistent_drafts(self):
        app = self.app()
        self.assertEqual(app.title[0].value, "Control room")
        self.assertEqual(len(app.metric), 4)
        self.button(app, "Log an Incident").click().run()
        self.assertEqual(app.title[0].value, "Log incident")
        self.button(app, "Submit incident").click().run()
        self.assertTrue(app.error)
        self.assertEqual(database.read_database()["claims"], [])
        app.selectbox(key="incident_supplier").select("Gombak Veggie WholeSale").run()
        app.number_input(key="incident_quantity").set_value(3).run()
        app.text_area(key="incident_notes").input("Three KG damaged during unloading.").run()
        self.assertEqual(app.metric[0].value, "RM 25.50")
        app.switch_page("screens/manager_dashboard.py").run()
        self.assertEqual(app.title[0].value, "Manager dashboard")
        self.assertEqual(len(app.metric), 4)
        app.switch_page("screens/log_incident.py").run()
        self.assertEqual(app.number_input(key="incident_quantity").value, 3)
        self.assertEqual(app.text_area(key="incident_notes").value, "Three KG damaged during unloading.")
        self.button(app, "Submit incident").click().run()
        self.assertTrue(app.success)
        self.assertIsNone(app.selectbox(key="incident_supplier").value)
        self.assertIsNone(app.number_input(key="incident_quantity").value)
        self.assertEqual(app.text_area(key="incident_notes").value, "")
        claim = database.read_database()["claims"][0]
        app.switch_page("screens/control_room.py").run()
        self.assertEqual(app.metric[0].value, "01")
        self.assertEqual(app.metric[1].value, "01")
        self.assertEqual(app.metric[3].value, "RM 25.50")
        app.switch_page("screens/manager_dashboard.py").run()
        self.assertEqual(app.metric[1].value, "RM 25.50")
        app.button(key="nav_review").click().run()
        self.assertEqual(app.title[0].value, "Review & authorize")
        self.assertEqual(len(app.metric), 0)
        # Synchronize AppTest's last explicit page request after a shortcut
        # changes the page. Browser navigation maintains this automatically.
        app.switch_page("screens/review_authorize.py").run()
        letter = claim["letter"] + "\nReviewed by test manager."
        app.text_area(key=f"letter_{claim['id']}").input(letter).run()
        self.button(app, "Authorize claim").click().run()
        self.assertTrue(app.error)
        self.assertEqual(database.read_database()["claims"][0]["status"], "pending_review")
        app.switch_page("screens/audit_history.py").run()
        self.assertEqual(len(app.dataframe[0].value), 1)
        app.switch_page("screens/review_authorize.py").run()
        self.assertEqual(app.text_area(key=f"letter_{claim['id']}").value, letter)
        app.text_input(key=f"signature_{claim['id']}").input("Test Manager").run()
        self.button(app, "Authorize claim").click().run()
        self.assertTrue(app.success)
        self.assertEqual(len(app.text_area), 0)
        saved = database.read_database()["claims"][0]
        self.assertEqual(saved["finalLetter"], letter)
        self.assertEqual(saved["authorizedBy"], "Test Manager")
        app.switch_page("screens/manager_dashboard.py").run()
        self.assertEqual([metric.value for metric in app.metric], ["RM 25.50", "RM 0.00", "RM 25.50", "00"])
        app.switch_page("screens/audit_history.py").run()
        self.assertEqual(app.dataframe[0].value.iloc[0]["Authorized by"], "Test Manager")
        self.assertEqual(app.dataframe[0].value.iloc[0]["Decision"], "Authorized · demo")
        self.assertFalse(app.exception)

    def test_empty_review_and_audit_routes(self):
        app = self.app()
        app.switch_page("screens/review_authorize.py").run()
        self.assertEqual(len(app.text_input), 0)
        self.assertTrue(any("queue is clear" in item.value for item in app.success))
        app.switch_page("screens/audit_history.py").run()
        self.assertEqual(len(app.dataframe), 0)
        self.button(app, "Log an incident").click().run()
        self.assertEqual(app.title[0].value, "Log incident")
        self.assertFalse(app.exception)


if __name__ == "__main__":
    unittest.main()
