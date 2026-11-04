# Plan: 20261104-repository-bootstrap
Status: Approved (repository bootstrap explicitly requested)
Linked Requirement: REQ-BOOT-001

## 目标、现状与预期用户价值

Turn the placeholder repository into a reproducible local project foundation with a minimal, honest vertical slice. This does not claim the v0.1.0 MVP is complete.

## 技术方案与架构边界

- Frontend: React + TypeScript + Vite + Arco Design React; route/page components call a typed API client.
- Backend: FastAPI adapter → application use case → domain metadata type; an RDFLib infrastructure adapter reads the bundled ontology and fixture.
- Keep the existing candidate ontology, SHACL, SPARQL queries, mapping schema, and negative fixtures under `ontology/`.
- Bind local development to `127.0.0.1`; expose read-only metadata only.
- Import, user workspace writes, assessment policy, and snapshot activation remain out of this bootstrap.

## 受影响文件（路径）

- Root: `AGENTS.md`, bilingual README files, `CONTRIBUTING.md`, `.gitignore`, `pyproject.toml`, `Makefile`.
- Backend: `backend/app/{api,application,domain,ports,adapters}` and API tests.
- Frontend: `frontend/src/{api,components,pages}`, Vite/TypeScript/npm configuration.
- Ontology: `ontology/models`, `ontology/shapes`, `ontology/queries`, `ontology/fixtures`, `ontology/mappings/v1`.
- Governance: `.agent/skills`, `.github/workflows`, `.github/PULL_REQUEST_TEMPLATE.md`, `docs/features`, `docs/plans`, `docs/designs`, `docs/standards`, `docs/qa`.
- Local scripts and evidence: `scripts/`, `tests/`, `e2e/`, `evidence/`.

## API / 本体 / 映射 / 快照变化

Add read-only `GET /api/v1/health` and `GET /api/v1/meta`. Metadata describes the bundled demo fixture, an unversioned candidate ontology, and `validation: not_run`. No ontology URI, SHACL policy, mapping semantics, or active user snapshot is changed.

## 时序图或数据流

`React page → typed API client → FastAPI route → metadata use case → ontology catalog port → RDFLib adapter → bundled Turtle files`

## TDD: RED 测试、GREEN 实现、REFACTOR

Add the API metadata contract test first and confirm it fails because the endpoint is absent. Implement the domain/application/adapter/API layers, then make the test pass. Preserve and relocate the supplied ontology regression suite; keep SHACL missing-dependency behavior as a failure in the strict gate.

## 单元 / API / SPARQL / SHACL / E2E / 安全测试

- `python scripts/verify_baseline.py`: pytest plus SHACL positive/negative fixture gate.
- `python scripts/validate_mapping_schema.py`: bundled mapping profile example against the v1 schema.
- `ruff check backend scripts tests`.
- `npm --prefix frontend run build`.
- `scripts/e2e-run.sh`: Playwright Chromium smoke test for the shell and honest not-run state.
- Verify backend and Vite bind to loopback and unknown Host headers are rejected.

## 风险、回滚、可观测证据

The imported ontology and historical documents are candidate/reference material, not proof of product readiness. Rollback is limited to reverting this bootstrap's added files and README replacement; no user data or snapshots are written. Test and build outputs are reported from the current run only.

## 文档同步清单

Update the root entry points, current product baseline, API contract, bootstrap feature, this plan, quick-start instructions, QA evidence index, and workflow commands together.

## 人工审批与执行结果

Repository bootstrap was explicitly requested. No ontology semantics or snapshot rules are modified. The bootstrap scope is implemented; the current verification record is in `docs/qa/bootstrap-verification-20261104.md`. Python, ontology, schema, lint, and frontend build gates pass. The corrected Playwright configuration still needs one browser E2E run: the sandbox launch hit the macOS MachPort restriction, and the allowed one-time external run reused an unrelated app on port 5173. Port 5174 and `reuseExistingServer: false` now isolate the suite. A further external run requires authorization under the repository instructions.
