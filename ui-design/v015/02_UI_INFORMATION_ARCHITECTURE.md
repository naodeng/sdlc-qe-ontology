# 页面与导航设计 / Information architecture

## Shell
Desktop: left sidebar + top dataset/snapshot switcher (read-only) + global validation banner + page content. Tablet/mobile: collapsible navigation, list fallback for graph, sticky status labels. Show snapshot ID and policy version in every decision detail. Global footer/About displays app, ontology, policy, dataset and UI build versions.

| Route | Page | P0 purpose | Empty/error/unknown behavior |
|---|---|---|---|
| `/` | Overview | active snapshot, totals, validation health, latest assessment | show counts with data freshness and completeness labels; no fake zero |
| `/ontology` | Ontology Explorer | classes, properties, definitions, bilingual labels, provenance | missing translation fallback English + indicator |
| `/relationships` | Relationship Graph | bounded 1–2 hop graph and equivalent accessible list | truncation badge; never imply hidden nodes absent |
| `/evidence` | Evidence Explorer | obligation → case → execution → evidence with filters | incomplete inventory displays Unknown |
| `/decisions` | Quality Decisions | assessment, assurance, reasons, source evidence and policy | blocked assurance prominent, no approval button |
| `/validation` | Validation Status | SHACL results, test run, timestamps, report versions | not_run shown distinctly from passed |
| `/settings` | Settings & About | theme, locale, reset, readonly version and runtime health | storage unavailable handled in-memory with notice |

## Page interaction contracts
**Overview:** counts include `asOf`, `scope`, `isComplete`; cards link to filtered lists. **Explorer:** searchable classes and properties, copy IRI, inspect provenance; no edit controls. **Graph:** cap nodes/edges/depth; keyboard-select node; equivalent list with same selection; filter and export only sanitized snapshot-bound data. **Evidence:** filter by obligation/release/build/status, show mismatch diagnostics; provenance drilldown. **Decisions:** always pair assessment and assurance; show reason codes and validation link; provide advisory-only language. **Validation:** list each gate `passed|failed|not_run|stale`, show reproducibility metadata. **Settings:** three-mode theme and locale, persistence/reset, version matrix.

## Design system / Animal Island UI
Use adapter components (`AppCard`, `AppButton`, `StatusTag`, `AppDialog`, `DataTable`, `AppDrawer`) rather than direct package imports in feature modules. Semantic tokens must cover surface, text, border, focus, danger, warning, success and unknown in light/dark modes. Never rely on color alone; pair icon, text, reason. Reduced motion and focus-visible required. Avoid cartoon styling on dense data and evidence screens.

## Layout breakpoints (targets, not verified)
360–599 px: one column; graph defaults to list. 600–1023 px: collapsible sidebar and two-column cards. ≥1024 px: persistent sidebar and detail split pane. Validate 200% zoom, long IRI strings and Chinese/English text expansion.
