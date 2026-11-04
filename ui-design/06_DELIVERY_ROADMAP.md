# MVP Roadmap / 迭代与准入

## Sprint 0 — 语义与环境阻断解除（先决条件）
- UI-000 盘点 v0.10 schema/query/fixtures，固定 snapshot 机制。
- UI-001 完成三态 policy ADR、数据完整性矩阵、测试金标。
- UI-002 在完整环境执行 pySHACL，保留正反样本报告；失败则阻断质量状态页。
- UI-003 标准术语精确 URI/许可审计：不影响 UI 原型但阻断正式 baseline 批准。
**Exit**：状态判定契约评审通过，测试样本完整；SHACL 实际执行有证据。

## Sprint 1 — Backend read-only API
- UI-101 RDF loader + snapshot hash；UI-102 allowlisted SPARQL adapter；UI-103 三态判定器；UI-104 API v1 schema + pytest。
**Exit**：UI-001~009 对应 backend tests 全绿，API 仅只读。

## Sprint 2 — Core pages
- UI-201 Overview；UI-202 Ontology Explorer；UI-203 Evidence Explorer；UI-204 Quality Decision；UI-205 中英切换。
**Exit**：主要旅程可用，Unknown 视觉不误导。

## Sprint 3 — Graph & Validation
- UI-301 局部关系图及列表 fallback；UI-302 Validation Status；UI-303 错误态/可访问性；UI-304 Playwright E2E + 性能/安全 smoke。
**Exit**：P0 E2E、可访问性与安全门禁全绿。

## MVP Go/No-Go
**Go** 仅当：P0 验收通过、SHACL 真实验证通过、0 false-qualified、API 不可写、可追溯快照与规则版本、运行手册与回滚方案齐全。
**No-Go**：任意 Unknown→Qualified 误判；缺失字段导致绿色通过；SHACL 被跳过；原始 RDF 被 UI 修改；无法重现判定结果。

## 后续非 MVP
任意 SPARQL 查询、标准映射编辑、本体版本比较、团队权限、数据源连接器、自动导入 PR/CI 数据；均需单独风险与安全设计。
