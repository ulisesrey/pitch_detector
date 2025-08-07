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

def plot_f0(data, fmin, fmax, frame_length, hop_length, label=None):
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

    # Optionally overlay voicing probability
    # plt.plot(times, voiced_prob * f0_range_Hz[1], label='Voiced Probability (scaled)', alpha=0.5)

    # Formatting
    plt.xlabel('Time (s)')
    plt.ylabel('Fundamental Frequency (Hz)')
    plt.title(f'F₀ estimation of {label}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    #plt.show()


if __name__ == "__main__":
    filename = 'data/raw/oddcast-b07f2d6d-6b666bb1-8f934c9f-8e8628ec-19bf6b1e'
    filename = filename + ".wav"
    data, fs = librosa.load(filename, sr=None)
    file = data
    fmin = 50
    fmax = 450
    frame_length = 1024
    hop_length = 256  # or 512
    
    accent_dict = {
        "Tone 1 ( ̄)": "\u0304",
        "Tone 2 ( ́)": "\u0301",
        "Tone 3 ( ̌)": "\u030C",
        "Tone 4 ( ̀)": "\u0300",
        "Tone 5 (neutral)": "aeiouü"
    }
    tone = "Tone 1 ( ̄)"
    sounds = accent_dict[tone]
    print(sounds)
    df = pd.read_csv("data/raw/basic_chinese_characters_ankicard.csv", header=0)
    # format agnostic path
    df["sound_path"] = df["mp3_path"].str.removesuffix(".mp3")

    # Fitler for character
    filtered_df = df[df["Pinyin_nfd"].str.contains(sounds, na=False)]

    sound_data_root = "data/sounds"
    for index, row in filtered_df.iterrows():
        filepath = os.path.join(sound_data_root, row["sound_path"]+".wav")
        print(filepath)
        data, fs = librosa.load(filepath,sr=None)
        plot_f0(data, fmin, fmax, frame_length, hop_length, label=tone)
    plt.show()