import pickle

# Load model once
model = pickle.load(open("src/ml/model.pkl", "rb"))

def predict_stress(data):
    features = [[
        data.sleepDuration,
        data.quality_of_sleep,
        data.physical_activity_level,
        data.heart_rate,
    ]]

    score = model.predict(features)[0]
    return float(score)