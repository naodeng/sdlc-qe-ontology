---
name: dev-build
description: Implement approved SDLC-QE features via TDD and layer boundaries
---
# dev-build

Use RED→GREEN→REFACTOR. Keep Python domain pure, FastAPI adapter thin, React views separated from API services, ontology RDF/OWL separate from SHACL constraints. Import writes occur only through quarantined validation and user-approved mapping, then atomic snapshot activation. Run relevant tests, document actual evidence and never report not_run as passed.

## Delivery
Provide touched files, exact commands and status, failure evidence, docs-sync results, security impacts and remaining risks.
