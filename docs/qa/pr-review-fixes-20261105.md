# PR review fixes verification / PR Review 修复验证

Date / 日期: 2026-11-05

PR: [#1](https://github.com/naodeng/sdlc-qe-ontology/pull/1)
Requirement: `REQ-WORKSPACE-001`, phase 1 only.
Plan: [`20261105-pr-review-fixes.md`](../plans/20261105-pr-review-fixes.md).

## Review findings addressed / 已处理的 Review 问题

- Destination symlink race: a regression run against the submitted implementation failed because creation did not raise and the outside `manifest.json` was overwritten. After the fix, publication is anchored to a no-follow directory handle on POSIX; Windows atomically renames the complete staging directory and rejects existing destinations.
- Direct Playwright invocation: `frontend`'s npm `e2e` script now uses the isolated runner, and Playwright config rejects invocations that do not carry the runner's temporary-data marker.

## Passed / 已通过

- `./.venv/bin/pytest tests/test_workspace_store.py -q` — passed after the fix.
- `./scripts/verify.sh` — passed: 76 pytest tests and 58 subtests; Ruff; SPARQL CQs; SHACL positive/negative fixtures; mapping schema checks; TypeScript; Vite production build.
- `env -u SDLC_QE_DATA_DIR -u SDLC_QE_E2E_DATA_ROOT -u E2E_FRONTEND_PORT npm --workspace frontend run e2e` — 3 Playwright tests passed in 8.2 seconds using the isolated temporary data root.
- No `sdlc-qe-e2e.*` temporary roots remained after the E2E run.
- `env -u SDLC_QE_DATA_DIR -u SDLC_QE_E2E_DATA_ROOT ./node_modules/.bin/playwright test --config frontend/playwright.config.ts --list` — rejected before launching servers because no isolated runner marker was present.
- `bash -n scripts/e2e-run.sh` and `git diff --check` — passed.

## Limits / 限制

- The Windows-specific directory-rename path was not executed in this macOS run.
- This is phase 1 only; workspace import, global active-workspace selection, single-writer locking, snapshots, and assessment remain out of scope. Overall MVP status remains Candidate / No-Go.
