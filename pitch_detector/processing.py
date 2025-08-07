import pandas as pd
import unicodedata
import re


def clean_df(path="data/raw/basic_chinese_characters_ankicard.txt"):

    column_names = ["Character", "CharacterHTML", "PinyinHTML",
        "EnglishGloss", "Example1", "Example2", "Example3", "Example4", "Example5",
        "ChineseSentenceHTML", "EnglishTranslation", "PinyinSentence", "SoundTag",
        "StrokeOrderImage", "CharSetNumber"
    ]

    df = pd.read_csv(path, sep="\t", names=column_names, engine="python", on_bad_lines="skip")
    df["mp3_path"] = df["SoundTag"].str.extract(r'\[sound:(.*?)\]')

    # get the pinyin without html
    df["Pinyin"] = df["PinyinHTML"].str.extract(r'<span class="[^"]+">([^<]+)</span>')
    df["Pinyin_nfd"]=df["Pinyin"].apply(transform_accents)
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

if __name__ == "__main__":
    df = clean_df()
    print(df)
    df.to_csv("data/raw/basic_chinese_characters_ankicard.csv")
    filtered_df = df[df["Pinyin"].str.contains("ǎ", na=False)]
    print("end")