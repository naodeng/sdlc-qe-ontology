# Build vs Reuse 决策 v0.2

> 决策状态：Proposed。ADR 尚未批准；需经许可证核查和技术 Spike 后冻结。

## 决策原则

1. 优先复用开放标准词汇与成熟解析、验证工具；不复制未经许可确认的模型文件。
2. 只有业务语义确有缺口时才定义新概念；每个新增概念需有能力问题（Competency Question）与测试。
3. 本体规范和实例数据分离；OWL 逻辑约束与 SHACL 数据校验分离。
4. Local-first、模型无关、无强制图数据库；不得依赖 AI 生成才能执行核心查询。

| 组件 | 初步决策 | 备选 | 决策门禁 |
|---|---|---|---|
| RDF 解析与 SPARQL | Reuse RDFLib | Jena | 能解析样本、运行查询、生成可重复结果 |
| SHACL | Reuse pySHACL | Jena SHACL | 负样本必须失败，报告可解释 |
| OWL 推理 | Defer，先做 OWL-RL Spike | 其他推理器 | 确认所需推理片段，测试一致性与性能 |
| 溯源语义 | Reuse PROV-O | 自定义最小映射 | 来源关系方向与审计信息正确 |
| 测试资源语义 | Align OSLC QM | 自定义兼容映射 | 概念/属性映射和冲突清单完整 |
| 质量义务/声明/证据充分性 | Build 最小扩展 | SACM/GSN 映射 | 不与现有标准冲突；有可执行 CQ |
| PR 影响分析 | Build reference queries | 纯 SQL baseline | 召回率和证据可追溯率可比较 |
| Graph DB | Not now | Fuseki/GraphDB | 仅数据规模或查询能力证明需要时引入 |
| Agent | Later optional | 非 Agent CLI | 禁止影响核心离线验证 |

## 方案比较

| 方案 | 优势 | 风险 | 结论 |
|---|---|---|---|
| A 完全自研语义体系 | 控制力强 | 重复标准、难互通 | 不推荐 |
| B 全量引入大型工程本体 | 概念丰富 | 学习成本、imports/许可负担 | 仅作对照 Spike |
| C 最小核心 + 标准对齐 + 独立扩展 | 可控、易迭代 | 映射工作量 | **推荐（待验证）** |

## 待批准 ADR

- ADR-001：最小核心 + 模块化本体。
- ADR-002：Turtle/OWL + SHACL 双层契约。
- ADR-003：PROV-O 复用及 OSLC 映射优先。
- ADR-004：Local-first、无强制数据库。
- ADR-005：变更影响不等于因果证明，输出证据等级与不确定性。

## 决策退出条件

若模型映射严重不兼容、许可证限制无法接受、标注基准上没有可证明收益，暂停本体扩展，转为通用质量关系规范及实验性项目。
