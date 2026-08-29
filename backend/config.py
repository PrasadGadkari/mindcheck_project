"""
backend/config.py
Central place for constants: colors, disclaimer text, crisis text,
and paths to generated illustration assets.
Nothing here changes the original scoring/UI logic - it only
relocates the constants that used to live at the top of app.py.
"""

import os

# =========================================================
# --- PATHS ---
# =========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

IMG_HEADER = os.path.join(ASSETS_DIR, "header_brain.png")
IMG_DEPRESSION = os.path.join(ASSETS_DIR, "depression_illustration.png")
IMG_ANXIETY = os.path.join(ASSETS_DIR, "anxiety_illustration.png")
IMG_STRESS = os.path.join(ASSETS_DIR, "stress_illustration.png")
IMG_CALM = os.path.join(ASSETS_DIR, "calm_illustration.png")
IMG_METHODOLOGY = os.path.join(ASSETS_DIR, "methodology_illustration.png")

# =========================================================
# --- COLORS (unchanged from original) ---
# =========================================================
COLOR_MILD = "#4CAF50"       # green
COLOR_MODERATE = "#FFC107"   # yellow / amber
COLOR_SEVERE = "#E53935"     # red
COLOR_NEUTRAL = "#B0BEC5"    # grey (used for the "max score" reference bar)

# Per-category accent colors, used for the illustrations / page headers
CATEGORY_COLOR = {
    "Depression": "#5C6BC0",  # indigo
    "Anxiety": "#FF8A65",     # coral
    "Stress": "#26A69A",      # teal
}

# =========================================================
# --- TEXT CONSTANTS (unchanged from original) ---
# =========================================================
CRISIS_TEXT = """
If you are in crisis or having thoughts of self-harm, please reach out immediately:

📞 Call or text 988 — Suicide & Crisis Lifeline (USA, available 24/7)

💬 Text "HOME" to 741741 — Crisis Text Line

🚨 Call 911 / your local emergency number if you are in immediate danger


You are not alone, and help is available right now.
"""

DISCLAIMER_TEXT = (
    "⚠️ Disclaimer: This tool is for educational / screening purposes only "
    "and does not provide a clinical diagnosis. It is a simplified academic "
    "demonstration and cannot replace a licensed mental health professional. "
    "In case of an emergency, call 988 or seek professional help immediately."
)
