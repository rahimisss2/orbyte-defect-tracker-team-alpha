from page_transition import show_page_transition
from views import review_authorize

show_page_transition("review")
# Keep the judging workflow usable after a confirmed Gemini gateway timeout.
# The panel always labels simulated output; signatures/authorization stay manual.
# Suggestions are read-only; managers may copy text into the editable draft.
review_authorize(allow_simulated_fallback=True)
