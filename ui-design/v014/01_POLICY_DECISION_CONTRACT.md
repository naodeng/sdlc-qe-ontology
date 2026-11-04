# Quality Policy & Assurance Contract v0.14

## Key distinction
`assessmentStatus` is **qualified | unqualified | unknown**: a policy calculation over a named immutable snapshot and policy version. `assuranceStatus` is **verified | blocked | not_run | stale | unavailable**: confidence in required validation, not a fourth assessment state. A computed qualified assessment with assurance != verified MUST be rendered as **provisional / not verified**, never a green verified pass.

## Obligation-level algorithm (proposed ADR-001)
1. Determine inventory/edge completeness from an explicit signed-off import manifest and coverage declaration. Absence of RDF triples is **not** proof of absence (OWL open-world assumption).
2. Evaluate global hard blockers (e.g. confirmed tampering or forbidden build association) per policy; such blockers make `unqualified` only when scope and identity are sufficiently established. Otherwise `unknown`.
3. If required fields, release cutoff, environment, build identity, evidence origin, or inventory coverage are incomplete => `unknown` unless an independently conclusive non-overridable violation is confirmed.
4. If at least one eligible evidence record meets all policy checks and no non-overridable blocker exists => `qualified` at assessment layer; preserve failed attempts in history.
5. If coverage is certified complete, all candidates were examined and none qualifies => `unqualified` with explicit reason(s). If candidate enumeration is incomplete => `unknown`.
6. Evidence digest **presence** is not digest verification. Treat authenticity as unverified until bytes and trusted source are checked.

## Release aggregation (proposed)
| Inventory | Obligations | Aggregate |
|---|---|---|
| incomplete/unknown | any | unknown unless independently conclusive hard-blocker is confirmed; see ADR |
| certified complete, nonempty | any unqualified | unqualified |
| certified complete, nonempty | no unqualified, any unknown | unknown |
| certified complete, nonempty | all qualified | qualified |
| certified complete, empty | none | unknown (no vacuous pass) |

**Important precedence nuance:** when inventory itself is incomplete, known unqualified findings must be surfaced as blocking findings, but a single aggregate status is **unknown** until an approved policy explicitly defines the independent hard-blocker exception. Do not silently infer completeness. This resolves the conflicting precedence found in v0.13 review by prioritizing inventory trust.

## Assurance gate
- `verified` requires SHACL run passed against the **same snapshot**, required semantic tests passed, policyVersion and ontologyVersion pinned, no stale validation report, provenance verification at the policy-required level, and complete source manifest.
- `blocked` for known failed mandatory gate; `not_run` if never executed; `stale` if snapshot/policy changed; `unavailable` if report cannot be retrieved.
- UI may display evidence and diagnostics under any assurance status, but only `qualified + verified` may use the phrase **Qualified (verified)**; never label this as Release Approved.

## Test truth table
| Case | assessment | assurance (example) |
|---|---|---|
| Complete + one eligible pass + all gates passed | qualified | verified |
| Complete + all executions failed | unqualified | verified |
| Missing release cutoff | unknown | blocked/not_run |
| Missing build environment | unknown | blocked/not_run |
| Partial import manifest | unknown | blocked |
| Empty obligation inventory | unknown | verified (verification of data ≠ complete scope) |
| Pass and fail for same obligation, valid pass remains | qualified | verified |
| Wrong build only, complete enumeration | unqualified | verified |
| Passing evidence but SHACL not_run | qualified (provisional) | not_run |
| Snapshot switched after assessment | unknown until recomputed | stale |

## Reason code examples
`MISSING_CUTOFF`, `MISSING_ENVIRONMENT`, `INCOMPLETE_INVENTORY`, `WRONG_BUILD`, `FAILED_EXECUTION`, `NO_ELIGIBLE_EVIDENCE`, `DIGEST_NOT_VERIFIED`, `VALIDATION_NOT_RUN`, `STALE_SNAPSHOT`, `UNTRUSTED_SOURCE`. Stable codes + localized text, never free-text-only semantics.

## Cautions
No automatic Go/No-Go. A release decision is a human process with independent business risk and exception approval. Qualification does not prove test effectiveness or requirement coverage.
