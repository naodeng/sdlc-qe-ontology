# QA evidence index

Trace each requirement to a test case, reproducible command, current run report, and gate state. `not_run` and `blocked` are not `passed`.

Current verification report: [`pr-review-fixes-20261105.md`](pr-review-fixes-20261105.md).

Current workspace gates:

- `./scripts/verify.sh` passed on 2026-11-05: Ruff, 76 pytest tests and 58 subtests, SPARQL CQs, SHACL positive/negative fixtures, mapping profile schema, TypeScript, and Vite build.
- Playwright browser E2E: `npm --workspace frontend run e2e` passed all 3 tests using isolated temporary storage and an available loopback port.
- Direct Playwright CLI invocation without the isolation marker is rejected before servers start.

Historical bootstrap run record: [`bootstrap-verification-20261104.md`](bootstrap-verification-20261104.md). Historical results do not establish the current checkout's status.
Earlier workspace and storage hardening evidence: [`workspaces-verification-20261105.md`](workspaces-verification-20261105.md) and [`workspace-storage-race-hardening-20261105.md`](workspace-storage-race-hardening-20261105.md).

Test code lives in `tests/` and `e2e/tests/`. This directory holds case descriptions and evidence indexes; current-run results must be recorded separately from the historical logs in `evidence/`.
