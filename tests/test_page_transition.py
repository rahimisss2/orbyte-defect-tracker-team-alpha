"""Keep the entrance indicator brief and independent of business state."""

import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from page_transition import show_page_transition


class PageTransitionTests(unittest.TestCase):
    def test_navigation_animates_once_and_widget_reruns_do_not_delay(self):
        with patch("page_transition.st") as streamlit, patch("page_transition.time.sleep") as sleep:
            streamlit.session_state = {"existing_draft": "Keep this draft"}
            show_page_transition("")
            self.assertEqual(sleep.call_count, 20)
            self.assertAlmostEqual(sum(call.args[0] for call in sleep.call_args_list), 0.5)
            bar = streamlit.progress.return_value
            self.assertEqual([call.args[0] for call in bar.progress.call_args_list], list(range(5, 101, 5)))
            bar.empty.assert_called_once()

            show_page_transition("")
            self.assertEqual(sleep.call_count, 20)
            for page in ("intake", "audit", "manager", "review", ""):
                previous = sleep.call_count
                show_page_transition(page)
                show_page_transition(page)
                self.assertEqual(sleep.call_count, previous + 20)
            self.assertEqual(streamlit.session_state["existing_draft"], "Keep this draft")
