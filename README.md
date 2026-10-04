# ECHO 🌊

> *Emotions don't disappear; they echo over time.*

ECHO is a privacy-first emotional awareness system. It lets you log mood, sleep, and short reflections, then surfaces patterns over time — without diagnosing, advising, or judging.

This repository contains a **Streamlit-based demo/prototype build** of ECHO, used for rapid prototyping of the core logic (sentiment analysis, weekly summaries, sleep–mood correlation) before any production decisions are made.

🔗 **Live demo (synthetic data only):** [tryecho.streamlit.app](https://tryecho.streamlit.app/)

---

## Table of Contents

- [What This Is](#what-this-is)
- [What This Is Not](#what-this-is-not)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Core Features](#core-features)
- [Design Principles](#design-principles)
- [Getting Started](#getting-started)
- [Resetting Demo Data](#resetting-demo-data)
- [Data & Privacy](#data--privacy)
- [Sentiment Analysis](#sentiment-analysis)
- [Deployment Notes](#deployment-notes)
- [Roadmap](#roadmap)
- [Tech Stack](#tech-stack)
- [License](#license)
- [Academic Context](#academic-context)

---

## What This Is

ECHO started as a personal tool to answer a simple question: *what if a mood tracker didn't try to diagnose you, sell your data, or guilt you into "staying positive"?*

It does three things, deliberately kept simple:

1. **Logs** — a mood score (1–10), optional journal text, sleep, and context tags, once per day.
2. **Reflects** — shows trends, weekly summaries, and sentiment, without labeling or judging.
3. **Exports** — your data is yours; one click downloads everything as CSV.

That's it. No streaks to guilt you, no push notifications, no "wellness score."

---

## What This Is Not

To keep scope honest and avoid harm, ECHO explicitly does **not**:

- Diagnose any mental health condition
- Intervene in crises or contact anyone on your behalf
- Provide therapy, medical advice, or clinical recommendations
- Train models on your data without explicit, opt-in consent
- Sell or share your data with third parties

These aren't missing features — they're deliberate boundaries. See [Design Principles](#design-principles) below.

---

## Architecture

```
┌─────────────────────────────────────┐
│         Streamlit (Python)          │
│                                     │
│  st.session_state (RAM only)        │
│  — wiped on refresh/restart         │
│  — never written to disk            │
│                                     │
│  VADER sentiment (NLTK)             │
│  pandas/numpy analysis              │
│  Altair visualizations              │
└─────────────────────────────────────┘
```

No backend database, no disk writes, no external API calls for core functionality. Everything runs inside the Streamlit process itself, scoped to a single browser session.

---

## Project Structure

```
echo/
├── app.py                      # Entry point — UI orchestration only
├── constants.py                 # MOOD_LABELS, CONTEXT_TAGS, copy strings
├── auth/
│   └── auth.py                  # Demo login screen (no real auth)
├── data/
│   ├── demo_data.py             # Synthetic data generator
│   └── storage.py                # Session-state read/write (no disk I/O)
├── logic/
│   ├── sentiment.py              # VADER sentiment wrapper
│   ├── summaries.py              # Weekly summary generator
│   └── correlation.py            # Sleep × mood correlation
├── ui/
│   ├── dashboard.py               # Dashboard tab
│   ├── history.py                 # History tab
│   └── insights.py                # Insights tab
├── requirements.txt
├── LICENSE
└── README.md
```

Each module has a single responsibility:
- `logic/` — pure functions, no UI dependency, easy to test or swap out
- `data/` — all state management, isolated so storage strategy can change without touching UI code
- `ui/` — rendering only, calls into `logic/` and `data/`
- `app.py` — stays intentionally small; just wires the tabs together

---

## Core Features

### Mood Logging
- 1–10 scale, mapped to energy/clarity labels (*Drained → Heavy → Steady → Light → Clear*) rather than vague "good/bad" framing
- One entry per day; editable same-day
- Optional free-text journal — no prompts, no word limits, no formatting requirements

### Sleep Tracking
- Hours slept, sleep quality (1–5), optional notes
- Correlated against mood over time (Pearson correlation coefficient)

### Sentiment Analysis
- Uses [VADER](https://github.com/cjhutto/vaderSentiment) (via NLTK) — a rule-based model tuned for short, informal text, including negation and punctuation handling
- Output is always one of `Positive / Neutral / Negative` — shown subtly, never as a warning or alert

### Weekly Summary
- Average mood, trend arrow (↑ → ↓), and a plain-language description
- Example: *"This week appears emotionally stable with mild fluctuations."*
- No motivational language, no scoring, no gamification

### Context Tags
- One-tap tags (Work, Sleep, Social, Health, Study, Family, Exercise, Other)
- Surfaced later as "average mood per tag" to show what correlates with higher/lower energy — descriptively, not causally

### Pattern Insights
- Sleep × mood correlation with a plain-English interpretation
- Sentiment distribution over time (donut chart)
- Context tag impact on mood (bar chart)

### Data Export
- One-click CSV download of the current session's data, always available, no paywall

### Explicitly NOT Implemented (by design)
These are locked / future items in the product brief — not missing by accident:

| Feature | Status | Why |
|---|---|---|
| Emergency alerts | Not implemented | Ethical and legal risk; requires validated clinical models |
| Auto-messaging contacts | Planned | Needs explicit consent flows + high-confidence detection |
| Push notifications | Deferred | Engagement optimization isn't a v0 goal |
| Facial emotion detection | Research only | Privacy concerns, CV complexity, not essential |
| Therapy language / advice | Rejected for v0 | Avoids false authority and potential harm |

---

## Design Principles

Every feature decision is checked against these rules. If a feature violates one, it's rejected — not debated.

1. **Simplicity over completeness**
2. **No medical claims**
3. **No emotional manipulation**
4. **User always in control**
5. **Data belongs to the user**
6. **Everything explainable** — every sentiment/summary result can be traced to the input that produced it
7. **Features grow incrementally**

> *"If a feature makes the system feel heavier, smarter than the user, or emotionally authoritative, it does not belong in this version."*

---

## Getting Started

### Requirements
- Python 3.9+
- pip

### Install

```bash
git clone https://github.com/rohanpauldev/echo.git
cd echo
pip install -r requirements.txt
```

`requirements.txt`:
```
streamlit
pandas
numpy
altair
nltk
bcrypt
```

### Run

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

On first login (any name works — this is demo mode, no real authentication), the app seeds itself with 30 days of synthetic entries using a deterministic random seed, so the Dashboard, History, and Insights tabs are populated immediately without requiring you to type anything personal.

---

## Resetting Demo Data

Click **"🔄 Reset demo data"** in the sidebar at any time to regenerate the synthetic dataset from scratch.

---

## Data & Privacy

This is the part that matters most, so it gets its own section.

- Data lives in `st.session_state` — **RAM only, for the duration of your browser tab**
- **Nothing is written to disk.** No CSV files, no database, no persistent storage of any kind
- Refreshing the page or the server restarting wipes all data — this is intentional, not a bug
- Seeded with synthetic data on login so no real personal information is ever required to explore the app

This design exists specifically because **Streamlit Community Cloud's filesystem is ephemeral and the hosting repo is public on the free tier.** Writing real user data to disk in this context would both leak it publicly and lose it on every restart anyway. Session-only state avoids both problems entirely for a public-facing demo.

### What This Project Will Never Do
- Sell or share data with third parties
- Train models on user data without explicit, opt-in, revocable consent
- Add silent background analytics or tracking
- Require data to leave the user's control for the app to function

---

## Sentiment Analysis

### Current Approach

A rule-based classifier (VADER) was chosen deliberately over an LLM or black-box model, because:

- **Explainable**: results can be traced to specific words/patterns in the input
- **No external API calls**: works fully offline, no latency, no cost
- **No training data risk**: nothing learned from or leaked from user entries

### Known Limitations
- Sarcasm and irony are not reliably detected
- Mixed-sentiment entries ("great day but exhausted") collapse to a single label
- Short or ambiguous text ("fine", "okay") can under-represent true emotional state

### Planned Improvements
- Multi-dimensional output (energy, clarity, anxiety — not just positive/negative)
- Optional, consent-based transformer model for higher accuracy, used statelessly (data processed and immediately discarded, never stored)

---

## Deployment Notes

### ⚠️ Streamlit Cloud Specifics

If deploying this publicly, be aware:

- The free tier requires a **public GitHub repo** — never commit real data files
- The container filesystem is **ephemeral** — any disk writes are lost on restart/sleep
- `data/storage.py` deliberately avoids disk/database writes for exactly this reason — all storage is `st.session_state`

**Do not** repurpose this demo build for real users by swapping in persistent storage (e.g., a database) without re-evaluating the entire privacy architecture first. This build is a prototype, not a production-ready system for handling real personal emotional data.

---

## Roadmap

### Near-term
- [ ] Modularize `app.py` fully into the file structure listed above (currently distributed with `# ===== FILE: path =====` markers for easy splitting)
- [ ] Multi-dimensional mood (energy / clarity / anxiety axes instead of single positive–negative score)
- [ ] Unit tests for `logic/` modules (pure functions, straightforward to test)

### Mid-term
- [ ] Optional, explicit-consent backend for advanced/transformer-based sentiment, stateless by design
- [ ] Situation-based story matching (non-diagnostic peer normalization, curated sources only)
- [ ] Client-side-only production version (data stored on user's own device, not a server)

### Explicitly deferred (see [Core Features](#core-features) table)
Emergency alerts, auto-messaging, push notifications, facial emotion detection — all require separate ethical/legal review before implementation.

---

## Tech Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| Charts | Altair |
| Sentiment | VADER (NLTK) |
| Data handling | pandas, numpy |
| Storage | `st.session_state` (RAM only) |
| Auth (demo) | bcrypt (session-only, not production-grade) |
| Hosting | Streamlit Community Cloud (demo data only) |

---

## License

MIT License — see [`LICENSE`](./LICENSE) for details.

---

## Academic Context

This project was developed as part of the **Design Thinking and Industrial Innovation Lab**, exploring what emotional-awareness software looks like when designed around user trust, data ownership, and ethical restraint first — features second.

If you're reviewing this as part of an academic or internship evaluation: this is a **research/demo prototype**, not a production system. See [Data & Privacy](#data--privacy) and [Deployment Notes](#deployment-notes) for the reasoning behind its current architecture, and [Roadmap](#roadmap) for what a production version would require.
