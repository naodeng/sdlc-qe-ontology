# SDLC-QE Ontology 竞品与标准调研 v0.2

> 状态：研究候选 / 非最终结论。调研日期：2026-10-29。研究范围：GitHub 公开项目与规范网站。未完成每个候选的全量源码、Issue、Release、许可证及贡献活跃度审计。**不得将“未检索到”表述为“不存在”。**

## 1. 执行摘要

- **已存在软件工程本体**：SEON 和 Seamless Digital Engineering Ontology 说明软件工程本体不是空白市场。
- **已存在跨研发工具互联语义**：OSLC QM 将 TestPlan、TestCase、TestResult 等质量资源与需求、变更等关联；新项目不能将此视为原创。
- **已有来源标准**：PROV-O 描述 Entity、Activity、Agent 及生成、使用、归属关系。
- **项目定位建议**：可运行、可验证、适合 AI Native SDLC + QE 的轻量参考本体，重点在跨领域 TestObligation、QualityClaim、Evidence 与变更影响的端到端实验。
- **结论等级**：可行性“初步支持”；差异化“尚待基准实验证实”；许可兼容“待法律/合规核验”。

## 2. 参考项目与证据

| 候选 | 类型 | 适合借鉴 | 不应直接假设 | 原始资料 |
|---|---|---|---|---|
| SEON | 软件工程本体网络/研究 | 分层本体、软件工程概念 | 不可断言已覆盖所有现代 DevOps 活动 | https://github.com/fabianoruy/SEON |
| OSLC Specifications / QM 2.1 | 生命周期资源与互操作标准 | 测试计划、用例、结果、需求和变更链接 | OSLC 并非完整的 QA 逻辑推理体系 | https://github.com/oslc-op/oslc-specs ; https://docs.oasis-open-projects.org/oslc-op/qm/v2.1/quality-management-spec.html |
| Seamless Digital Engineering Ontology | OWL 工程本体 | 标准驱动概念、OWL imports、定义来源 | 引入 BFO/CCO 有额外成本 | https://github.com/systems-praxis/seamless-digital-engineering-ontology |
| W3C PROV-O | 溯源本体标准 | Entity / Activity / Agent，生成和归属 | 溯源不等于证据充分性 | https://www.w3.org/TR/prov-o/ |
| OpenTelemetry Semantic Conventions | 语义约定工程仓库 | 术语治理、生成式文档、版本兼容 | 它不是 OWL 本体 | https://github.com/open-telemetry/semantic-conventions |
| RDFLib | RDF 工具 | 本地 RDF 图、SPARQL | 不是业务本体 | https://github.com/RDFLib/rdflib |
| pySHACL | SHACL 验证器 | 约束报告、数据检查 | 不取代 OWL 推理 | https://github.com/RDFLib/pySHACL |
| OWL-RL | 推理工具 | 可控规则推理 | 不覆盖全部 OWL 2 DL 语义 | https://github.com/RDFLib/OWL-RL |

## 3. 概念重叠矩阵（设计假设，待逐项文件级核查）

符号：● 明确在已检查的规范/介绍中出现；△ 相关领域可能覆盖但尚未核对精确术语；— 本轮没有证据，不表示不存在。

| 概念 | SEON | OSLC QM | SDE Ontology | PROV-O | 本项目建议 |
|---|---|---|---|---|---|
| Requirement | △ | ●（链接目标） | △ | — | 映射/扩展 |
| CodeChange / PullRequest | △ | △（Change Management） | △ | — | 本地定义，后续对齐 |
| TestCase | △ | ● | △ | — | 优先对齐 OSLC |
| TestResult | △ | ● | △ | — | 优先对齐 OSLC |
| TestObligation | — | — | — | — | 候选新增；查重后冻结 |
| QualityRisk | △ | △ | △ | — | 候选新增/映射 |
| QualityClaim | △ | — | △ | — | 候选新增/映射 |
| Evidence provenance | △ | △ | △ | ● | 优先复用 PROV-O |
| Release / Build | △ | △ | △ | — | 本地定义/外部映射 |

**警告**：不能依据此表认定 `TestObligation` 或 `QualityClaim` 是学术原创；必须检索 assurance case、GSN、SACM、requirements verification、test obligation 相关标准与研究。

## 4. 按维度比较（非主观打分）

| 维度 | SEON | OSLC | SDE | PROV-O | 计划行动 |
|---|---|---|---|---|---|
| 语义覆盖 | 软件工程 | 研发资源互联 | 数字工程 | 溯源 | 提取最小概念清单 |
| 表达形式 | 本体网络 | RDF/资源规范 | OWL | OWL | 采用 Turtle/OWL + SHACL |
| 集成复杂度 | 待测 | API 及资源模型 | BFO/CCO imports | 低到中 | 独立 Spike |
| 许可与复用 | 待核实 | 核查规范许可 | MPL-2.0，图片另有许可 | W3C 文档条款 | 不复制原文件直到审查完成 |
| CI/Eval | 待核实 | 有工具和规范 | 部分工具说明 | 标准非应用 | 自建回归与 benchmark |

## 5. GitHub 代码级审查任务

- [ ] SEON：定位完整本体文件、命名空间、模块依赖、原始论文、最新提交与许可证。
- [ ] OSLC：逐一提取 QM、RM、CM 资源类型和属性的规范 URI、定义域、值域及版本。
- [ ] SDE：使用 Protégé 加载 imports，记录可复用概念及 BFO/CCO 依赖成本。
- [ ] PROV-O：验证 TestExecution → prov:Activity、Evidence → prov:Entity 的映射是否成立；避免错误 `prov:wasGeneratedBy` 方向。
- [ ] OpenTelemetry：研究 schema 变更和自动生成文档的机制。
- [ ] 补充检索：SACM、GSN、SQA ontology、DevOps ontology、CI/CD ontology、test obligation 及 GitHub 最新维护状态。

## 6. 研究结论与不确定性

建议立项做 **限定范围技术 Spike**，暂不宣布“领先”“唯一”“替代 OSLC”。先用 10 个需求、5 个 PR、30 个测试、10 份证据的人工标注小数据集验证可用性。采用可重复的对照实验比较关系表、普通检索和本体查询；如果本体无显著增益，保留语义规范而不强制引入推理引擎。
