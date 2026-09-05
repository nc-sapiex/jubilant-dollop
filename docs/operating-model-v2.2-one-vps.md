# Operating model — v2.2 revised for one VPS

Applies to `jubilant-dollop` (regulatory knowledge platform) on `srv1447173`.
Sources: Agentic Development Platform v2.2 (29 Aug 2026) and the one-VPS revision.

Hermes in this session is the private specialist: architecture, review, deployment plans, memory curation. It does not edit the production repo on `main`, merge, deploy, or run production migrations.

## Disposition vs the earlier BMAD/GSD/Ponytail/Pi instruction

That stack is **not** used for this product. v2.2 already accepted dropping BMAD, GSD, Ponytail, OpenClaw, and Hermes-as-runtime. Net loop:

```
you (spec / merge)
  + Superpowers brainstorm on the trusted side
  + GitHub issues (already #1–#26)
  + implementer on a worker identity (Claude Code fail-closed; Codex only as cold reviewer on trigger)
  + Hindsight later, one bank per repo, not on the worker until the §6 trigger
  + Paperclip only when unattended governed runs are needed
```

BMAD trigger in v2.2 §6: first greenfield product needing a PRD — **web bundle, no infrastructure**. The PRD already exists in-repo. Do not stand up GSD `.planning/` as a second tracker (it would duplicate GitHub issue state). Local Hermes `planning-with-files` under `/home/developer/regulatory-knowledge-platform/.planning/` is specialist scratch, not the product tracker.

## Configuration on this host (one VPS stepping stone)

Not Configuration A (Mac-only) and not Configuration B (two VPS). This is the one-VPS compromise: workable for a single trust domain, not the target state.

Conditions that must hold before any agent mutates `jubilant-dollop`:

1. Paperclip (if used) runs as OS user `paperclip`, home `0700`. Its Postgres is loopback/unix socket. Password not in the worker environment.
2. Implementer runs as non-root `wk-main`: no sudo, no `docker` group, no `docker.sock`, no host SSH keys, no production secrets.
3. Paperclip Environment is `driver: ssh` to `127.0.0.1` as `wk-main`, **not** `hermes_local` / local target. Local target = control-plane identity, unsandboxed.
4. Claude Code on `wk-main`: `failIfUnavailable`, `allowUnsandboxedCommands: false`, strict egress allowlist.
5. systemd slice for `wk-main` with `MemoryMax` / `CPUQuota` so extraction/Playwright cannot OOM Paperclip's DB or Hermes.

What this host currently is (measured 2026-09-05): `developer` runs Hermes, Paperclip (`127.0.0.1:3100`, embedded Postgres `:54329`), Docker, AEGIS work. Paperclip Sapiex agent is `hermes_local`. Claude Code is installed and **not logged in**. Pi has xAI OAuth only. There is no `wk-main` user. That is the "not to build" shape (control plane + local adapter on the trusted account). Do not dispatch implementer through `hermes_local`.

## Coding-worker policy (enforced)

Allowed: task branch, commit off `main`, install **project** deps in the worktree, lint/typecheck/tests, PR with a narrowly scoped token, task artifacts.

Approval required: dependency upgrades with security/build impact; database migration **generation**; new SaaS/API; infrastructure/IaC; authn/z; billing.

Denied: merge to `main`; force push; production deploy; production database migration; reading host credentials; disabling tests/security checks; unrestricted outbound network.

T01 (PostgreSQL 18 + pgvector on this VPS) is **infrastructure**, not an allowed coding-worker task. It needs explicit approval and must not share Paperclip's embedded Postgres.

## Product vs platform databases

| Database | Owner | Port today | Role |
|----------|-------|------------|------|
| Paperclip embedded PG | Paperclip | 54329 loopback | Issues, runs, tokens |
| RKP PostgreSQL 18 + pgvector ≥ 0.8.2 | product (`jubilant-dollop`) | not installed | Knowledge graph + DBOS |
| AEGIS Postgres | AEGIS local | if any | Out of scope |

Do not put RKP data in Paperclip's embedded instance.

## Hermes specialist outputs (this session)

- Architecture critique + threat model
- R0 acceptance and delivery phases
- Memory candidates (review, do not auto-retain unattended)

Hermes does not: `git push` to `main`, `apt install postgresql`, Docker compose up of product DB without approval, merge PRs.

## Reintroduction triggers (from v2.2 §6, unchanged)

- Second VPS: first client repo or first incident (shared-kernel escape, loopback leak, or contention).
- Cold Codex reviewer: defect reaches `main`, or you stop reading every PR line.
- Worker Hindsight: three context-loss incidents + bank-scoped tokens.
- Planner agent: more parallel streams than you can spec by hand.
- BMAD web bundle only: another greenfield PRD.
- GSD Core: milestone outgrows issue-per-story **and** you accept dual state.
- Chat intake (Hermes gateway / OpenClaw): phone-first becomes routine **and** the pipeline is already trusted.

## Residual risks on one VPS

- Shared kernel: bwrap escape is root next to Paperclip secrets and (once installed) RKP evidence.
- Loopback: test `curl 127.0.0.1:5432` from inside the sandbox; do not assume blocked.
- Contention with Hermes (RK-06): OCR concurrency 1; `wk-main` MemoryMax before any VLM OCR.
- Paperclip Environments BETA: if SSH-to-localhost misbehaves, fallback is `process` adapter wrapping `ssh wk-main claude -p …`, still not `hermes_local`.
- Review depth: Superpowers review subagent + human merge. No standing reviewer agent.
