# SDLC-QE Ontology Workbench

A local-first workbench for tracing software delivery and quality evidence.

**Current status:** the UI defaults to Simplified Chinese and includes an English switch. Users can create, list, and open local workspaces in a read-only detail view; bundled example data remains a separate read-only source. Restricted JSON is the selected first importer, but import, mapping approval, snapshot publishing, and quality assessment are not implemented. Demo data is not a validation result.

## Quick start

Requirements: Python 3.12+, Node.js 22.12+, and npm.

~~~bash
make setup
make dev
~~~

Open the local workbench at http://127.0.0.1:5174. Local API docs are at http://127.0.0.1:8000/api/docs.

Workspace data stays in the API user's local data directory: macOS defaults to `~/Library/Application Support/SDLC-QE Ontology Workbench`, Windows to `%LOCALAPPDATA%/SDLC-QE Ontology Workbench`, and other systems use `$XDG_DATA_HOME/sdlc-qe-ontology-workbench` or `~/.local/share/sdlc-qe-ontology-workbench`. Set `SDLC_QE_DATA_DIR` to override the location; relative paths resolve from the API process working directory and `~` is expanded. Startup and read requests do not create the data directory.

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
- Local FastAPI health, metadata, and workspace APIs; only explicit workspace creation writes to the local data directory.
- Local workspace creation, listing, and read-only details backed by strictly validated manifests and atomic directory publication.
- RDFLib ontology adapter; local services bind to 127.0.0.1.
- Candidate ontology, SHACL positive/negative fixtures, SPARQL competency queries, and mapping profile schema.
- Python, ontology, schema, and frontend build gates; a Playwright Chromium smoke test; and a GitHub Actions workflow.
- Honest UI states: Unknown and not run remain visible instead of being shown as passed.

## MVP work not implemented yet

- Global active-workspace selection and a single-writer lock before changing existing workspace data.
- The restricted JSON first importer (profile still open), followed by CSV/controlled RDF import and source-field preview.
- Visual mapping editor, explicit human confirmation, and approval invalidation.
- Data preflight, complete SHACL/policy validation, and atomic immutable snapshot activation.
- Evidence qualification and source-linked quality reports.

## Documentation

- [Product and implementation baseline](docs/designs/current-baseline.md)
- [Local workspace requirement and implementation plan](docs/features/REQ-WORKSPACE-001-local-workspaces.md)
- [Latest workspace verification evidence](docs/qa/workspace-storage-race-hardening-20261105.md)
- [Repository bootstrap plan](docs/plans/20261104-repository-bootstrap.md)
- [Engineering standards](docs/standards/README.md)
- [Implemented API contract](docs/designs/api.yaml)
- [v0.18 product decisions](ui-design/v018/00_START_HERE_AND_DECISIONS.md)
- [QA gates and evidence state](docs/qa/README.md)

Logs in evidence/ were imported from earlier versions for historical reference and do not establish that the current checkout passes those checks. A release license has not yet been selected.
