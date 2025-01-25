from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import numpy as np
import joblib  # For loading the trained model
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Requests for frontend integration

# Configure Tesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Update path as needed

# Load the trained model
model = joblib.load('scaler.pkl')  # Replace with your model path

# API Route: Handle Image Upload and Prediction
@app.route('/predict', methods=['POST'])
def predict_diabetes():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if not file:
        return jsonify({"error": "Invalid file"}), 400

    try:
        # Step 1: Process the image
        image = Image.open(file)
        ocr_text = pytesseract.image_to_string(image)

        # Step 2: Convert OCR text into feature vector
        # Example: Dummy logic (you can expand based on your use case)
        bmi = 28.0  # Replace with real features extracted from OCR text
        insulin_levels = 20.0
        age = 45
        features = np.array([bmi, insulin_levels, age]).reshape(1, -1)

        # Step 3: Predict using the model
        prediction = model.predict(features)[0]
        diabetes_type = "Type 1" if prediction == 1 else "Type 2"

        return jsonify({
            "ocr_text": ocr_text,
            "diabetes_type": diabetes_type
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
