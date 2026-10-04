import datetime
import pandas as pd

from constants import SLEEP_SUGGESTIONS

def generate_weekly_summary(entries: pd.DataFrame):
    if entries.empty:
        return None

    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    df = entries.copy()
    df["date_parsed"] = pd.to_datetime(df["date"])
    week_entries = df[(df["date_parsed"].dt.date >= week_ago) & (df["date_parsed"].dt.date <= today)]

    if week_entries.empty:
        return None

    avg_mood = round(week_entries["mood"].mean(), 1)

    week_sorted = week_entries.sort_values("date_parsed")
    half = max(1, len(week_sorted) // 2)
    first_half_avg = week_sorted.iloc[:half]["mood"].mean()
    second_half_avg = week_sorted.iloc[half:]["mood"].mean() if len(week_sorted) > half else first_half_avg

    if second_half_avg > first_half_avg + 0.5:
        trend, description = "↑", "showing improvement"
    elif second_half_avg < first_half_avg - 0.5:
        trend, description = "↓", "showing decline"
    else:
        trend, description = "→", "emotionally stable with mild fluctuations"

    result = {
        "avg_mood": avg_mood,
        "trend": trend,
        "description": description,
        "entry_count": len(week_entries),
    }

    sleep_entries = week_entries.dropna(subset=["sleep_hours"])
    if not sleep_entries.empty:
        avg_sleep_hours = round(sleep_entries["sleep_hours"].mean(), 1)
        avg_sleep_quality = round(sleep_entries["sleep_quality"].mean(), 1)

        if avg_sleep_hours < 6:
            suggestion = SLEEP_SUGGESTIONS["low_hours"]
        elif avg_sleep_quality < 2.5:
            suggestion = SLEEP_SUGGESTIONS["low_quality"]
        elif avg_sleep_hours >= 7 and avg_sleep_quality >= 3.5:
            suggestion = SLEEP_SUGGESTIONS["good"]
        else:
            suggestion = SLEEP_SUGGESTIONS["default"]

        result.update({
            "avg_sleep_hours": avg_sleep_hours,
            "avg_sleep_quality": avg_sleep_quality,
            "sleep_suggestion": suggestion
        })

    return result