# Page-by-page MVP Specifications

## Global shell
Persistent navigation: Overview / Ontology / Relationships / Evidence / Quality / Validation / Settings. Header shows active snapshot ID (short display + full copy), assurance state and theme/locale controls. Loading, empty, stale, error and truncated states are distinct. Small screens use accessible drawer; all pages expose data source and timestamp.

| Page | Primary question | API | Acceptance / edge state |
|---|---|---|---|
| Overview | Which snapshot and validation state am I seeing? | `/system/info`, `/overview` | never show green if assurance not verified; unknown inventory prominently |
| Ontology Explorer | What is this class/property and its canonical IRI? | `/ontology/terms`, `/ontology/terms/{id}` | search/pagination; bilingual labels with fallback; no edits |
| Relationships | How are entities connected? | `/graph/neighborhood` | 2-hop / 100-node hard cap, truncated warning, equivalent table |
| Evidence Explorer | What execution/evidence supports this obligation? | `/obligations`, `/obligations/{id}/evidence` | provenance + digest verification distinction, wrong build visible |
| Quality Decision | Why is this release qualified/unqualified/unknown? | `/releases`, `/releases/{id}/assessments` | reason codes, inventory status, assessment vs assurance; advisory disclaimer |
| Validation Status | Which checks ran on which snapshot? | `/validation/status` | not_run/failed/stale not disguised as passed |
| Settings | How do I change preferences and inspect versions? | `/system/info` + local storage | theme/locale/reset, readonly version fields, system mode |

## Responsive behavior
Desktop: navigation rail and detail panel; tablet: collapsible rail; mobile: drawer and single-column cards. Graph never the sole representation. Tables scroll with persistent headers only when accessible and tested.

## UX copy guardrails
- `qualified + verified`: “Qualified evidence (verified)”; **never** “Approved for release”.
- `qualified + not_run`: “Provisional qualification — validation not run”.
- `unknown`: “Insufficient information — do not infer a pass”.
- `unqualified`: “Evidence does not meet policy” + reason.
- Empty query result: “No matching records in this snapshot”, not “No risk”.
