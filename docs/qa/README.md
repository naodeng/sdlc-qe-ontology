# QA evidence index

Trace each requirement to a test case, reproducible command, current run report, and gate state. `not_run` and `blocked` are not `passed`.

Current bootstrap gates:

- Python/API, SPARQL CQ, and SHACL positive/negative fixtures: `scripts/verify_baseline.py`.
- Mapping profile schema positive/negative checks: `scripts/validate_mapping_schema.py`.
- Python lint and frontend build: `scripts/verify.sh`.
- Browser smoke test: `scripts/e2e-run.sh`.

Latest run record: [`bootstrap-verification-20261104.md`](bootstrap-verification-20261104.md). The corrected Playwright runner has not yet had a successful E2E run; do not treat the manual Ego preview as an E2E pass.

Test code lives in `tests/` and `e2e/tests/`. This directory holds case descriptions and evidence indexes; current-run results must be recorded separately from the historical logs in `evidence/`.
