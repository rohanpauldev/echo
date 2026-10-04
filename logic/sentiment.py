import streamlit as st
import nltk

from nltk.sentiment.vader import SentimentIntensityAnalyzer

@st.cache_resource
def _load_analyzer():
    nltk.download("vader_lexicon", quiet=True)
    return SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> str:
    if not text or not text.strip():
        return "Neutral"
    sia = _load_analyzer()
    score = sia.polarity_scores(text)["compound"]
    if score > 0.05:
        return "Positive"
    if score < -0.05:
        return "Negative"
    return "Neutral"

