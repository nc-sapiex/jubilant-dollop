# Threat model — R0 on one VPS

Scope: `jubilant-dollop` through R0 (durable acquisition spike). Not a full STRIDE of R4 answers.

## Assets

- Public RBI PDFs and their SHA-256 (low confidentiality, high integrity)
- Pipeline history / DBOS checkpoints (integrity, audit)
- Directus licence key, OpenAI key (secrets)
- Paperclip master key and run tokens (out of product, on this host)
- Hermes session memory and this specialist's notes
- GitHub `main`

## Actors

- Public internet (watchers later)
- Coding agent (prompt-injectable)
- Hermes conversational agent (this process, `developer`)
- Human merger
- Directus licensing service, OpenAI US

## Threats and mitigations for R0

| ID | Threat | Mitigation now | Residual |
|----|--------|----------------|----------|
| T-1 | Agent writes `main` | Branch protection (not yet). Policy: PRs only | Until protection is on, a PAT can push main |
| T-2 | Agent reads host credentials | Denied in coding-worker policy; do not pass `~/.ssh` or Paperclip master.key | Same user today — policy is not isolation |
| T-3 | PDF prompt injection | FR-25 tests; content as data | No extraction yet |
| T-4 | Shared kernel escape | Two-VPS trigger; AppArmor when sandbox exists | Accepted for one-VPS |
| T-5 | Loopback to Paperclip PG :54329 | Socket perms; sandbox egress test | Untested |
| T-6 | RKP DB confused with Paperclip DB | Never use port 54329 for RKP | T01 not started |
| T-7 | OCR OOMs Hermes | OCR concurrency 1; MemoryMax on `wk-main` | No slice yet |
| T-8 | Directus/OpenAI data leak | Register rows DPR-01/02; public material only | Model IDs not pinned |
| T-9 | Hindsight poisoning | No worker retain | — |
| T-10 | Unattended Hermes_local run | Do not assign product work to Paperclip Hermes agent | Agent still exists idle |

## Trust boundary to add before T03

`wk-main` + SSH Environment + fail-closed Claude Code. Without it, T03 crash-replay code may be written, but it must not run as `developer` against a database that shares fate with Paperclip.
