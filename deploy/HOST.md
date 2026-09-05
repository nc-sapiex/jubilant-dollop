# R0 host notes (not secrets)

- Worker user: `wk-main` uid 1999, no docker group, password locked, nologin.
- systemd slice `wk-main.slice`: MemoryMax=4G.
- Product Postgres: Docker `rkp-postgres` image `pgvector/pgvector:pg18`, host `127.0.0.1:5433` only.
- Paperclip embedded Postgres remains `127.0.0.1:54329` — do not use it.
- Credentials: `/etc/rkp/rkp-postgres.env` mode 640 root:docker. Not in git.
- Evidence root: `/var/lib/rkp/evidence` owned by `wk-main`.
- Verified 2026-09-05: PostgreSQL 18.6, pgvector 0.8.6.
