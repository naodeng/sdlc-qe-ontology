# 三态判定与保证状态的正式候选契约

## Types and invariants
`assessmentStatus ∈ {qualified, unqualified, unknown}`; `assuranceStatus ∈ {verified, unverified, blocked}`; `dataStatus ∈ {ready, partial, invalid, unavailable}`. An API failure may return HTTP 503 with diagnostics instead of a fabricated assessment.

**Obligation-level rules, in order:**
1. If the obligation's existence, applicability, required build/environment/cutoff, or completeness of relevant evidence search cannot be established, `unknown` unless a policy-defined disqualifying fact is already verified.
2. If a **verified** disqualifying fact exists (e.g., required test definitively failed for the relevant build under policy), `unqualified` even if other data is missing; report uncertainty separately. Whether failure is overriding or superseded is policy-versioned, never inferred from recency alone.
3. If a complete, scoped search establishes no qualifying evidence, `unqualified` with `NO_QUALIFYING_EVIDENCE`. Without completeness attestation, `unknown` with `EVIDENCE_INVENTORY_INCOMPLETE`.
4. If qualifying evidence exists and mandatory checks pass, `qualified`. If any required check is missing, `unknown`.

**Release aggregation:** if release obligation inventory is not attested complete, never `qualified`. If at least one verified, applicable obligation is `unqualified`, aggregate `unqualified` (with coverage caveat); otherwise if any unknown or incomplete inventory, aggregate `unknown`; only all qualified + complete inventory yields `qualified`. Zero obligations is `unknown` unless explicit approved zero-obligation policy and completeness proof exist.

**Assurance:** `verified` requires matching snapshot/policy/validation-run IDs, SHACL success, evidence provenance integrity and mandatory rule tests; `blocked` for failed validation, invalid graph, mismatch or critical integrity failure; `unverified` for checks not run or stale. UI never combines `qualified + unverified` into a green verified badge. If `blocked`, UI shows diagnostic warning and disables positive release-ready language.

## Example decision table
| Input | Assessment | Assurance | Reason |
|---|---|---|---|
| Complete inventory, passing current-build evidence, all checks pass | qualified | verified | ALL_OBLIGATIONS_QUALIFIED |
| Missing cutoff | unknown | unverified | CUTOFF_MISSING |
| Wrong build only, evidence inventory complete | unqualified | verified* | NO_QUALIFYING_EVIDENCE |
| Wrong build only, inventory incomplete | unknown | unverified | EVIDENCE_INVENTORY_INCOMPLETE |
| Definitive failure under policy | unqualified | verified* | REQUIRED_TEST_FAILED |
| SHACL not run | computed assessment may be retained for diagnostics | unverified | SHACL_NOT_RUN |
| SHACL fails on critical shape | no trusted positive conclusion | blocked | SHACL_FAILED |
| Snapshot IDs differ across data and evaluation | unknown or 409 | blocked | SNAPSHOT_MISMATCH |

`*` Verified applies only if the source inventory, relevant negative fact, and all mandatory checks are themselves verified.

## Explicit unresolved policy choices
- Which failed executions invalidate an obligation versus being superseded by a newer pass? **Must be decided by ADR-007.**
- How to assert completeness for imported CI data? **Must be decided by ADR-008.**
- Evidence cryptographic authenticity is not implied by a non-empty digest. Verification needs explicit algorithm, bytes, source and trust policy.

## Tests before implementation
Fixtures: complete pass; mixed pass/fail; stale pass; wrong build; wrong environment; no cutoff; no inventory; duplicate execution; zero obligations; failed SHACL; stale validation; mixed snapshots; malicious literal; conflicting provenance. Each fixture must specify expected assessment, assurance, reason codes and evidence IDs.
