'''
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import joblib
import json

@csrf_exempt
def predict_view(request):
    if request.method == 'POST':

        # Load models and scaler
        diabetes_model = joblib.load('diabetes_classification_model.pkl')
        diabetes_type_model = joblib.load('diabetes_type_classification_model.pkl')
        scaler = joblib.load('scaler.pkl')

        # Ensure correct feature order by using the feature names from training
        expected_features = scaler.feature_names_in_
    
        try:
            body = json.loads(request.body)
            # Extract data from the body
            age = body.get('age')
            blood_pressure = body.get('bloodPressure')
            insulin_level = body.get('insulinLevel')
            BMI = body.get('BMI')
            diabetes_pedigree_function = body.get('diabetesPedigreeFunction')
            blood_glucose = body.get('bloodGlucose')
            
            pregnancies = body.get('pregnancies')

            # Perform prediction logic here
            new_input = {
                age: age,
                blood_pressure: blood_pressure,
                insulin_level: insulin_level,
                BMI: BMI,
                diabetes_pedigree_function: diabetes_pedigree_function,
                blood_glucose: blood_glucose,
                pregnancies: pregnancies
            }

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

            return JsonResponse(diabetes_type, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
'''