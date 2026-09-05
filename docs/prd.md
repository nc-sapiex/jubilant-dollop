# Automated regulatory knowledge platform — Product Requirements Document

Version 1.0 — 5 September 2026 — companion to design document v2

This document states what the platform must do, for whom, and how completion will be judged. It is deliberately silent on how the requirements are met except where a constraint is itself a requirement; the design document v2 of the same date covers implementation. Requirement identifiers are stable and are to be referenced in tickets, tests and release manifests. Priorities follow MoSCoW: Must (pilot cannot ship without it), Should (expected in pilot unless measurement shows it unnecessary), Could (post-pilot). Where a numeric target is marked "provisional", it is a starting point to be replaced by the figure measured in Phase A, not a claim that the figure is achievable.

Stage 0 lock (2026-09-05) is recorded in `docs/stage-0-decisions.md` and does not renumber any FR/NFR/RK identifier below.

## A. Problem and opportunity

1. Regulated entities and their advisers work from long, frequently amended instruments (master directions, circulars, notifications, rules) published as PDFs. Locating the current, applicable, in-force requirement for a specific entity on a specific date, with its exceptions and thresholds, is manual, slow and error-prone. Existing approaches — reading PDFs, maintaining spreadsheets of obligations, or generic retrieval-augmented chat over document dumps — either do not scale, lose the link between assertion and evidence, or produce confident answers unsupported by the source.

2. The opportunity is a system in which the mechanical work (acquisition, extraction, structuring, comparison, validation, indexing, dependency analysis, drafting) is automated, and scarce regulatory expertise is spent only on exceptions, interpretations and publication decisions — while every published statement remains traceable to an immutable source version.

## B. Goals and non-goals

3. Goals:
   (i) Every published regulatory assertion resolves to an approved atomic obligation and an exact, immutable source version with page-level provenance.
   (ii) A regulatory amendment is detected automatically and every affected obligation, page, checklist and approved answer is identified without manual inventory.
   (iii) A user can ask an applicability question for a stated entity profile and as-of date and receive one of three honest outcomes: definitive within stated assumptions; conditional pending named facts; unable to determine from approved coverage.
   (iv) Reviewer effort is directed by impact and uncertainty, and every reviewer correction is captured as labelled evaluation data.
   (v) The whole pipeline is replayable from original inputs under pinned configurations for audit.

4. Non-goals for the pilot:
   (i) Legal advice or a guarantee of legal accuracy; the product publishes reviewed knowledge with stated assumptions.
   (ii) Unsupervised publication of new or substantively changed regulatory conclusions.
   (iii) Coverage of more than one regulator and one entity category.
   (iv) Processing of confidential client documents (deferred until a data-processing decision is approved).
   (v) Fine-tuning models on reviewer corrections.
   (vi) Authoritative publication of non-Latin-script content before its evaluation gate passes.

## C. Users and roles

5. Roles:

| Role | Description | Primary needs |
|---|---|---|
| Platform administrator | Defines coverage manifest, sources, roles, budgets | Control of scope; visibility of pipeline health and cost |
| Regulatory reviewer | Domain expert approving evidence, obligations, applicability logic and products | Evidence, extracted structure and impact shown together; minimal, prioritised queue |
| Editor | Prepares wiki/checklist wording and consultancy interpretations | Clear separation of duty text from interpretation; regeneration on approval |
| Public visitor | Reads public wiki pages and quick answers | Current, cited, dated content |
| Subscriber | Saves an entity profile; receives change notifications; runs applicability questions | Relevance to own profile; as-of queries; auditable answers |
| Client (post-pilot) | Uploads own documents for private evidence and control testing | Isolation of private material; permission-aware answers |
| Auditor | Reconstructs how a published statement was produced | Release manifests, job history, review decisions |

6. Personas are not elaborated here; the reviewer role is the one whose time the product exists to conserve, and every functional requirement in Section E was tested against the question "does this reduce or misdirect reviewer attention".

## D. Scope of the pilot release

7. In scope: one regulator; one entity category; public instruments listed in the coverage manifest; English text with a gated route for any Hindi/bilingual pages; the full vertical slice from acquisition to published wiki page, checklist and approved answer; amendment detection and replay for the pilot corpus.

8. Out of scope: multiple regulators; client document ingestion; payment or subscription billing; mobile applications; public API for third parties.

9. Constraints that are themselves requirements:
   (i) Deployment on the available single VPS (16 GB RAM, 200 GB storage, no GPU) for the pilot.
   (ii) Directus 12 as reviewer application under the Open Innovation Grant licence; the operating entity's continued eligibility is a standing dependency (Section J).
   (iii) No external transfer of client or personal data to model or OCR providers without an entry in the data-processing register.
   (iv) Canonical data in PostgreSQL; approval is a database fact, not a CMS setting.

## E. Functional requirements

10. Coverage and acquisition:

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| FR-01 | Administrator can define a coverage manifest (regulator domains, entity categories, subjects, instrument types, listing URLs, date range, exclusions, cadence, escalation owner) | Must | Manifest saved and versioned; discovery is confined to manifest domains; a query outside coverage is reported as "outside approved coverage" |
| FR-02 | System acquires documents from scheduled watchers, intake folder, reviewer-submitted URL and authenticated API | Must | Each trigger creates exactly one source-version record with URL, headers, retrieval time, SHA-256 and fingerprints |
| FR-03 | Exact duplicates, changed bytes at the same URL and probable alternate copies are detected | Must | Re-submitting an identical file creates no new source version; a changed file at a known URL creates a new version linked to the same source |
| FR-04 | Uploads are type-checked and malware-scanned; active content rejected | Must | Test file with embedded script is rejected and logged |
| FR-05 | Original files stored immutably with content addressing and off-site encrypted copy | Must | Original bytes are retrievable by hash; deletion is not possible through the application; restore drill passes |
| FR-06 | Official status and legal effect recorded independently of byte identity | Must | Source-version record has separate `official_status` and `legal_status` fields, both defaulting to unverified |

11. Triage and extraction:

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| FR-07 | Per-page classification: text-native/scanned/mixed, language and script, tables, forms, footnotes, annexures, encryption, blank/duplicate pages | Must | Classification stored per page with route decision and risk flags |
| FR-08 | Extraction produces a typed document structure with item-level page and coordinate provenance | Must | Every text item, table cell and heading has page number and bounding box; a random sample of 50 items renders to the correct crop |
| FR-09 | Scanned and degraded pages routed to an OCR engine selected by corpus benchmark | Must | Route selection recorded per page with engine and version; benchmark results attached to the release |
| FR-10 | Non-Latin-script and bilingual pages follow a gated route requiring reviewer verification | Must | Such pages carry `script_gate=pending`; no obligation derived from them can reach `approved` until gate is passed for that script |
| FR-11 | Extraction QA checks run before structuring (coverage, clause continuity, table consistency, headers/footers, OCR noise, confusable characters, numeric spans) | Must | Each check records pass/fail per page; failing pages are reprocessed with alternate settings before human queue |
| FR-12 | Visual crop verification of every number, date and threshold that could be published | Must | A model reading of the crop under strict schema is compared deterministically with the extracted value; mismatch creates an extraction exception |
| FR-13 | Encrypted, unreadable or password-protected documents routed to exception queue | Must | Such documents never enter structuring |

12. Instrument identification and provision structure:

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| FR-14 | Extract issuer, title, type, reference number, publication/effective/update dates, stated applicability and amendment statements | Must | Fields populated with cited spans or null; no field populated without a span or `derived` label |
| FR-15 | Resolve instruments against the catalogue and create typed relations (`amends`, `supersedes`, `withdraws`, `retains`, `defines`, `excepts`) | Must | Relations carry evidence spans; ambiguous cases enter legal-resolution queue instead of being auto-set |
| FR-16 | Build provision tree (part/chapter/section/paragraph/definition/proviso/table/annexure/footnote) with stable logical IDs and immutable version IDs | Must | Same provision across two source versions shares logical ID; each version has its own version ID and coordinates |
| FR-17 | Resolve internal and external cross-references; unresolved references block definitive treatment where they may affect meaning | Must | An obligation depending on an unresolved reference cannot be approved as definitive |
| FR-18 | Search chunks are subordinate to the provision tree | Must | Every chunk maps to exactly one provision version; chunks are never cited as the legal unit |

13. Obligation extraction and verification:

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| FR-19 | Extract atomic obligations (actor, modality, action, object, conditions, trigger, deadline/frequency, exceptions, dependencies, source locators, excerpts, unresolved questions) under a strict schema | Must | 100% of gateway responses validate against the schema; invalid responses are rejected, not repaired silently |
| FR-20 | Missing facts remain null/unknown; permissions and recommendations are never recorded as duties | Must | Test set of permissive clauses yields zero `mandatory` records |
| FR-21 | Nine verification passes (entailment, coverage, modality, numeric, exception, duplicate, contradiction, citation, applicability completeness) run on every draft | Must | Each pass writes a structured `validation_issue` on failure; a draft with any open Must-level issue cannot enter obligation review as clean |
| FR-22 | Citation check resolves every locator to the stored source version and a provenance item | Must | Zero dangling citations in approved records |
| FR-23 | Model cannot set approval or publication status | Must | Schema has no such field; database constraint prevents non-reviewer writes to status |
| FR-24 | Every gateway call records prompt version, model, provider, region, schema version and cost | Must | Audit query returns these for any obligation version |
| FR-25 | Document content treated as untrusted data | Must | Injection test corpus (instructions embedded in PDFs) produces no change to system behaviour or output fields beyond flagging |

14. Review:

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| FR-26 | Five review queues (source integrity, extraction exception, legal resolution, obligation review, product review) with role-based access | Must | Reviewer sees only queues assigned to their role |
| FR-27 | Review screen shows source image, extracted text, proposed fields, linked definitions/exceptions, diff from prior version and impacted products together | Must | All seven elements visible without navigation for a sample of 20 records |
| FR-28 | Queue ordering by impact score (duty created/removed, dependent products, effective-date proximity, thresholds, uncertainty, conflicts) | Should | Ordering is reproducible from stored factors; reviewer can see why an item is ranked |
| FR-29 | Reviewers approve structured fields, not prose summaries; every correction stored as labelled feedback | Must | Correction records include field, old value, new value, reviewer, rationale |
| FR-30 | Regulatory state machine enforced in canonical schema (`extracted → validated → in_review → approved/rejected/needs_evidence`; `superseded/withdrawn` only via decisions) | Must | Illegal transitions are rejected at database level; CMS draft/publish cannot bypass |
| FR-31 | Batch review of similar records | Could | Reviewer can approve a set of mechanically identical corrections in one action with individual audit entries |

15. Applicability and products:

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| FR-32 | Approved conditions compiled to decision tables (fact, operator, value/unit, measurement date, true/false/unknown outcomes, source version, approval version) | Must | Rules engine evaluates a minimal entity profile deterministically; unknown facts produce `unknown`, never a default |
| FR-33 | AI may explain a computed applicability result but cannot compute it or supply missing facts | Must | Explanation text references the rule evaluation record; no numeric comparison is performed by the model |
| FR-34 | Approval event triggers dependency-aware generation of wiki page, quick-reference card, checklist, evidence request list, change-impact note, FAQ draft, search index and embeddings | Must | Each product stores dependency list and generator/template version |
| FR-35 | Duties and consultancy interpretations rendered with visibly distinct labels | Must | Rendered pages pass an automated check that no interpretation text appears in a duty-labelled block |
| FR-36 | Product changes classified mechanical/editorial/substantive/unresolved; only approved low-risk classes auto-publish | Must | A substantive change cannot be published without a product-review approval record |

16. Publication and answers:

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| FR-37 | Immutable release manifest listing source, obligation and product versions for every publication | Must | Any public page can be traced to its manifest |
| FR-38 | Pre-publication tests (links, citations, permissions, schema, representative queries) and post-publication smoke tests; automatic rollback on technical failure | Must | Injected broken citation blocks release; rollback restores prior manifest within the drill |
| FR-39 | Public, subscriber and client indexes are separate; permission filtering before retrieval | Must | Subscriber-only content never appears in public retrieval candidates, verified by test harness |
| FR-40 | Answer engine follows the defined query path (authenticate, classify, ask for missing facts, filter by effective date and applicability, lexical then semantic retrieval, expand linked material, reject stale/conflicted, prefer approved answer, validate claims, return structured answer, audit) | Must | Each step recorded in the answer audit; every material claim has a resolving citation |
| FR-41 | Three honest outcomes supported: definitive within assumptions; conditional pending named facts; unable to determine from approved coverage | Must | Evaluation set items designed for each outcome return the correct outcome type |
| FR-42 | Answer returns conclusion, assumptions, actions, exceptions, source and reviewed-through date | Must | Response schema validated |
| FR-43 | Answer audit stored under access, privacy and retention controls | Must | Retention job deletes expired records; access requires auditor role |

17. Amendment automation:

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| FR-44 | Scheduled watchers detect new or changed content; watcher failure is separately alertable; "no change" recorded only after a successful check | Must | Simulated network failure produces an alert, not a "no change" record |
| FR-45 | Provision-aware diff classifies addition, deletion, substitution, renumbering, cosmetic change and proposes old-to-new mappings | Must | Test amendment with renumbering maps ≥ 95% of unchanged provisions automatically (provisional target) |
| FR-46 | Affected obligations and products identified through dependency links; dependent products marked `review_required` where impact may be substantive | Must | Amendment drill flags every known dependent product in the test corpus |
| FR-47 | Re-extraction limited to changed context and linked definitions | Should | Unchanged provisions are not re-sent to the model |
| FR-48 | Reviewer briefing generated (what changed, why it may matter, affected entities and products) | Must | Briefing links to diff and dependency records |
| FR-49 | Subscriber notifications for saved profiles intersecting affected conditions | Should | Notification issued only after approval; content limited to approved change note |

18. Administration, audit and operations:

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| FR-50 | Every workflow and step records IDs, versions, timestamps, attempts, outputs, validation results and human decisions; workflows are replayable from original inputs under pinned configuration | Must | A completed pipeline run can be replayed and produces identical structured outputs or a documented diff |
| FR-51 | Idempotent processing: repeated jobs cannot create duplicate sources, provisions or obligations | Must | Re-running any stage on the same input creates zero new records |
| FR-52 | Budgets for tokens, OCR time and concurrency enforced per queue; circuit breakers for providers | Must | Exceeding a budget pauses the queue and alerts |
| FR-53 | Operational dashboard: queue age, retry rate, terminal failures, cost per page/obligation/query | Should | Metrics in Section G are visible without database access |
| FR-54 | Data-processing register listing provider, region, data class and approval for every external processing route, including Directus licence validation | Must | No external call path exists without a register entry |

## F. Non-functional requirements

19. Security and privacy:
   (i) NFR-01 (Must): public regulatory material and confidential client evidence separated at storage, database and retrieval layers.
   (ii) NFR-02 (Must): transport encryption everywhere; backups encrypted; secrets (including the Directus licence key) outside source control.
   (iii) NFR-03 (Must): least-privilege service accounts; administrative interfaces restricted; access logged.
   (iv) NFR-04 (Must): document processing in isolated workers without executable privileges.
   (v) NFR-05 (Must): personal or client data redacted or blocked before external model/OCR calls per the register.
   (vi) NFR-06 (Must): dependency versions pinned; security advisories for PostgreSQL, pgvector (≥ 0.8.2), Directus, Docling and the orchestration library tracked and patched.

20. Reliability and recoverability:
   (i) NFR-07 (Must): forced worker crash mid-workflow resumes from last checkpoint with no duplicate records.
   (ii) NFR-08 (Must): nightly database dump plus continuous WAL archive and evidence-store sync off-site; monthly restore drill with documented recovery time.
   (iii) NFR-09 (Must): publication rollback to prior release manifest demonstrated in each phase.
   (iv) NFR-10 (Should): watcher cadence met without backlog growth over a rolling seven days in steady state (measured, not assumed).

21. Performance (provisional, to be reset from Phase A measurements):
   (i) NFR-11: extraction throughput per route measured in pages per hour on the VPS; a documented figure exists before Phase B sizing. No target is set in advance for CPU-mode VLM OCR.
   (ii) NFR-12: public page render under 1 second at the 95th percentile from cache; answer engine response under 15 seconds at the 95th percentile excluding clarifying-question round trips.
   (iii) NFR-13: OCR/extraction load must not raise public page latency beyond NFR-12; enforced by worker resource caps.

22. Auditability:
   (i) NFR-14 (Must): for any published statement, an auditor can reconstruct source version, provision version, obligation version, validation results, reviewer decisions, release manifest and model/prompt versions within a single query path.
   (ii) NFR-15 (Must): audit and evidence records retained for the defined retention period; answer audit records subject to their own retention.

23. Accessibility and usability:
   (i) NFR-16 (Should): reviewer screens usable on a 13-inch laptop without horizontal scrolling for the seven required elements.
   (ii) NFR-17 (Should): public pages meet WCAG 2.2 AA for the components under the project's control.

## G. Success metrics

24. Metrics are measured, not assumed, and reported per phase:
   (i) Percentage of pages extracted without manual correction, by route and script.
   (ii) Percentage of obligations approved unchanged, corrected or rejected.
   (iii) Citation, numeric and crop verification failure rates.
   (iv) Provision coverage gaps (operative provisions without obligation or disposition).
   (v) Median reviewer minutes per approved obligation.
   (vi) Time from source publication or detection to reviewed impact note.
   (vii) Percentage of affected products correctly flagged in amendment drills.
   (viii) Answer escalation, missing-fact and unsupported-answer rates on the evaluation set.
   (ix) Cost per processed page, approved obligation and answered query.
   (x) Queue age, retry rate and terminal-failure volume.

25. Pilot success is declared only when the release gates in the design document (Section H) pass on the full evaluation set and metrics (i), (v) and (ix) have baselines from at least the pilot corpus. Improvement targets are set after baselines exist.

## H. Release plan

26. Releases align with design phases; each has an exit gate that is a test, not a date:

| Release | Content | Exit gate |
|---|---|---|
| R0 — Spike | Orchestration spike on the VPS; Directus 12 installed with grant licence | Crash-and-replay test passes (NFR-07); fallback decision recorded if not |
| R1 — Foundation (Phase A) | FR-01 to FR-13, FR-50 to FR-54; corpus extraction benchmark | Any input traceable through every step to evidence and a queue after forced restart |
| R2 — Structuring (Phase B) | FR-14 to FR-31 | Pilot obligations reviewed with complete evidence and dependencies |
| R3 — Products (Phase C) | FR-32 to FR-39 | Modifying a test obligation regenerates or flags every expected product |
| R4 — Answers (Phase D) | FR-40 to FR-43 | No known wrong-entity, superseded-source or unsupported definitive answer in the test set |
| R5 — Updates (Phase E) | FR-44 to FR-49 | Simulated amendment detected, mapped, reviewed and propagated without manual inventory |

27. Demonstration corpus for R1–R5 acceptance: at least one text PDF, one scanned PDF, one complex table, one non-Latin-script or bilingual page, one amendment, one exception, one historical as-of question, one deliberately missing fact and one forced worker crash.

Stage 0 S0-2 excludes Hindi/bilingual from the pilot corpus. The live demo list is `docs/demo-corpus.md` (eight items). FR-10 remains in the schema.

## I. Risks and mitigations

28. Risks:

| ID | Risk | Likelihood / impact | Mitigation |
|---|---|---|---|
| RK-01 | CPU-only VPS makes VLM OCR too slow for watcher cadence | Moderate / high | Measure in R1; scaling triggers defined; external OCR for public material permitted under register |
| RK-02 | Non-Latin-script extraction accuracy inadequate | Moderate / high (if Hindi in scope) | Gated route; separate evaluation set; no authoritative publication until gate passes. Pilot: English only, so RK-02 is dormant. |
| RK-03 | Directus licence eligibility lost (headcount or revenue threshold) or licence-validation data transfer unacceptable | Low / medium | Eligibility re-checked annually; commercial licence budgeted as contingency; canonical data in PostgreSQL keeps substitution feasible |
| RK-04 | Orchestration spike fails | Low / medium | Documented Celery/Redis fallback; spike time-boxed to two weeks |
| RK-05 | Model outputs pass schema but fail truth | Certain at some rate / high | Validators are the authority; crop check; reviewer gates; evaluation set grows from every production error |
| RK-06 | Single-VPS contention degrades public site | Moderate / medium | Worker resource caps; latency alerting; scaling triggers. This host also runs Hermes. |
| RK-07 | Scope creep to second regulator or client documents before gates pass | Moderate / medium | Non-goals in Section B; change requires PRD revision |
| RK-08 | Reviewer bottleneck | Moderate / high | Impact-ranked queues; structured approvals; measure minutes per obligation from R2 |
| RK-09 | Prompt injection via regulatory or uploaded PDFs | Low / high | Content treated as data; injection test corpus in evaluation set (FR-25) |

## J. Dependencies

29. External dependencies: availability of the regulator's official web sources and listing pages; approved model API provider(s) and their structured-output and multimodal capabilities; Directus Open Innovation Grant terms and the operating entity's continued eligibility; off-site S3-compatible backup destination; VPS provider.

30. Internal dependencies: a named escalation owner per coverage manifest; at least one regulatory reviewer available from R2; an approved data-processing policy before any client document or external OCR route is enabled.

## K. Open questions

31. Original list, closed 2026-09-05 in `docs/stage-0-decisions.md`:
   (i) Regulator and entity: RBI, NBFCs.
   (ii) Hindi/bilingual: English only.
   (iii) VPS: `srv1447173.hstgr.cloud`, 4 vCPU, 16 GB, no GPU; off-site backup still missing.
   (iv) Directus grant entity: Sapiex (thresholds not independently verified).
   (v) Retention: evidence and pipeline/review audit 7 years; answer_audit 12 months.
   (vi) Model: OpenAI, United States; pin model IDs before first call.

## L. Glossary

32. Terms:
   (i) Source version: an immutable, hash-identified retrieval of a regulatory instrument.
   (ii) Provision: a stable logical unit of an instrument (clause, definition, proviso, table, annexure) with versions over time.
   (iii) Atomic obligation: one separately testable duty, prohibition, permission or recommendation with actor, action, object, conditions and exceptions.
   (iv) Applicability condition: an executable rule mapping entity facts to whether an obligation applies.
   (v) Knowledge product: a wiki page, card, checklist, evidence list, impact note or approved answer generated from approved obligations.
   (vi) Release manifest: the immutable list of source, obligation and product versions constituting a publication.
   (vii) Gate: a test whose passage is required before a state transition; never removed on the basis of model agreement alone.
