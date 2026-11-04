# 评估协议与 ADR 待批准事项 v0.3

## 对照组设计

- B0：无本体，基于固定关系表的确定性查询。
- B1：RDF + SPARQL（不使用 OWL 推理）。
- B2：RDF + SPARQL + 约束验证；若需要再加入 OWL 规则推理。
- B3：后续 Agent 增强；使用相同输入、模型、预算和固定随机种子，单独评估。

每组使用相同的人工标注样本和任务定义。分别报告 TP、FP、FN、Precision、Recall、F1、耗时、内存、维护工时。小样本只做探索性结果，不宣称统计显著性。保留失败样本与可复现脚本。

## 风险与失败标准

- 只要查询把未知关联当作“不受影响”，判为严重错误。
- 只要证据来源不可追溯，不允许自动判定质量声明通过。
- 若 RDF 模型相对简单关系表无可测收益，应保留简化实现选项。

## ADR 待签署

| ADR | 建议 | 状态 |
|---|---|---|
| ADR-001 | Shared Core + SDLC + QE 模块化 | PROPOSED |
| ADR-002 | RDFLib / Turtle / SHACL Local-first | PROPOSED |
| ADR-003 | PROV-O 复用、OSLC 映射审查后采用 | PROPOSED |
| ADR-004 | 本体不负责发布门禁策略裁决 | PROPOSED |
| ADR-005 | 正式 IRI 由受控域名提供，实验 IRI 不发布为稳定契约 | PROPOSED |

**评审结论：当前属于候选基线；须完成阻断 Spike 和 ADR 审批后才可启动 v0.1。**
