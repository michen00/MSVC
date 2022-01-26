"""visualize inference"""

# core
import numpy as np
import pandas as pd

# visualization
import seaborn as sns
import matplotlib.pyplot as plt


def visualize(df: np.ndarray) -> plt.Axes:
    """plots one row of .predict_proba output"""
    # reformat
    df = (
        pd.DataFrame(df)
        .rename(columns={0: "negative", 1: "neutral", 2: "positive"})
        .T.reset_index()
        .rename(columns={"index": "valence", 0: "probability"})
    )
    df.probability = df.probability * 100  # %

    # adapted from https://stackoverflow.com/a/39566040/3772517
    SMALL_SIZE = 5
    MEDIUM_SIZE = 6
    BIGGER_SIZE = 7
    rc = plt.rc
    rc("font", size=SMALL_SIZE)  # controls default text sizes
    rc("axes", titlesize=SMALL_SIZE)  # fontsize of the axes title
    rc("axes", labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the xtick labels
    rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the ytick labels
    rc("legend", fontsize=SMALL_SIZE)  # legend fontsize
    rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title

    sns.set_style("white")
    palette = sns.color_palette("colorblind", 10)
    fig = sns.catplot(
        data=df,
        x="valence",
        y="probability",
        kind="bar",
        palette=[palette[8], palette[7], palette[9]],  # yellow, grey, light blue
        height=1.4,
        aspect=1.5,
    )
    ax = plt.gca()
    plt.bar_label(ax.containers[0], fmt="%.1f%%")  # adds probability % labels
    _ = plt.suptitle(
        f"prediction: {df.loc[df.probability == df.probability.max()].valence.iloc[0]}"
    )
    sns.despine(**dict.fromkeys(("left", "right", "top"), True))
    _ = plt.xlabel("")
    ax.set_ylim([0.0, 100.0])
    _ = plt.ylabel("")
    plt.tight_layout()
    return fig
