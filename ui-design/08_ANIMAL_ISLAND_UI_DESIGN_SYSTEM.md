# Animal Island UI adaptation — v0.12

Status: design proposal; not implemented.

## References
- https://guokaigdg.github.io/animal-island-ui/
- https://github.com/guokaigdg/animal-island-ui
- https://github.com/guokaigdg/animal-island-ui/tree/main/docs/design-system

## Decision
Adopt `animal-island-ui` as the preferred React UI component library, subject to dependency/version and accessibility spikes. Do not fork or copy source code. Pin an exact tested version in lockfile; verify package exports before use. Import `animal-island-ui/style`. Respect MIT attribution obligations.

## Design language
- Cream canvas, warm brown text, sage/mint primary, peach highlights, muted blue for navigation.
- Large rounded cards, capsule filters, subtle 3D primary buttons, optional ribbon titles.
- Prefer quiet information density over excessive game-like animation.
- Text + icon + color for statuses; never rely on color alone.
- Respect reduced-motion preferences; focus visibility and keyboard navigation are mandatory.
- Use consistent tokens; exact values come from the pinned upstream design-system spec rather than guessed values.

## Page mapping
| Page | Components | Custom parts |
|---|---|---|
| Overview | Background, Card, Title, Tag, Skeleton | Snapshot status summary |
| Ontology Explorer | Input, Tabs, Collapse, Tag, Drawer | RDF term inspector |
| Relationship Graph | Card, Tooltip, Drawer, Select | Accessible graph canvas + list fallback |
| Evidence Explorer | Table, Pagination, Tag, Select | Evidence lineage table |
| Quality Decision | Card, Tag, Collapse, Tooltip | Tri-state rationale panel |
| Validation Status | Card, Table, Progress, Notification | SHACL/CI evidence status |

## Semantic safety
`Qualified`, `Unqualified`, `Unknown` are returned by the existing read-only API and must not be computed from colors or inferred by the frontend. Missing required fields, unrun SHACL, stale snapshot, or API failure must never render as Qualified. Distinguish `No results` from `No gaps`. Always display dataset/snapshot id, rule version, and evaluation timestamp.

## Out of scope
Ontology editing, rule editing, publishing approval, write APIs, decorative loading that obscures errors, automatic Go decisions.
