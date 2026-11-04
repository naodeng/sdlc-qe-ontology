# Sprint 0 可执行工作包（先验证，再开发）

| ID | 任务 | 前置 | TDD/Spike 产物 | Done 定义 |
|---|---|---|---|---|
| S0-01 | 规则真值表和 reason codes | 无 | golden + adversarial fixtures | false Qualified=0，unknown 覆盖缺字段 |
| S0-02 | SHACL 真实运行 | Python 依赖 | pySHACL 日志、正反样本 | 负例被拒绝，0 mandatory skips |
| S0-03 | 标准映射审计 | 无 | term URI/definition/license ledger | 每项 verified 或明确 deferred，不滥用等价 |
| S0-04 | Snapshot manifest 与版本 | S0-01 | schema、哈希与兼容测试 | cross-snapshot 409，哈希可复现 |
| S0-05 | API contract | S0-01/04 | OpenAPI + contract tests | 所有端点状态码和 schema 可检验 |
| S0-06 | Animal Island UI Spike | 无 | lockfile、build、a11y、theme evidence | 可构建、主题兼容、license 通过 |
| S0-07 | Settings shell | S0-06 | theme/i18n tests | 系统切换、持久化、异常回退通过 |
| S0-08 | localhost 安全 Spike | S0-05 | CORS/Origin/路径攻击测试 | 无跨站/越界读取 |
| S0-09 | Go/No-Go 评审 | S0-01..08 | evidence index + ADR | 阻断项清零或批准明确缩范围 |

建议每个任务保留 `RED.md`（先失败）、`GREEN.md`（通过）、`REFACTOR.md`（回归）和运行命令、版本、哈希、日期。若 pySHACL/组件依赖无法安装，记录环境阻断，不得标为 Passed。
