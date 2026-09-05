from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Fetcher(Protocol):
    def get(self, url: str) -> bytes: ...


@dataclass(frozen=True)
class WatchResult:
    url: str
    outcome: str  # "changed" | "no_change" | "failure"
    sha256: str | None
    alert: bool


def check_listing(
    *,
    url: str,
    fetcher: Fetcher,
    previous_sha256: str | None,
) -> WatchResult:
    """FR-44: failure is not recorded as no_change."""
    import hashlib

    try:
        body = fetcher.get(url)
    except Exception:
        return WatchResult(url=url, outcome="failure", sha256=None, alert=True)
    digest = hashlib.sha256(body).hexdigest()
    if previous_sha256 is not None and digest == previous_sha256:
        return WatchResult(url=url, outcome="no_change", sha256=digest, alert=False)
    return WatchResult(url=url, outcome="changed", sha256=digest, alert=False)
