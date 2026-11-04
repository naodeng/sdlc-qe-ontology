# Current product and implementation baseline

**State:** Bootstrap implemented; automated browser E2E remains pending. MVP remains Candidate / No-Go until Sprint 0 evidence and product workflows are implemented.

## Accepted product decisions

- Local-first SDLC/QE quality evidence workbench.
- Real project data import is in MVP scope (PRODUCT-ADR-008).
- Mapping uses standard templates plus a visual editor and explicit human confirmation (PRODUCT-ADR-009). AI must not approve or write semantic mappings.
- React + TypeScript + Vite + Arco Design React is the selected UI direction; Animal Island UI is retired.
- Evidence decision status (`qualified`, `unqualified`, `unknown`) and assurance status (`verified`, `blocked`, `not_run`, `stale`, `unavailable`) remain separate.
- Missing or unverified evidence must not be shown as verified `Qualified`.

## Implemented in the repository bootstrap

- Local-only frontend and API startup scripts.
- Read-only health and metadata endpoints over bundled candidate Turtle files.
- Chinese-first Arco workbench with an English switch and Overview, Ontology, Import, and Analysis routes.
- Existing ontology, SHACL, SPARQL, and mapping-schema candidate assets with strict checks.

## Not implemented yet

- Workspace creation and selection.
- CSV, JSON, or RDF import and visual field mapping.
- Mapping approval records and invalidation.
- Preflight, full SHACL/policy evaluation, immutable snapshot creation, and atomic activation.
- Evidence qualification, release assessment, and traceable report export.
- GitHub/CI synchronization or remote service access.

The design-package history remains under `ui-design/`. The v0.18 product baseline takes precedence over older design packages; v0.19 governs repository structure and engineering workflow.
