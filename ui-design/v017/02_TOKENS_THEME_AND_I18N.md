# Tokens, theme, i18n and version metadata

## Theme
- User preference `themeMode`: `system | light | dark`, default `system`.
- Effective theme = explicit choice or OS `prefers-color-scheme` when system.
- Apply Arco theme mechanism and application semantic tokens consistently, before first paint. Verify current Arco React dark-mode API in installed version; do not assume Figma variables map 1:1.
- Persist only non-sensitive preferences in versioned localStorage. Malformed/unsupported values reset to safe defaults; reset never touches ontology or snapshots.
- System change updates only `system` mode; manual light/dark overrides system until changed.
- Check focus, contrast, graph edges, tables, overlays, loading and print for both themes; honor reduced motion.

## Locale
- `locale`: `system | en | zh-CN`, default system with English fallback. Set Arco ConfigProvider locale and application dictionaries together.
- API reason codes remain stable language-neutral enums; translate at display boundary. Unknown codes display safe fallback and original code.
- Locale changes must not affect assessment or snapshot.

## Version panel
Read-only fields: `appVersion`, `ontologyVersion`, `policyVersion`, `datasetVersion`, `snapshotId`, `validationReportId`, `apiVersion`. Missing values display `Unavailable`, never a design version placeholder.

## Semantic colors
Map Qualified/Unqualified/Unknown to Arco success/error/warning only for visual cues; status words and reason codes are always present. `assuranceStatus` is separately displayed (e.g. Verified/Blocked/Unavailable). Use tested tokens, not copied Animal Island colors.
