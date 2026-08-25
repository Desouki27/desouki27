#!/usr/bin/env python3
"""Strip the avatar and all text out of a profile-3d-contrib SVG,
leaving only the 3D contribution calendar.

Usage:  python3 scripts/clean-3d.py profile-3d-contrib/profile-night-green.svg
"""

import pathlib
import re
import sys

# Set to True if a bare circle remains where the avatar was.
# Off by default: circles are sometimes used elsewhere in the drawing.
DROP_CIRCLES = False


def clean(svg: str) -> str:
    # avatar is drawn as an <image>, in either self-closing or paired form
    svg = re.sub(r"<image\b[^>]*?/>", "", svg)
    svg = re.sub(r"<image\b.*?</image>", "", svg, flags=re.S)

    # username, contribution counts, stars/forks, month and day labels
    svg = re.sub(r"<text\b[^>]*?/>", "", svg)
    svg = re.sub(r"<text\b.*?</text>", "", svg, flags=re.S)

    if DROP_CIRCLES:
        svg = re.sub(r"<circle\b[^>]*?/>", "", svg)
        svg = re.sub(r"<circle\b.*?</circle>", "", svg, flags=re.S)

    # collapse the blank lines the removals leave behind
    svg = re.sub(r"\n\s*\n+", "\n", svg)
    return svg


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: clean-3d.py <file.svg> [more.svg ...]")

    for name in sys.argv[1:]:
        path = pathlib.Path(name)
        if not path.exists():
            print(f"skip (missing): {path}")
            continue

        before = path.read_text(encoding="utf-8")
        after = clean(before)
        path.write_text(after, encoding="utf-8")

        removed = len(before) - len(after)
        viewbox = re.search(r'viewBox="([^"]+)"', after)
        print(f"cleaned {path}  (-{removed} bytes)")
        if viewbox:
            print(f"  viewBox is {viewbox.group(1)}")


if __name__ == "__main__":
    main()
