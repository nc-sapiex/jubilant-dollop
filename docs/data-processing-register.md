# Data-processing register

FR-54 / NFR-05. No external call path without a row. Public regulatory material only in the pilot.

| ID | Provider | Region | Data class | Purpose | Approval | Status |
|----|----------|--------|------------|---------|----------|--------|
| DPR-01 | OpenAI | United States | Public RBI PDF text, page crops of public instruments, prompts, schema | Structured obligation extraction; visual crop verification | Stage 0 S0-6 (2026-09-05). Model IDs to be pinned before first call | pending-config |
| DPR-02 | Directus licensing service | per Directus network-requirements docs | Licence key, instance validation payload (confirm from vendor docs; no client data) | Directus 12 grant licence validation | Required for DR-1. Record exact payload after first successful validation | pending-install |
| DPR-03 | Off-site S3-compatible backup | TBD | Encrypted database dumps, WAL, content-addressed evidence | NFR-08 / FR-05 | Not approved until bucket and encryption keys exist | missing |
| DPR-04 | External OCR API | — | — | Not used unless R1 benchmark shows CPU VLM cannot meet watcher cadence (DR-4) | not approved | unused |

Rules:

- No personal or client data on any row.
- Document content is untrusted data, not instructions (FR-25).
- Changing provider, region, or data class requires a new row and a review, not an in-place edit of an approved row.
