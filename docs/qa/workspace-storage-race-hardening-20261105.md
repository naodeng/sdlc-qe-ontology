# Workspace storage hardening verification / 工作区存储加固验证

Date / 日期: 2026-11-05

Plan / 计划: [`20261105-workspace-storage-race-hardening.md`](../plans/20261105-workspace-storage-race-hardening.md)

## Passed / 已通过

- TDD regression: `test_list_reports_no_follow_eloop_as_corrupt_and_continues` — RED reproduced `WorkspaceStorageUnavailable` for Darwin `errno.ELOOP`; GREEN passed and kept other workspace summaries available.
- TDD regression: `test_create_retries_collision_at_atomic_destination_claim` — RED reproduced failure of the prior check-then-rename implementation; GREEN passed, retried with a new UUID, and preserved the colliding workspace manifest and directory.
- `test_list_ignores_workspace_with_active_creation_marker` — passed; an incomplete in-progress directory is not reported as a corrupt workspace.
- `./.venv/bin/pytest tests/test_workspace_store.py -q` — 26 passed.
- `./scripts/verify.sh` — passed: 75 pytest tests and 58 subtests, Ruff, SPARQL CQs, SHACL positive/negative fixtures, mapping schema checks, TypeScript, and Vite production build.
- `bash -n scripts/e2e-run.sh` — passed.
- `npm --workspace frontend run e2e -- --list` — discovered all 3 Playwright tests in 2 files.
- Final `make e2e` — passed all 3 Playwright tests in 8.1 seconds, with 3 workers.

## Playwright startup investigation / Playwright 启动问题定位

- The first sandboxed attempt failed before page assertions because macOS denied Chromium's `MachPortRendezvousServer` access (`Permission denied (1100)`). This was a sandbox process-launch restriction, not an application assertion failure.
- The first authorized outside-sandbox run got past that restriction but found `127.0.0.1:5174` already held by a Node service from another local project. That process was left running.
- The runner now asks the OS for an ephemeral loopback port and passes it consistently to Vite, Playwright, and FastAPI's exact allowed-Origin entry. The subsequent outside-sandbox `make e2e` completed all tests.

The original [`workspaces-verification-20261105.md`](workspaces-verification-20261105.md) remains the record of the initial sandbox attempt; this report records the completed follow-up.
