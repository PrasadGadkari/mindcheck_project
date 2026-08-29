# MindCheck — Mental Health Screening Tool

A diploma project demo built with Streamlit. Combines PHQ-9 (Depression),
GAD-7 (Anxiety), and PSS-style (Stress) screeners into one assessment with
instant visual feedback, themed illustrations, and a generated background.

## Folder structure

```
mindcheck_project/
├── frontend/
│   └── app.py              # Streamlit entry point — run this file
├── backend/
│   ├── __init__.py
│   ├── config.py           # colors, disclaimer/crisis text, asset paths
│   ├── questions.py        # 26-question bank (9 + 9 + 8) and answer scales
│   ├── scoring.py          # scoring engine (per-category totals + severity)
│   ├── advice.py           # self-care tips per category
│   └── session.py          # Streamlit session-state helpers
├── visuals/
│   ├── __init__.py
│   ├── charts.py           # combined chart + per-category bar/donut/gauge charts
│   ├── illustrations.py    # generates the 6 small page icons (Pillow)
│   ├── background.py       # generates the full-page themed background (Pillow)
│   └── styles.py           # embeds the background as CSS + glass-card styling
├── assets/                  # generated PNGs land here (auto-created on first run)
├── requirements.txt
└── README.md
```

## Setup (VS Code / terminal)

1. Open the `mindcheck_project` folder in VS Code.
2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate        (Windows PowerShell)
   source venv/bin/activate     (macOS/Linux)
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app **from the project root folder** (not from inside `frontend/`):
   ```
   streamlit run frontend/app.py
   ```
5. Your browser will open automatically at `http://localhost:8501`.

## Notes

- The first run generates images into `assets/` (background + icons). Every
  run after that reuses the cached files, so startup is instant.
- `frontend/app.py` adds the project root to Python's import path at the
  top of the file, so `from backend...` and `from visuals...` imports work
  correctly even though `app.py` lives one folder down.
- All original scoring logic is unchanged from the initial version — only
  reorganized into modules.
