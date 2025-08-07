# Initialization
import matplotlib.pyplot as plt
import pandas as pd


def plot_tone_distribution(df):
    """Plot tone distribution"""
    df["tone"].value_counts().plot.bar()
    


if __name__ == "__main__":
    df = pd.read_csv("data/raw/basic_chinese_characters_ankicard.csv", index_col=0, header=0)
    plot_tone_distribution(df)