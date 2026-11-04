# Plan: 20261104-ci-rolldown-lockfile
Status: Approved
Linked Requirement: REQ-BOOT-001

## 目标、现状与预期用户价值
修复 GitHub Actions 在 Ubuntu 上构建前端时缺少 `@rolldown/binding-linux-x64-gnu` 的问题。当前锁文件只有 macOS ARM64 对应的 Rolldown optional package；本机验证通过不能覆盖 Linux CI。

## 技术方案与架构边界
用 CI 所用的 npm 11.19.1 从干净依赖锁状态生成完整 workspace lockfile，保留各平台 optional native packages。只改依赖锁文件，不改运行时行为、API、本体或数据语义。

## 受影响文件（路径）
- `package-lock.json`
- `docs/qa/bootstrap-verification-20261104.md`
- 本计划

## API / 本体 / 映射 / 快照变化
无。

## 时序图或数据流
GitHub Actions: checkout → `make setup` / `npm ci` → `make verify` / Vite build → Playwright E2E。

## TDD: RED 测试、GREEN 实现、REFACTOR
- RED：Actions run `41819755874` 在 Ubuntu 的 `vite build` 因缺少 Linux binding 失败；新增的锁文件覆盖检查也先以 RED 运行，发现 24 个缺失的 platform-specific package records。
- GREEN：补齐 26 个 Rolldown / LightningCSS optional package records；干净安装后锁文件覆盖检查通过。
- REFACTOR：不涉及代码重构。

## 单元 / API / SPARQL / SHACL / E2E / 安全测试
- npm 11.19.1 的干净副本中执行 `npm ci` 与 `npm --workspace frontend run build`：通过。
- 隔离 worktree 执行 `./scripts/verify.sh`：通过，27 tests、58 subtests，含 Ruff、SPARQL、SHACL、mapping schema 与前端构建。
- GitHub Actions run `41823621216`：Linux 质量门、Chromium 安装和 Playwright E2E 全部通过。

## 风险、回滚、可观测证据
锁文件可能包含 npm 重新计算的包布局；通过审查差异并做干净安装检查。失败时不推送，恢复本次锁文件改动即可。远端 Actions run 和本地验证记录作为证据。

## 文档同步清单
- 更新 QA 记录：补充 CI 失败根因、修复后的命令和结果。
- 不修改双语产品文档；本次不涉及用户可见功能。

## 人工审批与执行结果
用户已授权修复。未涉及语义、破坏性操作或高风险变更。本地 RED/GREEN、干净安装、完整质量门，以及远端 Linux CI 和 E2E 均已通过。
