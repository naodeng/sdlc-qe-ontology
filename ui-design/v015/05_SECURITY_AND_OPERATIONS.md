# Local-first 安全、性能、运维与升级

## Threat model
Localhost is **not automatically trusted**. Threats: DNS rebinding, cross-site requests to loopback, untrusted RDF literals, path traversal, malicious imported dataset, oversized graphs, resource exhaustion, stale browser state, package supply-chain compromise.

## Mandatory controls
- Bind loopback by default, never `0.0.0.0`; validate Host and Origin; use a session capability token or equivalent CSRF/rebinding defense for local HTTP API, even for sensitive read-only datasets.
- Restrict CORS to explicit local UI origin; reject arbitrary external Origins; deny state-changing methods and unapproved file access.
- Escape/sanitize RDF labels, IRI and error messages; no HTML rendering of untrusted RDF; restrictive CSP.
- RDF input size/time limits, safe parsers, graph node/edge/depth caps, query timeouts, memory bounds, deterministic pagination.
- Snapshot files immutable after ingest; hash and manifest verification; versioned validation artifacts; avoid accidental exposure of sensitive imported data in logs.
- Pin package versions and inspect package license and transitive dependencies before adopting Animal Island UI; avoid copying demo assets without checking usage rights.
- Do not auto-upgrade incompatible ontology/manifest versions. Provide clear unsupported-version diagnostics and a reversible import workflow; preserve original data.

## Performance budgets (proposed, must be measured)
On a defined benchmark fixture and target laptop: overview P95 < 500 ms after warmup; paged concepts P95 < 750 ms; bounded graph P95 < 1500 ms; 2-hop graph cap 200 nodes/400 edges; UI first meaningful content < 3 s. These are targets, **not measured results**. Log fixture size, hardware, runtime, and cache state.

## Accessibility
WCAG 2.2 AA target; keyboard access for all controls; focus return from dialogs; 200% zoom and 320 px layout; status icons+text; reduced motion; list parity for graph; contrast checked for both themes and high-contrast mode. Automated axe plus manual screen-reader/keyboard audit.

## Rollback
Rollback application and adapter package via pinned lockfile/build; snapshot never overwritten; preserve prior manifest and validation reports. On incompatible schema, refuse to open rather than attempt unsafe reverse migration.
