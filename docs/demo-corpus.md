# Demonstration corpus (R1–R5)

PRD H.27 required nine items. Stage 0 S0-2 dropped the non-Latin/bilingual page. Eight items remain. All English. Public or synthetic fixtures only.

| ID | Item | Used by |
|----|------|---------|
| DC-1 | Text-native PDF (RBI NBFC instrument or synthetic equivalent) | R1 extraction native route |
| DC-2 | Scanned PDF, Latin script | R1 VLM OCR route |
| DC-3 | Complex table | R1 table route / exception queue |
| DC-4 | Amendment (old + new source versions of the same instrument) | R5 mapping drill |
| DC-5 | Exception / proviso | R2 obligation + exception pass |
| DC-6 | Historical as-of question | R4 answer engine |
| DC-7 | Deliberately missing entity fact | R4 conditional outcome |
| DC-8 | Forced worker crash mid-workflow | R0 / NFR-07 |

Dropped vs PRD H.27: non-Latin-script or bilingual page. Re-add only via PRD revision.

Fixtures live under `tests/fixtures/` when added. Do not commit copyrighted PDFs if the licence is unclear; prefer official public RBI files with recorded URL + SHA-256, or synthetic PDFs built for the tests.
