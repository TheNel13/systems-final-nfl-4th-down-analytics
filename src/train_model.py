import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

"""
This script:
1. Loads NFL play-by-play data (2009–2016)
2. Extracts 4th-down plays
3. Builds subsets:
   - Go (run/pass)
   - Field goals
   - Punts
4. Trains 3 WPA regression models
5. Saves them into /src/
"""

# ============================
# Load dataset (from assets/)
# ============================
df = pd.read_csv("assets/NFL Play by Play 2009-2016 (v3).csv", low_memory=False)

# ============================
# Filter to 4th down plays
# ============================
fourth = df[df["down"] == 4].copy()

# ============================
# REQUIRED COLUMNS FROM YOUR DATASET
# posteam, DefensiveTeam, ydstogo, yrdline100, TimeSecs, ScoreDiff, WPA
# ============================
fourth = fourth.dropna(subset=[
    "posteam",
    "DefensiveTeam",
    "ydstogo",
    "yrdline100",
    "TimeSecs",
    "ScoreDiff",
    "WPA"
])

# Ensure consistent defensive team label
fourth["defteam"] = fourth["DefensiveTeam"]

# ============================
# Encode teams using LabelEncoder
# ============================
teams = pd.concat([fourth["posteam"], fourth["defteam"]]).unique()
encoder = LabelEncoder()
encoder.fit(teams)

fourth["offense_val"] = encoder.transform(fourth["posteam"])
fourth["defense_val"] = encoder.transform(fourth["defteam"])

# ============================
# Feature columns (MUST MATCH app.py)
# ============================
feature_cols = [
    "offense_val",
    "defense_val",
    "yrdline100",      # correct field position column
    "ydstogo",
    "down",
    "TimeSecs",
    "ScoreDiff"        # correct score differential column
]

# ============================
# Build decision subsets
# ============================
go_df = fourth[fourth["PlayType"].isin(["Run", "Pass"])]
fg_df = fourth[fourth["FieldGoalResult"].notna()]
punt_df = fourth[fourth["PlayType"] == "Punt"]

# ============================
# Train + save model helper
# ============================
def train_and_save(df_slice, model_path):
    X = df_slice[feature_cols]
    y = df_slice["WPA"]

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42
    )
    model.fit(X, y)
    
    pickle.dump(model, open(model_path, "wb"))

# ============================
# Train all 3 models
# ============================
train_and_save(go_df, "src/model_go.pkl")
train_and_save(fg_df, "src/model_fg.pkl")
train_and_save(punt_df, "src/model_punt.pkl")

# ============================
# Print team encoding so you can paste into app.py
# ============================
print("\nTEAM ENCODING — copy into app.py team_map:")
for team, code in zip(encoder.classes_, encoder.transform(encoder.classes_)):
    print(f"{team}: {code}")

print("\nModels trained and saved successfully!")