from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare a portrait for ASCII conversion.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/source-prepped.png"))
    args = parser.parse_args()

    image = Image.open(args.source).convert("RGB")
    image = ImageOps.fit(image, (900, 900), method=Image.Resampling.LANCZOS)
    image = ImageOps.grayscale(image)
    image = ImageOps.autocontrast(image)
    image = ImageEnhance.Contrast(image).enhance(1.35)
    image.save(args.output)

    print(f"Prepared portrait -> {args.output}")


if __name__ == "__main__":
    main()
