# API & Semantic Contract / API 与语义契约

## Read-only endpoints
- `GET /api/v1/meta`：ontology version、dataset snapshot、validation summary。
- `GET /api/v1/ontology/classes?search=`：概念列表。
- `GET /api/v1/ontology/entities/{encoded_iri}`：定义、属性、映射。
- `GET /api/v1/graph?root=...&depth=1|2&limit=...`：有界局部图 + truncated。
- `GET /api/v1/releases`：发布索引。
- `GET /api/v1/releases/{id}/assessments`：按 obligation 的资格结果。
- `GET /api/v1/obligations/{id}/evidence`：证据详情。
- `GET /api/v1/validation`：校验状态。

## 判定模型
状态：`qualified` / `unqualified` / `unknown`。**三态是新 UI policy 设计，不是 v0.10 已实现功能。**

决策顺序（待 TDD 验证并经 ADR 审批）：
1. 快照、Release、Build、Requirement→Obligation 链或必需字段不完整 → `unknown` + 明确 reason；不使用 CQ-10 的空结果作为通过证据。
2. 数据完整，存在符合策略的关联证据 → `qualified`。
3. 数据完整，但无合格证据，且已知存在失败/环境不符/过期等明确反例 → `unqualified`。
4. 无证据但数据完整性/采集覆盖无法证明 → `unknown`（不默认 Unqualified）。

## Reason codes (MVP)
`MISSING_RELEASE_CUTOFF`, `MISSING_BUILD_ENVIRONMENT`, `MISSING_EXECUTION_STATUS`, `MISSING_EXECUTION`, `MISSING_EVIDENCE`, `FAILED_EXECUTION`, `ENVIRONMENT_MISMATCH`, `EXECUTION_AFTER_CUTOFF`, `EMPTY_DIGEST`, `WRONG_BUILD_LINK`, `UNVERIFIED_SOURCE`, `INCOMPLETE_GRAPH`, `VALIDATION_NOT_RUN`, `DATASET_PARSE_ERROR`。

## 溯源要求
每条 assessment 必须包含 `releaseId`, `obligationId`, `status`, `reasons[]`, `policyVersion`, `snapshotId`, `evaluatedAt`, `evidenceIds[]`；无法提供 provenance 时必须有 `UNVERIFIED_SOURCE`。

## 版本隔离
- UI adapter `api/v1` 不等于 ontology `v0.1`。
- UI 新字段不写回原始 RDF；不向现有本体添加 `owl:equivalentClass`。
- CQ-09/10 保留不改，用新判定器作为 UI 的唯一权威状态来源；两者差异记录到 regression report。
- 禁止将 `qualified` 翻译为“允许发布”；只翻译为“证据符合当前规则”。
