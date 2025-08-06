import pandas as pd



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

    return df


if __name__ == "__main__":
    df = clean_df()
    print(df)
    df.to_csv("data/raw/basic_chinese_characters_ankicard.csv")
    filtered_df = df[df["Pinyin"].str.contains("ǎ", na=False)]
    print("end")