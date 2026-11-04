# v0.10 — Evidence qualification adversarial evaluation

## Goal
Evaluate CQ-09 and CQ-10 against adversarial graph fixtures without claiming that query success proves production-grade evidence integrity.

## Cases
- mixed-outcomes: one valid execution and one failed retry; qualified evidence must include only the valid evidence.
- missing-execution: evidence-producing execution is not attached to the build.
- late-only: execution occurs after the release cutoff.
- empty-digest: empty evidence digest string.
- wrong-evidence-link: evidence references a different execution.
- missing-cutoff, missing-build-environment, missing-status: missing required facts.

## Important finding
CQ-10 silently omits releases with missing `releaseCutoff` or builds without `buildEnvironment`. These are **data completeness gaps**, not successful releases. The current CQ-10 is not a full release readiness verdict. A separate completeness check and explicit three-valued status (qualified / unqualified / unknown) are required before Go.

## Remaining risks
- No cryptographic digest verification; a digest-like string is not proof of integrity.
- No policy for multiple builds, retries, revocations or trusted execution provenance.
- RDF Open World Assumption means absence in a graph snapshot is not global absence.
- SHACL validation has not passed in this environment.
