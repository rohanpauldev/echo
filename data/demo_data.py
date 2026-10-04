# Generates realistic synthetic entries so the app is explorable without
# any real personal data. Deterministic seed = same demo every run.
import datetime
import random

import numpy as np
import pandas as pd

from constants import CONTEXT_TAGS

def generate_demo_entries(days: int = 30) -> pd.DataFrame:
    random.seed(42)
    np.random.seed(42)

    sample_journals = {
        "Positive": [
            "Felt really productive today, finished the project I've been putting off.",
            "Had a great call with an old friend, felt grateful and connected.",
            "Slept well and woke up feeling clear-headed and motivated.",
            "Went for a run this morning, energy has been steady all day.",
        ],
        "Neutral": [
            "Pretty average day, nothing major happened.",
            "Did some studying, felt okay overall.",
            "Normal work day, steady but unremarkable.",
            "",
        ],
        "Negative": [
            "Felt overwhelmed with deadlines, hard to focus today.",
            "Didn't sleep well, feeling drained and a bit anxious.",
            "Stressful day at work, mind felt foggy by the evening.",
            "Feeling a bit low, not sure exactly why.",
        ],
    }

    context_pool = CONTEXT_TAGS

    rows = []
    today = datetime.date.today()
    mood_walk = 6  # start steady, random-walk it for realism

    for i in range(days, 0, -1):
        date = today - datetime.timedelta(days=i)

        mood_walk += random.choice([-1, -1, 0, 0, 0, 1, 1])
        mood_walk = max(1, min(10, mood_walk))
        mood = mood_walk

        bucket = "Positive" if mood >= 7 else "Negative" if mood <= 4 else "Neutral"
        journal = random.choice(sample_journals[bucket])

        sleep_hours = round(np.clip(np.random.normal(
            7.2 if mood >= 6 else 5.8, 1.0), 3, 10), 1)
        sleep_quality = int(np.clip(round(np.random.normal(
            3.5 if mood >= 6 else 2.2, 0.8)), 1, 5))

        tags = random.sample(context_pool, k=random.randint(0, 2))

        rows.append({
            "date": date.isoformat(),
            "mood": mood,
            "journal": journal,
            "sentiment": bucket,
            "sleep_hours": sleep_hours,
            "sleep_quality": sleep_quality,
            "sleep_notes": "",
            "context_tags": ",".join(tags),
            "energy": max(1, min(10, mood + random.choice([-1, 0, 1]))),
        })

    return pd.DataFrame(rows)