# 文档变更记录和兼容策略

## Changes from v0.14
Adds policy edge-case contract, seven-page IA, startup settings/versions, endpoint-level API outline, local security/performance targets, staged releases 0.1–1.0, dependency-aware backlog, evaluation KPIs and explicit risk gate. All changes are **proposals** until ADR approval. v0.10 ontology, queries and fixtures remain unchanged in this package.

## Compatibility matrix
| Area | v0.10 | v0.14 | v0.15 |
|---|---|---|---|
| RDF ontology | candidate | unchanged | unchanged |
| Evidence queries | candidate | unchanged | unchanged |
| UI | not implemented | design contract | refined design + roadmap |
| API | not implemented | OpenAPI draft | endpoint specification, not implemented |
| Preferences | absent | proposed | startup/migration specified |
| Three-state policy | gap identified | proposed | edge cases refined, ADR pending |

## Change control
Future model changes require: ADR → version bump → migration/compatibility plan → golden tests → validation → bilingual docs. No unsafe automatic conversion of older snapshots.
