import json
import os

import pandas as pd


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
RAW_FILE = os.path.join(PROJECT_ROOT, "data", "raw", "trending_raw.json")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
CLEANED_FILE = os.path.join(PROCESSED_DIR, "trending_cleaned.csv")


def load_raw_data(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        payload = json.load(file)
    return payload.get("items", [])


def clean_dataframe(items):
    df = pd.DataFrame(items)

    if df.empty:
        raise ValueError("No rows found in raw dataset.")

    df["name"] = df["name"].astype(str).str.strip()
    df["owner"] = df["owner"].astype(str).str.strip()
    df["description"] = df["description"].fillna("No description provided").astype(str).str.strip()
    df["language"] = df["language"].fillna("Unknown").astype(str).str.strip()
    df["stars"] = pd.to_numeric(df["stars"], errors="coerce").fillna(0).astype(int)
    df["forks"] = pd.to_numeric(df["forks"], errors="coerce").fillna(0).astype(int)
    df["open_issues"] = pd.to_numeric(df["open_issues"], errors="coerce").fillna(0).astype(int)

    for column in ["created_at", "updated_at"]:
        df[column] = pd.to_datetime(df[column], errors="coerce")

    df = df.drop_duplicates(subset=["name"]).reset_index(drop=True)
    df = df.sort_values("stars", ascending=False).reset_index(drop=True)

    df.columns = [
        "repository",
        "description",
        "language",
        "stars",
        "forks",
        "open_issues",
        "updated_at",
        "created_at",
        "url",
        "owner",
    ]

    return df


if __name__ == "__main__":
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    raw_items = load_raw_data(RAW_FILE)
    cleaned_df = clean_dataframe(raw_items)

    cleaned_df.to_csv(CLEANED_FILE, index=False)
    print(f"Cleaned data saved to {CLEANED_FILE} ({len(cleaned_df)} rows)")
