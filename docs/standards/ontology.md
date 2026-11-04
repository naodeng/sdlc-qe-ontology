# 本体与语义建模规范

- 英文稳定 URI/ID；`rdfs:label` 和解释性文档支持中文，英文规范版优先。任何概念删除或 URI 重命名需兼容性 ADR。
- 开放世界推理（OWL）不代替闭合式质量预检（SHACL）；未知不等于不存在。
- 一条 `TestCase` 记录不能证明义务已满足；Qualified 需要证据满足构建、环境、时间、来源和规则等有效性要求。
- 数据缺失、验证不可用或来源不可确认，不得返回 `verified Qualified`。
- SPARQL 查询必须有快照限定、规模上限与对抗性样本；不可允许任意未经限制的远程端点查询。
- 所有语义变更同步 ontology、SHACL、CQ、双语描述、正负 fixture、golden 决策和 ADR。
