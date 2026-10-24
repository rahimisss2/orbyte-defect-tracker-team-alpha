"""Use inert test fixtures only; never inspect or persist real secrets."""

import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import ai_review
import runtime_secrets
from streamlit.runtime.secrets import Secrets


class RuntimeSecretsTests(unittest.TestCase):
    def test_replit_bridge_enables_strict_native_secret_lookup_without_files(self):
        store = Secrets()
        with patch.dict(os.environ, {"GEMINI_API_KEY": "inert-runtime-fixture"}), \
             patch.object(runtime_secrets.st, "secrets", store), \
             patch.object(store, "load_if_toml_exists", return_value=False), \
             patch("builtins.open", side_effect=AssertionError("No credential files allowed")):
            self.assertIsNone(runtime_secrets.configure_replit_secrets())
            self.assertEqual(ai_review.get_api_key(), "inert-runtime-fixture")
            runtime_secrets.configure_replit_secrets()
            self.assertEqual(store["GEMINI_API_KEY"], "inert-runtime-fixture")

    def test_unset_or_blank_injection_does_not_break_other_pages(self):
        for value in (None, "", "   "):
            with self.subTest(value=value), patch.dict(os.environ, {}, clear=True), \
                 patch.object(runtime_secrets.st, "secrets") as store:
                if value is not None:
                    os.environ["GEMINI_API_KEY"] = value
                runtime_secrets.configure_replit_secrets()
                store.load_if_toml_exists.assert_not_called()
                store.merge_programmatic_secrets.assert_not_called()

    def test_startup_does_not_allow_file_value_to_replace_injected_secret(self):
        store = Secrets()
        def load_file():
            store.merge_programmatic_secrets({
                "GEMINI_API_KEY": "inert-file-fixture", "unrelated_setting": "preserved",
            })
            return True
        with patch.dict(os.environ, {"GEMINI_API_KEY": "inert-runtime-fixture"}), \
             patch.object(runtime_secrets.st, "secrets", store), \
             patch.object(store, "load_if_toml_exists", side_effect=load_file):
            runtime_secrets.configure_replit_secrets()
            self.assertEqual(store["GEMINI_API_KEY"], "inert-runtime-fixture")
            self.assertEqual(store["unrelated_setting"], "preserved")
            self.assertEqual(os.environ["GEMINI_API_KEY"], "inert-runtime-fixture")


if __name__ == "__main__":
    unittest.main()
