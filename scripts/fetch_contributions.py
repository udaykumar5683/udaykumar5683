from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "udaykumar5683"
OUT = Path("data/contributions.json")
URL = f"https://github.com/users/{USERNAME}/contributions"


def parse_count(cell) -> int:
    candidates = [
        cell.get("aria-label", ""),
        cell.get("data-count", ""),
        cell.get_text(" ", strip=True),
    ]
    tool_tip = cell.find("tool-tip")
    if tool_tip:
        candidates.append(tool_tip.get_text(" ", strip=True))
        candidates.append(tool_tip.get("for", ""))

    text = " ".join(value for value in candidates if value)
    # Handles both "12 contributions..." and "1 contribution...".
    match = re.search(r"(\d[\d,]*)\s+contributions?\b", text, re.I)
    if match:
        return int(match.group(1).replace(",", ""))

    # A zero-contribution cell often says "No contributions".
    return 0


def main() -> None:
    response = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0 github-profile-art/2.0",
            "Accept": "text/html,application/xhtml+xml",
        },
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    cells = soup.select("td.ContributionCalendar-day[data-date]")
    if not cells:
        cells = soup.select("td[data-date][data-level]")

    days: list[dict] = []
    for cell in cells:
        raw_date = cell.get("data-date")
        raw_level = cell.get("data-level", "0")
        if not raw_date:
            continue

        try:
            level = int(raw_level)
        except ValueError:
            level = 0

        days.append(
            {
                "date": raw_date,
                "count": parse_count(cell),
                "level": max(0, min(5, level)),
            }
        )

    if not days:
        raise RuntimeError("GitHub contribution calendar could not be parsed.")

    days.sort(key=lambda item: item["date"])

    current_streak = 0
    longest_streak = 0
    streak = 0
    for item in days:
        if item["count"] > 0 or item["level"] > 0:
            streak += 1
            longest_streak = max(longest_streak, streak)
        else:
            streak = 0

    for item in reversed(days):
        if item["count"] > 0 or item["level"] > 0:
            current_streak += 1
        else:
            break

    monthly = defaultdict(int)
    for item in days:
        monthly[item["date"][:7]] += item["count"]

    total = sum(item["count"] for item in days)
    best = max(days, key=lambda item: (item["count"], item["level"]))

    # When GitHub exposes levels but omits tooltip counts, preserve the
    # truthful calendar levels and report that the exact count was unavailable.
    exact_counts = sum(1 for item in days if item["count"] > 0)
    estimated = exact_counts == 0 and any(item["level"] > 0 for item in days)

    payload = {
        "username": USERNAME,
        "generated_at": __import__("datetime").date.today().isoformat(),
        "days": days,
        "stats": {
            "total": total,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "best_day": best,
            "months": dict(sorted(monthly.items())),
            "counts_estimated": estimated,
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(
        f"Saved {len(days)} contribution days -> {OUT} "
        f"(nonzero levels={sum(1 for d in days if d['level'] > 0)}, exact counts={exact_counts})"
    )


if __name__ == "__main__":
    main()
