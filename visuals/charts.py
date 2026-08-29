"""
visuals/charts.py
Visualization functions.

- plot_results() is the ORIGINAL combined grouped-bar chart from app.py,
  kept completely unchanged so existing behaviour still works.
- plot_depression_bar(), plot_anxiety_donut(), plot_stress_gauge() are
  NEW, each using a different chart type so Depression / Anxiety / Stress
  each get their own distinct visualization instead of sharing one chart.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

from backend.config import COLOR_MILD, COLOR_MODERATE, COLOR_SEVERE, COLOR_NEUTRAL, CATEGORY_COLOR
from backend.scoring import severity_level, severity_color


# =========================================================
# --- ORIGINAL COMBINED CHART (unchanged) ---
# =========================================================
def plot_results(category_scores: dict):
    """Builds a grouped bar chart: user score vs max score per category,
    with the user's bar color-coded by severity level."""
    sns.set_style("whitegrid")
    categories = list(category_scores.keys())
    user_scores = [category_scores[c]["score"] for c in categories]
    max_scores = [category_scores[c]["max"] for c in categories]
    levels = [severity_level(category_scores[c]["score"], category_scores[c]["max"])
              for c in categories]
    user_colors = [severity_color(lvl) for lvl in levels]

    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(x - width / 2, user_scores, width, label="Your Score",
           color=user_colors, edgecolor="black")
    ax.bar(x + width / 2, max_scores, width, label="Max Possible Score",
           color=COLOR_NEUTRAL, edgecolor="black", alpha=0.6)

    ax.set_ylabel("Score")
    ax.set_title("Your Screening Results by Category")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)

    legend_handles = [
        mpatches.Patch(color=COLOR_MILD, label="Mild"),
        mpatches.Patch(color=COLOR_MODERATE, label="Moderate"),
        mpatches.Patch(color=COLOR_SEVERE, label="Severe"),
        mpatches.Patch(color=COLOR_NEUTRAL, label="Max Possible", alpha=0.6),
    ]
    ax.legend(handles=legend_handles, loc="upper right", fontsize=8)

    fig.tight_layout()
    return fig


# =========================================================
# --- NEW: per-category charts, each a different chart type ---
# =========================================================
def plot_depression_bar(score: int, max_score: int):
    """Depression: vertical single-category bar chart."""
    level = severity_level(score, max_score)
    color = severity_color(level)
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(4, 4.5))
    ax.bar(["Depression"], [score], color=color, edgecolor="black", width=0.5)
    ax.bar(["Depression"], [max_score - score], bottom=[score],
           color=COLOR_NEUTRAL, alpha=0.4, edgecolor="black", width=0.5)
    ax.set_ylim(0, max_score)
    ax.set_ylabel("Score")
    ax.set_title(f"Depression — {level}\n{score} / {max_score}")
    fig.tight_layout()
    return fig


def plot_anxiety_donut(score: int, max_score: int):
    """Anxiety: donut / pie chart showing % of max score reached."""
    level = severity_level(score, max_score)
    color = severity_color(level)
    remaining = max(max_score - score, 0)
    sns.set_style("white")
    fig, ax = plt.subplots(figsize=(4, 4.5))
    wedges, _ = ax.pie(
        [score, remaining] if max_score else [1],
        colors=[color, COLOR_NEUTRAL],
        startangle=90,
        wedgeprops=dict(width=0.35, edgecolor="white"),
    )
    pct = (score / max_score * 100) if max_score else 0
    ax.text(0, 0, f"{pct:.0f}%", ha="center", va="center", fontsize=20, fontweight="bold")
    ax.set_title(f"Anxiety — {level}\n{score} / {max_score}")
    fig.tight_layout()
    return fig


def plot_stress_gauge(score: int, max_score: int):
    """Stress: horizontal gauge-style bar."""
    level = severity_level(score, max_score)
    color = severity_color(level)
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(6, 2.2))
    ax.barh(["Stress"], [max_score], color=COLOR_NEUTRAL, alpha=0.4, edgecolor="black", height=0.5)
    ax.barh(["Stress"], [score], color=color, edgecolor="black", height=0.5)
    ax.set_xlim(0, max_score)
    ax.set_title(f"Stress — {level}   ({score} / {max_score})")
    ax.set_yticks([])
    fig.tight_layout()
    return fig


def plot_category(category: str, score: int, max_score: int):
    """Dispatch helper: returns the right chart type for a given category name."""
    if category == "Depression":
        return plot_depression_bar(score, max_score)
    elif category == "Anxiety":
        return plot_anxiety_donut(score, max_score)
    elif category == "Stress":
        return plot_stress_gauge(score, max_score)
    else:
        # fallback: simple bar, in case a new category is ever added
        return plot_depression_bar(score, max_score)
