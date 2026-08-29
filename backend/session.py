"""
backend/session.py
Streamlit session-state helpers - unchanged from the original app.py.
"""

import streamlit as st


def init_session_state():
    defaults = {
        "started": False,
        "current_q": 0,
        "answers": {},
        "submitted": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def reset_assessment():
    st.session_state.started = False
    st.session_state.current_q = 0
    st.session_state.answers = {}
    st.session_state.submitted = False
