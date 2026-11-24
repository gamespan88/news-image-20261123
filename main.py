#!/usr/bin/env python3
"""Delivery program for the make.fun news-image-20261123 entry.

The newspaper page is drawn ahead of time by build_image.py and ships in
this repository as entry.png. At run time this program does one thing
only: it copies those bytes, unchanged, to /output/entry.png.

Standard library only -- no imaging library, no drawing, no network.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUTPUT_DIR = "/output"
OUTPUT = os.path.join(OUTPUT_DIR, "entry.png")


def main():
    if not os.path.isfile(SOURCE):
        print("entry.png is missing next to main.py", file=sys.stderr)
        return 1
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    # the copy must be exact: same byte count as the shipped page
    if os.path.getsize(OUTPUT) != os.path.getsize(SOURCE):
        print("copied entry.png does not match the shipped file",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
