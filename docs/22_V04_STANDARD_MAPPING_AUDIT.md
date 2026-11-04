# v0.4 标准映射核查与复用边界

状态：**待验证（proposed）**。以下为设计映射，不代表已对每个规范的权威 URI、资源 Shape、许可条件完成审计。

| 本地概念 | 候选标准 | 映射策略 | 核查事项 | 状态 |
|---|---|---|---|---|
| Requirement | OSLC Requirements Management | 资源级关联优先；不直接宣称 owl:equivalentClass | 官方术语 URI、Shape、版本 | OPEN |
| TestCase | OSLC Quality Management | 资源链接及适配层 | 官方术语 URI、约束 | OPEN |
| TestExecution | PROV-O Activity | `rdfs:subClassOf prov:Activity` 候选 | 活动语义是否一致 | PARTIAL |
| TestEvidence | PROV-O Entity | `rdfs:subClassOf prov:Entity` 候选 | 证据来源和实体边界 | PARTIAL |
| CodeChange | OSLC Change Management | 映射候选，不强制等同 ChangeRequest | 变更请求与实际提交区别 | OPEN |
| TestObligation | 本项目扩展 | 本地独立概念 | 与 TestCase、AcceptanceCriterion 区别 | PROPOSED |
| QualityClaim | 本项目扩展 | 本地独立概念 | 支持关系与证据充分性标准 | PROPOSED |

## 决策约束

1. 禁止未经语义等价证明使用 `owl:equivalentClass` 或 `owl:sameAs`。
2. 本地 `https://example.org/` 命名空间仅供实验，正式发布前须迁移至稳定、受控的 URI。
3. OWL 开放世界语义不能代替 SHACL 的数据完整性检查；SHACL 通过也不能证明业务事实正确。
4. 许可证及版权审查完成前，不直接复制外部规范文件。
5. 每个复用项必须记录来源、标准版本、URI、映射理由、测试和 reviewer。

## 权威参考

- OSLC: https://open-services.net/specifications/
- W3C PROV-O: https://www.w3.org/TR/prov-o/
- W3C SHACL: https://www.w3.org/TR/shacl/
- SEON: https://github.com/fabianoruy/SEON
- Seamless Digital Engineering Ontology: https://github.com/systems-praxis/seamless-digital-engineering-ontology
