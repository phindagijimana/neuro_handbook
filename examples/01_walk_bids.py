"""Walk a BIDS dataset and print one row per imaging file.

Run with the bundled fixture:

    python examples/01_walk_bids.py fixtures/sub-tiny

The fixture is a stripped-down BIDS dataset with empty placeholder files,
just enough to exercise the walker without shipping real data.
"""

from __future__ import annotations

import sys
from pathlib import Path

from neuro_handbook.bids import walk_bids


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: 01_walk_bids.py <bids-root>", file=sys.stderr)
        return 2
    root = Path(argv[1])
    n = 0
    for img in walk_bids(root):
        ses = f"ses-{img.session}" if img.session else "—"
        print(f"sub-{img.subject:<10} {ses:<10} {img.datatype:<6} {img.suffix:<6} {img.path}")
        n += 1
    print(f"\n{n} images found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
