# ADR Candidates & Risks

## Proposed ADRs (not yet approved)
- ADR-UI-001：UI 是独立只读 adapter，不能修改 ontology v0.10。
- ADR-UI-002：Python FastAPI + RDFLib，避免双重语义实现。
- ADR-UI-003：React + TS + Vite，Graph 库通过 Spike 选型。
- ADR-UI-004：MVP 无持久化数据库，文件快照作为数据版本边界。
- ADR-UI-005：三态资格判定由后端 policy 统一提供，前端不推断。
- ADR-UI-006：默认 localhost，同源发布，禁用任意 SPARQL 和外部 URL 载入。

## Risks
| Risk | Impact | Mitigation |
|---|---|---|
| CQ-10 缺字段漏报 | 虚假质量信心 | 独立完整性检查 + Unknown + adversarial tests |
| OWL 开放世界与 UI 关闭世界误用 | 错误否定/肯定 | 明确数据快照范围、三态、policy 假设 |
| SHACL 未执行 | 无法确认结构约束 | 独立严格门禁、显示 not_run |
| 标准映射未核实 | 错误语义复用 | URI/定义/许可逐条审计 |
| Graph 太大 | UI 卡顿、关系误解 | 两跳限制、截断标记、列表视图 |
| 证据摘要仅字段非空 | 误认为真实性已证实 | 解释性文案、UNVERIFIED_SOURCE |
| 本地服务暴露 | 数据泄漏 | 127.0.0.1、路径白名单、无任意查询 |
| 规则版本漂移 | 无法复现 | snapshot + policyVersion + fixtures + lockfile |

## Decision status
所有 ADR 为 **proposed**；UI MVP 方案批准不等于本体基线 Go。正式批准需要评审记录与测试证据。
