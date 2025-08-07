import pandas as pd
import unicodedata
import re
from tones import TONE_DICT

def clean_df(path="data/raw/basic_chinese_characters_ankicard.txt"):

    column_names = ["character", "character_HTML", "pinyin_HTML",
        "english_gloss", "example1", "example2", "example3", "example4", "example5",
        "chinese_sentence_HTML", "english_translation", "pinyin_sentence", "sound_tag",
        "stroke_order_image", "char_set_number"
    ]

    df = pd.read_csv(path, sep="\t", names=column_names, engine="python", on_bad_lines="skip")
    df["mp3_path"] = df["sound_tag"].str.extract(r'\[sound:(.*?)\]')
    # format agnostic path
    df["sound_path"] = df["mp3_path"].str.removesuffix(".mp3")
    # TODO: add full path to audio file
    # df["audio_full_path"]=os.path.join(root, df["sound_path"])
    
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
    NOTE: Tone is already specified in dataframe before this,
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