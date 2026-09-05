from __future__ import annotations

import hashlib
from pathlib import Path


class EvidenceStore:
    """Content-addressed store. Path layout: {root}/{sha256[:2]}/{sha256}."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, data: bytes) -> str:
        digest = hashlib.sha256(data).hexdigest()
        path = self._path(digest)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            tmp = path.with_suffix(".tmp")
            tmp.write_bytes(data)
            tmp.replace(path)
        return digest

    def get(self, digest: str) -> bytes:
        return self._path(digest).read_bytes()

    def _path(self, digest: str) -> Path:
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError("digest must be sha256 hex")
        return self.root / digest[:2] / digest
