# v0.18 API 候选增量（相对 v0.17）

> 以下为资源语义草案，必须合并入 OpenAPI 3.1 后通过 schema contract test；不是已部署接口。

| Method | Path | 说明 |
|---|---|---|
| GET | `/api/v1/workspaces` | 本地工作区列表（仅显示已登记目录） |
| POST | `/api/v1/workspaces` | 创建工作区，路径受限 |
| GET | `/api/v1/workspaces/{id}` | workspace manifest/active snapshot |
| POST | `/api/v1/workspaces/{id}/imports` | 创建 job、登记上传文件/模板 |
| GET | `/api/v1/workspaces/{id}/imports/{jobId}` | job 状态、预览和诊断 |
| PUT | `/api/v1/workspaces/{id}/imports/{jobId}/mapping` | 保存映射草稿（revision） |
| POST | `/api/v1/workspaces/{id}/imports/{jobId}/mapping-confirmations` | 确认 fileHash+mappingHash+revision |
| POST | `/api/v1/workspaces/{id}/imports/{jobId}/validations` | 执行 DQ+SHACL，幂等键 |
| POST | `/api/v1/workspaces/{id}/imports/{jobId}/commits` | 原子提交，前置版本检查 |
| POST | `/api/v1/workspaces/{id}/imports/{jobId}/cancellations` | 请求取消 |
| GET | `/api/v1/workspaces/{id}/snapshots` | 快照历史 |
| GET | `/api/v1/workspaces/{id}/snapshots/{snapshotId}` | manifest 与验证摘要 |

所有写接口需 Origin/Host 检查、CSRF 防护策略、body 限制、job ownership/workspace 隔离；localhost 不是信任边界。错误 envelope：`code`、`message`、`details`、`requestId`；冲突用 409、不可处理映射用 422、过大用 413、锁定用 423（候选）；禁止向前端返回绝对系统路径。

所有分析 API 继续要求 snapshotId；新增 import/commit 写接口**不代表**开放本体编辑、任意查询或 release approval。
