# TSA STEM Career Quiz 

A Flask-powered web app that helps middle and high school students discover their STEM career path through a 15-question personality quiz.

Flask-powered web application to help students discover their best-fitting STEM career path through a 15-question quiz. 

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

## How it Works
Each question has 6 answer options, each corresponding to a pre-declared "persona type".
Program counts which answers you chose most often (and, which persona they correspond to) and returns:
- Your **primary persona** (highest score)
- Your **secondary persona** (second highest score)
- **Score breakdown** across all 6 types
- 3 **matching careers** with roadmaps, salary, education, and resources
