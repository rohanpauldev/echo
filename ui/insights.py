import altair as alt
import streamlit as st

from data.storage import load_entries
from logic.correlation import (
    analyze_sleep_mood_correlation,
    analyze_context_impact
)

def render_insights():
    entries = load_entries()

    if len(entries) < 7:
        st.info(f"Need at least 7 entries for pattern analysis. You have {len(entries)}.")
        return

    st.header("🔍 Pattern Insights")
    st.caption("Descriptive analysis only — never diagnostic.")

    correlation_result = analyze_sleep_mood_correlation(entries)
    if correlation_result:
        st.subheader("Sleep × Mood Correlation")
        c1, c2 = st.columns(2)
        c1.metric("Correlation coefficient", correlation_result["correlation"])
        c2.metric("Sample size", correlation_result["sample_size"])
        st.info(correlation_result["insight"])

    st.subheader("Sentiment Distribution")
    if entries["sentiment"].notna().any():
        sentiment_counts = entries["sentiment"].value_counts().reset_index()
        sentiment_counts.columns = ["sentiment", "count"]
        sent_chart = alt.Chart(sentiment_counts).mark_arc(innerRadius=60).encode(
            theta="count:Q",
            color=alt.Color("sentiment:N", scale=alt.Scale(
                domain=["Positive", "Neutral", "Negative"],
                range=["#22c55e", "#9ca3af", "#ef4444"]
            )),
            tooltip=["sentiment:N", "count:Q"]
        ).properties(height=300)
        st.altair_chart(sent_chart, use_container_width=True)

    st.subheader("Context Tag Impact on Mood")
    tag_avg = analyze_context_impact(entries)
    if tag_avg is not None:
        tag_chart = alt.Chart(tag_avg).mark_bar().encode(
            x=alt.X("mood:Q", title="Average Mood", scale=alt.Scale(domain=[0, 10])),
            y=alt.Y("tag:N", sort="-x", title=""),
            color=alt.value("#8b5cf6")
        ).properties(height=300)
        st.altair_chart(tag_chart, use_container_width=True)
    else:
        st.caption("No context tags logged yet.")