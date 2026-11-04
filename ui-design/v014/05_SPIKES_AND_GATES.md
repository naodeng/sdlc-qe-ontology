# Sprint 0 Spikes, Backlog and Go/No-Go

## Sequencing (TDD red -> green -> refactor)
| ID | Task | Depends on | Exit evidence |
|---|---|---|---|
| S0-01 | Approve policy decision table and reason codes | none | ADR-001 + adversarial goldens |
| S0-02 | Manifest, immutable snapshot and stale policy | S0-01 | deterministic hash and 409 tests |
| S0-03 | API schema freeze (all pages) | S0-01/02 | schema parse + contract tests |
| S0-04 | Settings theme/locale/storage subsystem | none | unit and Playwright tests |
| S0-05 | Animal Island UI package spike | S0-04 | lockfile, build, keyboard/contrast and license evidence |
| S0-06 | pySHACL and semantic negative cases | S0-01 | actual run logs, no skip |
| S0-07 | OSLC/PROV-O term/attribution audit | none | exact URI/source/license evidence |
| S0-08 | Local security and graph bounds spike | S0-02/03 | threat-model tests |
| S0-09 | Decision review and signed gate | all | Go/No-Go record |

## MVP implementation after Sprint 0 gate
Sprint 1: snapshot-aware read-only backend, fixed query endpoints, policy engine and provenance. Sprint 2: Overview, Explorer, Evidence and Quality pages plus Settings. Sprint 3: graph/list parity, Validation page, full accessibility, performance and E2E. Each sprint needs regression evidence and rollback plan.

## Blocking gates
G0 requirements/ADR approved; G1 source/ontology provenance; G2 SHACL actual positive+negative validation; G3 deterministic policy goldens incl partial inventory; G4 OpenAPI implementation and snapshot consistency; G5 Animal Island UI integration, accessibility and security; G6 public release checks. Missing mandatory evidence = No-Go. Never convert `not_run` to pass.

## Test matrix
- Policy: 0 false `qualified + verified` on fixed adversarial corpus; unknown on incomplete inventory; wrong build; duplicate execution; stale cutoff; failed execution; mixed pass/fail; forged digest.
- API: 200/400/404/409/422/503, bounded list pagination, fixed snapshot, no cross-snapshot joins, no arbitrary SPARQL.
- Preferences: first load system mode, OS changes, manual override, reload, corrupt/future schema, denied storage, reset does not touch RDF.
- UI: light/dark/locale, status accessible text, loading/error/empty, truncated graph/list, keyboard/focus, reduced motion, mobile widths.
- Security: Host/Origin, XSS literals, path traversal, CSP, timeouts and payload caps.

## Evidence recording template
Command; date/time; commit hash; dependency lock hash; OS/browser; fixture hash; expected; actual; pass/fail; artifacts/logs; reviewer; unresolved risk. No claims of passing runtime gates without captured evidence.
