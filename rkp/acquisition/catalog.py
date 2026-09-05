from __future__ import annotations

from dataclasses import dataclass

import psycopg


SCHEMA_SQL = """
CREATE SCHEMA IF NOT EXISTS rkp;

CREATE TABLE IF NOT EXISTS rkp.sources (
    id              bigserial PRIMARY KEY,
    url             text NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS rkp.source_versions (
    id              bigserial PRIMARY KEY,
    source_id       bigint NOT NULL REFERENCES rkp.sources(id),
    sha256          char(64) NOT NULL,
    headers         jsonb NOT NULL DEFAULT '{}'::jsonb,
    official_status text NOT NULL DEFAULT 'unverified',
    legal_status    text NOT NULL DEFAULT 'unverified',
    created_at      timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_id, sha256)
);

CREATE INDEX IF NOT EXISTS source_versions_sha256 ON rkp.source_versions (sha256);
"""


@dataclass(frozen=True)
class SourceVersion:
    source_id: int
    source_version_id: int
    sha256: str
    url: str


class Catalog:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        with psycopg.connect(self.dsn) as conn:
            conn.execute(SCHEMA_SQL)
            conn.commit()

    def reset_for_tests(self) -> None:
        with psycopg.connect(self.dsn) as conn:
            conn.execute("DROP SCHEMA IF EXISTS rkp CASCADE")
            conn.execute("DROP SCHEMA IF EXISTS dbos CASCADE")
            conn.commit()
        self._ensure_schema()

    def record_source_version(
        self, *, url: str, sha256: str, headers: dict | None = None
    ) -> SourceVersion:
        headers = headers or {}
        with psycopg.connect(self.dsn) as conn:
            source_id = conn.execute(
                """
                INSERT INTO rkp.sources (url) VALUES (%s)
                ON CONFLICT (url) DO UPDATE SET url = EXCLUDED.url
                RETURNING id
                """,
                (url,),
            ).fetchone()[0]
            row = conn.execute(
                """
                INSERT INTO rkp.source_versions (source_id, sha256, headers)
                VALUES (%s, %s, %s::jsonb)
                ON CONFLICT (source_id, sha256) DO UPDATE
                  SET source_id = rkp.source_versions.source_id
                RETURNING id, sha256
                """,
                (source_id, sha256, psycopg.types.json.Json(headers)),
            ).fetchone()
            conn.commit()
        return SourceVersion(
            source_id=source_id,
            source_version_id=row[0],
            sha256=row[1],
            url=url,
        )

    def count_sources(self) -> int:
        with psycopg.connect(self.dsn) as conn:
            return conn.execute("SELECT count(*) FROM rkp.sources").fetchone()[0]

    def count_source_versions(self) -> int:
        with psycopg.connect(self.dsn) as conn:
            return conn.execute("SELECT count(*) FROM rkp.source_versions").fetchone()[0]
