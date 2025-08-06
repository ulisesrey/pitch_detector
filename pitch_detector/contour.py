# Initialization
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy
import scipy.fft
import numpy as np
import librosa
import librosa.display


filename = 'data/raw/oddcast-b07f2d6d-6b666bb1-8f934c9f-8e8628ec-19bf6b1e'
filename = filename + ".wav"
data, fs = librosa.load(filename, sr=None)

datalength = len(data)
time = np.arange(datalength)/fs

plt.plot(time, data)
plt.show()

# Typically fundamental frequencies lie roughly in the range 80 to 450 Hz
fmin = 80
fmax = 450
frame_length = 1024
hop_length = 256  # or 512

f0pyin, voiced_flag, voiced_prob = librosa.pyin(data.astype(float), 
                                    sr = fs, # sampling frequency
                                    fmin=fmin, 
                                    fmax=fmax, 
                                    frame_length=frame_length, 
                                    hop_length=hop_length) 



# Convert frame indices to time (in seconds)
times = librosa.frames_to_time(np.arange(len(f0pyin)), sr=fs, hop_length=hop_length)

# Plot
plt.figure(figsize=(10, 4))
plt.plot(times, f0pyin, label='Estimated F₀ (pyin)', color='blue')

# Optionally overlay voicing probability
# plt.plot(times, voiced_prob * f0_range_Hz[1], label='Voiced Probability (scaled)', alpha=0.5)

# Formatting
plt.xlabel('Time (s)')
plt.ylabel('Fundamental Frequency (Hz)')
plt.title('F₀ estimation using librosa.pyin')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
