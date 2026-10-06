from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "udaykumar5683"
OUT = Path("data/contributions.json")
URL = f"https://github.com/users/{USERNAME}/contributions"


def main() -> None:
    response = requests.get(
        URL,
        headers={"User-Agent": "github-profile-art/1.0"},
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        cells = soup.select("td[data-date][data-level]")

    days: list[dict] = []
    for cell in cells:
        raw_date = cell.get("data-date")
        level = cell.get("data-level")
        if not raw_date or level is None:
            continue

        label = cell.get("aria-label", "")
        match = re.search(r"(\d[\d,]*) contribution", label, re.I)
        count = int(match.group(1).replace(",", "")) if match else 0

        days.append(
            {
                "date": raw_date,
                "count": count,
                "level": int(level),
            }
        )

    if not days:
        raise RuntimeError("GitHub contribution calendar could not be parsed.")

    days.sort(key=lambda item: item["date"])

    counts = [item["count"] for item in days]
    total = sum(counts)
    best = max(days, key=lambda item: item["count"])

    current_streak = 0
    longest_streak = 0
    streak = 0
    for item in days:
        if item["count"] > 0:
            streak += 1
            longest_streak = max(longest_streak, streak)
        else:
            streak = 0

    for item in reversed(days):
        if item["count"] > 0:
            current_streak += 1
        else:
            break

    monthly = defaultdict(int)
    for item in days:
        monthly[item["date"][:7]] += item["count"]

    payload = {
        "username": USERNAME,
        "generated_at": date.today().isoformat(),
        "days": days,
        "stats": {
            "total": total,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "best_day": best,
            "months": dict(sorted(monthly.items())),
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved {len(days)} contribution days -> {OUT}")


if __name__ == "__main__":
    main()
