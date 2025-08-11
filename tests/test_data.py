import pytest
import pandas as pd
import os
import matplotlib.pyplot as plt
import librosa
from pitch_detector_app.contour import compute_f0
from pitch_detector_app.plots import plot_f0

# TODO: Should move to a config yaml?
TXT_PATH = "data/raw/basic_chinese_characters_ankicard.txt"
CSV_PATH = "data/raw/basic_chinese_characters_ankicard.csv"

def test_csv_exists():
    assert os.path.exists(CSV_PATH), f"CSV not found at {CSV_PATH}"

def test_txt_exists():
    assert os.path.exists(TXT_PATH), f"CSV not found at {TXT_PATH}"

def test_csv_columns():
    df = df = pd.read_csv(CSV_PATH)
    actual_columns = set(df.columns)
    # These are different than the ones in processing clean_df(), becaus new ones are generated
    expected_columns = {"character", "character_HTML", "pinyin_HTML",
        "english_gloss", "example1", "example2", "example3", "example4", "example5",
        "chinese_sentence_HTML", "english_translation", "pinyin_sentence", "audio_full_path",
        "stroke_order_image", "char_set_number"}
    
    missing = expected_columns - actual_columns

    assert expected_columns.issubset(actual_columns), f"Missing columns: {missing}"

def test_plot_returns_axes():
    # Call your plotting function (it should return an Axes object or array of Axes)
    # TODO: Change these to global params
    fmin = 50
    fmax = 450
    frame_length = 1024
    hop_length = 256
    wav_filepath = "data/examples/xiao_example.wav"
    data, fs = librosa.load(wav_filepath, sr=None)

    f0pyin, voiced_flag, voiced_prob, times = compute_f0(data, fs, fmin, fmax, frame_length, hop_length)
    ax = plot_f0(f0pyin, voiced_flag, voiced_prob, times)
    assert isinstance(ax, plt.Axes) or (
        hasattr(ax, "__iter__") and all(isinstance(a, plt.Axes) for a in ax)
    ), f"Expected matplotlib Axes, got {type(ax)}"



def test_tone_dict_exists_and_matches():

    from pitch_detector_app.tones import TONE_DICT
    expected = {
        "Tone 1 ( ̄)": "\u0304",
        "Tone 2 ( ́)": "\u0301",
        "Tone 3 ( ̌)": "\u030C",
        "Tone 4 ( ̀)": "\u0300",
        # "Tone 5 (neutral)": None
    }
    assert TONE_DICT == expected, f"TONE_DICT does not match expected values"
