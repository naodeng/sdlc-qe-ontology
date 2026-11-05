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
- Windows now holds no-follow handles without delete sharing for both storage roots and child workspace directories. Manifest reads use a no-follow file handle; creation locks staging while writing and verifies the directory identity after rename. Native Windows junction race regressions are in `platform-tests/windows/test_workspace_store_reparse_races.py`; they ran in hosted Windows CI, not in this macOS session.
- POSIX creation fsyncs the staged directory before publishing it, so the manifest directory entry is durable before the no-replace rename.
- When first creating storage, POSIX now fsyncs each parent after creating a data-root component and fsyncs the data-root handle after creating `workspaces/`. The regression asserts that each parent fsync occurs after its corresponding mkdir.
- OpenAPI now documents `403 origin_not_allowed` on every GET operation affected by the Origin middleware. Four API regression cases cover health, metadata, workspace list, and workspace detail.
- OpenAPI describes the workspace name limit after server trimming; an API regression accepts surrounding whitespace around an 80-codepoint name and verifies the normalized response.
- POSIX creation fails closed when safe directory handles or the platform's atomic no-replace rename are unavailable.

## TDD and gates / TDD 与门禁

- RED: the workspace-root swap tests failed against an isolated archive of submitted commit `4278bf0` — list returned data from the outside root and create did not reject the swap.
- RED: `test_create_does_not_publish_into_replaced_destination_directory` failed against submitted commit `565734e`; the old mkdir-then-publish flow wrote into the replacement directory.
- RED: an isolated replay against submitted commit `1e2600f` replaced a checked manifest with a FIFO; the old open blocked until a 2-second watchdog killed the process.
- GREEN: `.venv/bin/pytest tests/test_workspace_store.py -q` — 33 passed, including root/destination swaps, FIFO replacement, and directory-fsync ordering regressions.
- Baseline replay: the new workspace E2E case was run against an isolated archive of `origin/main`; it failed at the first workspace heading assertion because the baseline has no Workspaces route. This is a review-time replay, not evidence that the original implementation was developed RED-first.
- `./scripts/verify.sh` — passed at commit `64784e4`: 87 pytest tests and 58 subtests, with no skips; Ruff; SPARQL CQs; SHACL positive/negative fixtures; mapping schema checks; TypeScript; Vite production build.
- `env -u SDLC_QE_DATA_DIR -u SDLC_QE_E2E_DATA_ROOT -u E2E_FRONTEND_PORT npm --workspace frontend run e2e` — 3 Playwright tests passed in 9.6 seconds; the runner's temporary data root was removed.
- GitHub Actions at commit `64784e4`: [`verify` passed](https://github.com/naodeng/sdlc-qe-ontology/actions/runs/41997269821/job/127143409184), including its 3-test browser E2E; [`windows-storage` passed](https://github.com/naodeng/sdlc-qe-ontology/actions/runs/41997269821/job/127143408722) with 43 passed and 12 skipped.
- Unisolated Playwright CLI launch was rejected before server startup. `bash -n scripts/e2e-run.sh` and `git diff --check` passed.

## UI theme boundary / UI 主题边界

The light UI was reviewed in Chinese and English at 390px and 1440px, including keyboard creation, empty/corrupt states, and overflow. This product phase has no dark theme implementation or color-scheme rule; dark-theme review is therefore not applicable and remains not implemented/not tested.

## Limits / 限制

- The Win32 storage path was verified by the hosted Windows CI job, not locally on macOS. The 12 Windows skips cover POSIX-only regressions and symlink cases skipped because creating those links may require additional privileges.
- Workspace import, global active-workspace selection, single-writer locking, snapshots, and assessment remain out of scope. Overall MVP remains Candidate / No-Go.
