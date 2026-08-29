"""
backend/advice.py
Self-care tips content - unchanged from the original app.py.
"""

SELF_CARE_TIPS = {
    "Depression": [
        "Keep a consistent sleep schedule (7-9 hours) — good sleep hygiene matters.",
        "Try to get outside for at least 15-20 minutes of sunlight daily.",
        "Engage in light physical activity like walking or stretching.",
        "Stay connected — talk to a friend or family member regularly.",
    ],
    "Anxiety": [
        "Practice deep breathing or a 5-minute mindfulness/meditation session.",
        "Limit caffeine intake, which can heighten anxious feelings.",
        "Try grounding techniques (e.g., the 5-4-3-2-1 sensory method).",
        "Break large tasks into smaller, manageable steps.",
    ],
    "Stress": [
        "Schedule short breaks throughout your day to reset.",
        "Try journaling to organize thoughts and identify stress triggers.",
        "Practice progressive muscle relaxation or light yoga.",
        "Prioritize tasks and set realistic, achievable goals.",
    ],
}


def get_advice(category: str, level: str) -> list:
    """Returns a list of tip strings depending on severity level."""
    if level == "Severe":
        return []  # handled separately with a crisis alert box
    return SELF_CARE_TIPS.get(category, [])
