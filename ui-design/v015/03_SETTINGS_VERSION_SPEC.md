# 设置、主题、语言与版本治理

## Preference schema
`{schemaVersion:1, theme:'system'|'light'|'dark', language:'system'|'en'|'zh-CN'}`. Defaults: system theme and system language (supported locale else English). Save non-sensitive preferences only; localStorage may fail or be denied, then operate in memory with a nonblocking notice. Never store ontology/evidence or secrets in localStorage.

## Startup algorithm
1. Parse preferences with schema validation and explicit migration; unknown future schema => safe defaults, do not overwrite unknown record without user action.
2. Resolve `system` via `matchMedia('(prefers-color-scheme: dark)')`; apply `data-theme` before first render to avoid flash.
3. Listen to media query changes only while mode is `system`; manual selection wins.
4. Resolve locale from navigator languages; load English fallback; persist explicit user override.
5. Apply Animal Island UI token adapter; include reduced-motion and high-contrast behavior.
6. Reset requires confirmation, affects only UI preferences; does not mutate snapshots, validations, or reports.

## Version metadata
| Field | Source | Example placeholder | Editable? |
|---|---|---|---|
| appVersion | build-time package metadata | `0.1.0-dev` | no |
| uiBuildCommit | CI/build metadata | SHA | no |
| ontologyVersion | ontology manifest | semantic version or IRI | no |
| policyVersion | signed/versioned policy manifest | `policy-v1` | no |
| datasetVersion | dataset manifest | dataset-specific version | no |
| snapshotId | content-addressed snapshot manifest | digest | no |
| validationRunId | actual validation report | run ID | no |
| uiDesignBaseline | docs | `v0.15` | no |

Missing values render `Unavailable` and diagnostic reason; never substitute design version for application version. If manifest is stale, label stale. API `GET /api/v1/system/info` returns values with origin and last-updated metadata.

## Acceptance scenarios
System light→dark; manual override; reload; corrupt record; future schema; storage blocked; reset scope; missing translation; missing version; stale backend; contrast in both modes; focus and keyboard navigation; no flash on first paint.
