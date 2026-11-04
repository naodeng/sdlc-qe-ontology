# Security, Graph Bounds and Accessibility

## Threat model (local-first != inherently safe)
- Bind backend to `127.0.0.1` only by default; enforce Host allowlist (including IPv4/IPv6 policy) and reject unexpected Origin on browser requests. Explicitly restrict CORS to configured local UI origin; no wildcard credentials.
- Do not expose mutation routes. Disable arbitrary SPARQL, RDF upload, remote URL fetching, local path parameters and unrestricted IRI dereferencing in MVP. SPARQL queries are server-side fixed templates with typed parameter binding, not string concatenation.
- Reject malformed/oversized IDs and path traversal. Do not echo filesystem paths or secrets in errors. Bounded response size, timeouts and query budgets; pagination and hard graph node/edge caps.
- Serve UI with restrictive CSP; sanitize untrusted RDF literal text and avoid HTML injection in graph labels. No telemetry by default; avoid embedding external fonts/images.
- Keep UI settings separate from authoritative policy/ontology data. Use file read-only handles and explicit source directory permissions.

## Graph semantics
Graph endpoints return `truncated`, `limit`, `returnedNodes`, `returnedEdges`, `omittedNodesKnown` (nullable) and `scope`. Never label a truncated graph as complete. Provide equivalent sortable accessible relationship table. Max 2 hops and max 100 nodes for MVP; enforce server cap even if client requests more.

## Accessibility
Target WCAG 2.2 AA. Test keyboard-only flows, visible focus, skip link, accessible names, heading hierarchy, screen-reader announcement of snapshot and assurance changes, status without color reliance, focus return after modal close, no motion essential to comprehension, graph list parity. Automated axe checks are necessary but not sufficient; record manual screen-reader audit.

## Security negative tests
Host spoofing / DNS rebinding, foreign Origin, oversized graph request, malicious RDF literal HTML, malformed IRI, snapshot mismatch, CORS preflight, cross-origin browser fetch, forced file path query, query timeout, CSP violation.
