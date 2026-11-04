# UI integration TDD and spikes — v0.12

## Spike A: package integration
Given a clean React+TS+Vite scaffold, install a pinned compatible animal-island-ui release, import its stylesheet, render Button/Card/Table/Tag/Drawer. Validate build, production bundle, license notice, and browser console. Do not claim completed until executed.

## Spike B: accessibility
Keyboard tab order, visible focus, table headers, modal focus trap and escape, color contrast, reduced motion, screen reader status announcements; axe-core and Playwright checks. Upstream component behavior must be verified, not assumed.

## Spike C: graph usability
At 50, 200, 1000 nodes measure interaction latency and label overlap; cap initial graph to 2 hops and 100 nodes, with explicit truncation and searchable table fallback. Thresholds are candidate targets pending baseline hardware measurements.

## Acceptance tests (write first)
1. Unknown release shows explicit Unknown text and reason, never success color only.
2. Missing release cutoff stays Unknown even if a passing execution exists.
3. SHACL not run displays validation unavailable; not a green check.
4. Mixed passing/failing evidence uses backend result and shows provenance.
5. Stale snapshot displays a freshness warning.
6. Empty evidence search does not show `no quality gaps`.
7. Drawer and filters are keyboard operable; focus returns to trigger.
8. Reduced-motion mode disables decorative transitions.
9. All read-only routes reject attempted mutations server-side.
10. Data set ID and rule version are visible on decision detail.

## Exit gates
- Design accepted: component map and tokens reviewed.
- Integration accepted: clean build + accessibility spike evidence.
- MVP accepted: TDD green, E2E green, tri-state false-Qualified count = 0 on goldens, no skipped critical tests.
- Ontology baseline still blocked independently until SHACL and standards audit pass.
