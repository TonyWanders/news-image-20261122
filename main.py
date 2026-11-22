#!/usr/bin/env python3
"""make.fun entry: Sum up 22 November's world news in one image.

The entry is the finished picture held in this folder, entry.png.
This program only puts that picture where the judge expects it:
the file /output/entry.png (or a path given on the command line).

It is deterministic by construction: it copies the same bytes every
run, uses no network, no clock and no randomness, so two runs write
byte-identical output.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DEFAULT_TARGET = Path("/output/entry.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 16):
            digest.update(block)
    return digest.hexdigest()


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    target = Path(args[0]) if args else Path(os.environ.get("OUTPUT_PATH", DEFAULT_TARGET))
    target.parent.mkdir(parents=True, exist_ok=True)
    if not SOURCE.exists():
        print("entry.png is missing from this folder", file=sys.stderr)
        return 1
    shutil.copyfile(SOURCE, target)
    if sha256_of(SOURCE) != sha256_of(target):
        print("copy failed: output does not match entry.png", file=sys.stderr)
        return 1
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
