from __future__ import annotations

import hashlib

from rkp.acquisition.watcher import check_listing


URL = "https://rbi.org.in/fixtures/listing.html"
BODY = b"<html>listing v1</html>"


class OkFetcher:
    def get(self, url: str) -> bytes:
        assert url == URL
        return BODY


class FailFetcher:
    def get(self, url: str) -> bytes:
        raise OSError("simulated network failure")


def test_failure_alerts_and_is_not_no_change() -> None:
    result = check_listing(url=URL, fetcher=FailFetcher(), previous_sha256="abc")
    assert result.outcome == "failure"
    assert result.alert is True
    assert result.sha256 is None


def test_successful_unchanged_check_is_no_change() -> None:
    digest = hashlib.sha256(BODY).hexdigest()
    result = check_listing(url=URL, fetcher=OkFetcher(), previous_sha256=digest)
    assert result.outcome == "no_change"
    assert result.alert is False
    assert result.sha256 == digest


def test_first_successful_check_is_changed() -> None:
    result = check_listing(url=URL, fetcher=OkFetcher(), previous_sha256=None)
    assert result.outcome == "changed"
    assert result.alert is False
