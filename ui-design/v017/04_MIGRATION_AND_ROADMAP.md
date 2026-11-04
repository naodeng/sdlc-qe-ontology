# Migration plan and product roadmap

## Migration from v0.16 design
1. Mark `08_ANIMAL_ISLAND_UI_DESIGN_SYSTEM.md` and `09_ANIMAL_ISLAND_UI_TDD_AND_SPIKES.md` as historical/superseded. Do not delete provenance.
2. Replace any `animal-island-ui` dependency/imports with Arco adapter calls when code exists; scan package manifests, lockfiles, CSS, docs, CI and tests. Current package contains designs, not proof of a working UI implementation.
3. Extract actual representative Figma frames (dashboard, table, detail, settings) and map layout, typography, spacing, color and component variants; provided node is only a banner.
4. Perform Arco React dependency/license/React/Vite/theme/i18n/accessibility Spike.
5. Build AppShell and Settings first; run TDD; then migrate seven pages incrementally without changing API or policy.
6. Verify screenshot diffs, accessibility and all quality-state regression tests before deprecating old styling.

## Iterations (gated, not dates)
| Stage | Delivery | Exit gate |
|---|---|---|
| Sprint 0 | Arco integration Spike; app shell; theme/locale/version; policy/SHACL proof | Build + E2E + semantic gate evidence |
| v0.1.0 | 7 read-only pages, graph/list, snapshot-bound API, quality and assurance states | Goldens, security, a11y, performance |
| v0.2.0 | Controlled local dataset import and snapshot lifecycle | Preflight, rollback, malformed data isolation |
| v0.3.0 | Evidence analytics and policy simulation (read-only) | Deterministic baseline comparison |
| v0.4.0 | Authorized GitHub/CI read adapters | Provenance, credential safety, revocation |
| v0.5.0 | Ontology version diff, standards mapping view | Compatibility and migration evidence |
| v0.6.0 | Adapter extensibility and scalable graph | Performance and contract tests |
| v1.0.0 | Stable contracts and real-project validation | Two real projects, upgrade/recovery, security and a11y review |

## No-Go blockers
- pySHACL positive/negative execution not evidenced.
- Standards URI/semantics/license audit incomplete.
- Arco integration and theme behavior not validated in runtime.
- Policy tri-state and assurance golden tests not demonstrated.
- Provided Figma node insufficient to claim pixel-level reference coverage.
