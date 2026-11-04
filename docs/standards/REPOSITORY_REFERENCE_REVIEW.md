# InspireChina/ai4se-demo-project 规范借鉴评审（2026-11-04）

参考仓库：https://github.com/InspireChina/ai4se-demo-project
参考分支：`main`，树 SHA `e02408b92a0fb085f8ac0bb72f0d010c4bbbe809`（GitHub API 读取时）。

| 原项目可核查规范 | 适用性 | 本项目处理 |
|---|---|---|
| 根级 AGENTS.md 明确架构、依赖、代码和测试约束 | 高 | 吸收为正式根规范；增加本体语义/安全/导入规则 |
| `docs/features`, `plans`, `designs`, `standards` 的文档分类 | 高 | 全部引入，明确定稿事实与过程文档边界 |
| `.agent/skills/dev-plan`, `dev-build`, `dev-debug` | 高 | 重新编写为 Python/React/本体专用 Skills |
| API、E2E、手工和冒烟用例与研发规范关联 | 高 | 加入 REQ → Test → Evidence 门禁 |
| 变更同步事实文档 + PR 检查清单 | 高 | 引入 docs-sync gate 与 PR 模板 |
| 后端 DDD 四层结构 | 中 | 只借鉴职责隔离；**不复制** Java 聚合/事务注解 |
| `e2e-run.sh` 一键 E2E | 高 | 增加安全、可恢复的本地脚本骨架，未配置时显式失败 |
| `.mcp.json` / `opencode.jsonc` | 低 | 不复制默认工具、服务器或凭据；按实际环境审批配置 |
| Vue 3、Spring Boot、JWT、MySQL、MariaDB4j | 不适用 | 不采纳；继续 React/FastAPI/Local-first/RDFLib/SHACL |

## 验证边界
本次核查了实际 `AGENTS.md`、README 和三个 SKILL.md，并检查仓库顶层结构。未执行参考仓库 CI 或对其运行质量做验证。该仓库没有 GitHub license 元数据，因此本包没有复制其源码或文档正文，仅做规则提炼和重新编写。
