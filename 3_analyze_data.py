import json
import os

import pandas as pd


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CLEANED_FILE = os.path.join(PROJECT_ROOT, "data", "processed", "trending_cleaned.csv")
SUMMARY_FILE = os.path.join(PROJECT_ROOT, "data", "processed", "analysis_summary.json")


def summarize_data(csv_path: str):
    df = pd.read_csv(csv_path)

    if df.empty:
        raise ValueError("No cleaned data available for analysis.")

    summary = {
        "total_repositories": int(len(df)),
        "average_stars": round(float(df["stars"].mean()), 2),
        "average_forks": round(float(df["forks"].mean()), 2),
        "top_repository": df.loc[df["stars"].idxmax(), "repository"],
        "top_repository_stars": int(df["stars"].max()),
        "most_common_language": df["language"].mode().iloc[0] if not df["language"].empty else "Unknown",
        "top_languages": df["language"].value_counts().head(5).to_dict(),
        "top_3_by_stars": df[["repository", "stars", "forks"]].head(3).to_dict("records"),
    }

    return summary


if __name__ == "__main__":
    summary = summarize_data(CLEANED_FILE)

    with open(SUMMARY_FILE, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    print("Analysis summary:")
    print(json.dumps(summary, indent=2))
    print(f"Summary saved to {SUMMARY_FILE}")
