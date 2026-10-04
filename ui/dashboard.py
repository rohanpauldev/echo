import datetime
import pandas as pd
import streamlit as st

from constants import CONTEXT_TAGS, get_mood_label
from data.storage import load_entries, save_entry
from logic.sentiment import analyze_sentiment
from logic.summaries import generate_weekly_summary

def render_dashboard():
    entries = load_entries()
    today = datetime.date.today().isoformat()
    today_row = entries[entries["date"] == today]
    today_entry = today_row.iloc[0].to_dict() if not today_row.empty else None

    st.header("Capture Today's Echo")

    col1, col2 = st.columns(2)

    with col1:
        mood = st.slider(
            "Energy & Clarity (1: Drained — 10: Clear)",
            1, 10,
            int(today_entry["mood"]) if today_entry else 5
        )
        st.caption(f"**{get_mood_label(mood)}**")

        energy = st.slider(
            "Energy Level (1: Low — 10: High)",
            1, 10,
            int(today_entry["energy"]) if today_entry and pd.notna(today_entry.get("energy")) else 5
        )

        context_tags = st.multiselect(
            "What influenced today?",
            CONTEXT_TAGS,
            default=today_entry["context_tags"].split(",")
            if today_entry and today_entry.get("context_tags") else []
        )

    with col2:
        sleep_hours = st.number_input(
            "Sleep Hours Last Night",
            min_value=0.0, max_value=24.0, step=0.5,
            value=float(today_entry["sleep_hours"]) if today_entry and pd.notna(today_entry.get("sleep_hours")) else 7.0
        )
        sleep_quality = st.slider(
            "Sleep Quality (1: Poor — 5: Excellent)",
            1, 5,
            int(today_entry["sleep_quality"]) if today_entry and pd.notna(today_entry.get("sleep_quality")) else 3
        )
        sleep_notes = st.text_input(
            "Sleep Notes (optional)",
            value=today_entry["sleep_notes"] if today_entry and pd.notna(today_entry.get("sleep_notes")) else ""
        )

    journal = st.text_area(
        "What's echoing in your mind? (optional)",
        value=today_entry["journal"] if today_entry and pd.notna(today_entry.get("journal")) else "",
        height=120,
        placeholder="Let your thoughts flow freely..."
    )

    if journal.strip():
        sentiment_preview = analyze_sentiment(journal)
        badge = {"Positive": "🟢", "Negative": "🔴", "Neutral": "⚪"}[sentiment_preview]
        st.caption(f"{badge} Detected sentiment: **{sentiment_preview}**")

    if st.button("💾 Save Echo", type="primary", use_container_width=True):
        sentiment = save_entry(
            today, mood, journal, sleep_hours, sleep_quality,
            sleep_notes, context_tags, energy
        )
        st.success(f"Echo saved to session! Sentiment detected: {sentiment}")
        st.rerun()

    st.divider()

    entries = load_entries()
    summary = generate_weekly_summary(entries)

    if summary:
        st.subheader("📊 Weekly Summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("Average Mood", f"{summary['avg_mood']}/10", summary["trend"])
        c2.metric("Entries This Week", summary["entry_count"])
        if "avg_sleep_hours" in summary:
            c3.metric("Average Sleep", f"{summary['avg_sleep_hours']}h")

        st.info(f"This week appears **{summary['description']}**.")
        if "sleep_suggestion" in summary:
            st.warning(summary["sleep_suggestion"])

