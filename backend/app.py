# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pytesseract
# from PIL import Image
# import numpy as np
# import joblib  # For loading the trained model
# import os

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)  # Allow Cross-Origin Requests for frontend integration

# # Configure Tesseract
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Update path as needed

# # Load the trained model
# model = joblib.load('scaler.pkl')  # Replace with your model path

# # API Route: Handle Image Upload and Prediction
# @app.route('/predict', methods=['POST'])
# def predict_diabetes():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files['file']
#     if not file:
#         return jsonify({"error": "Invalid file"}), 400

#     try:
#         # Step 1: Process the image
#         image = Image.open(file)
#         ocr_text = pytesseract.image_to_string(image)

#         # Step 2: Convert OCR text into feature vector
#         # Example: Dummy logic (you can expand based on your use case)
#         bmi = 28.0  # Replace with real features extracted from OCR text
#         insulin_levels = 20.0
#         age = 45
#         features = np.array([bmi, insulin_levels, age]).reshape(1, -1)

#         # Step 3: Predict using the model
#         prediction = model.predict(features)[0]
#         diabetes_type = "Type 1" if prediction == 1 else "Type 2"

#         return jsonify({
#             "ocr_text": ocr_text,
#             "diabetes_type": diabetes_type
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)
# ###################################################
from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import numpy as np
import cv2
import re
import joblib
import pandas as pd
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Requests for frontend integration

# Configure Tesseract
#pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Update path if needed

# Load models and scaler
diabetes_model = joblib.load('diabetes_classification_model.pkl')
diabetes_type_model = joblib.load('diabetes_type_classification_model.pkl')
scaler = joblib.load('scaler.pkl')

# Ensure correct feature order by using the feature names from training
expected_features = scaler.feature_names_in_


# Regular expressions to extract feature values from OCR text
regex_patterns = {
    'Glucose': r'Glucose\s*[:=]?\s*(\d+)',
    'BloodPressure': r'Blood\s*Pressure\s*[:=]?\s*(\d+)',
    'SkinThickness': r'Skin\s*Thickness\s*[:=]?\s*(\d+)',
    'Insulin': r'Insulin\s*[:=]?\s*(\d+)',
    'BMI': r'BMI\s*[:=]?\s*([\d.]+)',
    'DiabetesPedigreeFunction': r'Diabetes\s*Pedigree\s*Function\s*[:=]?\s*([\d.]+)',
    'Age': r'Age\s*[:=]?\s*(\d+)',
    'Pregnancies': r'Pregnancies\s*[:=]?\s*(\d+)'
}

# Home route to display a welcome message
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Diabetes Prediction API. Use the /predict endpoint to analyze an image."})


def process_image_and_extract_features(image):
    # Convert PIL image to OpenCV format
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale and apply thresholding for better OCR performance
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    processed_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 11, 2)

    # Extract text using OCR
    extracted_text = pytesseract.image_to_string(processed_img)

    # Extract features using regex
    parameters = {key: None for key in regex_patterns.keys()}
    
    for key, pattern in regex_patterns.items():
        match = re.search(pattern, extracted_text, re.IGNORECASE)
        if match:
            parameters[key] = float(match.group(1)) if '.' in match.group(1) else int(match.group(1))

    # Filter only extracted parameters
    important_text = {key: value for key, value in parameters.items() if value is not None}

    return parameters, extracted_text


@app.route('/predict', methods=['POST'])
def predict_diabetes():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if not file:
        return jsonify({"error": "Invalid file"}), 400

    try:
        # Step 1: Process the image and extract features
        image = Image.open(file)
        extracted_features, ocr_text = process_image_and_extract_features(image)

        # Check if any value is None (missing values)
        if None in extracted_features.values():
            missing_fields = [k for k, v in extracted_features.items() if v is None]
            return jsonify({
                "error": "Some values were not extracted correctly. Please check the image quality.",
                "extracted_text": ocr_text,
                "missing_fields": missing_fields
            }), 400

        # Step 2: Prepare data for model prediction
        print("This is the extracted shit")
        print({key: extracted_features[key] for key in expected_features})
        new_input = pd.DataFrame([{key: extracted_features[key] for key in expected_features}])

        # Scale input data
        new_input_scaled = scaler.transform(new_input)

        # Step 3: Predict if the person has diabetes
        diabetes_prediction = diabetes_model.predict(new_input_scaled)

        if diabetes_prediction[0] == 1:
            diabetes_status = "The person has diabetes."

            # Predict the type of diabetes (Type 1 or Type 2)
            diabetes_type_prediction = diabetes_type_model.predict(new_input_scaled)
            diabetes_type = "1" if diabetes_type_prediction[0] == 0 else "2"

        else:
            diabetes_status = "The person does NOT have diabetes."
            diabetes_type = "0"
        
        return jsonify({
            ## "diabetes_status": diabetes_status,
            "diabetes_type": diabetes_type,
            "extracted_features": extracted_features
        })
        

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict_from_data', methods=['POST'])
def predict_from_data():
    try:
        body = json.loads(request.data)
        # Extract data from the body
        Age = body.get('age')
        BloodPressure = body.get('bloodPressure')
        Insulin = body.get('insulinLevel')
        bmi = body.get('BMI')
        DiabetesPedigreeFunction = body.get('diabetesPedigreeFunction')
        Glucose = body.get('bloodGlucose')
        Pregnancies = body.get('pregnancies')
        SkinThickness = body.get('skinThickness')

        # Ensure correct feature order by using the feature names from training
    
        # Perform prediction logic here
        new_input = {
            'Glucose': float(Glucose),
            'BloodPressure': float(BloodPressure),
            'SkinThickness': float(SkinThickness),
            'Insulin': float(Insulin),
            'BMI': float(bmi),
            'DiabetesPedigreeFunction': float(DiabetesPedigreeFunction),
            'Age': float(Age),
            'Pregnancies': float(Pregnancies),
            
        }
        print(expected_features)
        print({key: new_input[key] for key in expected_features})

        new_input = pd.DataFrame([{key: new_input[key] for key in expected_features}])
        new_input_scaled = scaler.transform(new_input)

        # Step 3: Predict if the person has diabetes
        diabetes_prediction = diabetes_model.predict(new_input_scaled)

        if diabetes_prediction[0] == 1:
            diabetes_status = "The person has diabetes."

            # Predict the type of diabetes (Type 1 or Type 2)
            diabetes_type_prediction = diabetes_type_model.predict(new_input_scaled)
            diabetes_type = "1" if diabetes_type_prediction[0] == 0 else "2"

        else:
            diabetes_status = "The person does NOT have diabetes."
            diabetes_type = "0"

        return jsonify({
            'diabetes_type': diabetes_type
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)