from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
DATA = Path("data/contributions.json")
OUT = Path("contrib-heatmap.svg")


def esc(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    days = payload["days"]
    stats = payload["stats"]

    # GitHub's contribution calendar is displayed as 7 rows of weekdays.
    # We align cells by weekday and let the x-axis represent weeks.
    first = datetime.fromisoformat(days[0]["date"]).date()
    start_offset = first.weekday()  # Monday=0
    ordered = [{"date": None, "count": 0, "level": 0}] * start_offset + days
    weeks = (len(ordered) + 6) // 7

    cell = 11
    gap = 3
    left = 32
    top = 26
    grid_w = weeks * (cell + gap)
    width = left + grid_w + 10
    height = 150

    rects = []
    for index, item in enumerate(ordered):
        week = index // 7
        row = index % 7
        x = left + week * (cell + gap)
        y = top + row * (cell + gap)
        level = max(0, min(5, int(item.get("level", 0))))
        delay = index * 0.006
        rects.append(
            f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" '
            f'fill="{PALETTE[level]}" opacity="0" aria-label="{esc(str(item.get("date") or ""))}">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.25s" begin="{delay:.3f}s" fill="freeze"/></rect>'
        )

    total = f'{stats.get("total", 0):,}'
    current = stats.get("current_streak", 0)
    longest = stats.get("longest_streak", 0)
    best = stats.get("best_day", {}).get("count", 0)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" rx="14" fill="#050505"/>
<text x="20" y="17" fill="#69f0a0" font-family="monospace" font-size="10">uday@github ~ $ ./contributions.sh</text>
<g font-family="monospace" font-size="8" fill="#7d8590">
  <text x="2" y="{top+7}">M</text>
  <text x="2" y="{top+28}">W</text>
  <text x="2" y="{top+49}">F</text>
</g>
<g>{''.join(rects)}</g>
<g font-family="monospace">
  <text x="20" y="133" fill="#ffffff" font-size="9">LAST YEAR</text>
  <text x="88" y="133" fill="#69f0a0" font-size="9">{total} contributions</text>
  <text x="250" y="133" fill="#7d8590" font-size="8">streak:{current}d</text>
  <text x="320" y="133" fill="#7d8590" font-size="8">best:{best}</text>
  <text x="380" y="133" fill="#7d8590" font-size="8">record:{longest}d</text>
  <text x="{width-112}" y="133" fill="#7d8590" font-size="8">LESS</text>
  <rect x="{width-84}" y="125" width="9" height="9" rx="2" fill="{PALETTE[0]}"/>
  <rect x="{width-70}" y="125" width="9" height="9" rx="2" fill="{PALETTE[2]}"/>
  <rect x="{width-56}" y="125" width="9" height="9" rx="2" fill="{PALETTE[4]}"/>
  <rect x="{width-42}" y="125" width="9" height="9" rx="2" fill="{PALETTE[5]}"/>
  <text x="{width-4}" y="133" text-anchor="end" fill="#7d8590" font-size="8">MORE</text>
</g>
</svg>'''
    OUT.write_text(svg, encoding="utf-8")
    print(f"Rendered {OUT}")


if __name__ == "__main__":
    main()
