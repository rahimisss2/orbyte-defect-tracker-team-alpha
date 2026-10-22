"""The HTML audit presentation must not interpret record data as markup."""

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from audit_ui import render_audit_records


class AuditPresentationTests(unittest.TestCase):
    def test_escapes_record_fields_and_allowlists_badge_classes(self):
        with patch("audit_ui.st.markdown") as markdown:
            render_audit_records([{
                "Claim ID": "CLM-123",
                "Supplier": '<script>alert("unsafe")</script>',
                "Decision": 'Pending review" onclick="unsafe',
                "Authorized by": "<b>Not markup</b>",
            }])
            markup = markdown.call_args.args[0]
            self.assertNotIn("<script>", markup)
            self.assertNotIn("<b>Not markup</b>", markup)
            self.assertIn("&lt;script&gt;", markup)
            self.assertIn("&quot; onclick=&quot;unsafe", markup)
            self.assertIn('<span class="orbyte-audit__badge">', markup)
            self.assertTrue(markdown.call_args.kwargs["unsafe_allow_html"])
