# Tests

Run against the product Postgres on this VPS (`127.0.0.1:5433`), not Paperclip `:54329`.

```bash
export RKP_TEST_DATABASE_URL="postgresql://rkp:…@127.0.0.1:5433/rkp"
PYTHONPATH=. pytest -q
```

Store tests run without a database. Catalog, acquire, and DBOS replay tests skip unless `RKP_TEST_DATABASE_URL` is set.
