# Initialization
import os
import matplotlib.pyplot as plt
import pandas as pd
import librosa
import numpy as np
from tones import TONE_DICT

NPZ_FILEPATH = "data/processed/f0_values.npz"

def plot_f0(data, fs, fmin, fmax, frame_length, hop_length, ax=None, label=None):
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
    if ax is None:
        ax = plt.gca()
    
    ax.plot(times, f0pyin, color='grey')

    # Formatting
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Fundamental Frequency (Hz)')
    ax.set_title(f'F₀ estimation of {label}')
    ax.legend()
    ax.grid(True)
    #ax.tight_layout()

def plot_tone_distribution(df):
    """Plot tone distribution"""
    df["tone"].value_counts().plot.bar()


def plot_f0_all(df, f0_data):
    """Plot the F0 of each tone based on the dataframe and the npz file generated
    with the contour module."""
    
    fig, axes = plt.subplots(ncols=len(df["tone"].unique()))
    for tone_n, tone in enumerate(df["tone"].unique()):
        filtered_df = df[df["tone"]==tone]    
        for index, row in filtered_df.iterrows():
            f0pyin = f0_data[f"{index}_f0pyin"]
            times = f0_data[f"{index}_times"]

            axes[tone_n].plot(times, f0pyin, alpha=0.3, color="grey")
            axes[tone_n].set_title(f"F₀ of {tone}")

    for ax in axes:
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("F₀ (Hz)")
        ax.set_ylim([50, 250])
        ax.set_xlim([0, 2])
        ax.grid(True)
            
if __name__ == "__main__":
    df = pd.read_csv("data/raw/basic_chinese_characters_ankicard.csv", index_col=0, header=0)
    f0_data = np.load("data/processed/f0_values.npz")
    #plot_tone_distribution(df)
    #plt.show()
    #plot_f0_all_tones(df)
    plot_f0_all(df, f0_data)
    plt.show()