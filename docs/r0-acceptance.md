# R0 acceptance — orchestration spike

Product gate (design para 51, NFR-07): Stage 1 acquisition as one DBOS workflow on PostgreSQL 18; forced crash resumes; zero duplicate `source_version`; history queryable. Fail within two weeks → record Celery/Redis (DR-2).

## Execution overlay (must precede product gate)

- [ ] `wk-main` exists, non-root, no docker group
- [ ] systemd slice MemoryMax/CPUQuota
- [ ] Implementer is not Paperclip `hermes_local`
- [ ] Branch protection on `jubilant-dollop` `main`
- [ ] RKP Postgres ≠ Paperclip :54329
- [ ] T01 approved as infrastructure (human)

## Product acceptance (issues #2–#5)

- [ ] #2 PostgreSQL 18 + pgvector ≥ 0.8.2
- [ ] #3 Directus 12 grant — **blocked on licence key + eligibility**; do not install on core tier
- [ ] #4 DBOS acquisition + crash replay
- [ ] #5 Watcher skeleton (fixture URL, failure ≠ no-change)

Directus (#3) is in the R0 *release table* but is not required to prove NFR-07. Sequence: E1–E4 → #2 → #4 → #5. #3 in parallel once the licence key is in a secret store, not git.

## Demo corpus item for R0

DC-8 only (forced crash). DC-1..7 wait for R1.

## Human merge

Every PR. Hermes reviews; does not merge.
