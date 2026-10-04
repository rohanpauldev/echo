import streamlit as st

from auth.auth import login_screen
from constants import DEMO_BANNER_TEXT
from data.storage import load_entries, reset_demo_data
from ui.dashboard import render_dashboard
from ui.history import render_history
from ui.insights import render_insights

def main():
    st.set_page_config(
        page_title="ECHO — Demo",
        page_icon="🌊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        login_screen()
        return

    st.warning(DEMO_BANNER_TEXT, icon="🧪")

    with st.sidebar:
        st.markdown(f"### 👋 {st.session_state.username}")
        st.caption("ECHO — Portfolio Demo Build")
        st.divider()

        if st.button("🔄 Reset demo data", use_container_width=True):
            reset_demo_data()
            st.rerun()

        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

        st.divider()
        st.caption(
            "**Architecture note:** production ECHO is a React app storing "
            "data client-side in IndexedDB. This Streamlit build is a research "
            "prototype used to test analysis logic before porting it client-side."
        )

    st.markdown(
        """
        <h1 style="background: linear-gradient(90deg,#22c55e,#8b5cf6,#3b82f6);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   display:inline;">ECHO</h1>
        <span style="color:#6b7280; font-style:italic;"> — Emotions echo over time</span>
        """,
        unsafe_allow_html=True
    )

    tab1, tab2, tab3 = st.tabs(["📝 Dashboard", "📜 History", "🔍 Insights"])
    with tab1:
        render_dashboard()
    with tab2:
        render_history()
    with tab3:
        render_insights()


if __name__ == "__main__":
    main()
