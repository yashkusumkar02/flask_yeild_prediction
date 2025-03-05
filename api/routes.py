from flask import Blueprint, request, jsonify

yield_prediction = Blueprint("yield_prediction", __name__)

# Sample crop yield data (kg per acre)
crop_yield_data = {
    "wheat": 450,
    "rice": 500,
    "corn": 600,
    "cotton": 300,
    "soybean": 400
}

@yield_prediction.route('/yield-prediction', methods=['POST'])
def predict_yield():
    try:
        data = request.get_json()
        crop_name = data.get("cropName", "").lower()
        area = float(data.get("area", 0))

        if crop_name not in crop_yield_data:
            return jsonify({"error": "Crop not found"}), 400

        predicted_yield = crop_yield_data[crop_name] * area
        return jsonify({"crop": crop_name, "area": area, "predicted_yield": round(predicted_yield, 2)})

    except Exception as e:
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500
