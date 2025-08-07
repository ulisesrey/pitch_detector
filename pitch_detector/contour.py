# Initialization
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy
import scipy.fft
import numpy as np
import librosa
import librosa.display
import pandas as pd
import os
from tones import TONE_DICT

def plot_f0(data, fmin, fmax, frame_length, hop_length, label=None):
    """Calculate and plot F0 Frequency using PYIN algorithm"""
    f0pyin, voiced_flag, voiced_prob = librosa.pyin(data.astype(float), 
                                    sr = fs, # sampling frequency
                                    fmin=fmin, 
                                    fmax=fmax, 
                                    frame_length=frame_length, 
                                    hop_length=hop_length) 

    # Convert frame indices to time (in seconds)
    times = librosa.frames_to_time(np.arange(len(f0pyin)), sr=fs, hop_length=hop_length)

    # Plot
    #plt.figure(figsize=(10, 4))
    plt.plot(times, f0pyin, color='grey')

    # Formatting
    plt.xlabel('Time (s)')
    plt.ylabel('Fundamental Frequency (Hz)')
    plt.title(f'F₀ estimation of {label}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    #plt.show()


if __name__ == "__main__":
    # Parameters
    sound_data_root = "data/sounds"
    fmin = 50
    fmax = 450
    frame_length = 1024
    hop_length = 256  # or 512
    
    df = pd.read_csv("data/raw/basic_chinese_characters_ankicard.csv", header=0)

    for tone, tone_unicode in TONE_DICT.items():
        print(f"Starting with tone {tone}")
        if tone != "Tone 5 (neutral)":
            # Fitler for tone
            filtered_df = df[df["Pinyin_nfd"].str.contains(tone_unicode, na=False)]
        else:
            filtered_df = df
        for index, row in filtered_df.iterrows():
            print(index, row["sound_path"])
            try:
                filepath = os.path.join(sound_data_root, row["sound_path"]+".wav")
                print(filepath)
                data, fs = librosa.load(filepath,sr=None)
                plot_f0(data, fmin, fmax, frame_length, hop_length, label=tone)
            except Exception as e:
                print(f"⚠️ Error processing {filepath}: {e}")
            

        plt.show()