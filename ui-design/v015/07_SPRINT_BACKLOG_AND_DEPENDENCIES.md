# 可执行 Backlog、依赖和验收

| ID | Priority | Work item | Depends | Definition of Done |
|---|---|---|---|---|
| S0-01 | Blocker | Approve policy truth table and unknown/completeness semantics | — | 20+ goldens, ADR signed, 0 false verified Qualified |
| S0-02 | Blocker | Run pySHACL positive and negative fixtures | — | logs + pinned deps + no skip |
| S0-03 | Blocker | Audit OSLC/PROV-O exact URI/meaning/rights | — | mapping worksheet + primary-source citations + reviewer |
| S0-04 | Blocker | Define manifest and snapshot binding | S0-01 | hash, provenance, stale 409, rollback tests |
| S0-05 | P0 | Animal Island UI package/build/license/accessibility spike | — | npm lockfile, build, contrast, keyboard evidence |
| S0-06 | P0 | Theme/locale preference foundation | S0-05 | system/manual/reload/corrupt/future schema tests |
| S0-07 | P0 | OpenAPI complete schema and codegen trial | S0-01/04 | lint + client/server contract tests |
| S0-08 | Blocker | Loopback security + graph bound tests | S0-04/07 | Host/Origin/XSS/timeout/path tests |
| S0-09 | Gate | Review evidence and approve sprint 1 | all | signed Go/No-Go, unresolved risk register |
| BE-01 | P0 | Snapshot loader + immutable cache | S0-04 | no cross-snapshot joins |
| BE-02 | P0 | Policy evaluator + reason codes | S0-01/02 | deterministic fixture results |
| BE-03 | P0 | Fixed query endpoints + pagination | S0-07/08 | contract and limit tests |
| FE-01 | P0 | Shell, settings, version display | S0-05/06 | light/dark/system, en/zh E2E |
| FE-02 | P0 | Overview and ontology browser | BE-01/03 | loading/empty/error, keyboard |
| FE-03 | P0 | Evidence and decision pages | BE-02/03 | assurance and unknown visible |
| FE-04 | P1 | Graph + accessible list parity | BE-03 | caps, truncation, list equivalence |
| QA-01 | Blocker | Release E2E + security + WCAG audit | all FE/BE | traceable test logs, 0 critical skips |
| REL-01 | Gate | Public alpha/beta/0.1 release approval | QA-01 | docs, reproducible fixture, license, rollback |

## Dependency critical path
S0-01→S0-04→S0-07→S0-08→S0-09→BE-01/02/03→FE-03→QA-01→REL-01. S0-02/03/05 are parallel blockers. UI can be prototyped in isolation before approval, but must not claim release-ready.

## Sprint review checklist
Every story: user outcome, exact inputs/outputs, error states, tests written first, evidence links, accessibility check, English/中文 labels, performance budget, security and rollback implications.
