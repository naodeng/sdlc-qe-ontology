# v0.18 — MVP 真实项目导入 + 字段映射 B（决策基线）

**状态**：产品范围与映射方案已由用户确认；技术细节为待 Spike 验证的候选设计。设计版本 v0.18，不等于软件发布版本。

## 决策记录
- PRODUCT-ADR-008（Accepted）：真实项目本地数据导入前移到 **0.1.0 MVP**。原 v0.17 的「MVP 不含外部导入」及旧路线图「0.2.0 才导入」均被覆盖。
- PRODUCT-ADR-009（Accepted）：选择 **B：标准模板 + 可视化字段映射 + 人工确认**。AI 自动映射不进入 MVP；可以提供确定性别名提示，但不得自动确认。
- UI-ADR-017（保持）：Arco Design Pro 2.0 设计参考、Arco React 候选组件库；**不再使用 Animal Island UI**。
- SEC-ADR-018（Proposed）：所有导入均先在隔离区完成解析、映射、验证和快照制作；失败不得改变 active snapshot。

## 不变的原则
Local-first；无云账号、无外部自动同步；语义模型不由 UI 反向定义；仅数据导入工作流可写入工作区，分析查询仍只读；用户最终确认；审计与可追溯；不自动批准发布。

## 必须在 Sprint 0 冻结的开放项
1. JSON 输入格式：只接受平台定义的数组/对象 schema，还是支持 JSONPath 子集；推荐前者。
2. RDF 支持格式：推荐 Turtle 与 JSON-LD 受限 profile，禁止远程 context；是否支持 RDF/XML 需安全 Spike。
3. workspace manifest、锁机制、文件系统原子 rename 的平台兼容性。
4. Ontology、policy、mapping profile 版本兼容矩阵与迁移策略。
5. 最小真实项目样本与公开演示数据脱敏规则。

## 文档入口
01 需求；02 架构；03 映射契约；04 UI；05 TDD；06 迭代；07 风险；08 真实项目演练；09 API；schemas/ 示例和校验脚本。
