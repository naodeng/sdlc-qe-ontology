# PR second-pass review verification / PR 二次审查验证

Date / 日期: 2026-11-05

PR: [#1](https://github.com/naodeng/sdlc-qe-ontology/pull/1)
Requirement: `REQ-WORKSPACE-001`, phase 1 only.
Plan: [`20261105-pr-review-second-pass.md`](../plans/20261105-pr-review-second-pass.md).

## Review findings / Review 问题

- Successful POSIX creation left the staged manifest behind after linking it into the final directory. The new assertion failed before the fix and passes after cleanup uses the owned-directory cleanup helper.
- Replacing a workspace directory with a symlink after the initial `lstat()` returned the outside manifest as a valid workspace. The new regression failed before the fix and passes after directory-handle reads verify identity before and after manifest access.
- Replacing `workspaces/` after path validation allowed list/create to follow the outside symlink. Both regressions fail against the submitted implementation and pass after POSIX data-root, workspaces-root, and UUID operations were anchored to directory handles.
- Manifest publication fails closed when safe POSIX directory handles are unavailable; Windows uses atomic whole-directory rename for creation.

## TDD and gates / TDD 与门禁

- RED: `.venv/bin/pytest tests/test_workspace_store.py -q -k 'create_writes_v1 or replaced_with_symlink'` — 2 failed before the fix: stale `.staging-*` remained and the outside manifest was returned as `empty`.
- RED: the two workspaces-root swap tests failed against an isolated archive of submitted commit `4278bf0` — list returned data from the outside root and create did not reject the swap.
- GREEN: `.venv/bin/pytest tests/test_workspace_store.py -q -k 'create_writes_v1 or replaced_with_symlink or replaced_destination_symlink'` — 3 passed after the first fix; the complete workspace store test file now passes 30/30, including the root-swap regressions.
- Baseline replay: the new workspace E2E case was run against an isolated archive of `origin/main`; it failed at the first workspace heading assertion because the baseline has no Workspaces route. This is a review-time replay, not evidence that the original implementation was developed RED-first.
- `./scripts/verify.sh` — passed after the root-race fix: 79 pytest tests and 58 subtests; Ruff; SPARQL CQs; SHACL positive/negative fixtures; mapping schema checks; TypeScript; Vite production build.
- `env -u SDLC_QE_DATA_DIR -u SDLC_QE_E2E_DATA_ROOT -u E2E_FRONTEND_PORT npm --workspace frontend run e2e` — 3 Playwright tests passed in 8.9 seconds after the final storage changes; the runner's temporary data root was removed.
- Unisolated Playwright CLI launch was rejected before server startup. `bash -n scripts/e2e-run.sh` and `git diff --check` passed.

## UI theme boundary / UI 主题边界

The light UI was reviewed in Chinese and English at 390px and 1440px, including keyboard creation, empty/corrupt states, and overflow. This product phase has no dark theme implementation or color-scheme rule; dark-theme review is therefore not applicable and remains not implemented/not tested.

## Limits / 限制

- Windows behavior was not runtime-verified in this macOS session. Windows workspace reads use path-based identity checks because Python does not expose the POSIX directory-descriptor path used above.
- Workspace import, global active-workspace selection, single-writer locking, snapshots, and assessment remain out of scope. Overall MVP remains Candidate / No-Go.
