# 架构与数据生命周期

## 分层
- React/TypeScript/Vite + Arco React：Workspace、Import Wizard、Mapping Editor、Validation Review、Snapshot History、现有 7 个分析页面。
- FastAPI：本地受限上传/文件选择接口；导入作业状态机；只读快照查询；无任意文件路径参数。
- Import service：流式大小检查、解析器、schema/profile、映射编译、转换、引用校验、数据质量报告。
- Semantic engine：RDFLib、SHACL、SPARQL CQ、三态 policy；**policy 只读取已发布快照**。
- Storage：workspace manifest、staging/jobs/<id>、snapshots/<content-addressed-id>、active pointer、mapping profiles、audit events；无 DB 依赖作为 MVP 默认。

## 状态机
CREATED → PARSING → PREVIEW_READY → MAPPING_DRAFT → MAPPING_CONFIRMED → VALIDATING → REVIEW_READY → COMMITTING → COMMITTED。
任一可失败阶段 → FAILED / CANCELLED（终态）；commit 失败回到可恢复状态但不自动重试；不能从 FAILED 跳过校验直接 COMMITTED。

## 原子提交协议（候选）
1. 在工作区内 staging 生成数据、映射快照、validation report、manifest；每项写入后 fsync（依平台能力）。
2. manifest 包含 ontologyVersion、policyVersion、mappingProfileVersion、datasetVersion、source hashes、validationRunId、createdAt、文件 digest；所有路径为相对路径且不能逃逸 workspace。
3. 完整性校验成功后，将 staging 快照移至 snapshots（同卷 rename）；原子替换 active pointer；追加 audit。
4. 崩溃恢复：active pointer 只能指向已验证存在的快照；孤立 staging 隔离清理；不允许将部分数据呈现为 active。
5. 并发：同一 workspace 单写者锁；旧快照查询允许继续；跨 snapshot API 请求返回冲突，不静默混用。

## 隔离与安全
文件最大尺寸、记录数、深度、解析时间、图节点数均可配置且默认有限；拒绝 symlink/path traversal、公式注入导出、远程 JSON-LD context、XML 外部实体、恶意压缩包；导入内容始终视为不可信。浏览器 UI 对导入文本做安全渲染；后端只绑定 loopback 并检查 Host/Origin。

## 失败原则
解析失败：保留错误摘要，active 不变；映射失败：返回字段级错误；SHACL 失败：保留报告，不得自动 commit；可配置的非阻断警告必须经人工确认并保留 risk acceptance，阻断错误不能通过风险接受绕过。
