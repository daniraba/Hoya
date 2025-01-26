# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
# def predict_view(request):
#     if request.method == 'POST':
#         try:
#             body = json.loads(request.body)
#             # Extract data from the body
#             age = body.get('age')
#             blood_pressure = body.get('bloodPressure')
#             insulin_level = body.get('insulinLevel')
#             BMI = body.get('BMI')
#             diabetes_pedigree_function = body.get('diabetesPedigreeFunction')
#             blood_glucose = body.get('bloodGlucose')
#             family_history = body.get('familyHistory')
#             pregnancies = body.get('pregnancies')

#             # Perform prediction logic here
#             result = {
#                 "predictedType": "Type 1 Diabetes"  # Example prediction result
#             }

#             return JsonResponse(result, status=200)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)
