# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Confirmed project direction from the referenced product conversation and v0.19 package: React + TypeScript + Vite + Arco Design React; Python + FastAPI; RDFLib + SHACL. Local-first, without a default database or remote synchronization.

## Users

Inferred from the product planning materials and subject to future user validation: QA/test engineers and quality leads who need to understand whether delivery evidence supports a change or release; developers and release reviewers are secondary readers.

## Product Purpose

Connect requirements, code changes, builds, tests, evidence, and releases so teams can inspect traceability and identify evidence gaps. Success means users can follow a quality conclusion back to its source and understand what remains unknown.

## Positioning

A local-first semantic workbench for verifiable SDLC/QE traceability and explainable quality evidence. It advises with evidence and does not automatically approve releases.

## Operating Context

Users run the workbench locally, start with bundled example data, and (in the planned MVP) import a project dataset, review its field mapping, validate it, and inspect traceable assessments. GitHub/CI online synchronization is deferred.

## Capabilities and Constraints

- Accepted MVP direction: local project data import for CSV, JSON, or a controlled RDF profile.
- Accepted mapping direction: standard templates plus visual field mapping and explicit human confirmation (PRODUCT-ADR-008/009).
- Implementation order selected by the product owner on 2026-11-05: implement the restricted JSON importer first. Its exact input profile and limits remain open for a follow-up plan; this does not remove CSV or controlled RDF from the MVP scope.
- Import validation, evidence qualification, and snapshot activation are product scope; the implementation now includes local workspace create/list/detail plus bundled-example metadata, but no import or snapshot writes.
- Unknown evidence and unrun validation must not be presented as verified Qualified.
- Data completeness, assessment status, and assurance status are separate dimensions.
- No AI auto-approval, cloud multi-tenancy, remote synchronization, or automatic release approval in the MVP.
- The specific JSON/RDF parsing profiles and snapshot recovery protocol remain open for Sprint 0 validation.

## Brand Commitments

The product name is SDLC-QE Ontology Workbench. The prior product conversation selected an Arco Design Pro 2.0 direction and retired the Animal Island UI approach. The interface defaults to Simplified Chinese and offers an English switch. Following direct owner feedback, the interface uses a warm neutral canvas, deep forest navigation, leaf accents, and amber for unassessed states. Chinese system fonts and a serif heading stack avoid remote font dependencies. No standalone logo asset has been approved.

## Evidence on Hand

The repository contains candidate ontology and SHACL files, SPARQL queries, synthetic example fixtures, an example mapping profile, and design/engineering documents. It contains no validated real-project dataset, user study, production result, or business acceptance evidence. Historical gate logs under `evidence/` describe earlier runs and do not prove this checkout's state.

## Product Principles

- Keep user data local by default.
- Preserve source and snapshot traceability for quality claims.
- Keep `Unknown` visible when evidence or validation is insufficient.
- Require human confirmation before a semantic field mapping is used.
- Report only checks that actually ran.

## Accessibility & Inclusion

The UI must support keyboard operation, visible focus, readable status labels, and layouts that remain usable with Chinese and English text. The current shell still needs accessibility verification.
