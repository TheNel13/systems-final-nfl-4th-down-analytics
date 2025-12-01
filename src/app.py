import os
import pickle
import numpy as np
from flask import Flask, render_template, request, jsonify

# ------------------------------------------------------
# FORCE FLASK TO USE THE CORRECT ROOT DIRECTORY
# ------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# ------------------------------------------------------
# LOAD MODELS
# ------------------------------------------------------

MODEL_GO_PATH = os.path.join(BASE_DIR, "src", "model_go.pkl")
MODEL_FG_PATH = os.path.join(BASE_DIR, "src", "model_fg.pkl")
MODEL_PUNT_PATH = os.path.join(BASE_DIR, "src", "model_punt.pkl")

with open(MODEL_GO_PATH, "rb") as f:
    model_go = pickle.load(f)

with open(MODEL_FG_PATH, "rb") as f:
    model_fg = pickle.load(f)

with open(MODEL_PUNT_PATH, "rb") as f:
    model_punt = pickle.load(f)

# ------------------------------------------------------
# TEAM ENCODING MAP (SAME AS TRAINING)
# ------------------------------------------------------
TEAM_MAP = {
    "ARI": 0, "ATL": 1, "BAL": 2, "BUF": 3, "CAR": 4, "CHI": 5, "CIN": 6,
    "CLE": 7, "DAL": 8, "DEN": 9, "DET": 10, "GB": 11, "HOU": 12, "IND": 13,
    "JAC": 14, "JAX": 15, "KC": 16, "LA": 17, "MIA": 18, "MIN": 19, "NE": 20,
    "NO": 21, "NYG": 22, "NYJ": 23, "OAK": 24, "PHI": 25, "PIT": 26, "SD": 27,
    "SEA": 28, "SF": 29, "STL": 30, "TB": 31, "TEN": 32, "WAS": 33
}

# ------------------------------------------------------
# ROUTES
# ------------------------------------------------------

@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    try:
        offense = TEAM_MAP.get(data["offense"], None)
        defense = TEAM_MAP.get(data["defense"], None)
        yardline = float(data["yardline"])
        ydstogo = float(data["ydstogo"])
        time_left = float(data["time_left"])
        score_diff = float(data["score_diff"])
    except Exception as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400

    if offense is None or defense is None:
        return jsonify({"error": "Invalid team abbreviation"}), 400

    down = 4
    # model expects inputs in fixed order
    X = np.array([[offense, defense, yardline, ydstogo, down, time_left, score_diff]])

    go_wpa = float(model_go.predict(X)[0])
    fg_wpa = float(model_fg.predict(X)[0])
    punt_wpa = float(model_punt.predict(X)[0])

    best = max(go_wpa, fg_wpa, punt_wpa)
    if best == go_wpa:
        decision = "GO FOR IT"
    elif best == fg_wpa:
        decision = "KICK FIELD GOAL"
    else:
        decision = "PUNT"

    return jsonify({
        "go_wpa": go_wpa,
        "fg_wpa": fg_wpa,
        "punt_wpa": punt_wpa,
        "decision": decision
    })


# ------------------------------------------------------
# RUN APP (FOR python src/app.py)
# ------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)