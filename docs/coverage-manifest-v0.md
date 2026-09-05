# Coverage manifest v0

Version: 0
Status: draft (administrator-approved when R1 FR-01 lands)
Escalation owner: TBD (PRD J.30)

## Scope

- Regulator: Reserve Bank of India (RBI)
- Entity categories: NBFCs (pilot). Subcategories to be enumerated when the first instrument set is listed.
- Subjects: as listed per instrument; not a free crawl.
- Instrument types: master directions, circulars, notifications, rules that apply to NBFCs and are published as public English PDFs.
- Date coverage: as stated on each official listing; historical as-of questions are in scope for included instruments.
- Languages: English. Excluded: Hindi, bilingual, other non-Latin scripts.
- Cadence: TBD in R5; watcher failure must alert (FR-44).

## Allowed domains (draft)

Populate with official RBI hosts only. Discovery is confined to these domains. A query outside this coverage is reported as "outside approved coverage" (FR-01).

- `rbi.org.in` and documented official listing URLs (exact list to be frozen before first watcher run)

## Exclusions

- Client / confidential documents
- Non-RBI regulators
- Non-NBFC entity categories (UCBs, commercial banks, SFBs, RRBs) except where an instrument's stated applicability is needed as a negative test
- Hindi / bilingual pages

## Listing URLs

TBD — freeze before T04 watcher runs against production RBI URLs. Until then, tests use fixtures under `tests/fixtures/`.
