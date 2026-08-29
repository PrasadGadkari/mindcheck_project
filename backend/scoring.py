"""
backend/scoring.py
Scoring engine - EXACT same logic as the original app.py.
Only moved into its own module, nothing about the algorithm changed.
"""

from backend.questions import QUESTIONS
from backend.config import COLOR_MILD, COLOR_MODERATE, COLOR_SEVERE


def compute_category_scores(answers: dict) -> dict:
    """
    Sums the raw answer values (0-3) per category.
    Returns a dict: {category: {"score": int, "max": int}}
    """
    categories = {}
    for q in QUESTIONS:
        cat = q["category"]
        val = answers.get(q["id"], 0)
        if cat not in categories:
            categories[cat] = {"score": 0, "max": 0}
        categories[cat]["score"] += val
        categories[cat]["max"] += 3  # each question max = 3
    return categories


def severity_level(score: int, max_score: int) -> str:
    """
    Classifies a score into Mild / Moderate / Severe based on
    what fraction of the maximum possible score was reached.
    0%   - 33%  -> Mild
    34%  - 66%  -> Moderate
    67%  - 100% -> Severe
    """
    ratio = score / max_score if max_score else 0
    if ratio <= 0.33:
        return "Mild"
    elif ratio <= 0.66:
        return "Moderate"
    else:
        return "Severe"


def severity_color(level: str) -> str:
    return {"Mild": COLOR_MILD, "Moderate": COLOR_MODERATE, "Severe": COLOR_SEVERE}[level]
