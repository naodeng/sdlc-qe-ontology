# TDD 测试策略、金标和质量门禁

## TDD 执行顺序
每个用户故事：先写失败测试（Red）→ 最小实现（Green）→ 重构（Refactor）→ 正反例/安全/回归 → 证据归档。不得以 Mock-only 测试代替文件系统与 SHACL 集成测试。

| Case | Given | When | Then | Gate |
|---|---|---|---|---|
| T01 | 标准 CSV | 导入并确认模板 | 预览/映射/校验/快照成功 | P0 |
| T02 | 自定义列名 | 用户映射并确认 | 目标字段与来源准确可追溯 | P0 |
| T03 | 字段映射未确认 | 尝试发布 | 403/409，不生成 active | P0 |
| T04 | 修改已确认映射 | 再次提交 | 旧审批失效 | P0 |
| T05 | 重复主键/孤立外键 | 校验 | Blocking，报告行号/字段 | P0 |
| T06 | 执行时间无时区 | 证据资格判定 | Unknown/阻断，不给 Qualified | P0 |
| T07 | 缺 Build 或 release cutoff | 评估 | Unknown，reasonCode 可见 | P0 |
| T08 | SHACL 未安装/执行失败 | 验证 | assurance != verified，禁止 verified badge | P0 |
| T09 | 导入中断/断电模拟 | commit | 原 active hash 保持一致 | P0 |
| T10 | 并发导入同一 workspace | 两个 commit | 单写者锁、一个冲突 | P0 |
| T11 | JSON-LD 远程 context | 解析 | 禁止网络请求，拒绝输入 | P0 |
| T12 | 超限文件/递归 JSON | 解析 | 有界拒绝，资源不失控 | P0 |
| T13 | XSS 字符串/CSV 公式 | 预览/导出 | 安全渲染/转义 | P0 |
| T14 | 快照切换中查询 | 读取多个 API | 同一 snapshot 或显式冲突 | P0 |
| T15 | 无证据的义务集合 | 发布评估 | Unknown，不出现 vacuous Qualified | P0 |
| T16 | 中英切换/系统主题 | 向导操作 | 语言和主题保持，焦点可见 | P0 |
| T17 | 失败后重试相同输入 | 再次导入 | 不污染快照，不生成重复活跃提交 | P0 |
| T18 | RDF 恶意 IRI/路径 | 解析/浏览 | 不触发任意文件读取或网络请求 | P0 |

## 质量门禁
G0：语义三态金标 + SHACL 依赖实测；G1：解析器安全 + 受控 mapping schema；G2：文件系统隔离、原子切换和故障恢复；G3：端到端真实项目闭环；G4：Arco 构建、a11y、浏览器 E2E；G5：至少一个经脱敏的真实项目验收（1.0 目标仍为至少两个项目）。

**零容忍项**：误判 Qualified、未验证展示 Verified、跨快照拼接、导入失败污染 active、越界读取、未审批映射提交。通过率与覆盖率阈值需在 Sprint 0 基于实际测试框架冻结，不虚构数字。
