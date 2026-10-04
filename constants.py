MOOD_LABELS = {
    1: {"label": "Drained", "color": "#a855f7"},
    2: {"label": "Drained", "color": "#a855f7"},
    3: {"label": "Heavy",   "color": "#8b5cf6"},
    4: {"label": "Heavy",   "color": "#818cf8"},
    5: {"label": "Steady",  "color": "#818cf8"},
    6: {"label": "Steady",  "color": "#60a5fa"},
    7: {"label": "Light",   "color": "#60a5fa"},
    8: {"label": "Light",   "color": "#34d399"},
    9: {"label": "Clear",   "color": "#22c55e"},
    10: {"label": "Clear",  "color": "#16a34a"},
}

CONTEXT_TAGS = ["Work", "Sleep", "Social", "Health", "Study", "Family", "Exercise", "Other"]

SLEEP_SUGGESTIONS = {
    "low_hours": "⚠️ Average sleep is below 6 hours. Sleep debt compounds — prioritize rest this week.",
    "low_quality": "💤 Sleep quality seems low. Try: no caffeine after 2 PM, consistent bedtime, cooler room.",
    "good": "✨ Great sleep patterns — this is likely supporting your emotional clarity. Keep it up.",
    "default": "Keep logging sleep consistently — patterns take about 7+ entries to become reliable.",
}

ENTRY_COLUMNS = [
    "date", "mood", "journal", "sentiment",
    "sleep_hours", "sleep_quality", "sleep_notes",
    "context_tags", "energy"
]

DEMO_BANNER_TEXT = (
    "🧪 **Demo Mode** — this deployment uses synthetic data stored only in your "
    "browser session (RAM). Nothing is saved to a server or disk. Refresh the "
    "page to reset. [See production architecture →]"
)


def get_mood_label(mood: int) -> str:
    return MOOD_LABELS.get(int(mood), {"label": "Steady"})["label"]
