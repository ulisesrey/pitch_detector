from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import librosa
import librosa.display
import matplotlib
matplotlib.use('Agg')  # This is the critical line to prevent GUI errors
import matplotlib.pyplot as plt

import numpy as np
import sys

from .contour import compute_f0
from .plots import plot_f0

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

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
PLOT_FOLDER = os.path.join(os.path.dirname(__file__), 'static/plots')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PLOT_FOLDER):
    os.makedirs(PLOT_FOLDER)

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

            # Define parameters for pitch detection
            fmin = 80
            fmax = 500
            hop_length = 256
            frame_length = 8 * hop_length

            # Let's create a plot
            
            # Compute
            f0pyin, voiced_flag, voiced_prob, times = compute_f0(data, fs, fmin, fmax, frame_length, hop_length)
            # # Plot
            # fig, ax = plt.subplots()
            # ylims = [75, 350]
            # ax = plot_f0(f0pyin, voiced_flag, voiced_prob, times, ax=ax, label=None)
            # # ax.set_ylim(ylims)
            # ax.set_title("F₀ estimation of your input")
            # # Save the plot to the static folder so the frontend can access it
            # plot_filename = f"{os.path.splitext(audio_file.filename)[0]}_f0_plot.png"
            # plot_filepath = os.path.join(PLOT_FOLDER, plot_filename)
            # plt.savefig(plot_filepath)
            # plt.close(fig) # Close the figure to free up memory

            # Return the path to the plot in the JSON response
            return jsonify({
                'message': 'File uploaded and analyzed successfully',
                'filepath': filepath,
                'f0': to_list(f0pyin), #.tolist(),
                'times': to_list(times), #.tolist(),
                'voiced_flag': to_list(voiced_flag),
                'voiced_prob': to_list(voiced_prob),
                'default_fmin': fmin,
                'default_fmax': fmax,
            }), 200

    except Exception as e:
        print(f"Server-side error during file upload/analysis: {e}", file=sys.stderr)
        # Also include the type of error for better debugging
        return jsonify({'error': f'Processing failed: {type(e).__name__} - {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

