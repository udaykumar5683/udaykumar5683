from __future__ import annotations

import argparse
import math
from pathlib import Path

RAMP = " .`:-=+*cs#%@"
OUT = Path("ascii-portrait.svg")

DEFAULT_ART = [
"                    .-=========-.",
"                .:=###############=:",
"              .+#####################+.",
"            .+#########################+.",
"           +#############%%#############+",
"         .#############%%%%%%############.",
"        +#############%%%%%%%%############+",
"       *#############%%%%%%%%%%############*",
"      *############%%%%%%%%%%%%############*",
"     +###########%%%%%%@%%%%%%%############+",
"     ###########%%%@@@@@@@@%%%%%############",
"    +##########%%%@@@@@@@@@@%%%%############+",
"    ##########%%%%@@@@@@@@@@%%%%############",
"    ##########%%%%@@@@@@@@%%%%%%############",
"    +###########%%%%%%@%%%%%%%%############+",
"     ############%%%%%%%%%%%%%%############",
"      *############%%%%%%%%%%############*",
"       *#############%%%%%%%%############*",
"        +#############%%%%%%############+",
"         .#############%%##############.",
"            +#########################+",
"              .+#####################+.",
"                .:=###############=:.",
"                    '---------'",
"",
"          [ U D A Y   K U M A R ]",
"             [ AI / ML ENGINEER ]",
]


def esc(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render(lines: list[str]) -> str:
    width = max(len(line) for line in lines)
    char_w = 8
    line_h = 11
    svg_w = width * char_w + 20
    svg_h = len(lines) * line_h + 20

    nodes = []
    for row, line in enumerate(lines):
        delay = row * 0.08
        y = 18 + row * line_h
        nodes.append(
            f'<text x="10" y="{y}" fill="#69f0a0" font-family="monospace" '
            f'font-size="10" opacity="0">{esc(line)}'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{delay:.2f}s" fill="freeze"/></text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">
<rect width="100%" height="100%" rx="14" fill="#050505" stroke="#19372d"/>
<text x="12" y="12" fill="#7d8590" font-family="monospace" font-size="7">PORTRAIT_RENDERER // MONOCHROME // AUTO-TYPE</text>
{''.join(nodes)}
</svg>'''


def image_to_ascii(path: Path, cols: int = 54) -> list[str]:
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:
        raise SystemExit("Install Pillow first: pip install Pillow") from exc

    image = Image.open(path).convert("L")
    ratio = image.height / max(image.width, 1)
    rows = max(12, int(cols * ratio * 0.48))
    image = ImageOps.autocontrast(image).resize((cols, rows))

    lines = []
    for y in range(image.height):
        row = []
        for x in range(image.width):
            brightness = image.getpixel((x, y))
            idx = int((255 - brightness) / 256 * len(RAMP))
            idx = min(len(RAMP) - 1, idx)
            row.append(RAMP[idx])
        lines.append("".join(row).rstrip())
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Create animated ASCII SVG.")
    parser.add_argument("--image", type=Path, help="Optional source photo.")
    args = parser.parse_args()

    lines = image_to_ascii(args.image) if args.image else DEFAULT_ART
    OUT.write_text(render(lines), encoding="utf-8")
    print(f"Rendered {OUT}")


if __name__ == "__main__":
    main()
