# API 与数据契约 v0.15

## Contract principles
Read-only JSON; fixed server-owned queries; snapshot-bound; pagination and bounded graph; explicit `assessmentStatus`, `assuranceStatus`, `dataStatus`, `reasonCodes`, `snapshotId`, `policyVersion`, `validationRunId`. All user-visible counts include scope, completeness and timestamp. No raw SPARQL endpoint, no arbitrary URL fetching, no arbitrary filesystem paths.

## Endpoints (proposed)
| Method/path | Purpose | Key requirements |
|---|---|---|
| GET `/api/v1/system/info` | version/build/health | source + unavailable status |
| GET `/api/v1/snapshots` | available local snapshots | bounded list, readonly |
| GET `/api/v1/overview` | metrics for snapshot | completeness + asOf |
| GET `/api/v1/ontology/concepts` | paged classes/properties | language, search, page token |
| GET `/api/v1/ontology/concepts/{id}` | term detail | stable ID, labels, IRI, provenance |
| GET `/api/v1/relationships` | bounded subgraph | node ID, depth≤2, capped nodes/edges, truncated |
| GET `/api/v1/obligations` | evidence list | filters, pagination, completeness |
| GET `/api/v1/obligations/{id}` | evidence lineage | build/environment/cutoff and source |
| GET `/api/v1/releases/{id}/assessment` | tri-state quality | dual status + reason codes + validation run |
| GET `/api/v1/validation` | validation report | passed/failed/not_run/stale, source |

## Error semantics
400 invalid filter, 404 unknown object, 409 stale or conflicting snapshot, 422 invalid request schema, 503 dataset/validator unavailable. Return structured `{code,message,requestId,snapshotId?}`; do not return stack traces. `If-Match` or `snapshotId` must bind multi-call workflows to one immutable snapshot. On mismatch, return 409 and offer refresh; never join across snapshots.

## Example response (illustrative, not implemented)
```json
{
  "releaseId":"release-demo",
  "snapshotId":"sha256:example",
  "policyVersion":"policy-v1-candidate",
  "assessmentStatus":"unknown",
  "assuranceStatus":"unverified",
  "dataStatus":"partial",
  "reasonCodes":["EVIDENCE_INVENTORY_INCOMPLETE"],
  "validationRunId":null,
  "advisoryOnly":true
}
```

## Contract test requirements
Schema validation; reason code enum stability; pagination determinism; bounded graph and truncation; stale snapshot 409; malicious literals encoded; backend unavailable; partial inventory; no user-controlled query execution; no write methods.
