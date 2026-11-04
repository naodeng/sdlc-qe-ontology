# SDLC-QE Ontology Workbench

A local-first workbench for tracing software delivery and quality evidence.

**Current status:** the repository foundation is runnable. The UI defaults to Simplified Chinese and includes an English switch. The UI and API currently read only the bundled candidate ontology and example fixture. The v0.1.0 real-data import, mapping approval, snapshot publishing, and quality assessment workflows are not implemented. Demo data is not a validation result.

## Quick start

Requirements: Python 3.12+, Node.js 22.12+, and npm.

~~~bash
make setup
make dev
~~~

Open the local workbench at http://127.0.0.1:5174. Local API docs are at http://127.0.0.1:8000/api/docs.

Run the Python, ontology, mapping-schema, and frontend build gates:

~~~bash
make verify
~~~

Before the first browser smoke run, install Playwright's bundled Chromium:

~~~bash
cd frontend && npm run e2e:install
cd .. && make e2e
~~~

## Included in the bootstrap

- React + TypeScript + Vite + Arco Design React workbench shell.
- Read-only local FastAPI health and metadata API.
- RDFLib ontology adapter; local services bind to 127.0.0.1.
- Candidate ontology, SHACL positive/negative fixtures, SPARQL competency queries, and mapping profile schema.
- Python, ontology, schema, and frontend build gates; a Playwright Chromium smoke test; and a GitHub Actions workflow.
- Honest UI states: Unknown and not run remain visible instead of being shown as passed.

## MVP work not implemented yet

- Create, open, and switch local workspaces.
- Import CSV, JSON, or controlled RDF and preview source fields.
- Visual mapping editor, explicit human confirmation, and approval invalidation.
- Data preflight, complete SHACL/policy validation, and atomic immutable snapshot activation.
- Evidence qualification and source-linked quality reports.

## Documentation

- [Product and implementation baseline](docs/designs/current-baseline.md)
- [Repository bootstrap plan](docs/plans/20261104-repository-bootstrap.md)
- [Engineering standards](docs/standards/README.md)
- [Implemented API contract](docs/designs/api.yaml)
- [v0.18 product decisions](ui-design/v018/00_START_HERE_AND_DECISIONS.md)
- [QA gates and evidence state](docs/qa/README.md)

Logs in evidence/ were imported from earlier versions for historical reference and do not establish that the current checkout passes those checks. A release license has not yet been selected.
