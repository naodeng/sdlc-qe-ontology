# API v0.16 — 接口详细契约

统一前缀 `/api/v1`；所有业务查询只读。版本化 JSON；错误格式 `{code,message,requestId,snapshotId?,details?}`。所有业务响应包含 `{snapshotId, ontologyVersion, policyVersion, evaluatedAt, data}`；不得混合不同快照的资源。

| Endpoint | 必需参数 | 响应核心 | 特殊行为 |
|---|---|---|---|
| GET /system/info | — | appVersion, ontologyVersion, datasetVersion, snapshotId, policyVersion, buildCommit | 未连接时字段 null + availability |
| GET /system/health | — | api, dataset, validation, degraded | 不暴露敏感路径 |
| GET /snapshots/current | — | id, createdAt, manifestHash, completeness | 不可变 ID |
| GET /overview | snapshotId | counts, assessmentBreakdown, assurance | 数据不全时 counts 标明 partial |
| GET /ontology/concepts | snapshotId, cursor?, limit?, locale? | items, nextCursor | limit 1..100 |
| GET /ontology/concepts/{id} | snapshotId | IRI, labels, properties, mappings | ID 必须 canonical encode |
| GET /graph/neighborhood | snapshotId, nodeId, depth? | nodes, edges, truncated | depth<=2, nodes<=200 |
| GET /obligations | snapshotId, status?, cursor? | items, nextCursor | 固定查询 |
| GET /obligations/{id}/evidence | snapshotId | evidence, provenance, reasons | 不输出文件原始路径 |
| GET /releases/{id}/assessment | snapshotId | assessmentStatus, assuranceStatus, reasons, obligations | 所有结论带版本 |
| GET /validation/status | snapshotId | checkId, status, startedAt, reportHash | 未运行 != 通过 |

**版本语义**：`appVersion` 来自构建，`ontologyVersion` 来自本体，`datasetVersion` 来自数据集 manifest，`policyVersion` 来自规则包；UI 文档 v0.16 不能当作应用版本。

**错误码**：`SNAPSHOT_MISMATCH` (409)、`SNAPSHOT_NOT_FOUND` (404)、`INVALID_PARAMETER` (422)、`DATASET_UNAVAILABLE` (503)、`VALIDATION_BLOCKED` (200 内业务状态，不是 HTTP 失败)、`INTERNAL_ERROR` (500)。快照切换后，旧快照若仍保留可以继续查询，否则明确 409/410，禁止静默重定向到新快照。

**并发一致性**：客户端启动读取 currentSnapshot，后续请求显式传 snapshotId。发现切换时提示刷新整个视图；禁止只刷新单个证据卡而保留旧图谱。
