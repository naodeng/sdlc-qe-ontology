# SDLC-QE Ontology Workbench — UI MVP Design v0.11

Status: **Design Candidate / No-Go**. This is a design package, not an implemented UI or an approved ontology baseline.

定位：方案 A，Local-first 只读查询工作台。现有 v0.10 ontology、queries、shapes、tests 原样保留。UI 不负责修改 RDF、审批 Release、自动生成 Qualified 结论。

## 交付目录
- `01_PRODUCT_SCOPE.md`：定位、角色、边界和 MVP
- `02_ARCHITECTURE.md`：架构、技术选型和安全
- `03_PAGES_AND_WIREFRAMES.md`：页面、线框和交互
- `04_API_AND_SEMANTIC_CONTRACT.md`：API、状态语义和映射
- `05_TDD_ACCEPTANCE.md`：测试先行和可追溯验收
- `06_DELIVERY_ROADMAP.md`：Sprint、依赖和 Go/No-Go
- `07_ADR_AND_RISKS.md`：决策与风险
- `contracts/openapi.yaml`：API 候选契约
- `examples/release-assessment.json`：示例数据（非实际查询结果）

建议先解决 v0.10 CQ-10 缺字段漏报问题，再开放质量状态页面。UI 的 Unknown 判定需要独立的完整性检查，不能直接从 CQ-10 空结果推导。
