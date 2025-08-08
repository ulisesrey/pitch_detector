import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import soundfile as sf
import matplotlib.pyplot as plt
import io
import base64

# Initialize Flask app
app = Flask(__name__)
# Enable CORS to allow requests from your HTML file running in the browser
CORS(app)

# A placeholder for your actual F0 computation and plotting function
def compute_f0_and_plot(audio_file_path):
    """
    This is a placeholder function for your F0 calculation and plotting logic.
    
    Replace the code inside this function with your actual implementation.
    
    Args:
        audio_file_path (str): The path to the temporary audio file.
    
    Returns:
        io.BytesIO: A BytesIO object containing the Matplotlib plot as a PNG image.
    """
    try:
        # Load audio file (using soundfile, a great alternative to librosa for simple IO)
        data, samplerate = sf.read(audio_file_path)
        
        # --- YOUR F0 COMPUTATION LOGIC GOES HERE ---
        # For this example, we'll just plot a simple sine wave
        import numpy as np
        duration = len(data) / samplerate
        t = np.linspace(0., duration, len(data))
        f0_dummy = 200 + 50 * np.sin(2 * np.pi * 0.5 * t)
        
        # --- YOUR PLOTTING LOGIC GOES HERE ---
        plt.figure(figsize=(10, 4))
        plt.plot(t, f0_dummy, color='purple', label='F0 Dummy Plot')
        plt.title('Fundamental Frequency (F0) Analysis')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        # Save the plot to a BytesIO object instead of a file
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close() # Close the plot to free up memory
        
        return buffer
        
    except Exception as e:
        print(f"Error during F0 computation: {e}")
        return None

@app.route('/process-audio', methods=['POST'])
def process_audio():
    """
    API endpoint to receive an audio file, process it, and return a plot.
    """
    try:
        # Get the audio file from the request
        audio_file = request.files.get('audio')
        if not audio_file:
            return jsonify({'error': 'No audio file provided'}), 400

        # Save the audio file to a temporary location
        temp_audio_path = 'temp_audio.wav'
        audio_file.save(temp_audio_path)
        
        # Call your F0 computation and plotting function
        plot_buffer = compute_f0_and_plot(temp_audio_path)
        
        # Clean up the temporary file
        os.remove(temp_audio_path)

        if plot_buffer:
            # Read the bytes and encode to a base64 string
            plot_base64 = base64.b64encode(plot_buffer.getvalue()).decode('utf-8')
            return jsonify({'plot_data': plot_base64})
        else:
            return jsonify({'error': 'Failed to generate plot'}), 500

    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({'error': f'An internal server error occurred: {e}'}), 500

if __name__ == '__main__':
    # You can change the host and port if needed
    app.run(debug=True, port=5000)
