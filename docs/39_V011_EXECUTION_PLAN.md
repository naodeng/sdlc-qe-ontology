# v0.11 execution plan

1. **Completeness classification (TDD):** implement release-level `qualified / unqualified / unknown` evaluation, with explicit required fields and missing-fact reporting.
2. **SHACL:** run positive and negative fixtures under pinned pySHACL in CI and attach full logs.
3. **Standards audit:** verify exact OSLC RM/QM/CM and PROV-O terms, versioned URIs, mappings, licenses, and no unsafe `owl:equivalentClass`.
4. **Evidence security:** verify digest format and content, execution provenance, revocation and retention policy.
5. **Pilot:** evaluate at least one anonymized real PR→Build→Release trace against a deterministic non-ontology baseline.

Exit criterion: all blocking gates have independently reproducible evidence, otherwise No-Go.
