# v0.14 设计收敛与问题追踪 / Design remediation

**Status: Design Candidate / No-Go.** This is a design and executable contract-check package, not a working UI or certified ontology. Preserve v0.10 ontology/query semantics unchanged. Source: v0.12 design and v0.13 static review.

## Scope and non-goals
- Local-first, read-only, bounded ontology browsing and evidence exploration; advisory quality decisions only.
- No ontology editing, raw SPARQL execution, automatic release approval, file-system browsing, user-editable authoritative versions, or multi-user auth in MVP.
- Frontend React + TypeScript + Vite, UI adapter for Animal Island UI; backend FastAPI + Pydantic + RDFLib; pySHACL required for assurance.

## Remediation matrix
| Finding | Resolution in v0.14 | Acceptance evidence still needed |
|---|---|---|
| F01 | 01_POLICY_DECISION_CONTRACT | executable policy tests and ADR approval |
| F02 | 01 + 02 snapshot/coverage | partial data adversarial run |
| F03 | 01 assurance separation | backend and E2E gate tests |
| F04 | contracts/openapi.v014.yaml | implementation contract tests |
| F05 | 03_SETTINGS_AND_DESIGN_SYSTEM | browser tests |
| F06 | 02_SNAPSHOT_AND_VERSIONING | real metadata sources |
| F07 | 05_SPIKES_AND_GATES | npm lockfile, license, build, keyboard audit |
| F08 | 04_SECURITY_ACCESSIBILITY | security tests |
| F09 | 02_SNAPSHOT_AND_VERSIONING | concurrency and stale-tab tests |
| F10 | 04_SECURITY_ACCESSIBILITY | graph scale tests |
| F11 | 04_SECURITY_ACCESSIBILITY | axe and manual tests |
| F12 | 03_SETTINGS_AND_DESIGN_SYSTEM | translation tests |
| F13 | 01_POLICY_DECISION_CONTRACT | authenticity and policy tests |
| F14 | 03_SETTINGS_AND_DESIGN_SYSTEM | storage corruption tests |
| F15 | 05_SPIKES_AND_GATES | pySHACL, OSLC/PROV-O review |

## Approval boundaries
- **Design review:** candidate architecture and contracts can be reviewed now.
- **Sprint 0:** bounded spikes may begin with advisory-only UX.
- **Full MVP:** do not approve until F01–F09 and F13 contracts are approved and executable gates are green.
- **Release:** no critical skipped checks, no false-qualified results on fixed adversarial corpus, and evidence of accessibility/security/standards review.

## ADR queue
ADR-001 Policy semantics; ADR-002 Snapshot immutability; ADR-003 Assurance gates; ADR-004 UI dependency adapter; ADR-005 Loopback threat model; ADR-006 Preferences and version metadata. Each remains **Proposed**, with reviewer/date/evidence required before acceptance.
