"""
visuals/styles.py
Pure presentation layer: injects custom CSS into the Streamlit app for an
eye-catching, themed background (dusk sky, soft clouds, calming brain-wave
lines, gentle waves - generated in visuals/background.py) plus light
glassmorphism cards so text stays readable on top of it. This module only
returns/injects CSS - it does not touch any scoring/question/session logic.
"""

import base64


def _image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


_CSS_TEMPLATE = """
<style>
/* ---------- Themed background image (calm sky, clouds, brain-wave lines, waves) ---------- */
.stApp {
    background-image: url("data:image/png;base64,__BG_B64__");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-repeat: no-repeat;
    animation: bgDrift 40s ease-in-out infinite alternate;
}

@keyframes bgDrift {
    0%   { background-position: center top; }
    100% { background-position: center bottom; }
}

/* ---------- Main content sits above the background, in a soft glass card ---------- */
section.main > div.block-container {
    position: relative;
    z-index: 1;
    background: rgba(255, 255, 255, 0.68);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 22px;
    padding: 2.2rem 2.4rem !important;
    margin-top: 1.2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.5);
}

/* ---------- Sidebar glass treatment ---------- */
section[data-testid="stSidebar"] > div {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-right: 1px solid rgba(255, 255, 255, 0.4);
}

/* ---------- Rounded corners + soft shadow on images ---------- */
div[data-testid="stImage"] img {
    border-radius: 18px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.10);
}

/* ---------- Metric cards ---------- */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.6);
    border-radius: 14px;
    padding: 0.8rem 0.6rem;
    box-shadow: 0 4px 14px rgba(31, 38, 135, 0.08);
}

/* ---------- Primary buttons ---------- */
button[kind="primary"] {
    border-radius: 999px !important;
    box-shadow: 0 4px 14px rgba(92, 107, 192, 0.35);
}

/* ---------- Sidebar radio / info box readability ---------- */
section[data-testid="stSidebar"] .stAlert {
    background: rgba(255, 255, 255, 0.55);
    border-radius: 12px;
}
</style>
"""


def build_css(background_path: str) -> str:
    """Builds the full CSS block with the background image embedded as base64."""
    bg_b64 = _image_to_base64(background_path)
    return _CSS_TEMPLATE.replace("__BG_B64__", bg_b64)


def inject_custom_css(st, background_path: str):
    """Call with the streamlit module and the background image path:
    inject_custom_css(st, IMG_BACKGROUND)."""
    st.markdown(build_css(background_path), unsafe_allow_html=True)
