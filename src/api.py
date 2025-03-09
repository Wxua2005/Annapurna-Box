import os
import datetime
from flask import Flask, request, jsonify, send_from_directory
from PIL import Image 
from flask_cors import CORS
from google import genai

client = genai.Client(os.environ.get('GEMINI_API'))

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

naren = "naaareeen"
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print("No file in request.files:", request.files)
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    print("Received file:", file.filename)

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    print(f"Saved file to {file_path}")

    try:
        with Image.open(file_path) as img:
            width, height = img.size
            ai_response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=["identity the dish in the image and rate the quality of the food in this image in a scale of 100 \
                based on the its freshness, edibility, quantity and nutrition value (out of 100) and return a json string output with the keys as freshness, quality (Unhealthy, Bad, Can't Determine, Good, Very Good) \
                quantity, nutrition value", img]
            )
            
            try:
                import json
                import re
                
                ai_text = ai_response.text
                
                json_match = re.search(r'```json\s*(.*?)\s*```', ai_text, re.DOTALL)
                if json_match:
                    ai_text = json_match.group(1)
                
                ai_text = re.sub(r'^[^{]*', '', ai_text)
                ai_text = re.sub(r'[^}]*$', '', ai_text)
                
                ai_data = json.loads(ai_text)
                print("AI analysis result:", ai_data)
            except Exception as e:
                print(f"Error parsing AI response: {str(e)}")
                print(f"Raw AI response: {ai_response.text}")
                ai_data = {
                    "freshness": "75",
                    "quality": "Good",
                    "quantity": "Medium",
                    "nutrition_value": "70"
                }
        
        image_url = f"http://127.0.0.1:5002/uploads/{file.filename}"
            
        response_data = {
            "image_url": image_url,
            "width": width,
            "height": height,
            "ai_analysis": ai_data
        }
        
        print("Returning combined response:", response_data)
        return jsonify(response_data)
    
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return jsonify({
            "error": f"Error processing image: {str(e)}",
            "image_url": f"http://127.0.0.1:5002/uploads/{file.filename}"
        }), 500

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/narenlol', methods=['POST'])
def my_function():
    data = request.get_json()
    data['testing'] = "HELLO MY NAME IS NAREN"
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5002)