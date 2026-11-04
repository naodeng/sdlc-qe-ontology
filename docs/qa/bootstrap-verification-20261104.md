# Bootstrap verification / 项目基础验证

Date / 日期: 2026-11-04

Scope / 范围: repository bootstrap, not the complete MVP / 仓库基础搭建，不代表 MVP 完成

## Passed / 已通过

- `npm_config_cache=/private/tmp/sdlc-qe-npm-cache make setup` — passed. This machine's existing npm and pip caches are not writable; the npm cache override was local to this command, and no user cache permissions were changed.
- `./scripts/verify.sh` — passed: Ruff, 26 pytest tests (58 subtests), SPARQL competency queries, SHACL positive and negative fixtures, mapping-schema positive and negative cases, TypeScript, and Vite production build.
- Fresh root workspace install via `npm ci` — passed; npm reported 0 vulnerabilities across 69 audited packages.
- Local preview through `ego-browser` — after direct owner feedback, the UI defaults to Simplified Chinese and exposes an English switch. All four routes rendered in Chinese; switching to English changed the Analysis copy and document title. Overview and Analysis keep `未知` / `尚未评估` visible; the Import page clearly states that its workflow is not implemented and no file is uploaded. Desktop and 390px mobile screenshots are in [desktop.png](../../.impeccable/review/desktop.png) and [mobile.png](../../.impeccable/review/mobile.png).
- `npm --workspace frontend run e2e -- --list` — passed test discovery for the Chinese overview and English switch cases. This lists tests only; it does not execute browser E2E.
- Impeccable detector on `frontend/src/App.tsx` and `frontend/src/styles.css` — no findings.

## Browser E2E / 浏览器端到端

- `PLAYWRIGHT_BROWSERS_PATH=/private/tmp/sdlc-qe-playwright make e2e` inside the Codex sandbox was blocked when bundled Chromium exited with `MachPortRendezvousServer ... Permission denied`.
- The one-time sandbox-external run of `PLAYWRIGHT_BROWSERS_PATH=/private/tmp/sdlc-qe-playwright npm --workspace frontend run e2e` launched Chromium but reused an unrelated app already listening on `127.0.0.1:5173`. The test therefore saw that app and failed its first assertion; this was not a result from the workbench.
- The project now uses `127.0.0.1:5174`, and Playwright refuses to reuse an existing server. The corrected browser E2E has **not been run**. Per the repository's `AGENTS.md`, another sandbox-external run needs user authorization. The manual Ego preview above is not a substitute for this gate.

## 当前结论 / Current conclusion

Static, API, ontology, schema, build, and manual visual checks pass. Automated browser E2E remains `NOT_RUN` after the isolation fix, so the repository's full verification set is not yet green. This bootstrap does not implement project imports, mapping approvals, quality assessment, or snapshot activation; the MVP remains Candidate / No-Go.
