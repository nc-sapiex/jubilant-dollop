from __future__ import annotations

from dataclasses import dataclass

from dbos import DBOS, DBOSConfig, SetWorkflowID

from rkp.acquisition.catalog import Catalog, SourceVersion
from rkp.acquisition.store import EvidenceStore


@dataclass(frozen=True)
class AcquireResult:
    source_id: int
    source_version_id: int
    sha256: str
    url: str


def acquire(
    *,
    url: str,
    body: bytes,
    store: EvidenceStore,
    catalog: Catalog,
    headers: dict | None = None,
) -> AcquireResult:
    """Idempotent intake: CAS then catalog. Safe to replay after crash."""
    digest = store.put(body)
    recorded: SourceVersion = catalog.record_source_version(
        url=url, sha256=digest, headers=headers
    )
    return AcquireResult(
        source_id=recorded.source_id,
        source_version_id=recorded.source_version_id,
        sha256=recorded.sha256,
        url=recorded.url,
    )


def dbos_config(system_database_url: str) -> DBOSConfig:
    return DBOSConfig(
        name="rkp-acquisition",
        system_database_url=system_database_url,
        dbos_system_schema="dbos",
        run_admin_server=False,
        log_level="WARNING",
    )


@DBOS.step()
def store_bytes_step(root: str, body: bytes) -> str:
    return EvidenceStore(root).put(body)


@DBOS.step()
def catalog_version_step(
    dsn: str, url: str, sha256: str, headers: dict | None
) -> dict:
    rec = Catalog(dsn).record_source_version(url=url, sha256=sha256, headers=headers)
    return {
        "source_id": rec.source_id,
        "source_version_id": rec.source_version_id,
        "sha256": rec.sha256,
        "url": rec.url,
    }


@DBOS.workflow()
def acquire_workflow(
    dsn: str,
    root: str,
    url: str,
    body: bytes,
    headers: dict | None = None,
) -> dict:
    digest = store_bytes_step(root, body)
    return catalog_version_step(dsn, url, digest, headers)


def run_acquire_workflow(
    *,
    system_database_url: str,
    workflow_id: str,
    url: str,
    body: bytes,
    store: EvidenceStore,
    catalog: Catalog,
    headers: dict | None = None,
) -> AcquireResult:
    DBOS.destroy(workflow_completion_timeout_sec=0)
    DBOS(config=dbos_config(system_database_url))
    DBOS.launch()
    try:
        with SetWorkflowID(workflow_id):
            handle = DBOS.start_workflow(
                acquire_workflow,
                catalog.dsn,
                str(store.root),
                url,
                body,
                headers,
            )
            data = handle.get_result()
    finally:
        DBOS.destroy(workflow_completion_timeout_sec=5)
    return AcquireResult(
        source_id=data["source_id"],
        source_version_id=data["source_version_id"],
        sha256=data["sha256"],
        url=data["url"],
    )
