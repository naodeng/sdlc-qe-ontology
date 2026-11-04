# 可视化字段映射契约（方案 B）

## 受控映射域
首版概念：Requirement、Change/PR、Build、Release、TestObligation、TestExecution、Evidence。实际 RDF 类 URI 必须以现有本体文件为准；这里的名称是 UI 业务标签，不宣称已核实正式 URI。

字段映射规则：`sourceField` → `targetConcept` + `targetProperty`；类型支持 string、dateTime、boolean、integer、IRI/reference；可指定主键、外键、常量、日期格式、空值策略。禁止任意用户代码和不受限表达式。记录唯一性用 `(sourceId, entityType, externalId)` 组合；无稳定 ID 的数据不能被当作可信跨文件关系。

## 转换及冲突处理
- 不允许多对一冲突在无明确合并策略下静默覆盖。
- 必填列缺失、键冲突、无法解析时间、引用缺失 → Blocking；可选列缺失 → Warning（需明示）。
- 时间使用 ISO 8601 offset-aware；不允许无时区的执行时间参与 release cutoff 比较。
- `buildId`、`releaseId` 的引用必须在同一快照中可解析，或标为 Unknown，绝不猜测。
- 映射审批与文件 hash、mapping hash、schema version 绑定；源文件或规则修改必须重新审批。
- RDF 直接导入也必须校验 ontology/policy compatibility、SHACL、source provenance，不跳过安全边界。

## 质量判定边界
`assessmentStatus = qualified | unqualified | unknown` 与 `assuranceStatus = verified | blocked | not_run | stale | unavailable` 独立；所有义务集合为空、数据覆盖不完整、缺 cutoff/build/来源信息不得通过空集合真值变为 Qualified。Qualified + assurance != verified 时，UI 只能展示“计算候选结果，未验证”，不能使用已验证通过徽标。

## 映射预览
展示原始列、目标属性、转换样例、前后值、错误数、孤立引用数、来源文件和 hash；预览数据默认限制行数并避免记录敏感内容进入日志。
