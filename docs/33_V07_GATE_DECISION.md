# v0.7 Go/No-Go 决策

**结论：Candidate / No-Go。** 新增 CQ-05/06 与可执行金标测试，只能证明小规模 RDF 查询示例可运行，不能替代 SHACL、正式术语映射或端到端发布流程验证。

| Gate | 条件 | 状态 |
|---|---|---|
| G0 | 本体与 RDF 解析 | 依现有单测结果 |
| G1 | SPARQL CQ-01～06 回归 | 依测试执行证据 |
| G2 | SHACL 正反样本完整运行，无跳过 | 阻断：本环境缺 pySHACL |
| G3 | OSLC/PROV-O 逐术语审计 | 阻断：待核实 |
| G4 | 完整 Requirement→PR→Build→Release 参考链 | 阻断：尚未建模 |
| G5 | 正式 URI、许可证、兼容策略批准 | 阻断：未审批 |

## 下一 Sprint
1. 在可安装 pySHACL 的 CI 环境执行正反样本并保留日志；禁止跳过。
2. 增加 PR/Build/Release 语义模型前先定义能力问题、人工金标与反例。
3. 审查 OSLC/PROV-O 官方词汇与许可，明确 `skos:closeMatch`、`rdfs:subClassOf` 或自定义映射是否适用；不得臆用 `owl:equivalentClass`。
4. 完成后召开基线冻结评审，形成签署式 ADR。
