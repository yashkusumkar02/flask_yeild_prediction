from flask import Blueprint, request, jsonify
import pickle
import numpy as np
import pandas as pd
import os

yield_prediction = Blueprint("yield_prediction", __name__)

# Load Trained Model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/yield_model.pkl")

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
except Exception as e:
    model = None
    print(f"❌ Model loading failed: {str(e)}")

# Load Dataset to Get Feature Structure
DATA_PATH = os.path.join(os.path.dirname(__file__), "../models/crop_yield.csv")
df = pd.read_csv(DATA_PATH)

# One-Hot Encode Crop, State, and Season
df["Crop"] = df["Crop"].str.strip()
df["State"] = df["State"].str.strip()
df["Season"] = df["Season"].str.strip()

df_encoded = pd.get_dummies(df, columns=["Crop", "State", "Season"])

# Get Column Names (Ensuring Correct Feature Order)
feature_columns = df_encoded.drop(columns=["Yield"]).columns.tolist()

@yield_prediction.route('/yield-prediction', methods=['POST'])
def predict_yield():
    if model is None:
        return jsonify({"error": "Model not loaded properly. Check logs."}), 500

    try:
        data = request.get_json()

        # Validate request data
        required_fields = ["crop", "state", "season", "area", "rainfall", "fertilizer", "pesticide"]
        for field in required_fields:
            if field not in data or data[field] == "":
                return jsonify({"error": f"Missing or empty field: {field}"}), 400

        # Convert Inputs
        crop = data["crop"].strip()
        state = data["state"].strip()
        season = data["season"].strip()
        area = float(data["area"])
        rainfall = float(data["rainfall"])
        fertilizer = float(data["fertilizer"])
        pesticide = float(data["pesticide"])

        # Create One-Hot Encoded Input
        input_data = pd.DataFrame([[crop, state, season, area, rainfall, fertilizer, pesticide]],
                                  columns=["Crop", "State", "Season", "Area", "Annual_Rainfall", "Fertilizer", "Pesticide"])
        input_data = pd.get_dummies(input_data, columns=["Crop", "State", "Season"])

        # Ensure Column Order Matches Training Data
        input_data = input_data.reindex(columns=feature_columns, fill_value=0)

        # Convert to NumPy Array
        input_features = np.array(input_data).reshape(1, -1)
        print("🔹 Input Shape:", input_features.shape)

        # Make Prediction
        predicted_yield = model.predict(input_features)[0]
        predicted_yield = float(predicted_yield)  # ✅ Convert float32 → float

        return jsonify({
            "crop": crop,
            "state": state,
            "season": season,
            "area": area,
            "predicted_yield": round(predicted_yield, 2),
            "unit": "metric tons"
        })

    except Exception as e:
        print("🚨 Exception:", str(e))
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500
@yield_prediction.route('/get-options', methods=['GET'])
def get_options():
    try:
        # Get unique crop names, states, and seasons from the dataset
        crops = df["Crop"].unique().tolist()
        states = df["State"].unique().tolist()
        seasons = df["Season"].unique().tolist()

        return jsonify({
            "crops": crops,
            "states": states,
            "seasons": seasons
        })

    except Exception as e:
        return jsonify({"error": f"Error fetching options: {str(e)}"}), 500