# Plan: 20261105-workspace-storage-race-hardening
Status: Approved; implemented 2026-11-05 under the owner's explicit fix-and-run direction.
Linked Requirement: REQ-WORKSPACE-001

## 目标、现状与预期用户价值

修复整体改动 review 发现的两个存储竞态，并确保 Playwright E2E 不因固定端口冲突而停在浏览器启动前。原工作区计划保持冻结；本 follow-up 只补强实现，不改变 API 或产品行为。

## 技术方案与架构边界

- 用 `errno.ELOOP` 识别 `O_NOFOLLOW` 的符号链接竞态，避免 macOS 的 errno 62 被 Linux fallback 40 漏掉；该项按损坏条目报告，列表继续读取其他工作区。
- 创建时以独占 marker `.creating-<uuid>` 标记进行中的写入，在 staging 目录完整写入 manifest 后用 `mkdir` 原子占有最终 UUID 目录，再将完整 manifest 文件 rename 到该目录。目标已存在时清理本次 staging/marker 并换 UUID 重试。列表忽略 marker 存在且 manifest 尚未发布的目录，避免暴露短暂的空目录状态。
- E2E runner 从操作系统申请一个临时 loopback 端口，通过 `E2E_FRONTEND_PORT` 同步配置 Playwright、Vite 和 API 的精确 Origin allowlist；Vite 使用 strict port，服务仍只绑定 `127.0.0.1`。

## 受影响文件（路径）

- `backend/app/adapters/filesystem_workspace_store.py`
- `backend/app/main.py`
- `tests/test_workspace_store.py`
- `frontend/playwright.config.ts`
- `scripts/e2e-run.sh`
- 本 follow-up plan、`docs/qa/workspace-storage-race-hardening-20261105.md`、QA 索引、需求状态和 current baseline

## API / 本体 / 映射 / 快照变化

无公开 API、本体、映射或快照契约变化。E2E 仅增加本地临时端口配置，不改变默认应用 UI Origin 或网络绑定范围。

## 时序图或数据流

`E2E runner → 临时 127.0.0.1 端口 → Playwright/Vite`

`E2E_FRONTEND_PORT → FastAPI allowed Origin`

工作区创建先在 staging 中完成 manifest，再原子 claim 目标目录并发布完整 manifest。创建 marker 在 manifest 发布前阻止列表暴露不完整目录；manifest 发布后工作区可以正常读取，即使清理 marker 时进程中断。

## TDD: RED 测试、GREEN 实现、REFACTOR

- `test_list_reports_no_follow_eloop_as_corrupt_and_continues`：RED 时 `store.list()` 将 Darwin `errno.ELOOP` 冒泡为 `WorkspaceStorageUnavailable`；修复后 1 passed，损坏条目不再阻断有效项。
- `test_create_retries_collision_at_atomic_destination_claim`：对旧的 check-then-rename 路径注入目标竞态，RED 以 `WorkspaceStorageUnavailable` 失败；修复后创建重试新 UUID，并保留原 manifest 字节和目录 inode。
- `test_list_ignores_workspace_with_active_creation_marker`：RED 时空的进行中目录被列为 corrupt；修复后列表忽略该中间态。
- `./.venv/bin/pytest tests/test_workspace_store.py -q`：26 passed。

## 单元 / API / SPARQL / SHACL / E2E / 安全测试

- `./scripts/verify.sh`：75 pytest tests、58 subtests；Ruff、SPARQL CQs、SHACL 正反例、mapping schema、TypeScript 和 Vite production build 均通过。
- `bash -n scripts/e2e-run.sh`：通过。
- `npm --workspace frontend run e2e -- --list`：发现 3 个测试，2 个文件。
- `make e2e`：第一次沙箱执行在 Chromium 启动时遇到 macOS `MachPortRendezvousServer: Permission denied (1100)`。按用户明确要求及项目浏览器规则执行沙箱外验证；首次发现固定端口 5174 被另一项本地服务占用，未停止该进程。runner 改用临时 loopback 端口后再次运行，3/3 Playwright 用例通过。

## 风险、回滚、可观测证据

- E2E 通过系统临时端口分配后关闭 socket，再启动 Vite；若极小概率发生端口竞争，`--strictPort` 会明确失败，不会悄悄连接到错误服务。
- 每次 E2E 使用独立临时 `SDLC_QE_DATA_DIR`，脚本退出时只清理由该脚本创建的目录。
- 回滚仅涉及代码和测试文件；不删除、移动或修改已有用户工作区。
- 完整执行证据见 [`workspace-storage-race-hardening-20261105.md`](../qa/workspace-storage-race-hardening-20261105.md)。

## 文档同步清单

已同步 REQ-WORKSPACE-001 当前结果、current baseline、QA index 和中英文 README 的验证报告链接。原工作区实施计划和首次验证报告保留为历史记录。

## 人工审批与执行结果

Owner 明确要求修复 review 发现、补回归测试并实际跑完 Playwright。此 follow-up 已据此批准并执行；没有提交、推送或停止其他本地服务。
