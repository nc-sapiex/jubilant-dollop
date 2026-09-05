# Automated regulatory knowledge platform — revised design (v2)

Prepared: 5 September 2026 (revises the draft of the same date)

This revision incorporates the technology review carried out on 5 September 2026 and two changed facts: the production VPS is now available, and a Directus Open Innovation Grant licence key has been obtained. The regulatory design — evidence-first storage, provision tree as the legal unit of record, typed relations, deterministic checks surrounding AI, risk-based review and fail-closed answers — is unchanged. The component choices change in three places: (i) Directus 12 is confirmed as the reviewer application under the grant licence; (ii) Celery and Redis are replaced by Postgres-backed durable execution (DBOS Transact), subject to a Phase A spike; (iii) extraction keeps Docling as the structural backbone but routes scanned and degraded pages to vision-language OCR, with a corpus-specific benchmark and an explicit Hindi/Devanagari gate.

Stage 0 lock (2026-09-05): see `docs/stage-0-decisions.md`. Pilot is RBI + NBFCs, English only, on `srv1447173.hstgr.cloud`. The Hindi/Devanagari gate remains in the design; the pilot corpus does not exercise it.

## A. Summary of changes from the 5 September draft

1. Changes by section of the earlier draft:

| Earlier draft | v2 | Reason |
|---|---|---|
| Directus (version unstated) as reviewer UI, treated as open-source | Directus 12 under Open Innovation Grant licence; licence key configured; outbound access to the Directus licensing service permitted; grant eligibility recorded as a standing dependency | Directus 12 relicensed to MSCL in May 2026; unlicensed instances run on the capped core tier; the grant removes the caps |
| Celery workers + Redis broker + Celery Beat; hand-built `pipeline_jobs` ledger; Temporal as possible later replacement | DBOS Transact (Python) durable workflows, queues and cron on PostgreSQL; Redis removed; `pipeline_jobs` becomes a projection of DBOS state plus domain fields; Temporal question closed for the pilot | Durable, replayable, checkpointed execution is what the audit design needs; one fewer stateful service on a single VPS |
| Docling plus OCR fallback | Docling remains the document-structure backbone (typed document, page coordinates, MIT/LF governance); OCR route uses a VLM OCR engine via Docling plugin in CPU mode; external OCR APIs permitted only for public regulatory material; corpus benchmark and Devanagari gate added | 2026 VLM parsers exceed pipeline tools on raw OCR accuracy but generally lack the span-level provenance the citation checks depend on; non-Latin-script accuracy of many VLM parsers is poor |
| PostgreSQL (version unstated); pgvector "if used" | PostgreSQL 18; pgvector at or above 0.8.2 from the start, HNSW indexes with iterative scans for filtered retrieval; BM25 extension deferred pending evaluation | PostgreSQL 18 current; pgvector 0.8.2 fixed CVE-2026-3172; filtered ANN needed by the as-of/applicability query path |
| AI gateway enforces schema by post-hoc validation | Provider-native schema-constrained output as first layer; deterministic validators retained as second layer; VLM page-crop check added to numeric verification | Native structured output is now standard across major model APIs; it constrains shape, not truth |
| VPS "likely adequate", unspecified | Named single-VPS deployment with resource envelope, no GPU, explicit CPU-mode extraction budget | VPS is now available |

## B. Design verdict and operating principles

2. The optimal design remains an event-driven regulatory knowledge factory, not a sequence of manual PDF summarisation tasks. Original regulatory evidence is immutable; machines perform acquisition, extraction, structuring, comparison, validation, indexing, dependency analysis and product drafting; regulatory experts review only exceptions, material interpretations and publication candidates. Maximum automation does not mean unsupervised legal publication. No percentage of automatable work is asserted before a representative pilot is measured.

3. Assumptions (Stage 0 closed the unknowns):
   (i) Production VPS is 16 GB RAM / ~193 GB storage, Linux, no GPU, 4 vCPU (`srv1447173.hstgr.cloud`).
   (ii) Directus grant is held by Sapiex. Eligibility thresholds are assumed, not independently verified; re-check annually.
   (iii) Pilot: one regulator (RBI) and one entity category (NBFCs).
   (iv) English only in the pilot corpus. Hindi/bilingual instruments are out of corpus; the gated route stays in the schema.
   (v) Client documents are out of the pilot.

4. Operating principles:
   (i) Evidence first: preserve every original file, official URL, retrieval event, checksum and rendered page.
   (ii) One atomic obligation per record.
   (iii) Source text and interpretation are separate.
   (iv) Effective time is explicit.
   (v) Applicability is computed from facts; unknown facts remain unknown.
   (vi) Relationships are typed: `amends`, `supersedes`, `defines`, `creates`, `excepts`, `tests`, `publishes`.
   (vii) Every product has dependencies.
   (viii) Deterministic checks surround AI.
   (ix) Idempotent processing.
   (x) Fail closed.
   (xi) Provenance is preserved end to end (page and coordinates from extraction through obligation to published product).

## C. System architecture

5. Logical flow: official sources and uploaded PDFs → source watchers and intake API → evidence store (content-addressed objects) and DBOS durable workflows on PostgreSQL → extraction and structure workers → PostgreSQL 18 knowledge graph → validation and change engine → Directus 12 review queues → approved knowledge → wiki, checklists and quick answers.

6. Workers pass database and object identifiers through the queue, not PDF binaries. Workflow state, step checkpoints, attempts, errors and model/configuration versions are retained for audit and replay.

7. Components:

| Capability | Implementation (v2) | Purpose |
|---|---|---|
| Evidence storage | Controlled local filesystem for the pilot, content-addressed, plus encrypted off-site S3-compatible copy (destination still missing as of Stage 0) | Immutable PDFs, page images, extraction artifacts |
| Canonical data | PostgreSQL 18 with pgvector (≥ 0.8.2) | Regulatory records, versions, dependencies, embeddings |
| Reviewer application | Directus 12 (Open Innovation Grant licence) | Structured editing, roles, review states, draft/publish |
| Orchestration | DBOS Transact for Python on PostgreSQL | Replayable pipeline, retries, periodic watchers; no Redis |
| Extraction | Docling 2.x backbone; VLM OCR via Docling plugin for scanned/degraded pages; classical OCR as comparison | Layout-aware conversion with page and bounding-box provenance |
| AI gateway | Internal Python service wrapping OpenAI US | Native structured output, redaction, logging, budgets |
| Search | PostgreSQL full-text first; pgvector HNSW with iterative scans; BM25 deferred | Exact and conceptual discovery |
| Website | Existing web framework consuming approved views | Public and subscriber products |
| Monitoring | Metrics, structured logs, DBOS dashboard, dead-letter handling | Operational control |

8. Directus 12 notes: licence key required (core-tier caps otherwise); licence-validation egress must be recorded in the data-processing register; grant eligibility is on the entities whose staff log into Studio (Sapiex); regulatory state machine lives in PostgreSQL, not CMS draft/publish; `IP_TRUST_PROXY` must be set; Directus Flows are editorial/notifications only.

9. Orchestration notes: DBOS Transact over Celery/Redis; Celery/Redis is the documented fallback if the Phase A spike fails; Temporal is not in the pilot; DBOS state tables live in the same PostgreSQL instance in a separate schema.

10. Extraction notes: Docling retained for item-level provenance; VLM OCR inside Docling, not instead of it; no GPU, concurrency one page until measured; external OCR APIs only for public material under the register; Hindi/Devanagari gated and unused in this pilot.

## D. Automated pipeline

Stages 0–13 as in the 5 September v2 design: coverage manifest; acquisition workflow; triage and extraction routing; extraction QA including visual crop comparison; instrument identification; provision tree; atomic obligation extraction under native structured output; nine verification passes; five review queues; applicability compilation; product generation; publication with release manifests; answer engine with three honest outcomes; continuous amendment automation.

Routing table (design para 15): native text → Docling; scanned Latin → Docling + VLM OCR; mixed → page-level; complex tables → table model plus exception queue; non-Latin/bilingual → gated (unused in this pilot); encrypted/unreadable → exception queue.

Obligation JSON schema (design para 24): actor, modality (`mandatory|prohibited|permitted|recommended|explanatory|unknown`), action, object, applicability_conditions, trigger, deadline_or_frequency, exceptions, dependencies, source_locators, supporting_excerpts, unresolved_questions. Native structured output guarantees shape only; Stage 7 validators are the authority.

State machine: `extracted` → `validated` → `in_review` → `approved` | `rejected` | `needs_evidence`; `superseded` / `withdrawn` only via amendment or resolution decision.

## E–M

Control plane, canonical tables (`source_catalogues` through `data_processing_register`), security safeguards, quality gates, VPS resource envelope, implementation sequence Phases A–E, automation boundary, and decision record DR-1 through DR-7 are as in the 5 September v2 text.

Immediate build specification (para 64): one bounded workflow — `upload/official discovery → immutable storage → Docling extraction with provenance → provision tree → obligation JSON → automated validators including crop check → Directus 12 review → approved wiki page and checklist → dependency-aware amendment replay`, all as DBOS workflows on PostgreSQL 18.

First demonstration (para 65, as adjusted by Stage 0): DC-1 through DC-8 in `docs/demo-corpus.md`. Success means traceable, repeatable processing and correct escalation, not fluent summaries.

## Decision record (unchanged)

| ID | Decision | Reverses if |
|---|---|---|
| DR-1 | Directus 12 retained as reviewer UI under the Open Innovation Grant | Sapiex ceases to qualify and commercial licence cost is not accepted; or licence-validation data transfer is unacceptable |
| DR-2 | DBOS Transact on PostgreSQL replaces Celery/Redis | Phase A spike fails its pass criteria |
| DR-3 | Docling backbone with VLM OCR route | A VLM parser provides item-level coordinates with accuracy exceeding the Docling routes on the corpus benchmark |
| DR-4 | No GPU; CPU-mode extraction; external OCR APIs for public material only | Measured pages-per-hour cannot keep pace with watcher cadence |
| DR-5 | PostgreSQL 18 with pgvector ≥ 0.8.2; BM25 extension deferred | Retrieval evaluation shows lexical recall is the limiting factor |
| DR-6 | Native structured output as first layer, validators as authority | None anticipated; validators remain regardless |
| DR-7 | Non-Latin-script content gated until its evaluation set passes | Gate passes. Pilot corpus does not include such pages. |
