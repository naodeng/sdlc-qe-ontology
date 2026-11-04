# v0.9 Evidence qualification spike / 证据资格实验

## Scope

CQ-09 returns only evidence explicitly linked to a release build and an execution satisfying **passed status, matching environment, execution timestamp no later than release cutoff, and a non-empty digest string**. CQ-10 identifies release obligations lacking such evidence **within the provided RDF snapshot**.

These are **demonstration-level qualification predicates**, not security attestations. A non-empty digest is NOT cryptographic verification. A `passed` literal is NOT proof of test validity. Release cutoff is NOT an evidence TTL; freshness policy remains unspecified. No issuer signatures, provenance authentication, coverage sufficiency, authorization, or actual CI artifact integrity is checked.

## TDD fixtures

- `evidence-valid-v09.ttl`: positive control.
- `evidence-failed-v09.ttl`: unsuccessful execution.
- `evidence-environment-v09.ttl`: mismatch.
- `evidence-stale-v09.ttl`: execution later than release cutoff (not a general age-based stale rule).
- `evidence-missing-digest-v09.ttl`: empty digest.
- `evidence-wrong-build-v09.ttl`: execution not attached to the release build.

## Design constraints

Open-world ontology does not establish absence. `FILTER NOT EXISTS` is a **snapshot completeness policy** only. For production, introduce authoritative data source scope, completeness marker, signature/digest verification, allowed environment promotion, time windows, evidence issuer and artifact immutability. Avoid declaring `owl:equivalentClass` to OSLC terms before normative verification.

## Acceptance

Run `python -m unittest discover -s tests -v`; the legacy pySHACL test is intentionally required and will fail until the dependency is installed. Run targeted tests with `python -m unittest discover -s tests -p 'test_evidence_qualification_v09.py' -v`. Full Go remains blocked.
