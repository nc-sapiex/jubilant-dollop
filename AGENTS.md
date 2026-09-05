# Agent notes

This repository is `nc-sapiex/jubilant-dollop`, the regulatory knowledge platform. It is not AEGIS and not StayComplied.

## Start rules

- Implement only from GitHub issues labelled `ready-for-agent` with testable acceptance and no open blockers.
- Specs: `docs/prd.md`, `docs/design-v2.md`, `docs/stage-0-decisions.md`.
- Canonical approval is a PostgreSQL fact. Directus cannot bypass the state machine.
- Secrets (Directus licence, API keys) never in git. Use `.env.example`.
- Public RBI material only. No client or personal data to model providers without a data-processing register row.

## Stack pins

PostgreSQL 18, pgvector ≥ 0.8.2, Directus 12, Docling 2.x, DBOS Transact. Celery/Redis only if R0 spike fails (record the decision).

## Host

`srv1447173.hstgr.cloud` — 4 vCPU, 16 GB, no GPU. This machine also runs Hermes. OCR concurrency starts at 1. Measure pages/hour before sizing Phase B.
