# 🧭 PathFinder — STEM Career Quiz App

A Flask-powered web app that helps middle and high school students discover their STEM career path through a 15-question personality quiz.

## Features
- **15-question slideshow quiz** — one question at a time, auto-advances on selection
- **6 STEM Personas** — Investigator, Builder, Innovator, Analyst, Healer, Changer
- **18 STEM Careers** — 3 matched careers per persona with full details
- **Visual Roadmap** — step-by-step path for each career
- **Score breakdown** — animated bar chart of your results
- **Explore page** — browse all careers, filterable by persona

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python app.py
```

### 3. Open in browser
```
http://localhost:5000
```

## Project Structure
```
pathfinder/
├── app.py                  # Flask backend + quiz logic
├── requirements.txt
├── static/
│   └── style.css           # All styles
└── templates/
    ├── index.html          # Landing page
    ├── quiz.html           # 15-question slideshow quiz
    ├── results.html        # Persona + careers + roadmap
    └── explore.html        # Browse all careers
```

## How the Quiz Works
Each of the 15 questions has 6 answer options, one per persona type.
Python counts which persona type you chose most often and returns:
- Your **primary persona** (highest score)
- Your **secondary persona** (second highest)
- A **score breakdown** across all 6 types
- 3 **matching careers** with roadmaps, salary, education, and resources
