# Demo-only "login" — no real credential checking, no user data at stake.
# Production ECHO doesn't need server-side auth at all (client-side only).
import streamlit as st

def login_screen():
    st.markdown(
        """
        <div style="text-align:center; padding-top: 60px;">
            <h1 style="font-size:3rem; background: linear-gradient(90deg,#22c55e,#8b5cf6,#3b82f6);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                ECHO
            </h1>
            <p style="color:#6b7280; font-style: italic;">
                Emotions don't disappear; they echo over time
            </p>
            <p style="color:#9ca3af; font-size: 0.8rem;">Portfolio demo build</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.info("This is a demo — any name works, no password needed.", icon="ℹ️")
        with st.form("login_form"):
            name = st.text_input("Your name (for demo)", value="Guest")
            submitted = st.form_submit_button("Enter ECHO", use_container_width=True)
            if submitted:
                st.session_state.authenticated = True
                st.session_state.username = name or "Guest"
                st.rerun()

