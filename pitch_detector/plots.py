# Initialization
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy
import scipy.fft
import numpy as np
import IPython
import librosa

filename = 'data/raw/oddcast-b07f2d6d-6b666bb1-8f934c9f-8e8628ec-19bf6b1e'
filename = filename + ".wav"
data, fs = librosa.load(filename, sr=None)

datalength = len(data)
time = np.arange(datalength)/fs

IPython.display.display(IPython.display.Audio(data,rate=fs))
plt.figure(figsize=(6,3))
plt.plot(time,data)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.yticks([])
plt.show()

# Some params
window_length_ms = 30
window_length = int(window_length_ms*fs/1000)
fft_length = window_length

f0_range_Hz = np.array([80, 450])
f0_range = np.round(fs/np.flipud(f0_range_Hz)).astype(int)
f0_range_fft_indices = np.round(f0_range_Hz*fft_length/fs).astype(int)
windowing_function = np.sin(np.pi*np.arange(0.5,window_length,1)/window_length)**2

window_step = window_length // 2
window_count = (datalength - window_length)//window_step - 1

f0estimates = np.zeros([window_count, 4])

f0pyin, voiced_flag, voiced_prob = librosa.pyin(data.astype(float), 
                                    sr = fs, # sampling frequency
                                    fmin=f0_range_Hz[0], 
                                    fmax=f0_range_Hz[1], 
                                    frame_length=window_length, 
                                    hop_length=window_step)    

f0estimates[:,3] = f0pyin[1:window_count+1]

for window_ix in range(window_count):
    window = data[(window_ix*window_step):(window_ix*window_step+window_length)] * windowing_function

    correlation = np.correlate(window,window,mode='full')[window_length-1:]
    power_spectrum = np.abs(scipy.fft.rfft(window,n=fft_length))**2
    cepstrum = scipy.fft.irfft(10*np.log10(power_spectrum))

    max_corr_index = np.argmax(correlation[f0_range[0]:f0_range[1]])+f0_range[0]
    max_frequency_index = np.argmax(
        power_spectrum[f0_range_fft_indices[0]:f0_range_fft_indices[1]]) +f0_range_fft_indices[0]
    max_cepstral_index = np.argmax(cepstrum[f0_range[0]:f0_range[1]])+f0_range[0]

    f0estimates[window_ix, 0] = fs/max_corr_index
    f0estimates[window_ix, 1] = max_frequency_index*fs/fft_length        
    f0estimates[window_ix, 2] = fs/max_cepstral_index


plt.figure(figsize=(8,4))
plt.plot(np.arange(0,window_count)*fs/(1000*window_step),f0estimates)
plt.legend(['Correlation','Spectrum','Cepstrum','pYIN'],bbox_to_anchor=(1.05, 1.0))
plt.title('Pitch contour estimates')
plt.xlabel('Time (s)')
plt.ylabel('Pitch (Hz)')
plt.show()