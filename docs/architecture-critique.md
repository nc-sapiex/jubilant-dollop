# Architecture critique — jubilant-dollop R0

Hermes specialist review. Product design remains PRD v1.0 + design v2. This document is the operating overlay for **how work is executed** on one VPS, not a rewrite of the provision tree.

## Verdict

The product architecture (evidence-first, provision tree as legal unit, DBOS spike before schema that depends on it, Directus as review UI not source of truth) is sound for a pilot. The **execution architecture currently on srv1447173 is not**. Hermes, Paperclip `hermes_local`, Docker, and AEGIS share the `developer` account. That is the configuration v2.2 explicitly says not to build.

Do not start T01/T02/T03 as the `developer` user. Split identities first, or accept that every coding-agent command is unsandboxed next to Paperclip's secrets and this Hermes session.

## Delivery phases (product)

Unchanged from the plan: R0 spike → R1 foundation → R2 structuring → R3 products → R4 answers → R5 updates. Gates are tests, not dates.

## Delivery phases (execution overlay, this VPS)

| Phase | Content | Exit |
|-------|---------|------|
| E0 | Operating model locked (this pack). GitHub remains the tracker. No GSD dual state. | This document + issue comments |
| E1 | `wk-main` user, systemd slice, no docker group. Paperclip Environment = SSH to localhost as `wk-main` **or** skip Paperclip and run Claude Code as `wk-main` by hand. | `id wk-main`; slice limits visible; `docker.sock` not readable |
| E2 | Claude Code on `wk-main` fail-closed; `/sandbox` shows no missing deps; loopback to Paperclip PG and (later) RKP PG blocked or unauthenticated from the sandbox | `curl 127.0.0.1:54329` from a sandboxed command fails |
| E3 | Branch protection + required CI on `jubilant-dollop`. Agents open PRs only. | Cannot push `main`; CI required |
| E4 | T01 Postgres 18 + pgvector as **approved IaC/install**, not an agent surprise. Separate from Paperclip embedded PG. | Extension version ≥ 0.8.2; not port 54329 |
| E5 | T03 DBOS crash-replay on a task branch, PR, human merge | NFR-07 |

E1–E3 are approval-gated infrastructure. E4 is the T01 issue. E5 is the R0 product gate.

## Threat model (summary)

Full notes: `threat-model.md` in this directory.

Trust domains: (1) GitHub `main` + CI, (2) Paperclip control plane, (3) RKP data plane, (4) Hermes conversational runtime, (5) worker `wk-main`. Today 2–5 are the same OS user.

Highest risks for R0:

- Prompt injection via PDFs (FR-25 / RK-09) once extraction exists — treat as data.
- Memory poisoning if Hindsight auto-retains on the worker (v2.2 deferred).
- Shared-kernel escape once bubblewrap is in play.
- Loopback reachability to Paperclip PG and, later, RKP PG.
- Contention: VLM OCR vs Hermes (RK-06).
- Directus licence validation egress (DPR-02) and OpenAI US (DPR-01) as the only approved outbound model path.

## Ponytail / BMAD / GSD / Pi

Not used. YAGNI is a line in `AGENTS.md`, not a plugin. Pi is not authenticated except xAI; Claude Code is not logged in. Do not invent a second implementer.

## Paperclip

Authoritative for **status, owner, budget, approvals** only after a project exists under active company `SAP` (`6b9e3121-…`) and the Environment is SSH-to-`wk-main`. Until then GitHub issues #1–#26 are the engineering tracker. Do not create Paperclip issues that duplicate GitHub without a sync rule.

Sapiex Paperclip company `SAPA` is archived. Active `SAP` has a Hermes local agent — do not assign `jubilant-dollop` implementation to it.

## Hindsight

One bank per repo, on the trusted side, later. Candidate memories are listed at the end of this session for human review. No auto-retain from unattended runs.

## What Hermes will not do

Install PostgreSQL, put Directus on this host, merge to `main`, force-push, read `.env` / licence keys, disable tests, or run as `hermes_local` implementer.
