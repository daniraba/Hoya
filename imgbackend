from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define OCR endpoint
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Perform OCR on the image
    try:
        img = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(img)
    except Exception as e:
        return jsonify({"error": f"Failed to process image: {str(e)}"}), 500
    finally:
        os.remove(file_path)  # Clean up

    # Return extracted text
    return jsonify({"extracted_text": extracted_text})

if __name__ == '__main__':
    app.run(debug=True)
