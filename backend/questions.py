"""
backend/questions.py
Question bank for the screening tool.

Original file had 4 Depression + 3 Anxiety + 3 Stress questions.
Expanded so every category has 8-10 questions, in the SAME style/
format/scale as the original questions (no scoring logic touched).
"""

SCALE_PHQ_GAD = {
    0: "Not at all",
    1: "Several days",
    2: "More than half the days",
    3: "Nearly every day",
}

SCALE_PSS = {
    0: "Never",
    1: "Sometimes",
    2: "Often",
    3: "Very Often",
}

QUESTIONS = [
    # ---- PHQ-9 style (Depression) — 9 questions ----
    {"id": 1, "category": "Depression",
     "text": "Little interest or pleasure in doing things?"},
    {"id": 2, "category": "Depression",
     "text": "Feeling down, depressed, or hopeless?"},
    {"id": 3, "category": "Depression",
     "text": "Trouble falling/staying asleep, or sleeping too much?"},
    {"id": 4, "category": "Depression",
     "text": "Feeling tired or having little energy?"},
    {"id": 5, "category": "Depression",
     "text": "Poor appetite or overeating?"},
    {"id": 6, "category": "Depression",
     "text": "Feeling bad about yourself, or that you are a failure, "
             "or have let yourself or your family down?"},
    {"id": 7, "category": "Depression",
     "text": "Trouble concentrating on things, such as studying or watching TV?"},
    {"id": 8, "category": "Depression",
     "text": "Moving or speaking noticeably slowly, or being fidgety/restless?"},
    {"id": 9, "category": "Depression",
     "text": "Thoughts that you would be better off resting away from everything, "
             "or of not wanting to continue?"},

    # ---- GAD-7 style (Anxiety) — 9 questions ----
    {"id": 10, "category": "Anxiety",
     "text": "Feeling nervous, anxious, or on edge?"},
    {"id": 11, "category": "Anxiety",
     "text": "Not being able to stop or control worrying?"},
    {"id": 12, "category": "Anxiety",
     "text": "Worrying too much about different things?"},
    {"id": 13, "category": "Anxiety",
     "text": "Trouble relaxing?"},
    {"id": 14, "category": "Anxiety",
     "text": "Being so restless that it is hard to sit still?"},
    {"id": 15, "category": "Anxiety",
     "text": "Becoming easily annoyed or irritable?"},
    {"id": 16, "category": "Anxiety",
     "text": "Feeling afraid, as if something awful might happen?"},
    {"id": 17, "category": "Anxiety",
     "text": "Avoiding situations or places because they make you feel anxious?"},
    {"id": 18, "category": "Anxiety",
     "text": "Noticing physical symptoms (racing heart, sweating) when anxious?"},

    # ---- PSS style (Stress) — 8 questions ----
    {"id": 19, "category": "Stress",
     "text": "Felt that you were unable to control the important things in your life?"},
    {"id": 20, "category": "Stress",
     "text": "Felt difficulties were piling up so high that you could not overcome them?"},
    {"id": 21, "category": "Stress",
     "text": "Felt nervous or 'stressed' in general?"},
    {"id": 22, "category": "Stress",
     "text": "Felt that you could not cope with all the things you had to do?"},
    {"id": 23, "category": "Stress",
     "text": "Been angered because of things that were outside of your control?"},
    {"id": 24, "category": "Stress",
     "text": "Found yourself constantly thinking about things you still have to finish?"},
    {"id": 25, "category": "Stress",
     "text": "Felt overwhelmed by your daily responsibilities?"},
    {"id": 26, "category": "Stress",
     "text": "Had difficulty relaxing, even during your free time?"},
]

TOTAL_QUESTIONS = len(QUESTIONS)


def get_scale(category: str) -> dict:
    """Return the correct answer scale dict for a given question category."""
    if category == "Stress":
        return SCALE_PSS
    return SCALE_PHQ_GAD  # Depression & Anxiety share the same scale style
