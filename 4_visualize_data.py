import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CLEANED_FILE = os.path.join(PROJECT_ROOT, "data", "processed", "trending_cleaned.csv")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "data", "visuals", "trending_visualization.png")


def plot_trends(csv_path: str, output_path: str):
    df = pd.read_csv(csv_path)
    top_df = df.head(10).copy()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fig, axes = plt.subplots(2, 1, figsize=(12, 10))

    top_df = top_df.sort_values("stars", ascending=True)
    axes[0].barh(top_df["repository"], top_df["stars"], color="steelblue")
    axes[0].set_title("Top Repositories by Stars")
    axes[0].set_xlabel("Stars")
    axes[0].set_ylabel("Repository")

    language_counts = top_df["language"].value_counts()
    axes[1].pie(
        language_counts.values,
        labels=language_counts.index,
        autopct="%1.1f%%",
        startangle=90,
    )
    axes[1].set_title("Language Distribution")

    plt.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)

    print(f"Visualization saved to {output_path}")


if __name__ == "__main__":
    plot_trends(CLEANED_FILE, OUTPUT_FILE)
