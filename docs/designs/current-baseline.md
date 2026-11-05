# Current product and implementation baseline

**State:** Bootstrap and local workspace management slice implemented. Playwright E2E passed on 2026-11-05 using the project runner with an isolated data root and ephemeral loopback port. MVP remains Candidate / No-Go until Sprint 0 evidence and import/assessment workflows are implemented.

## Accepted product decisions

- Local-first SDLC/QE quality evidence workbench.
- Real project data import is in MVP scope (PRODUCT-ADR-008).
- The product owner selected restricted JSON as the first import format to implement; its exact profile and limits remain open. CSV and controlled RDF remain in MVP scope.
- Mapping uses standard templates plus a visual editor and explicit human confirmation (PRODUCT-ADR-009). AI must not approve or write semantic mappings.
- React + TypeScript + Vite + Arco Design React is the selected UI direction; Animal Island UI is retired.
- Evidence decision status (`qualified`, `unqualified`, `unknown`) and assurance status (`verified`, `blocked`, `not_run`, `stale`, `unavailable`) remain separate.
- Missing or unverified evidence must not be shown as verified `Qualified`.

## Implemented in the repository bootstrap

- Local-only frontend and API startup scripts.
- Read-only health and bundled-metadata endpoints plus local workspace create/list/read-only detail endpoints.
- Chinese-first Arco workbench with an English switch and Overview, Ontology, Import, Analysis, and Workspaces routes.
- Manifest-backed local workspace storage with private POSIX permissions, atomic creation, strict schema validation, and corrupt-entry reporting.
- Workspaces stay separate from the bundled, read-only example; JSON is identified in the UI as the selected first importer.
- Existing ontology, SHACL, SPARQL, and mapping-schema candidate assets with strict checks.

## Not implemented yet

- Global active-workspace selection and the single-writer lock required before any existing workspace data is changed.
- Restricted JSON import (selected first; exact profile and limits remain open), then CSV/controlled RDF and visual field mapping.
- Mapping approval records and invalidation.
- Preflight, full SHACL/policy evaluation, immutable snapshot creation, and atomic activation.
- Evidence qualification, release assessment, and traceable report export.
- GitHub/CI synchronization or remote service access.

The design-package history remains under `ui-design/`. The v0.18 product baseline takes precedence over older design packages; v0.19 governs repository structure and engineering workflow.
