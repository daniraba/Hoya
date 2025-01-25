import pytesseract
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import numpy as np

# Step 1: Load the Diabetes Dataset
file_path = '/mnt/data/diabetes_data.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Filter for 'Positive' diabetes cases
positive_cases = data[data['Diabetes_Status'] == 'Positive']

# Simulate Type 1 or Type 2 diabetes labels
def simulate_diabetes_type(row):
    if row['BMI'] < 25 and row['Insulin_Levels'] < 15:  # Example thresholds
        return 1  # Type 1
    elif row['BMI'] >= 25 or row['Triglyceride_Levels'] > 150:
        return 2  # Type 2
    else:
        return 2  # Default to Type 2

positive_cases['Diabetes_Type'] = positive_cases.apply(simulate_diabetes_type, axis=1)

# Encode categorical variables
categorical_columns = ['Family_History_of_Diabetes', 'Gestational_Diabetes', 'PCOS',
                       'Hypertension', 'Physical_Activity', 'Smoking', 'Alcohol_Consumption',
                       'Obesity', 'Diet', 'Sleep_Apnea']
for col in categorical_columns:
    positive_cases[col] = positive_cases[col].astype('category').cat.codes

# Step 2: Extract Text from Image Using OCR
def extract_text_from_image(image_path):
    # Load the image
    image = Image.open(image_path)
    # Extract text using Tesseract
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

# Simulate OCR: Replace with your actual image paths
image_texts = [
    "Patient has a history of Type 1 diabetes with elevated HbA1c levels.",
    "Type 2 diabetes diagnosed with insulin resistance and high BMI."
]

# Convert text data to numerical features using TF-IDF
vectorizer = TfidfVectorizer(max_features=100)
text_features = vectorizer.fit_transform(image_texts).toarray()

# Step 3: Combine OCR Text Features with Numerical Data
# Select numerical features from the dataset
numerical_features = positive_cases.drop(['Unnamed: 0', 'Diabetes_Status', 'Diabetes_Type'], axis=1).values

# Combine OCR features with numerical features
combined_features = np.hstack((numerical_features, text_features))

# Step 4: Define Target Variable
target = positive_cases['Diabetes_Type'].values

# Step 5: Split Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(combined_features, target, test_size=0.3, random_state=42)

# Step 6: Train a Random Forest Model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Step 7: Evaluate the Model
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Model Accuracy: {accuracy}")
print("Classification Report:")
print(classification_rep)
