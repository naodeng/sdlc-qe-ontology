# Contributing / 贡献指南

English identifiers and schemas are canonical; contributor-facing explanations may be bilingual. Process documents are Chinese-first. Read AGENTS.md and `docs/standards/` before proposing changes.

For nontrivial changes: open a proposal/issue; define REQ and plan; create failing tests; implement and run the relevant quality gates; update the current fact documents; submit a PR with test evidence, compatibility, risk and rollback. Avoid uploading real customer data. External contributors must not add remote services or AI providers without explicit review.

For ontology semantic changes, explain URI migrations, SHACL impact, competency-query impact and proof of no false qualified assessments. Branch protection and mandatory CI checks should be configured in GitHub; their existence is not asserted by this document.
