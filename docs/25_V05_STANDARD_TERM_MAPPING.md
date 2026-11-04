# v0.5 标准术语映射核查表（候选，不是已批准映射）

## 核查准则
- 每项映射必须记录：本地 URI、外部标准 URI、关系类型（`equivalentClass` / `subClassOf` / `relatedMatch` / 仅参考）、定义依据、版本、许可证、评审人和反例。
- **不能因为名称相似就使用 `owl:equivalentClass`。** OSLC Resource Shape 是资源约束，不自动等于 OWL 类。
- 证据溯源可以借鉴 PROV-O；证据充分性需要另建质量声明与规则模型。

| 本地术语 | 参考对象 | 当前建议 | 待完成核查 |
|---|---|---|---|
| `TestExecution` | `prov:Activity` | 已在实验本体声明 `rdfs:subClassOf` | 检查执行事件粒度与 PROV 语义 |
| `TestEvidence` | `prov:Entity` | 已在实验本体声明 `rdfs:subClassOf` | 证据对象是否是可持久标识的实体 |
| `Requirement` | OSLC RM Requirement | 仅候选对照，不声明等价 | 核对准确 URI、版本、定义、Shape |
| `TestCase` | OSLC QM TestCase | 仅候选对照，不声明等价 | 核对范围与关联语义 |
| `TestExecution` | OSLC QM TestExecutionRecord / TestResult | **不得自动等价** | 区分执行活动、执行记录和结果 |
| `CodeChange` | OSLC CM ChangeRequest | **不等价** | 代码差异与变更请求是不同实体 |
| `QualityClaim` | PROV / OSLC | 本地扩展候选 | 定义证据支持关系与充分性准则 |
| `TestObligation` | OSLC QM / SEON | 本地扩展候选 | 查重、记录概念差异及测试义务的可验证定义 |

## 权威来源（待逐项 URI 复核）
- OSLC Specifications: https://github.com/oslc-op/oslc-specs
- OSLC Quality Management: https://docs.oasis-open-projects.org/oslc-op/qm/v2.1/quality-management-spec.html
- W3C PROV-O: https://www.w3.org/TR/prov-o/
- SEON: https://github.com/fabianoruy/SEON

**结论：** 当前只有 PROV-O 两项在实验代码中建立了 subclass 关系；其他均为候选映射，不能在文档中声称已标准对齐。
