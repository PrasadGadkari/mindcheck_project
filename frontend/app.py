"""
Mental Health Screening Tool
A diploma project demo built with Streamlit.
Combines shortened versions of PHQ-9, GAD-7, and PSS screeners
into a single assessment with instant visual feedback.

Run with (from the project root folder):  streamlit run frontend/app.py

--------------------------------------------------------------
This is the FRONTEND entry point only. All data / scoring logic
lives in backend/, and all chart / image generation lives in
visuals/. The original scoring algorithm is untouched - only
relocated - see backend/scoring.py.

This file lives inside frontend/, while backend/ and visuals/ are
sibling folders at the project root. The two lines below add the
project root to Python's import path so "from backend..." and
"from visuals..." keep working no matter where this script is run
from.
--------------------------------------------------------------
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd

from backend.config import (
    DISCLAIMER_TEXT, CRISIS_TEXT,
    IMG_HEADER, IMG_DEPRESSION, IMG_ANXIETY, IMG_STRESS, IMG_CALM, IMG_METHODOLOGY,
)
from backend.questions import QUESTIONS, TOTAL_QUESTIONS, get_scale, SCALE_PHQ_GAD, SCALE_PSS
from backend.scoring import compute_category_scores, severity_level, severity_color
from backend.advice import get_advice
from backend.session import init_session_state, reset_assessment

from visuals.illustrations import ensure_illustrations
from visuals.charts import plot_results, plot_category
from visuals.background import ensure_background
from visuals.styles import inject_custom_css

# =========================================================
# --- CONFIGURATION ---
# =========================================================
st.set_page_config(
    page_title="Mental Health Screening Tool",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Generate the themed illustrations & background once (cached to /assets after first run)
ensure_illustrations()
bg_path = ensure_background()
inject_custom_css(st, bg_path)

init_session_state()

# =========================================================
# --- UI: SIDEBAR NAVIGATION ---
# =========================================================
st.sidebar.title("🧠 Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["Take Assessment", "About Project", "Methodology"],
)

st.sidebar.markdown("---")
st.sidebar.info(DISCLAIMER_TEXT)

# =========================================================
# --- PAGE: ABOUT PROJECT ---
# =========================================================
if page == "About Project":
    st.image(IMG_HEADER, use_container_width=True)
    st.title("🧠 Mental Health Screening Tool")
    st.subheader("About This Project")
    st.write(
        """
        This application is a diploma project demonstration that showcases how
        data-driven web apps can be used to build simple, interactive mental
        health self-screening tools.

        It combines shortened, adapted versions of three widely recognized
        psychological screening instruments into a single assessment:

        - **PHQ-9** — Patient Health Questionnaire (Depression) — 9 questions used
        - **GAD-7** — Generalized Anxiety Disorder scale (Anxiety) — 9 questions used
        - **PSS** — Perceived Stress Scale (Stress) — 8 questions used

        The tool then scores each category, classifies the severity level, and
        presents a visual breakdown along with self-care suggestions.
        """
    )
    st.warning(DISCLAIMER_TEXT)

    st.markdown("### Tech Stack")
    st.write("- **Streamlit** — web app framework (frontend, `app.py`)")
    st.write("- **backend/** — question bank, scoring engine, advice content")
    st.write("- **visuals/** — chart generation & themed illustrations")
    st.write("- **Pandas / NumPy** — data handling")
    st.write("- **Matplotlib & Seaborn** — data visualization")
    st.write("- **Pillow (PIL)** — generated illustrations")

    st.markdown("### A Glimpse at Each Dimension")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(IMG_DEPRESSION, caption="Depression", use_container_width=True)
    with col2:
        st.image(IMG_ANXIETY, caption="Anxiety", use_container_width=True)
    with col3:
        st.image(IMG_STRESS, caption="Stress", use_container_width=True)

# =========================================================
# --- PAGE: METHODOLOGY ---
# =========================================================
elif page == "Methodology":
    st.image(IMG_METHODOLOGY, use_container_width=True)
    st.title("📊 Methodology")

    st.markdown("### 1. Question Selection")
    st.write(
        """
        Questions were adapted from three validated screening tools to cover
        three key dimensions of mental wellbeing: mood (Depression), worry
        (Anxiety), and coping capacity (Stress). Each dimension now has
        8-10 questions for a more complete picture than a single-item check.
        """
    )

    st.markdown("### 2. Answer Scale")
    df_scale = pd.DataFrame({
        "Value": [0, 1, 2, 3],
        "PHQ-9 / GAD-7 Label": list(SCALE_PHQ_GAD.values()),
        "PSS Label": list(SCALE_PSS.values()),
    })
    st.table(df_scale)

    st.markdown("### 3. Scoring Engine")
    dep_max = sum(3 for q in QUESTIONS if q["category"] == "Depression")
    anx_max = sum(3 for q in QUESTIONS if q["category"] == "Anxiety")
    str_max = sum(3 for q in QUESTIONS if q["category"] == "Stress")
    st.write(
        f"""
        Each answer contributes a value from 0-3. The scores for questions
        belonging to the same category are summed to produce a **sub-score**.

        - Depression sub-score: max **{dep_max}**
        - Anxiety sub-score: max **{anx_max}**
        - Stress sub-score: max **{str_max}**
        """
    )

    st.markdown("### 4. Severity Classification")
    st.write(
        """
        Each category's score is converted into a percentage of its maximum
        possible score, then classified as:

        - **0% – 33%** → Mild / Low
        - **34% – 66%** → Moderate
        - **67% – 100%** → Severe
        """
    )
    st.info(
        "This is a simplified proportional cutoff for demonstration purposes. "
        "Real clinical tools (like the full PHQ-9) use validated, fixed "
        "cutoff scores established through research."
    )

    st.markdown("### 5. Visualization Approach")
    st.write(
        """
        Instead of a single combined chart, each dimension now gets a
        distinct visualization style so patterns are easier to read at a
        glance:

        - **Depression** → stacked bar chart
        - **Anxiety** → donut chart (percentage of max score)
        - **Stress** → horizontal gauge bar
        - A combined grouped bar chart is still shown for an overall summary.
        """
    )

# =========================================================
# --- PAGE: TAKE ASSESSMENT ---
# =========================================================
elif page == "Take Assessment":
    st.title("🧠 Mental Health Screening Assessment")

    # ---- Step 0: Disclaimer gate ----
    if not st.session_state.started:
        st.image(IMG_CALM, use_container_width=True)
        st.error(DISCLAIMER_TEXT)
        st.write(
            f"This assessment has **{TOTAL_QUESTIONS} questions** and takes about "
            "**4-6 minutes**. Your responses are not stored or shared."
        )
        if st.button("✅ I Understand — Start Assessment", type="primary"):
            st.session_state.started = True
            st.rerun()

    # ---- Step 1: Question-by-question flow ----
    elif st.session_state.started and not st.session_state.submitted:
        idx = st.session_state.current_q
        q = QUESTIONS[idx]
        scale = get_scale(q["category"])
        option_values = list(scale.keys())
        option_labels = [scale[v] for v in option_values]

        # Progress bar
        progress = (idx) / TOTAL_QUESTIONS
        st.progress(progress, text=f"Question {idx + 1} of {TOTAL_QUESTIONS}")

        st.markdown(f"#### Category: *{q['category']}*")
        st.subheader(q["text"])
        st.caption("Over the last 2 weeks, how often have you been bothered by this?")

        # Pre-select previous answer if the user is navigating back
        previous_val = st.session_state.answers.get(q["id"])
        default_index = option_values.index(previous_val) if previous_val is not None else 0

        selected_label = st.radio(
            "Select an answer:",
            option_labels,
            index=default_index,
            key=f"radio_{q['id']}",
        )
        selected_value = option_values[option_labels.index(selected_label)]

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if idx > 0:
                if st.button("⬅ Previous"):
                    st.session_state.answers[q["id"]] = selected_value
                    st.session_state.current_q -= 1
                    st.rerun()

        with col3:
            is_last = idx == TOTAL_QUESTIONS - 1
            button_label = "Submit ✅" if is_last else "Next ➡"
            if st.button(button_label, type="primary"):
                st.session_state.answers[q["id"]] = selected_value
                if is_last:
                    st.session_state.submitted = True
                else:
                    st.session_state.current_q += 1
                st.rerun()

    # ---- Step 2: Results ----
    elif st.session_state.submitted:
        st.success("✅ Assessment Complete!")
        st.header("📋 Your Results")

        category_scores = compute_category_scores(st.session_state.answers)

        # --- Summary cards ---
        cols = st.columns(len(category_scores))
        overall_severe = False
        for i, (cat, vals) in enumerate(category_scores.items()):
            level = severity_level(vals["score"], vals["max"])
            if level == "Severe":
                overall_severe = True
            with cols[i]:
                st.metric(
                    label=f"{cat} Score",
                    value=f"{vals['score']} / {vals['max']}",
                    delta=level,
                    delta_color="off",
                )

        st.markdown("---")

        # --- Combined chart (original) ---
        st.subheader("📊 Overall Visual Breakdown")
        fig = plot_results(category_scores)
        st.pyplot(fig)

        st.markdown("---")

        # --- NEW: separate chart per category, with matching illustration ---
        st.subheader("📈 Category Breakdown (individual charts)")
        icon_map = {"Depression": IMG_DEPRESSION, "Anxiety": IMG_ANXIETY, "Stress": IMG_STRESS}
        for cat, vals in category_scores.items():
            c_img, c_chart = st.columns([1, 2])
            with c_img:
                st.image(icon_map.get(cat, IMG_CALM), use_container_width=True)
            with c_chart:
                fig_cat = plot_category(cat, vals["score"], vals["max"])
                st.pyplot(fig_cat)

        st.markdown("---")

        # --- Crisis alert (shown once, at top, if ANY category is severe) ---
        if overall_severe:
            st.error("🚨 **RED ALERT: One or more of your scores indicate a SEVERE level.**")
            st.markdown(CRISIS_TEXT)
            st.markdown("---")

        # --- Per-category advice ---
        st.subheader("💡 Personalized Suggestions")
        st.image(IMG_CALM, use_container_width=True)
        for cat, vals in category_scores.items():
            level = severity_level(vals["score"], vals["max"])
            color = severity_color(level)

            st.markdown(
                f"<h4 style='color:{color};'>{cat} — {level}</h4>",
                unsafe_allow_html=True,
            )

            if level == "Severe":
                st.warning(
                    f"Your {cat.lower()} score suggests a **severe** level of "
                    f"distress. Please consider speaking with a licensed "
                    f"mental health professional as soon as possible."
                )
            else:
                tips = get_advice(cat, level)
                for tip in tips:
                    st.write(f"- {tip}")

        st.markdown("---")
        if st.button("🔄 Retake Assessment"):
            reset_assessment()
            st.rerun()

        st.caption(
            "Reminder: This tool is for educational purposes only and does "
            "not constitute a medical diagnosis."
        )
