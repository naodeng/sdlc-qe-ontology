# Snapshot, Version and Provenance Contract

## Version taxonomy
| Field | Authority | Editable? |
|---|---|---|
| appVersion | build artifact | no |
| uiDesignVersion | docs, not runtime | no |
| apiVersion | OpenAPI contract | no |
| ontologyIri / ontologyVersion | RDF ontology metadata | no |
| policyVersion | pinned policy manifest | no |
| shapesVersion | SHACL package manifest | no |
| datasetVersion | import manifest | no |
| snapshotId | hash of canonical snapshot manifest and content hashes | no |
| validationRunId | validation report | no |
| builtAt | build metadata | no |

Use `unavailable` / null for unknown authoritative fields; never silently substitute UI design version.

## Manifest and consistency
A snapshot manifest records source filenames as sanitized logical IDs, SHA-256 of each input byte stream, ontology/policy/shapes version and hash, import timestamp, provenance declaration, completeness scope and known exclusions. Compute a deterministic snapshotId from canonical JSON (sorted keys, UTF-8, stable separators) **excluding volatile timestamps**, and record timestamps separately. Avoid implying a bare hash proves external authenticity.

A request carries `X-Snapshot-Id` (or query `snapshotId` for deep links); server compares to active immutable handle. On mismatch respond `409 SNAPSHOT_MISMATCH` with current snapshot ID and safe retry guidance. Every list and detail response returns its own snapshotId; the UI discards mixed-snapshot results and clears cached assessment badges on switch. Validation report is keyed by `(snapshotId, ontologyVersion, policyVersion, shapesVersion, validationRunId)`.

No implicit cache reuse across policy changes; stale tabs display a visible banner and refresh affordance. Fail closed on unreadable manifests, conflicting duplicate IDs, incomplete imports and malformed RDF; browsing of last known good snapshot is allowed only when clearly labeled stale and without verified green badges.

## Proposed immutable snapshot manifest example
```json
{
  "manifestSchemaVersion": 1,
  "datasetVersion": "sample-2026-10",
  "ontologyVersion": "unavailable",
  "policyVersion": "policy-candidate-1",
  "shapesVersion": "shapes-candidate-1",
  "sourceCoverage": {"declaredComplete": false, "scope": "example-only", "exclusions": ["external-ci"]},
  "files": [{"logicalId": "example-graph", "sha256": "<64 lowercase hex characters>"}]
}
```
The example is a **schema illustration**, not a valid production hash or certified inventory.
