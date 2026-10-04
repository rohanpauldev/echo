import numpy as np
import pandas as pd

def analyze_sleep_mood_correlation(entries: pd.DataFrame):
    valid = entries.dropna(subset=["sleep_hours", "mood"])
    valid = valid[valid["sleep_hours"] > 0]

    if len(valid) < 7:
        return None

    correlation = np.corrcoef(valid["sleep_hours"], valid["mood"])[0, 1]

    if correlation > 0.5:
        insight = f"Strong positive link — better sleep tracks with better mood (r={correlation:.2f})"
    elif correlation > 0.2:
        insight = f"Mild positive link between sleep and mood (r={correlation:.2f})"
    elif correlation < -0.2:
        insight = f"Inverse pattern detected — worth reviewing sleep quality (r={correlation:.2f})"
    else:
        insight = f"Weak correlation (r={correlation:.2f}) — other factors likely matter more"

    return {
        "correlation": round(correlation, 2),
        "sample_size": len(valid),
        "insight": insight
    }


def analyze_context_impact(entries: pd.DataFrame):
    tag_rows = []
    for _, row in entries.iterrows():
        if pd.notna(row.get("context_tags")) and row["context_tags"]:
            for tag in str(row["context_tags"]).split(","):
                tag_rows.append({"tag": tag, "mood": row["mood"]})

    if not tag_rows:
        return None

    tag_df = pd.DataFrame(tag_rows)
    return tag_df.groupby("tag")["mood"].mean().reset_index().sort_values("mood", ascending=False)