# 风险登记、决策门禁与下一步

| Risk | Severity | Status | Mitigation / proof required |
|---|---|---|---|
| SHACL actual execution absent | Blocker | Open | pinned pySHACL run, negative fixture logs |
| OSLC/PROV-O exact term and rights | Blocker | Open | primary source review and mappings |
| Tri-state completeness ambiguity | Blocker | Open | ADR, goldens, CI-source attestation |
| Animal Island UI compatibility/license | High | Open | install/build/keyboard/license spike |
| Localhost origin/rebinding | High | Open | security tests and token strategy |
| Missing source versions | High | Open | immutable manifest contract |
| Policy/validation stale mismatch | High | Open | snapshot/version binding and 409 |
| A11y graph and dark mode | High | Open | list parity, axe/manual audit |
| Evidence authenticity confusion | High | Open | cryptographic source policy, clear UI wording |
| Unbounded graph/performance | Medium | Open | caps, timeout and benchmark |

## Decision gates
**G0 Design**: ADRs and goldens reviewed; **G1 Standards**: exact mapping/rights verified; **G2 Semantic**: real SHACL pass/fail fixtures; **G3 Policy**: adversarial decision goldens; **G4 API**: snapshot and schema contract; **G5 UI/security**: package build, theme/locale, a11y, loopback controls; **G6 Release**: pilots, docs, rollback, signed decision.

A design document or a passing static parser is not evidence of G2/G5. An unresolved blocker = No-Go for full MVP. Sprint 0 bounded validation work is authorized as a proposal, not automatically approved.

## Next actions
1. Approve ADR-001, 003, 007, 008 with product/QE reviewer; finalize policy goldens.
2. Run pySHACL in reproducible environment and attach real outputs.
3. Audit standards terms/rights and Animal Island UI package compatibility.
4. Implement snapshot manifest and API skeleton TDD.
5. Convene G0–G5 evidence review before Sprint 1 kickoff.
