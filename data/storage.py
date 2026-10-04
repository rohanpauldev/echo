import pandas as pd
import streamlit as st

from data.demo_data import generate_demo_entries
from logic.sentiment import analyze_sentiment


def init_storage():
    if "entries" not in st.session_state:
        st.session_state.entries = generate_demo_entries(30)


def load_entries() -> pd.DataFrame:
    init_storage()
    return st.session_state.entries


def save_entry(date, mood, journal, sleep_hours, sleep_quality,
               sleep_notes, context_tags, energy):
    sentiment = analyze_sentiment(journal)
    new_row = pd.DataFrame([{
        "date": date,
        "mood": mood,
        "journal": journal,
        "sentiment": sentiment,
        "sleep_hours": sleep_hours,
        "sleep_quality": sleep_quality,
        "sleep_notes": sleep_notes,
        "context_tags": ",".join(context_tags) if context_tags else "",
        "energy": energy,
    }])

    entries = load_entries()
    entries = entries[entries["date"] != date]
    entries = pd.concat([entries, new_row], ignore_index=True)
    entries["date_parsed"] = pd.to_datetime(entries["date"])
    entries = entries.sort_values("date_parsed", ascending=False).drop(columns=["date_parsed"])

    st.session_state.entries = entries.reset_index(drop=True)
    return sentiment


def reset_demo_data():
    st.session_state.entries = generate_demo_entries(30)