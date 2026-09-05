# Stage 0 decisions

Locked 2026-09-05. Source: user answers in the Hermes planning session, plus measurements on this host.

| ID | Question (PRD §K) | Decision | Evidence / note |
|----|-------------------|----------|-----------------|
| S0-1 | Regulator and entity category | RBI; NBFCs | User. Coverage manifest v0. |
| S0-2 | Hindi / bilingual in pilot | English only. Hindi and other non-Latin scripts excluded from the pilot corpus. `script_gate` remains in the schema and routing table but is unused until a later PRD revision. | User. Deviates from design assumption 3(iv) and from PRD H.27 demo item "non-Latin-script or bilingual page". Demo corpus for R1–R5 therefore has 8 items, not 9. |
| S0-3 | VPS identity, vCPU, backups | Host = this Hermes box: `srv1447173` / `srv1447173.hstgr.cloud` (AEGIS alias `vps-control`, 187.124.97.7). 4 vCPU (AMD EPYC 9355P KVM), 16 GB RAM (~12 GB available at measurement), 193 GB disk (20 GB used), no GPU, Ubuntu 24.04.4, kernel 6.8.0-138. No off-site backup job found (only `dpkg-db-backup`). | Measured 2026-09-05T16:32Z. FR-05 off-site copy still needs an S3-compatible destination. |
| S0-4 | Directus grant entity | Sapiex. Staff who log into Directus Studio must be Sapiex representatives. Eligibility (under USD 5M revenue, under 50 employees) is assumed; re-check annually and on ownership/headcount change (DR-1). | User named the entity; thresholds not independently verified. |
| S0-5 | Retention | Evidence + pipeline/review audit: 7 years. `answer_audit`: 12 months. | User accepted the recommendation. |
| S0-6 | Model provider / region | OpenAI, United States. Native structured-output models for obligation JSON; vision models for crop checks. Public regulatory material only. Pin model IDs in config, not in this document. | User asked for a recommendation. Register row required before first live call (FR-54). |
| S0-7 | GitHub repo | `https://github.com/nc-sapiex/jubilant-dollop` (public). Not AEGIS, not StayComplied. | User. Repo existed as empty GitHub template (LICENSE + stub README) at 2026-09-05T16:16Z. |

## Contention (RK-06)

This host already runs Hermes Agent, local AEGIS work, and Paperclip. Extraction OCR concurrency starts at 1 page. Worker RAM ceiling is the remainder after PostgreSQL 4 GB, Directus 1 GB, website 1 GB, monitoring/proxy 1 GB. Measure pages/hour in R0/R1 before Phase B sizing.

## Still open (not Stage 0 blockers)

- Off-site S3-compatible bucket for FR-05 / NFR-08.
- Exact OpenAI model IDs (structured + vision).
- Directus grant eligibility evidence (headcount, revenue).
- Named escalation owner on the coverage manifest (PRD J.30).
- At least one regulatory reviewer from R2.
