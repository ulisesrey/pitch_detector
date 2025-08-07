# Initialization
import librosa
import pandas as pd
import os
from tqdm import tqdm
import numpy as np

# TODO: Will contain the F0 detection code
def compute_f0(data, fs, fmin, fmax, frame_length, hop_length):
    """Compute F0 Frequency using PYIN algorithm"""
    f0pyin, voiced_flag, voiced_prob = librosa.pyin(data.astype(float), 
                                    sr = fs, # sampling frequency
                                    fmin=fmin, 
                                    fmax=fmax, 
                                    frame_length=frame_length, 
                                    hop_length=hop_length) 

    # Convert frame indices to time (in seconds)
    times = librosa.frames_to_time(np.arange(len(f0pyin)), sr=fs, hop_length=hop_length)

    return f0pyin, voiced_flag, voiced_prob, times

    
if __name__ == "__main__":
    fmin = 50
    fmax = 450
    frame_length = 1024
    hop_length = 256  # or 512

    df = pd.read_csv("data/raw/basic_chinese_characters_ankicard.csv", index_col=0, header=0)
    save_path = "data/processed/f0_values.npz"
    f0_data = {}
    if os.path.exists(save_path):
         print(f"Save Path already exists in {save_path}!")
    for index, row in tqdm(df.iterrows()):
        wav_filepath = row["audio_full_path"]
        # try if file exists
        try:
            os.path.exists(wav_filepath)
            data, fs = librosa.load(wav_filepath, sr=None)
            f0pyin, voiced_flag, voiced_prob, times = compute_f0(data,
                                                                fs,
                                                                fmin,
                                                                fmax,
                                                                frame_length,
                                                                hop_length)
            f0_data[f"{index}_f0pyin"] = f0pyin
            f0_data[f"{index}_voiced_flag"] = voiced_flag
            f0_data[f"{index}_voiced_prob"] = voiced_prob
            f0_data[f"{index}_times"] = times
        except Exception as e:
                print(f"⚠️ Error processing {wav_filepath}: {e}")

    # Save all in one compressed .npz file
    np.savez_compressed(save_path, **f0_data)
