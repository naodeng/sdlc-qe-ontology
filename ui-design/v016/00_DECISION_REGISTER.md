# v0.16 决策登记与基线范围

状态：**Design Candidate / No-Go**。本轮是实施级规格细化，不是运行时实现。保持 v0.10 RDF/OWL、SPARQL、SHACL 语义兼容；任何变更必须 ADR + 回归测试。

| ID | 决策 | 约束 | 验收证据 |
|---|---|---|---|
| ADR-016-01 | 单一不可变快照作为查询单位 | response 必带 snapshotId、policyVersion、evaluationId | 并发切换快照测试 |
| ADR-016-02 | 质量判定与保证状态正交 | UI 禁止把 computed Qualified 显示成 verified Qualified，除非 assurance=verified | 组合矩阵测试 |
| ADR-016-03 | 数据完整性独立标记 | 缺少截止时间、build 环境、义务全集证明时不可 Qualified | negative fixtures |
| ADR-016-04 | UI 不执行任意 SPARQL | 固定查询目录 + 参数白名单 | 注入测试 |
| ADR-016-05 | 设置优先于业务页面 | 主题/语言/版本元数据先落地 | Playwright + schema migration |
| ADR-016-06 | Animal Island UI 通过适配层 | 先核查版本、license、SSR/构建、主题 token、无障碍 | 兼容性 Spike 报告 |
| ADR-016-07 | 首版为只读单机工作台 | 无用户登录、远程同步、数据写入、自动 Go | API 权限与网络测试 |

**冻结前不得擅自决定**：标准术语的 `owl:equivalentClass`、证据“最新一次”覆盖规则、真实 CI 数据的完整性来源。每项必须记录 owner、证据、影响与决策日期。
