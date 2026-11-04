# Local-first 安全威胁模型与防护

| 威胁 | 防护 | 必测反例 |
|---|---|---|
| 浏览器恶意站点访问 localhost API | 127.0.0.1 bind；精确 Origin/CORS；禁止 wildcard；拒绝不受信跨站请求；敏感读取可增加本地会话能力令牌 | evil origin fetch |
| 任意 SPARQL 查询注入 | 只允许固定 query ID + typed parameters；禁任意 query 文本 | UNION/SERVICE/LOAD 注入 |
| 任意路径读取 | 数据集来自受控 workspace manifest，禁止客户端传绝对路径 | ../ 和符号链接越界 |
| RDF 字面量 XSS | 纯文本渲染、URI scheme allowlist、CSP、禁 dangerouslySetInnerHTML | HTML/JS literal |
| 图谱拒绝服务 | depth<=2、nodes<=200、超时与分页 | 巨型高出度图 |
| 快照混合/缓存污染 | snapshotId+policyVersion 进入所有业务 cache keys；不可变 manifest hash | 切换快照并发请求 |
| 依赖/许可证风险 | lockfile、SCA、SBOM、license review | UI 包版本升级 |
| 证据泄露 | 本地文件路径脱敏、只读、导出需显式确认（MVP 不提供） | API response 泄露路径 |

**安全边界**：Local-first ≠ 自动安全；localhost 服务仍需防 DNS rebinding、CSRF、Origin 误配置。MVP 不默认监听 0.0.0.0，不开启远程同步。日志不得记录证据正文或认证信息。
