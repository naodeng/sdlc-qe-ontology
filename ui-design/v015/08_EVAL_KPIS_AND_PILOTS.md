# 评估体系、指标和真实项目试点

## Four-layer quality model
1. **Model:** ontology parses, constraints pass, term mappings reviewed, version compatibility verified.
2. **Decision:** policy goldens and adversarial fixtures; 0 false `qualified + verified` in fixed corpus; measure precision/recall on labeled obligations and unknown rate separately.
3. **System:** API schema, snapshot consistency, local security, graph bounds, availability and performance.
4. **Experience:** keyboard/contrast/screen-reader, discoverability, reason comprehension, bilingual usability.

## KPI definitions (no fabricated results)
| Metric | Formula / definition | Target candidate |
|---|---|---|
| False Verified Qualified | incorrect verified-qualified outputs / all known negative goldens | 0 |
| Unknown coverage | correctly unknown / all incomplete-data goldens | 100% |
| SHACL negative detection | rejected invalid fixtures / total invalid fixtures | 100% for required shapes |
| Snapshot consistency | cross-snapshot contamination cases | 0 |
| Evidence explanation traceability | decisions with reason + source + snapshot + policy / decisions | 100% |
| A11y critical violations | confirmed WCAG AA critical defects | 0 at release |
| Graph boundedness | responses respecting configured caps / requests | 100% |

## Baseline comparison
B0 deterministic relational/JSON lookup, B1 RDF+SPARQL, B2 RDF+SHACL+policy. Same goldens, input inventory, hardware and query set. Report correctness, authoring cost, P95 latency, data maintenance cost, provenance explainability. Ontology is not automatically better; preserve counter-evidence.

## Pilot stages
P1 synthetic release corpus (all corner cases); P2 sanitized real project with at least 2 releases and independent human goldens; P3 second distinct repository/process. Do not use private customer data without permission. Success requires measurable benefit over B0 and no critical trust/security regressions.
