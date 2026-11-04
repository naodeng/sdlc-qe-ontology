# 更新后的迭代路线与依赖

## 时间假设
以下按 **1 名全职工程师 + 兼职 QE/Reviewer，2 周一个 Sprint** 的初步规划；为估算而非承诺。导入前移后，原 v0.16/v0.17 的 3 Sprint MVP 计划被覆盖。Sprint 0 的 Spike 结果可能改变排期。

| 阶段 | 目标 | 核心交付 | Exit Gate | 粗估 |
|---|---|---|---|---|
| Sprint 0 | 可行性与基线 | SHACL/规则金标、Arco 构建、解析器安全、快照原子性 Spike、Mapping schema | 阻断项通过/处置 | 2–3 周 |
| Sprint 1 | 工作区+UI 基座 | Workspace、Settings、Arco shell、manifest/lock、API contract | 端到端创建/打开工作区 | 2 周 |
| Sprint 2 | 导入与字段映射 | CSV/JSON/RDF 受限导入、模板、可视化映射、审批 | T01–T05、T11–T13 | 2 周 |
| Sprint 3 | 验证与快照 | SHACL、DQ、source provenance、原子提交/恢复 | T06–T10、T14、T17 | 2 周 |
| Sprint 4 | 分析与追溯 | 7 页、质量三态、证据链、reason codes、报告 | T07–T08、T15、跨页快照一致 | 2 周 |
| Sprint 5 | 真实项目验收 | 脱敏项目试点、性能、安全、a11y、安装恢复 | G0–G5、签署 Go | 2 周 |

**总粗估**：Sprint 0 后 10 周左右实施；含 Sprint 0 约 12–13 周。实际可能因 RDF 解析器安全和快照跨平台原子性上浮。

## 后续版本
- **v0.2.0**：映射配置复用、差异导入、增量更新预检、数据质量趋势；不再把“首次真实数据导入”作为卖点。
- **v0.3.0**：历史证据对比、策略模拟、风险解释；必须区分模拟与正式评估。
- **v0.4.0**：GitHub/CI 只读适配器、授权与 provenance、变更影响链。
- **v0.5.0**：Ontology 版本差异、兼容性诊断、迁移预览。
- **v0.6.0**：可重复 Eval、只读适配器扩展机制、性能基准。
- **v1.0.0**：至少两个真实项目复现、稳定 API/迁移/回滚、安全与无障碍审计。

## 关键依赖路径
Mapping contract → Parser safety → Preview → Mapping approval → DQ/SHACL → Snapshot commit → Quality policy → UI/E2E → Pilot。UI shell 可以并行，但不能绕过前述依赖做假数据“已验证通过”。

## 建议 GitHub Issues/Epics
EPIC-01 Workspace；EPIC-02 Import & Mapping；EPIC-03 Validation & Snapshot；EPIC-04 Evidence & Policy；EPIC-05 Arco UI；EPIC-06 Security & E2E；EPIC-07 Real Project Pilot。每项 Issue 包含 Given/When/Then、负例、依赖、完成证据和回退说明。
