# jubilant-dollop

Automated regulatory knowledge platform (pilot).

Every published assertion resolves to an approved atomic obligation and an immutable source version with page-level provenance. Fail closed. No unsupervised legal publication.

This is not [AEGIS](https://github.com/nc-sapiex/AEGIS) and not StayComplied.

## Pilot coverage (Stage 0, 2026-09-05)

| Fact | Value |
|------|--------|
| Regulator | Reserve Bank of India (RBI) |
| Entity category | NBFCs |
| Language | English only (Hindi/bilingual excluded from the pilot corpus; `script_gate` remains in the schema unused) |
| Host | This Hermes VPS: `srv1447173.hstgr.cloud` (Ubuntu 24.04, 4 vCPU, 16 GB RAM, ~193 GB disk, no GPU) |
| Operating entity (Directus grant) | Sapiex |
| Retention | Evidence + pipeline/review audit: 7 years. `answer_audit`: 12 months |
| Model path (public regulatory material) | OpenAI, United States; native structured output + vision for crop checks. Pin model IDs in config. |

Authoritative specs: [`docs/prd.md`](docs/prd.md), [`docs/design-v2.md`](docs/design-v2.md). Decisions: [`docs/stage-0-decisions.md`](docs/stage-0-decisions.md).

## Releases (test gates, not dates)

| Release | Exit gate |
|---------|-----------|
| R0 Spike | Forced crash mid-workflow resumes; zero duplicate `source_version` rows |
| R1 Foundation | Any input traceable to evidence and a review queue after restart |
| R2 Structuring | Pilot obligations reviewed with evidence and dependencies |
| R3 Products | Changing one test obligation regenerates or flags every expected product |
| R4 Answers | No wrong-entity, superseded-source, or unsupported definitive answer in the eval set |
| R5 Updates | Simulated amendment detected, mapped, reviewed, propagated without manual inventory |

## Stack (design v2)

PostgreSQL 18 + pgvector ≥ 0.8.2 · DBOS Transact (Celery/Redis fallback if R0 fails) · Directus 12 (Open Innovation Grant) · Docling 2.x + VLM OCR in CPU mode · internal AI gateway.

## Status

Stage 0 locked. Next: R0 DBOS acquisition spike on this VPS. Do not start R1 schema work that depends on DBOS until the spike gate passes.
