# v0.15 产品与工程基线候选 / Executive baseline

**Status: Design Candidate / No-Go.** This package extends v0.14; it does not assert that the runtime UI, SHACL, npm compatibility, or external standards audit has passed. The v0.10 ontology is preserved as-is.

## Positioning
A local-first, read-only SDLC-QE Ontology Workbench for ontology navigation, bounded relationship exploration, evidence inspection, advisory quality decisions, and validation diagnostics. Not an ontology authoring platform, release approval service, or autonomous agent.

## Non-negotiable invariants
1. `Qualified` is never presented as **verified** unless dataset integrity, mandatory SHACL validation, policy checks, and provenance assurance have passed for the **same immutable snapshot**.
2. A missing relationship in an open-world graph is **not** proof of nonexistence. Completeness assertions must be explicit, scoped, and source-backed.
3. Missing or invalid critical metadata yields `Unknown`, or a diagnostic `Unavailable` response when the computation cannot run; never silently default to `Qualified`.
4. `assessmentStatus` (quality result) and `assuranceStatus` (trust in evaluation) are separate fields; release authorization is **out of scope**.
5. UI preferences are never stored in or written to ontology snapshots.
6. User-facing version fields must be sourced from manifests/build metadata, not editable UI inputs.

## Design freeze proposal
Freeze P0 scope after ADR and API/decision goldens approved. Block new UI features until Sprint 0 technical evidence is accepted. Distinguish UI design version v0.15 from app release v0.1.0.

## Decision log to approve
ADR-001 tri-state semantics; ADR-002 snapshot identity/retention; ADR-003 assurance/SHACL gating; ADR-004 Animal Island UI adapter/license; ADR-005 local HTTP threat model; ADR-006 theme/locale persistence; ADR-007 evidence freshness and policy version; ADR-008 scoped completeness attestations.
