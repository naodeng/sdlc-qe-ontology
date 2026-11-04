# 后期迭代路线图 / Versioned roadmap

**Important:** historical document versions v0.10–v0.15 are *design/baseline candidates*, not released software. Product releases start at `0.1.0` after gates. Dates below are effort estimates, not commitments. Assume 1 full-time engineer + part-time QE/reviewer; 1 sprint ≈ 2 weeks. Re-estimate after Sprint 0.

| Phase / Release | Estimated effort | Main scope | Exit gate | Explicitly deferred |
|---|---:|---|---|---|
| Sprint 0 / Gate | 2–3 weeks | policy goldens, SHACL real run, standards term audit, manifest, Animal Island UI compatibility spike, theme/locale scaffold, local security | all P0 spikes reproducible; no skipped mandatory checks | business UI |
| Sprint 1 / `0.1.0-alpha.1` | 2 weeks | read-only backend, immutable snapshot, 10 endpoints, typed contracts, deterministic policy | API contract + golden cases + snapshot 409 | graph editor |
| Sprint 2 / `0.1.0-alpha.2` | 2 weeks | shell/settings, Overview, Ontology Explorer, Evidence Explorer, Quality Decisions | theme/locale E2E, no false verified badge | imports, multi-user |
| Sprint 3 / `0.1.0-beta.1` | 2 weeks | graph/list parity, Validation page, accessibility/security/perf | full E2E and benchmark evidence | free-form SPARQL |
| Release `0.1.0` | 1 week hardening | docs EN/中文, installer/local runbook, reproducible demo, changelog, rollback | release Go/No-Go signed | remote sync |
| `0.2.0` | 2–3 sprints | controlled local dataset import, schema validation, provenance & source mapping, incremental refresh, import preview | import safety, no overwrite, deterministic diff | live SaaS |
| `0.3.0` | 2–3 sprints | advanced evidence analysis: policy simulation (non-authoritative), richer risk explanations, history comparison | counterfactual tests, no false confidence | auto release decision |
| `0.4.0` | 2–3 sprints | GitHub/CI read-only adapters via explicit opt-in, connector credential isolation, data lineage | permission/security integration tests | write-back |
| `0.5.0` | 2–3 sprints | ontology version diff, mapping explorer, compatibility diagnostics, migration preview | semantic regression and version fixtures | ontology editor |
| `1.0.0` | after ≥2 pilot projects | stable public contracts, documented support policy, tested upgrade/rollback, quality benchmark & governance | real-world pilots, SLO, accessibility/security signoff | full platform |

## Cross-cutting work every release
TDD red→green→refactor; negative fixtures; policy and SHACL regression; bilingual docs; dependency and license review; threat model update; performance and accessibility; changelog and migration notes; baseline comparison against deterministic non-ontology query implementation.

## Prioritization logic
P0 = avoids false quality confidence, unsafe data access, or irreproducible result. P1 = improves usability/observability without weakening P0. P2 = integrations and advanced visualization. No feature proceeds if it requires changing v0.10 semantics without explicit ADR and migration tests.

## Resourcing risks
Animal Island UI API/version unknown until spike; pySHACL environment previously blocked; exact OSLC mapping/license still open; completeness attestation for CI imports may be expensive. Each can shift the schedule. Scope-cut rule: drop optional charts/animations before cutting policy/assurance/validation.
