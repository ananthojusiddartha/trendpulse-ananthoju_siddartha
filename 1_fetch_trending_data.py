import json
import os
from datetime import datetime

import requests


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
RAW_FILE = os.path.join(RAW_DIR, "trending_raw.json")


def fetch_trending_repos(query: str = "created:>2025-01-01", limit: int = 10):
    api_url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": limit,
    }

    response = requests.get(api_url, params=params, timeout=20)
    response.raise_for_status()
    payload = response.json()
    items = payload.get("items", [])

    cleaned_items = []
    for item in items:
        cleaned_items.append(
            {
                "name": item.get("full_name", "unknown/unknown"),
                "description": item.get("description") or "No description provided",
                "language": item.get("language") or "Unknown",
                "stars": item.get("stargazers_count", 0),
                "forks": item.get("forks_count", 0),
                "open_issues": item.get("open_issues_count", 0),
                "updated_at": item.get("updated_at"),
                "created_at": item.get("created_at"),
                "html_url": item.get("html_url"),
                "owner": item.get("owner", {}).get("login", "unknown"),
            }
        )

    return clean_items(cleaned_items)


def clean_items(items):
    cleaned = []
    for item in items:
        cleaned.append(
            {
                "name": str(item["name"]).strip(),
                "description": str(item["description"]).strip(),
                "language": str(item["language"]).strip() or "Unknown",
                "stars": int(item["stars"]),
                "forks": int(item["forks"]),
                "open_issues": int(item["open_issues"]),
                "updated_at": item["updated_at"],
                "created_at": item["created_at"],
                "html_url": item["html_url"],
                "owner": str(item["owner"]).strip(),
            }
        )
    return cleaned


if __name__ == "__main__":
    os.makedirs(RAW_DIR, exist_ok=True)
    trending_items = fetch_trending_repos()

    payload = {
        "fetched_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "count": len(trending_items),
        "items": trending_items,
    }

    with open(RAW_FILE, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)

    print(f"Fetched {len(trending_items)} repositories and saved to {RAW_FILE}")
