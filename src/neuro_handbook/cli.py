"""Minimal CLI entry point exposed as ``neuro-handbook``.

Intentionally tiny — just walk a BIDS dataset and pretty-print what's there.
The real value of this repo is the docs and library; the CLI exists so
``pip install -e .`` produces something runnable.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from neuro_handbook import __version__
from neuro_handbook.bids import walk_bids


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="neuro-handbook",
        description="Companion CLI for the neuro-handbook reference site.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_walk = sub.add_parser("walk-bids", help="List images in a BIDS dataset")
    p_walk.add_argument("root", type=Path, help="BIDS dataset root")

    args = parser.parse_args(argv)

    if args.command == "walk-bids":
        for img in walk_bids(args.root):
            ses = f"ses-{img.session}" if img.session else "—"
            print(f"sub-{img.subject:<10} {ses:<10} {img.datatype:<6} {img.suffix:<6} {img.path}")
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
