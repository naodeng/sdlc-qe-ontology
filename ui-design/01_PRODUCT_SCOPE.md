# Product Scope / 产品范围

## 目标
使 QA、开发、架构师和本体维护者在本地理解概念、查看关系、检查证据链与数据缺口；不要求使用者编写 SPARQL。

## MVP（P0）
1. **Overview**：数据集/本体版本、实体数量、校验状态、数据时间、不可判定数量；数据不足时不显示绿色通过。
2. **Ontology Explorer**：按类/属性浏览英文、中文标签、IRI、domain/range、父类、引用标准状态；只读。
3. **Relationship Graph**：从 Release/Requirement/TestObligation 进入局部关系子图，最多两跳、节点数上限，列表替代视图。
4. **Evidence Explorer**：按 Release、Obligation、Build、状态筛选，查看 execution、environment、cutoff、digest presence、provenance、缺失字段。
5. **Quality Decision**：Qualified/Unqualified/Unknown + reasons、规则版本、数据集快照、计算时间；显示“辅助判定，不是发布审批”。
6. **Validation Status**：显示本地校验结果、是否执行 SHACL、测试门禁状态；MVP 只读历史结果，不提供任意代码执行。

## 非目标
本体编辑、SHACL/规则编辑、任意 SPARQL 输入、数据写入、团队协作、权限后台、云同步、自动 Go/No-Go、外部 GitHub/CI 账户接入、生产级密码学验签。

## Personas & Jobs
- QA：回答“某发布的测试义务是否有可用证据？缺什么？”
- Developer：追踪 PR→Build→Execution→Evidence 关联。
- Ontology maintainer：解释某概念和关系的定义，识别实验性 URI。
- Release manager：审查证据和未知项；最终决策由人完成。

## 成功指标（建议验收目标，非当前实测）
- 100% Unknown 样本不显示 Qualified。
- 100% UI 状态可追溯至 reasons 和快照 ID。
- 主要查询在固定金标数据集上结果正确率 100%。
- 200 节点以内局部图交互可用；性能阈值在 Spike 中定标。
