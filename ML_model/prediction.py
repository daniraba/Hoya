import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load models and scaler
diabetes_model = joblib.load('diabetes_classification_model.pkl')
diabetes_type_model = joblib.load('diabetes_type_classification_model.pkl')
scaler = joblib.load('scaler.pkl')

# Ensure correct feature order by using the feature names from training
expected_features = scaler.feature_names_in_

# Create new patient data with the correct order
new_input = pd.DataFrame({
    'Glucose': [150],
    'BloodPressure': [70],
    'SkinThickness': [30],
    'Insulin': [80],
    'BMI': [28.5],
    'DiabetesPedigreeFunction': [0.5],
    'Age': [40],
    'Pregnancies': [2]
}, columns=expected_features)

# Scale the input data
new_input_scaled = scaler.transform(new_input)

# Predict if the person has diabetes
diabetes_prediction = diabetes_model.predict(new_input_scaled)

if diabetes_prediction[0] == 1:
    print("Diabetes Prediction: The person has diabetes.")

    # Predict the type of diabetes (Type 1 or Type 2)
    diabetes_type_prediction = diabetes_type_model.predict(new_input_scaled)

    if diabetes_type_prediction[0] == 0:
        print("Diabetes Type Prediction: Type 1 Diabetes")
    else:
        print("Diabetes Type Prediction: Type 2 Diabetes")
else:
    print("Diabetes Prediction: The person does NOT have diabetes.")
