from __future__ import annotations

from pathlib import Path

OUT = Path("info-card.svg")

ROWS = [
    ("ROLE", "AI / ML ENGINEER"),
    ("FOCUS", "GenAI • LLMs • Multi-Agent Systems"),
    ("VISION", "Computer Vision • Deep Learning"),
    ("CLOUD", "AWS • S3 • EC2 • API Gateway"),
    ("STACK", "Python • TypeScript • Next.js • SQL"),
    ("EDU", "B.Tech — AI & ML • CGPA 8.1"),
    ("MODE", "BUILD • LEARN • EXPERIMENT • SHIP"),
]


def esc(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def main() -> None:
    row_h = 27
    height = 48 + len(ROWS) * row_h + 24
    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="520" height="{height}" viewBox="0 0 520 {height}">',
        '<rect width="100%" height="100%" rx="14" fill="#050505" stroke="#19372d"/>',
        '<text x="22" y="25" fill="#69f0a0" font-family="monospace" font-size="12">uday@github ~ $ neofetch</text>',
        '<line x1="20" y1="36" x2="500" y2="36" stroke="#1b332b"/>',
    ]

    for i, (key, value) in enumerate(ROWS):
        y = 62 + i * row_h
        begin = 0.15 + i * 0.10
        pieces.append(
            f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{begin:.2f}s" fill="freeze"/>'
            f'<text x="22" y="{y}" fill="#69f0a0" font-family="monospace" font-size="10">{esc(key):<8}</text>'
            f'<text x="112" y="{y}" fill="#ffffff" font-family="monospace" font-size="10">{esc(value)}</text>'
            f'</g>'
        )

    pieces.append(
        f'<text x="22" y="{height-14}" fill="#7d8590" font-family="monospace" font-size="8">STATUS: ONLINE // PROFILE CORE v1.0</text>'
    )
    pieces.append("</svg>")

    OUT.write_text("".join(pieces), encoding="utf-8")
    print(f"Rendered {OUT}")


if __name__ == "__main__":
    main()
