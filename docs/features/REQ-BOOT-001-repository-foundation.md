# Feature: Runnable repository foundation

Status: Implemented (bootstrap scope only)
Requirement ID: REQ-BOOT-001
Owner: Project maintainers

## 背景与用户价值

The repository currently contains only a placeholder README. Contributors need a reproducible local foundation that reflects the v0.19 repository standards and the accepted v0.18 product direction.

## 角色与使用流程

Contributors create the Python environment and frontend dependencies, start the local API and UI, inspect the bundled ontology metadata, and run the repository quality gates.

## 范围与非范围

In scope: bilingual project entry points, governance and development skills, the candidate ontology/SHACL/SPARQL fixtures, a loopback-only FastAPI metadata endpoint, an Arco React workbench shell, and repeatable local checks.

Out of scope: real project import, mapping approval, SHACL-backed snapshot publishing, evidence assessment, report export, and external integrations. These remain MVP work and are not represented as implemented.

## 功能和非功能要求

- Local development binds services to `127.0.0.1`.
- The API reads only bundled candidate ontology and demo fixture files.
- The API reports validation as `not_run` until a validation run is actually performed.
- The UI surfaces the demo data and does not present a verified quality decision.
- Python domain code has no FastAPI, RDFLib, or filesystem dependency.
- The frontend uses the selected React, TypeScript, Vite, and Arco Design React stack.

## 安全/语义失败模式

- Do not turn absent evidence or unrun validation into `Qualified` or `Verified`.
- Do not accept broad network binding, arbitrary file paths, or write operations in the bootstrap API.
- Keep user import and snapshot activation unavailable until the quarantine and approval flow is implemented.

## Given/When/Then 验收准则

- Given a fresh checkout with documented prerequisites, when a contributor runs the setup and development commands, then the UI and API start on loopback.
- Given the bundled ontology and demo fixture, when a client reads `/api/v1/meta`, then the response identifies the demo snapshot and reports `validation: not_run`.
- Given the repository validation command, when its required dependencies are installed, then ontology tests, SHACL positive/negative fixtures, mapping schema validation, Python lint, and frontend build run as explicit gates.
- Given the current bootstrap state, when a user opens Import or Analysis, then the UI explains that those workflows are not implemented and does not imply a quality result.

## 关联 ADR、API、SHACL、金标测试

- Product baseline: `docs/designs/current-baseline.md`
- API: `docs/designs/api.yaml`
- Existing ontology and SHACL baseline: `ontology/`
- Historical product decisions and acceptance details: `ui-design/v018/`

## 依赖与待决策事项

The v0.18 decisions for local real-data import and human-confirmed mapping remain accepted. Import parser limits, the supported RDF profile, mapping approval invalidation, atomic snapshot activation, and policy version compatibility remain Sprint 0 implementation decisions.
