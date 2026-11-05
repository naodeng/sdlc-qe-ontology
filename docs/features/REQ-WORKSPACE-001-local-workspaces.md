# Feature: Local workspace management / 本地工作区管理

Status: Implemented for phase 1 (2026-11-05); Playwright E2E passed in follow-up verification
Requirement ID: REQ-WORKSPACE-001
Source: Current product baseline and owner direction; v0.18 WS-01 is retained for historical traceability.

## 背景与用户价值 / Background and user value

用户需要先创建本地工作区，才能导入项目数据。当前工作台仅展示仓库内置的只读示例，尚无工作区存储和管理流程。

Users need a named local workspace before importing project data. The current workbench only shows a bundled, read-only example and has no workspace storage or management flow.

本需求是 v0.18 WS-01 的第一阶段：先交付工作区目录、列表与只读详情。全局当前工作区选择，以及首次工作区内容写入前的单写者锁，需在后续导入计划中落地；本阶段不宣称 WS-01 完成。

This is the first phase of v0.18 WS-01: deliver workspace storage, listing, and read-only details. Global active-workspace selection and a single-writer lock must be completed in a later import plan before any existing workspace content can be mutated; this phase does not claim WS-01 is complete.

## 范围 / Scope

- 创建、列出并以只读详情页打开由工作台管理的本地工作区。
- 用户只提供显示名称；存储 ID 和路径由应用生成。
- 展示空工作区；损坏 manifest 必须可见，不得静默修复或隐藏。
- 仓库示例与用户工作区保持分离。创建或打开工作区不能让用户误以为示例 metadata 属于该工作区。

- Create, list, and open local workspaces managed by the workbench in a read-only details view.
- Let users provide a display name; the application generates the storage identifier and path.
- Show empty workspaces and visibly report a corrupt manifest without silently repairing or hiding it.
- Keep the bundled example separate from user workspaces. Creating or opening a workspace must not imply that the example metadata belongs to it.

不在范围内：删除或移动工作区、导入数据、映射审批、数据验证、快照创建和质量评估。

Out of scope: deleting or moving workspaces, importing data, mapping approval, validation, snapshot creation, and assessment.

## 验收标准 / Acceptance criteria

- 用户可通过名称创建工作区，无需提供文件系统路径。
- 用户可列出并打开现有工作区；空工作区是有效状态，且没有活动快照。
- 空名称、控制字符或孤立 surrogate、未知 ID、路径穿越和符号链接工作区条目均被安全拒绝。
- manifest 格式错误或版本不受支持时，工作区状态显示为不可用/损坏；系统不覆盖该 manifest，也不影响其他工作区的列表读取。
- 工作区 API 不返回本机绝对路径。
- UI 将工作区状态与仓库示例分开标注，不暗示创建工作区已导入或验证数据。

- A user can create a workspace by name without supplying a filesystem path.
- A user can list and open an existing workspace; an empty workspace is a valid state with no active snapshot.
- Empty names, control characters or lone surrogates, unknown IDs, path traversal attempts, and symlinked workspace entries are rejected safely.
- A malformed or unsupported manifest is reported as unavailable/corrupt, is not overwritten, and does not prevent other workspaces from being listed.
- Workspace API responses never expose local absolute paths.
- The UI labels workspace state separately from bundled example data and does not imply that workspace creation imported or validated data.

## 安全与语义边界 / Security and semantic boundaries

- 工作区由服务端在本地管理；客户端只能提交名称和不透明 ID，不能提交路径。
- 工作区操作不会创建活动快照或质量结论。
- 在单写者锁实现前，不提供修改既有工作区内容的 API。
- 仓库示例的验证状态继续为 `not_run`。
- 创建工作区是用户主动发起的本地写入，受 loopback、Host 和 Origin 保护。

- Workspace storage is local and server-managed; clients submit names and opaque IDs, never paths.
- No workspace operation creates an active snapshot or a quality decision.
- No API mutates existing workspace contents until the single-writer lock is implemented.
- The bundled example continues to report validation as `not_run`.
- Workspace creation is a user-initiated local write guarded by the existing loopback, Host, and Origin protections.

## 已批准的本阶段实现约定 / Approved phase 1 implementation decisions

具体数据目录、manifest v1、API 状态码/错误码和 UI 边界见已批准的 `docs/plans/20261105-local-workspaces.md`。全局工作区切换与单写者锁仍属于后续实现范围。

The approved plan defines the data directory, manifest v1, API status/error codes, and UI boundaries. Global workspace switching and the single-writer lock remain for a later implementation phase.

## Current implementation result / 当前实现结果

本阶段已交付本地工作区创建、列表、只读详情、manifest 损坏提示和仓库示例隔离。存储竞态修复与 PR review follow-up 计划及最新门禁结果见[存储加固计划](../plans/20261105-workspace-storage-race-hardening.md)、[PR review 修复计划](../plans/20261105-pr-review-fixes.md)、[二次审查计划](../plans/20261105-pr-review-second-pass.md)和[当前验证报告](../qa/pr-review-second-pass-20261105.md)。`./scripts/verify.sh` 与 Playwright E2E 均通过。工作区打开后不切换仓库示例，也不创建快照。

This phase delivers local workspace creation, listing, read-only details, corrupt-manifest reporting, and separation from the bundled example. Platform data-root defaults, the `SDLC_QE_DATA_DIR` override, and manifest v1 are defined in the [approved plan](../plans/20261105-local-workspaces.md); storage hardening, PR review fixes, and the latest gates are recorded in the [storage follow-up plan](../plans/20261105-workspace-storage-race-hardening.md), [PR review follow-up plan](../plans/20261105-pr-review-fixes.md), [second-pass plan](../plans/20261105-pr-review-second-pass.md), and [current verification report](../qa/pr-review-second-pass-20261105.md). `./scripts/verify.sh` and Playwright E2E both passed. Opening a workspace does not switch the bundled example or create a snapshot.
