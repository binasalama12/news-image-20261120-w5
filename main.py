#!/usr/bin/env python3
"""Publisher for the Numbers XL front page - Friday 20 November 2026.

The artwork (entry.png, 1024x1024) ships inside this repository. This
program validates the bundled image and copies it to the output
directory; it runs on the bare Python standard library, nothing else.
"""

import os
import shutil
import sys
from pathlib import Path

TITLE = "Numbers XL front page - Friday 20 November 2026"
IMAGE_NAME = "entry.png"
MAX_BYTES = 1048576  # 1 MiB competition limit

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def locate_image():
    here = Path(__file__).resolve().parent
    return here / IMAGE_NAME


def check_image(path):
    if not path.is_file():
        return f"{IMAGE_NAME} not found next to main.py"
    size = path.stat().st_size
    if size > MAX_BYTES:
        return f"{IMAGE_NAME} is {size} bytes, over the {MAX_BYTES} byte limit"
    with path.open("rb") as handle:
        head = handle.read(len(PNG_MAGIC))
    if head != PNG_MAGIC and not head.startswith(JPEG_MAGIC):
        return f"{IMAGE_NAME} does not start with a PNG or JPEG signature"
    return None


def output_dir():
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if raw:
        return Path(raw)
    return Path("/output")


def main():
    source = locate_image()
    problem = check_image(source)
    if problem is not None:
        return fail(problem)

    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / IMAGE_NAME
    shutil.copyfile(source, target)

    size = target.stat().st_size
    print(f"{TITLE}")
    print(f"done: published {IMAGE_NAME} ({size} bytes) -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
