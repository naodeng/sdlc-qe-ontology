# v0.7 标准映射与许可证审计台账

> 审计状态：**待完成 / 不可宣称合规**。下列 URI 是公开规范的候选术语，仍需对照原文定义、约束与许可后审批。

| 本地概念 | 外部候选 | 当前关系 | 风险 | 下一步 |
|---|---|---|---|---|
| TestExecution | `http://www.w3.org/ns/prov#Activity` | 现有 rdfs:subClassOf | 语义合理但需评估生成/使用关系 | 对照 PROV-O 文本与样例 |
| TestEvidence | `http://www.w3.org/ns/prov#Entity` | 现有 rdfs:subClassOf | 证据实体不代表充分性 | 增加证据来源和质量声明模型 |
| Requirement | OSLC RM Requirement 资源 | 候选映射 | 不能直接 owl:equivalentClass | 检查规范版本、资源 Shape |
| TestCase | OSLC QM TestCase 资源 | 候选映射 | 类/资源形态及约束可能不同 | 检查术语 URI 与范围 |
| TestExecution | OSLC QM TestExecutionRecord 等 | 候选映射 | 执行记录与执行活动不可简单等价 | 明确事件与记录区分 |
| TestEvidence | OSLC QM TestResult 等 | 候选映射 | 测试结果不等于原始证据 | 优先采用关联而非等价 |

## 审核清单
- [ ] 官方规范 URI、版本、发布日期、术语定义逐条核实
- [ ] RDF/OWL 公理与 OSLC Shape 约束语义区分
- [ ] 每个复用词汇记录来源、许可证、署名与分发要求
- [ ] 检查依赖包许可证和转授权/再分发约束
- [ ] 经评审后冻结正式命名空间、版本与兼容策略

参考入口： https://open-services.net/specifications/ ; https://www.w3.org/TR/prov-o/ ; https://github.com/oslc-op/oslc-specs
