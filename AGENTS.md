# AGENTS.md — SDLC-QE Ontology Workbench

> Current engineering governance baseline: v0.19 (candidate). Do not confuse historical v0.10–v0.18 design packages with implemented code.

## Mission
Local-first platform for verifiable SDLC/QE semantic traceability, real-data import, evidence qualification, and explainable advisory quality decisions. English stable IDs with Chinese-first process documents and bilingual project-facing docs.

## Repository boundaries
- `frontend/`: React + TypeScript + Vite + Arco Design React; old Animal Island UI is retired.
- `backend/`: FastAPI HTTP adapter → application use cases → pure domain; RDFLib/SHACL and file I/O as infrastructure adapters.
- `ontology/`: classes, properties, SHACL shapes, competency queries, fixtures.
- `docs/features`: requirements; `docs/plans`: proposed/frozen plans; `docs/designs`: approved facts and ADRs; `docs/standards`: engineering rules; `docs/qa`: test evidence.
- `e2e/`: browser E2E. Paths in this delivery package are under `01_project/`; adapt when moving into a repository root.

## Nonnegotiable invariants
1. Unknown evidence or failed/unavailable validation must not become verified Qualified.
2. Data completeness, decision status and verification/assurance status are different dimensions.
3. Import must follow quarantine → preview → human-approved mapping → preflight → SHACL → immutable snapshot → atomic activation; any failure preserves active snapshot.
4. No broad public network binding; treat even localhost input as untrusted.
5. Ontology URI changes require ADR, migration/compatibility plan and positive+negative tests.
6. UI displays active snapshot, truncation and evidence limitations; never hides Unknown.
7. Do not assert unrun quality gates have passed.

## Dependencies
Frontend UI/API client never directly mutates RDF files. FastAPI adapter has no policy logic. Pure domain does not import HTTP, RDFLib or filesystem. Infrastructure implements ports, not vice versa.

## Mandatory workflow
- Read requirements, relevant ADRs, tests and `docs/standards/*`.
- Draft plan using `docs/plans/_template.md`, request required human approval for semantics, destructive or high-risk changes.
- Add a failing test or goldens first; implement minimal feature, then refactor.
- Run relevant unit, API, RDF/SHACL/SPARQL, import-negative, and browser E2E tests; disclose not_run/blocked.
- Update docs, evidence, risks and rollback documentation.

## AI / tools authority
Read-only analysis by default; external writes, PR creation, releases, deletion and access to customer data require explicit permission. Never install/copy untrusted MCP configuration or embed keys. See `.agent/skills` and `docs/standards/ai-agent.md`.

## PR DoD
Every PR: linked requirement, Plan or ADR, changed files, RED/GREEN evidence, semantic compatibility, docs-sync check, security impacts, rollback, unresolved issues and Go/No-Go.
