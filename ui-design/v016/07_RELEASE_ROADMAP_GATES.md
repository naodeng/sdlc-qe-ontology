# 版本路线与质量门禁

| 版本 | 目标 | 可延期 | 必须通过的门禁 |
|---|---|---|---|
| Sprint 0 | 消除语义/验证/组件阻断 | 动画、图谱美化 | SHACL、规则金标、标准映射处置、UI 构建 Spike、安全 |
| 0.1.0-alpha.1 | 后端 + snapshot + policy API | 图谱 | API schema、snapshot 隔离、0 false Qualified |
| 0.1.0-alpha.2 | Settings + Overview/Explorer/Evidence/Decision | 高级筛选 | theme/i18n E2E、reason codes、a11y |
| 0.1.0-beta.1 | 图谱 + Validation + 完整 E2E | 导出 | 图表一致、负例、性能、安全 |
| 0.1.0 | 本地只读 MVP | 所有写入 | EN/中文文档、安装/恢复、签署 Go |
| 0.2.0 | 受控本地导入与快照 | 增量同步 | 恶意文件/回滚/迁移预检 |
| 0.3.0 | 证据历史分析与策略模拟 | 复杂评分 | 策略结果可解释、非权威标记 |
| 0.4.0 | GitHub/CI 只读适配器 | 多提供商 | 显式授权、权限最小化、来源完整性 |
| 0.5.0 | 本体差异与版本治理 | 可视化编辑 | 兼容性矩阵、语义回归 |
| 0.6.0（建议新增） | 可重复评估和插件化只读数据适配 | Marketplace | 契约测试、沙箱、性能基准 |
| 1.0.0 | 稳定发布 | SaaS、多租户 | ≥2 真实项目验证、升级/回滚、安全/a11y 审核 |

版本独立：设计文档 v0.16 与软件 0.1.0 不可混用。每个 release 都需 changelog、ADR、负例、测试证据和风险登记。单人开发估时仍不确定，Sprint 0 后重新估算，不提前承诺发布日期。

**明确不做**：MVP 不做 ontology editor、任意 SPARQL 控制台、自动 Go/No-Go、远程数据同步、账号体系。
