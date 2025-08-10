from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
# Enable CORS to allow your HTML file to make requests
CORS(app)

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET'])
def serve_index():
    """
    Serves the index.html file.
    """
    return render_template("index.html")

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    """
    API endpoint to receive and save an audio file.
    """
    try:
        # Check if the POST request has a file part
        if 'audio_file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        audio_file = request.files['audio_file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if audio_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if audio_file:
            # Save the file to the upload folder
            filepath = os.path.join(UPLOAD_FOLDER, audio_file.filename)
            audio_file.save(filepath)
            
            # Here you would add the analysis code, which we'll do in a later step
            print(f"File saved successfully at {filepath}")

            return jsonify({'message': 'File uploaded successfully', 'filepath': filepath}), 200

    except Exception as e:
        # Return an error message if something goes wrong
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Make sure to create a "templates" directory with your index.html file
    # and an "uploads" directory for the audio files.
    app.run(debug=True, port=5000)

