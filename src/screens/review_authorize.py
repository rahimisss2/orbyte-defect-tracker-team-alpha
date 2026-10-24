from page_transition import show_page_transition
from views import review_authorize

show_page_transition("review")
# Keep the judging workflow usable on Gemini errors, timeouts or invalid output.
# The panel always labels simulated output; signatures/authorization stay manual.
# Simulated text enters the draft only through the explicit insertion button.
review_authorize(allow_simulated_fallback=True)
