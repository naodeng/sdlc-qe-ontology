# Local workspace verification / 本地工作区验证 (initial run)

Date / 日期: 2026-11-05

This records the initial verification run. The follow-up storage hardening and completed Playwright E2E run are recorded in [`workspace-storage-race-hardening-20261105.md`](workspace-storage-race-hardening-20261105.md).

Requirement / 需求: `REQ-WORKSPACE-001`, phase 1 only. This report describes this checkout and does not claim complete WS-01 or MVP acceptance.

## Passed / 已通过

- `./scripts/verify.sh` — passed: Ruff; 72 pytest tests and 58 subtests; SPARQL competency queries; SHACL positive/negative fixtures; mapping-schema positive/negative checks; TypeScript and Vite production build.
- `bash -n scripts/e2e-run.sh` — passed.
- `npm --workspace frontend run e2e -- --list` — discovered all three Playwright tests across two files; this lists tests only and does not execute browser E2E.
- Isolated E2E-runner lifecycle check with a stub `npm` executable — confirmed the script exports a newly created `SDLC_QE_DATA_DIR` and removes only that temporary directory on exit. This validates runner cleanup, not browser E2E.
- Local manual review through `ego-browser` — Chinese and English workspace list; pointer and keyboard creation; detail view; list persistence after reload; empty workspace state; corrupt-manifest list row and direct detail error; JSON-first importer copy. The temporary QA workspace and corrupt fixture were removed afterward.
- At 390px and 1440px, `document.documentElement.scrollWidth` equaled `window.innerWidth`; workspace list/detail pages did not overflow horizontally. Screenshots were inspected during the session and removed with the temporary QA artifacts.
- `docs/designs/api.yaml` parsed as OpenAPI 3.1 and contains the collection and detail routes.

## Blocked / 受阻

- `make e2e` was attempted once. All three Playwright cases stopped before their first page assertion because bundled Chromium exited with `bootstrap_check_in org.chromium.Chromium.MachPortRendezvousServer... Permission denied (1100)` in the macOS Codex sandbox.
- Per the repository browser rule, Chromium was not retried outside the sandbox. Playwright E2E remains `blocked`; the manual Ego review is not E2E evidence.

## Implemented scope and limits / 实现范围与限制

- Users can create, list, and open local workspaces in a read-only detail view. Workspace IDs and filesystem paths are server-managed; API errors do not expose local paths or manifest contents.
- Empty workspaces have no imported data and no active snapshot. Corrupt manifests remain unchanged and appear as unavailable.
- Bundled example data stays separate and read-only. Workspace details do not switch the global data source.
- Restricted JSON is the selected first importer; its profile and limits remain open. No importer, mapping approval, validation, snapshot creation, workspace deletion, global active-workspace selector, or single-writer lock is implemented in this phase.
- MVP remains Candidate / No-Go. Passing static/API/ontology/build checks and manual review do not establish product acceptance or successful browser E2E.
