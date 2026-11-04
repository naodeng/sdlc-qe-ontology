# Settings, Theme, Locale and Animal Island UI Adaptation

## Sprint 0 P0 settings
- `theme: system | light | dark`, default system; `locale: system | en | zh-CN`, default system; unsupported system locale resolves to English.
- Store only non-sensitive preferences in `localStorage` key `sdlc-qe.preferences.v1`, strict allowlist schema `{schemaVersion:1,theme,locale}`. Ignore unexpected fields. Corrupt, inaccessible, future schema or quota errors must not prevent app startup. Unknown future schema => default in memory, do **not** overwrite future data until user explicitly resets.
- Settings reset removes only preference key, never RDF, snapshots or validation reports. Confirm reset and expose visible feedback.
- Theme applied before React mount via tiny trusted bootstrap; use `prefers-color-scheme` listener only while theme is system; remove listener on cleanup. Avoid flash of wrong theme. Locale selection is independent of theme.
- Preference changes immediate and keyboard accessible; persistence failure surfaces a nonblocking warning (current session still works).
- Reduced-motion respects OS and has no essential animation; focus ring and contrast tokens audited in both themes.

## UI adapter
Wrap third-party components behind `src/ui/adapter` exports (`Button`, `Card`, `Dialog`, `Tabs`, `Table`, `Tag`, `Drawer`) so upstream package changes cannot leak across the app. Use semantic tokens `--surface`, `--text`, `--muted`, `--border`, `--focus`, `--status-qualified`, `--status-unqualified`, `--status-unknown`; provide light/dark definitions and high-contrast checks. Quality status always includes text, icon and reason, not color alone.

## Theme token draft (illustrative, not final validated contrast)
| Token | Light | Dark |
|---|---|---|
| surface | #FFF9F0 | #232927 |
| panel | #FFFFFF | #303936 |
| text | #443D34 | #F4EEE4 |
| muted | #665B4D | #D0C4B5 |
| border | #D9CBB9 | #69756F |
| focus | #704E9E | #D1B3FF |

Do not freeze these token values before WCAG contrast checks.

## i18n rules
English is canonical key catalog; zh-CN complete translation for all P0 pages, status labels, error codes and settings. Missing keys fail CI. `Intl` for locale-sensitive dates/numbers; timestamps remain ISO 8601 in API. Switching language never changes RDF identifiers, query semantics or decision results. Distinguish localized display labels from ontology canonical IRI.

## Version panel
Display appVersion, apiVersion, ontologyVersion/IRI, policyVersion, shapesVersion, datasetVersion, snapshotId (copyable), validationRunId, validationStatus and builtAt from read-only `/api/v1/system/info`. Missing data shows `Unavailable`, not invented defaults.

## Component integration spike (not yet executed)
Pin exact package version and verify license/peer dependencies, exports/CSS, Vite production build, dark-mode token override, Dialog focus trap, keyboard navigation, contrast and reduced motion. If incompatible, adapter can use accessible local fallback; record tradeoff in ADR-004. No unverified assumption about published component exports is a pass criterion.
