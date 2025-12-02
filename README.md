# 🏈 NFL 4th Down Decision Model
### Systems Final Case Study – Fall 2025
Live App: https://systems-final-nfl-4th-down-analytics-production.up.railway.app/

## 1) Executive Summary
#### Problem
NFL coaches frequently face high-pressure 4th-down decisions: go for it, kick a field goal, or punt. These decisions meaningfully impact win probability, yet humans routinely misjudge the tradeoffs due to bias, incomplete information, or time pressure. The goal of this project is to build a data-driven decision engine that evaluates real NFL game situations and recommends the optimal 4th-down action based on historical outcomes.

#### Solution (Non-Technical Overview)
This project delivers a web-based tool where a user enters the game state (teams, field position, yards to go, time remaining, and score differential). The system runs three predictive machine-learning models—one each for going for it, kicking a field goal, and punting—trained on 8 years of real NFL play-by-play data.
The app then displays the expected Win Probability Added (WPA) for each option and provides a clear recommendation. The interface runs entirely in the browser, while a Flask backend performs model inference inside a containerized environment deployed on Railway.

## 2) System Overview
#### Course Concepts Used
This project explicitly integrates the following concepts from the course:
- Containerization & Reproducibility (Docker)
- Environment Configuration (.env, dependency isolation)
- Model Serving & APIs (Flask)
- CI/CD Automation (GitHub Actions → Railway deploy)
- Testing & Validation (pytest)
- Cloud Deployment (Railway)
As well as other smaller coding concepts from earlier in the course

#### Architecture Diagram
![Architecture](assets/architecture.png)

#### Architecture Summary
- Frontend
-- HTML/CSS/JS (dashboard.html, static/charts.js)
-- Sends POST requests to /predict
