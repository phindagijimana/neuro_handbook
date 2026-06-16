"""Walk a BIDS dataset, yielding (subject, session, datatype, image-path).

A teaching implementation. Does not understand modality agnostic files,
inheritance, or derivatives. Use PyBIDS for production work.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

# Subset of BIDS entity keys we parse out of a filename.
_ENTITY_PATTERN = re.compile(
    r"(?P<key>[a-zA-Z]+)-(?P<value>[a-zA-Z0-9]+)"
)

_DATATYPES = {"anat", "dwi", "func", "fmap", "perf", "pet", "eeg", "meg", "ieeg"}


@dataclass(frozen=True)
class BIDSEntity:
    """A parsed key-value pair from a BIDS filename, e.g. ``sub-001``."""

    key: str
    value: str


@dataclass(frozen=True)
class BIDSImage:
    """A single imaging file inside a BIDS dataset."""

    path: Path
    subject: str
    session: str | None
    datatype: str
    entities: tuple[BIDSEntity, ...]

    @property
    def suffix(self) -> str:
        # e.g., 'T1w', 'bold', 'dwi'
        stem = self.path.name
        # Strip .nii / .nii.gz / .json
        for ext in (".nii.gz", ".nii", ".json"):
            if stem.endswith(ext):
                stem = stem[: -len(ext)]
                break
        return stem.rsplit("_", 1)[-1]


def _parse_entities(name: str) -> tuple[BIDSEntity, ...]:
    return tuple(
        BIDSEntity(key=m.group("key"), value=m.group("value"))
        for m in _ENTITY_PATTERN.finditer(name)
    )


def walk_bids(root: Path | str) -> Iterator[BIDSImage]:
    """Yield every imaging file in a BIDS dataset rooted at *root*.

    Recognises subject/session/datatype folders. Skips ``derivatives/`` and
    other top-level non-subject directories.
    """
    root = Path(root)
    if not root.is_dir():
        raise FileNotFoundError(f"Not a directory: {root}")

    for sub_dir in sorted(root.glob("sub-*")):
        if not sub_dir.is_dir():
            continue
        subject = sub_dir.name.split("-", 1)[1]

        session_dirs = sorted(sub_dir.glob("ses-*"))
        if session_dirs:
            for ses_dir in session_dirs:
                session = ses_dir.name.split("-", 1)[1]
                yield from _walk_datatypes(ses_dir, subject, session)
        else:
            yield from _walk_datatypes(sub_dir, subject, None)


def _walk_datatypes(
    folder: Path, subject: str, session: str | None
) -> Iterator[BIDSImage]:
    for datatype_dir in folder.iterdir():
        if not datatype_dir.is_dir() or datatype_dir.name not in _DATATYPES:
            continue
        for img in sorted(datatype_dir.iterdir()):
            if img.suffix not in {".nii", ".gz"}:
                continue
            yield BIDSImage(
                path=img,
                subject=subject,
                session=session,
                datatype=datatype_dir.name,
                entities=_parse_entities(img.name),
            )
