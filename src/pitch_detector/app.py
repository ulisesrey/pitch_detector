from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import librosa
import yaml

import numpy as np
import sys

from .contour import compute_f0

def to_list(arr):
    """Convert numpy array to Python list, turning NaN into None for JSON."""
    arr = np.asarray(arr)
    out = []
    for x in arr:
        if isinstance(x, np.generic):
            x = x.item()
        if isinstance(x, float) and np.isnan(x):
            out.append(None)
        else:
            out.append(x)
    return out

# Initialize Flask app
app = Flask(__name__)
# Enable CORS to allow your HTML file to make requests
CORS(app)

# ----------  LOAD VARIABLES FROM config.yaml  ----------
# Path to config.yaml (same directory as this file)
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# Extract pitch detection params
pitch_detection_config = config.get("pitch_detection", {})
FMIN = pitch_detection_config.get("fmin", 80)
FMAX = pitch_detection_config.get("fmax", 1500)
HOP_LENGTH = pitch_detection_config.get("hop_length", 256)
frame_length_multiplier = pitch_detection_config.get("frame_length_multiplier", 8)
FRAME_LENGTH = HOP_LENGTH * frame_length_multiplier
# ---------- /LOAD VARIABLES FROM config.yaml ----------

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

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
    API endpoint to receive, save, and analyze an audio file.
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
            
            #print(f"File saved successfully at {filepath}")

            # Now, perform the audio analysis
            data, fs = librosa.load(filepath, sr=None)
          
            # Compute
            f0pyin, voiced_flag, voiced_prob, times = compute_f0(data,
                                                                 fs,
                                                                 FMIN,
                                                                 FMAX,
                                                                 FRAME_LENGTH,
                                                                 HOP_LENGTH)

            # Return the data in JSON response
            return jsonify({
                'message': 'File uploaded and analyzed successfully',
                'filepath': filepath,
                'f0': to_list(f0pyin),
                'times': to_list(times),
                'voiced_flag': to_list(voiced_flag),
                'voiced_prob': to_list(voiced_prob),
                'default_fmin': FMIN,
                'default_fmax': FMAX,
            }), 200

    except Exception as e:
        print(f"Server-side error during file upload/analysis: {e}", file=sys.stderr)
        # Also include the type of error for better debugging
        return jsonify({'error': f'Processing failed: {type(e).__name__} - {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

