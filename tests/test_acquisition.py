from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pytest

from rkp.acquisition.catalog import Catalog
from rkp.acquisition.store import EvidenceStore
from rkp.acquisition.workflow import acquire, run_acquire_workflow


FIXTURE_A = b"%PDF-1.4 fixture-a\n"
FIXTURE_B = b"%PDF-1.4 fixture-b-changed\n"
URL = "https://rbi.org.in/fixtures/md-nbfc.pdf"


@pytest.fixture
def evidence_root(tmp_path: Path) -> Path:
    root = tmp_path / "evidence"
    root.mkdir()
    return root


@pytest.fixture
def store(evidence_root: Path) -> EvidenceStore:
    return EvidenceStore(evidence_root)


def test_store_puts_bytes_at_sha256_path(store: EvidenceStore, evidence_root: Path) -> None:
    digest = store.put(FIXTURE_A)
    expected = hashlib.sha256(FIXTURE_A).hexdigest()
    assert digest == expected
    assert store.get(digest) == FIXTURE_A
    stored = evidence_root / digest[:2] / digest
    assert stored.read_bytes() == FIXTURE_A


def test_store_put_is_idempotent(store: EvidenceStore) -> None:
    a = store.put(FIXTURE_A)
    b = store.put(FIXTURE_A)
    assert a == b
    assert store.get(a) == FIXTURE_A


@pytest.fixture
def catalog() -> Catalog:
    url = os.environ.get("RKP_TEST_DATABASE_URL")
    if not url:
        pytest.skip("RKP_TEST_DATABASE_URL not set")
    c = Catalog(url)
    c.reset_for_tests()
    return c


def test_identical_bytes_do_not_create_new_source_version(catalog: Catalog, store: EvidenceStore) -> None:
    digest = store.put(FIXTURE_A)
    first = catalog.record_source_version(url=URL, sha256=digest, headers={"etag": "1"})
    second = catalog.record_source_version(url=URL, sha256=digest, headers={"etag": "1"})
    assert first.source_version_id == second.source_version_id
    assert catalog.count_source_versions() == 1
    assert catalog.count_sources() == 1


def test_changed_bytes_at_same_url_create_new_version_same_source(
    catalog: Catalog, store: EvidenceStore
) -> None:
    d1 = store.put(FIXTURE_A)
    d2 = store.put(FIXTURE_B)
    v1 = catalog.record_source_version(url=URL, sha256=d1, headers={})
    v2 = catalog.record_source_version(url=URL, sha256=d2, headers={})
    assert v1.source_id == v2.source_id
    assert v1.source_version_id != v2.source_version_id
    assert catalog.count_sources() == 1
    assert catalog.count_source_versions() == 2


def test_acquire_twice_is_idempotent(catalog: Catalog, store: EvidenceStore) -> None:
    r1 = acquire(url=URL, body=FIXTURE_A, store=store, catalog=catalog)
    r2 = acquire(url=URL, body=FIXTURE_A, store=store, catalog=catalog)
    assert r1.source_version_id == r2.source_version_id
    assert catalog.count_source_versions() == 1


def test_crash_between_store_and_catalog_does_not_duplicate(
    catalog: Catalog, store: EvidenceStore
) -> None:
    digest = store.put(FIXTURE_A)
    assert store.get(digest) == FIXTURE_A
    assert catalog.count_source_versions() == 0
    result = acquire(url=URL, body=FIXTURE_A, store=store, catalog=catalog)
    assert result.sha256 == digest
    assert catalog.count_source_versions() == 1
    replay = acquire(url=URL, body=FIXTURE_A, store=store, catalog=catalog)
    assert replay.source_version_id == result.source_version_id
    assert catalog.count_source_versions() == 1


def test_dbos_same_workflow_id_replays_without_new_version(
    catalog: Catalog, store: EvidenceStore
) -> None:
    dsn = os.environ["RKP_TEST_DATABASE_URL"]
    workflow_id = "acquire-dc8-replay"
    first = run_acquire_workflow(
        system_database_url=dsn,
        workflow_id=workflow_id,
        url=URL,
        body=FIXTURE_A,
        store=store,
        catalog=catalog,
    )
    second = run_acquire_workflow(
        system_database_url=dsn,
        workflow_id="acquire-dc8-replay",
        url=URL,
        body=FIXTURE_A,
        store=store,
        catalog=catalog,
    )
    assert first.source_version_id == second.source_version_id
    assert catalog.count_source_versions() == 1
    assert first.sha256 == hashlib.sha256(FIXTURE_A).hexdigest()
