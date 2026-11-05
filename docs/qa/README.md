# QA evidence index

Trace each requirement to a test case, reproducible command, current run report, and gate state. `not_run` and `blocked` are not `passed`.

Current verification report: [`workspace-storage-race-hardening-20261105.md`](workspace-storage-race-hardening-20261105.md).

Current workspace gates:

- `./scripts/verify.sh` passed on 2026-11-05: Ruff, 75 pytest tests and 58 subtests, SPARQL CQs, SHACL positive/negative fixtures, mapping profile schema, TypeScript, and Vite build.
- Playwright browser E2E: `make e2e` passed all 3 tests after the runner selected an available loopback port.
- `scripts/e2e-run.sh` isolates and removes its temporary `SDLC_QE_DATA_DIR`; the actual Playwright run completed and cleaned its test data.

Historical bootstrap run record: [`bootstrap-verification-20261104.md`](bootstrap-verification-20261104.md). Historical results do not establish the current checkout's status.

Test code lives in `tests/` and `e2e/tests/`. This directory holds case descriptions and evidence indexes; current-run results must be recorded separately from the historical logs in `evidence/`.
