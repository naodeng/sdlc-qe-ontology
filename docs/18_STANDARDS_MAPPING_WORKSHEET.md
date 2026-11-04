# 现有标准复用映射工作表 v0.3

**重要：候选映射不等于 `owl:equivalentClass` 或 `owl:equivalentProperty`。** 只有确认定义域、值域、语义、身份和时间边界完全一致后，才允许声明等价。优先采用 `rdfs:seeAlso` / 文档引用或显式转换适配器。

| 本地术语 | 参考标准/来源 | 候选对应 | 目前判断 | 待核验 |
|---|---|---|---|---|
| Requirement | OSLC RM | Requirement 资源 | 近似 | 精确 URI、资源 shape、版本语义 |
| TestCase | OSLC QM | TestCase 资源 | 近似 | URI、属性及实例约束 |
| TestExecution | OSLC QM | TestExecutionRecord / TestResult 相关概念 | **不可直接等价** | 活动与记录的区分 |
| TestEvidence | W3C PROV-O | `prov:Entity` | 候选子类 | 是否每种证据都是可标识实体 |
| TestExecution | W3C PROV-O | `prov:Activity` | 候选子类 | 活动起止、关联执行者 |
| wasGeneratedBy | W3C PROV-O | `prov:wasGeneratedBy` | 直接复用 | 活动与实体实例语义 |
| CodeChange | OSLC CM | ChangeRequest | **不等价** | 代码 diff 与变更请求不同 |
| TestObligation | 现有标准待查 | 无已确认等价概念 | 自研候选 | 搜索术语及学术模型 |
| QualityClaim | PROV-O + argumentation standards | 无已确认等价概念 | 自研候选 | 证据支持与来源关系分离 |

## 复核流程

1. 固定规范版本和来源 URL，记录访问日期与许可。
2. 抽取正式术语 URI、定义、domain/range、shape、规范示例。
3. 对照本地概念的身份、时间、开放世界/闭世界解释。
4. 决定 `reuse`、`subclass`、`mapping-only`、`reject`。
5. 用正反例测试映射，不在审查前发布强等价声明。

## 参考入口

- https://github.com/oslc-op/oslc-specs
- https://open-services.net/specifications/
- https://www.w3.org/TR/prov-o/
- https://github.com/fabianoruy/SEON
- https://github.com/systems-praxis/seamless-digital-engineering-ontology

> 当前只核对了公开仓库/标准入口与少量文件线索；完整术语级审计仍是阻断项。
