# PR second-pass review verification / PR 二次审查验证

Date / 日期: 2026-11-05

PR: [#1](https://github.com/naodeng/sdlc-qe-ontology/pull/1)
Requirement: `REQ-WORKSPACE-001`, phase 1 only.
Plan: [`20261105-pr-review-second-pass.md`](../plans/20261105-pr-review-second-pass.md).

## Review findings / Review 问题

- The first POSIX publication approach linked the staged manifest into the final directory and left staging residue. The final implementation publishes the fully written staging directory with an atomic no-replace rename; the no-residue assertion passes.
- Replacing a workspace directory with a symlink after the initial `lstat()` returned the outside manifest as a valid workspace. The new regression failed before the fix and passes after directory-handle reads verify identity before and after manifest access.
- Replacing `workspaces/` after path validation allowed list/create to follow the outside symlink. Both regressions fail against the submitted implementation and pass after POSIX data-root, workspaces-root, and UUID operations were anchored to directory handles.
- Replacing the UUID destination with an ordinary directory after a separate claim could publish the manifest into that replacement. The new regression fails against the submitted implementation and passes because the final directory is now claimed with an atomic no-replace rename.
- Replacing a manifest with a FIFO between type-check and open could block list/get. The new regression confirms the nonblocking open rejects it as unavailable.
- Windows now holds no-follow handles without delete sharing for both storage roots and child workspace directories. Manifest reads use a no-follow file handle; creation locks staging while writing and verifies the directory identity after rename. Native Windows junction race regressions are in `platform-tests/windows/test_workspace_store_reparse_races.py` and the new `windows-storage` CI job; they were not run in this macOS session.
- POSIX creation fsyncs the staged directory before publishing it, so the manifest directory entry is durable before the no-replace rename.
- OpenAPI now documents `403 origin_not_allowed` on every GET operation affected by the Origin middleware. Four API regression cases cover health, metadata, workspace list, and workspace detail.
- POSIX creation fails closed when safe directory handles or the platform's atomic no-replace rename are unavailable.

## TDD and gates / TDD 与门禁

- RED: the workspace-root swap tests failed against an isolated archive of submitted commit `4278bf0` — list returned data from the outside root and create did not reject the swap.
- RED: `test_create_does_not_publish_into_replaced_destination_directory` failed against submitted commit `565734e`; the old mkdir-then-publish flow wrote into the replacement directory.
- RED: an isolated replay against submitted commit `1e2600f` replaced a checked manifest with a FIFO; the old open blocked until a 2-second watchdog killed the process.
- GREEN: `.venv/bin/pytest tests/test_workspace_store.py -q` — 32 passed, including root/destination swaps and the FIFO replacement regression.
- Baseline replay: the new workspace E2E case was run against an isolated archive of `origin/main`; it failed at the first workspace heading assertion because the baseline has no Workspaces route. This is a review-time replay, not evidence that the original implementation was developed RED-first.
- `./scripts/verify.sh` — passed after the latest storage/API changes: 85 pytest tests and 58 subtests, with no skipped tests; Ruff; SPARQL CQs; SHACL positive/negative fixtures; mapping schema checks; TypeScript; Vite production build.
- `env -u SDLC_QE_DATA_DIR -u SDLC_QE_E2E_DATA_ROOT -u E2E_FRONTEND_PORT npm --workspace frontend run e2e` — 3 Playwright tests passed in 10.0 seconds; the runner's temporary data root was removed.
- Unisolated Playwright CLI launch was rejected before server startup. `bash -n scripts/e2e-run.sh` and `git diff --check` passed.

## UI theme boundary / UI 主题边界

The light UI was reviewed in Chinese and English at 390px and 1440px, including keyboard creation, empty/corrupt states, and overflow. This product phase has no dark theme implementation or color-scheme rule; dark-theme review is therefore not applicable and remains not implemented/not tested.

## Limits / 限制

- Windows behavior was not runtime-verified in this macOS session. The new Windows-only junction regressions require the `windows-storage` CI job to pass before treating Windows behavior as verified.
- Workspace import, global active-workspace selection, single-writer locking, snapshots, and assessment remain out of scope. Overall MVP remains Candidate / No-Go.
