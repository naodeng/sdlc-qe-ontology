# v0.10 Baseline gate decision

**Decision: Candidate / No-Go.**

| Gate | Status | Required closure evidence |
|---|---|---|
| RDF parse and SPARQL regression | Partially passed | Reproducible local logs and CI run |
| Adversarial CQ09/CQ10 | Locally evaluated | Independent review and broader fixtures |
| SHACL positive/negative validation | BLOCKED | pySHACL installed, real validation logs, zero skipped |
| Standards URI/semantics/license mapping | BLOCKED | Reviewed mapping worksheet with primary references |
| Release evidence completeness | BLOCKED | Explicit unknown vs unqualified vs qualified rules |
| Real project comparison | NOT STARTED | Baseline B0/B1/B2 evaluation and traceable gold set |

No ontology freeze or production release approval is implied.
