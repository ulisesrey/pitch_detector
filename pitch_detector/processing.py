import pandas as pd
import unicodedata
import re
import os
from tones import TONE_DICT

def clean_df(path="data/raw/basic_chinese_characters_ankicard.txt", sound_path="data/sounds"):

    column_names = ["character", "character_HTML", "pinyin_HTML",
        "english_gloss", "example1", "example2", "example3", "example4", "example5",
        "chinese_sentence_HTML", "english_translation", "pinyin_sentence", "sound_tag",
        "stroke_order_image", "char_set_number"
    ]

    df = pd.read_csv(path, sep="\t", names=column_names, engine="python", on_bad_lines="skip")
    # Process audio paths
    df["mp3_filename"] = df["sound_tag"].str.extract(r'\[sound:(.*?)\]')
    # wav file path
    df["wav_filename"] = df["mp3_filename"].str.replace(r'\.\w+$', '.wav', regex=True)
    df["audio_full_path"]=df["wav_filename"].apply(
        lambda x: os.path.join(sound_path, x)
        if pd.notna(x) else None)

    # Replace paths that don't exist with None
    df["audio_full_path"] = df["audio_full_path"].apply(
    lambda path: path if pd.notna(path) and os.path.exists(path) else None
)
    # drop rows with None or Nan audio full path
    df.dropna(subset=["audio_full_path"], inplace=True)
    # drop unneeded columns
    df.drop(columns=["sound_tag","mp3_filename", "wav_filename"], inplace=True)
    
    # get the pinyin without html
    df["pinyin"] = df["pinyin_HTML"].str.extract(r'<span class="[^"]+">([^<]+)</span>')
    # get the accent in unicode
    df["pinyin_nfd"]=df["pinyin"].apply(transform_accents)
    # detect tone
    df["tone"] = df["pinyin_nfd"].apply(identify_tone)

    return df

def transform_accents(word):
    """Convert words to have the accent.
    Ex: word='yī' becomes word_nfd='yī' (actually 'y ̄i')
    They loook the same but they are not.
     ̄ corresponds to \u0304
    If we run:
    "\u0304" in word
    False
    But if we run:
    "\u0304" in word_ndf
    True"""

    word_nfd = unicodedata.normalize("NFD", word)
    return word_nfd

def identify_tone(word_nfd):
    """Identify the corresponding Tone based on the NFD word
    NOTE: Tone is already specified in dataframe before doing this,
    Ex:
    <span class=""tone4"">诉</span>"""
    vowel_pattern = r"[aeiouü]"
    TONE_MARKS = list(TONE_DICT.values())
    tone_pattern = "[" + "".join(TONE_MARKS) + "]"

    if re.search(vowel_pattern, word_nfd):
        # calculate number of tones per word
        n_tones = len(re.findall(tone_pattern, word_nfd))
        if n_tones > 1:
            print("Multiple tones in word")
            return "Multiple Tones"
        else:
            for tone, unicode_tone in TONE_DICT.items():
                if unicode_tone in word_nfd:
                    return tone
            return "Tone 5 (neutral)"
    else:
        return "No vowel found"

    

if __name__ == "__main__":
    df = clean_df()
    print(df)
    df.to_csv("data/raw/basic_chinese_characters_ankicard.csv")
    filtered_df = df[df["pinyin"].str.contains("ǎ", na=False)]
    print("end")