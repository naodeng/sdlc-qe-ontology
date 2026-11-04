# 仓库工程化落地任务（候选 Sprint 0）

| ID | P | 内容 | 可验收结果 |
|---|---|---|---|
| GOV-01 | P0 | 确认 root AGENTS、文档分层与 ADR 归属 | 文档索引和路径全部可追溯 |
| GOV-02 | P0 | 收敛 OpenAPI v0.14–v0.18 差异 | 只有一个可校验的 approved OpenAPI |
| GOV-03 | P0 | 核对三态/保证状态规则与金标 | 反例返回 Unknown/Blocked，不假绿 |
| GOV-04 | P0 | CI 运行 ruff/pytest/SHACL/SPARQL/schema | 必须真实执行、输出报告 |
| GOV-05 | P0 | 数据导入 RED-first 测试和最小安全实现 | 文件安全、确认失效、原子快照 |
| GOV-06 | P0 | Arco React 依赖与 Figma UI 验证 | Build、a11y、light/dark/zh/en |
| GOV-07 | P0 | 本地 E2E 启停脚本 | 执行可重复，失败时进程可清理 |
| GOV-08 | P1 | Markdown link/doc-sync 检测 | 无死链，PR 列出 docs impact |
| GOV-09 | P1 | Contributor guide 与许可证审批 | 外部贡献路径和法律条件明确 |

禁止把脚手架、测试模板或工作流草案标为已通过 Gate 2。
