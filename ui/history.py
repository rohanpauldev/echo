import datetime

import altair as alt
import pandas as pd
import streamlit as st

from data.storage import load_entries

def render_history():
    entries = load_entries()

    if entries.empty:
        st.info("No entries yet.")
        return

    st.header("Emotional Timeline")

    chart_df = entries.copy()
    chart_df["date"] = pd.to_datetime(chart_df["date"])
    chart_df = chart_df.sort_values("date")

    mood_chart = alt.Chart(chart_df).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("mood:Q", title="Mood", scale=alt.Scale(domain=[1, 10])),
        tooltip=["date:T", "mood:Q", "sentiment:N", "sleep_hours:Q"],
        color=alt.value("#8b5cf6")
    ).properties(height=300)
    st.altair_chart(mood_chart, use_container_width=True)

    if entries["sleep_hours"].notna().sum() >= 3:
        sleep_chart = alt.Chart(chart_df.dropna(subset=["sleep_hours"])).mark_bar().encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("sleep_hours:Q", title="Sleep Hours"),
            tooltip=["date:T", "sleep_hours:Q", "sleep_quality:Q"],
            color=alt.value("#3b82f6")
        ).properties(height=200)
        st.altair_chart(sleep_chart, use_container_width=True)

    st.subheader("📋 Entry Log")
    display_cols = ["date", "mood", "sentiment", "sleep_hours", "sleep_quality", "context_tags", "journal"]
    st.dataframe(entries[display_cols].reset_index(drop=True), use_container_width=True, hide_index=True)

    csv = entries.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Export CSV (this session's data)",
        csv,
        f"echo-demo-export-{datetime.date.today().isoformat()}.csv",
        "text/csv",
        use_container_width=True
    )
