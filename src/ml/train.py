import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

# Loading dataset
df = pd.read_csv("src/ml/dataset/Sleep_health_and_lifestyle_dataset.csv")

# Selecting features
df = df[[
    "Sleep Duration",
    "Quality of Sleep",
    "Physical Activity Level",
    "Heart Rate",
    "Stress Level"
]]

df = df.dropna()

# Spliting data
X = df[[
    "Sleep Duration",
    "Quality of Sleep",
    "Physical Activity Level",
    "Heart Rate"
]]

y = df["Stress Level"]

# Training model
model = RandomForestRegressor()
model.fit(X, y)

# Saving model
model_path = "src/ml/model.pkl"

with open(model_path, "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved")