# TDD & Acceptance Plan / 测试先行验收

## 测试金字塔
1. **Policy unit tests**：纯函数输入固定的结构化数据 → status/reasons，先写失败测试再实现。
2. **RDF adapter contract tests**：使用 v0.10 golden/negative、evidence-* fixtures，验证查询结果和 IRI 关联，不修改原始数据。
3. **API tests**：响应 schema、错误码、snapshot 一致性、排序/分页、limit、无更新接口。
4. **UI component tests**：状态标签、Missing/Unknown、错误态、图谱截断、双语、键盘导航。
5. **Playwright E2E**：从 Release 到 Obligation 到 Evidence 的完整只读路径。
6. **Security/performance**：非法路径、非本机绑定、恶意参数、超大图、慢查询超时。

## 首批测试用例（必须先红后绿）
| ID | 输入/场景 | 预期 |
|---|---|---|
| UI-001 | v0.10 缺 releaseCutoff | unknown + MISSING_RELEASE_CUTOFF |
| UI-002 | 缺 buildEnvironment | unknown + MISSING_BUILD_ENVIRONMENT |
| UI-003 | passed、环境一致、时间合法、digest 非空、Build 正确 | qualified（实验资格） |
| UI-004 | 仅 failed execution，完整输入 | unqualified + FAILED_EXECUTION |
| UI-005 | 同义务既有 failed 又有合格 execution | qualified，保留其他失败记录供审查 |
| UI-006 | 不同 Build 的合格 evidence | 不得冒用；wrong link reason |
| UI-007 | RDF parse error | validation unavailable，决策 unknown |
| UI-008 | pySHACL 未运行 | validation not_run/unavailable，禁止显示“已验证” |
| UI-009 | CQ-10 返回空但元数据缺失 | 仍为 unknown，记录 CQ discrepancy |
| UI-010 | Graph 超过节点上限 | truncated=true，显示不完整警告 |
| UI-011 | 切换 snapshot | 缓存失效，所有详情同一 snapshot |
| UI-012 | API 恶意路径/非法 IRI | 4xx，禁止读取目录外文件 |
| UI-013 | 仅键盘操作图谱/详情 | 可访问核心信息 |
| UI-014 | 中英切换 | 文案正确，状态语义不变 |
| UI-015 | 空结果与网络错误 | 不显示 Qualified |

## 门禁
- 所有 P0 测试通过、0 skipped、0 xfail；SHACL 完整验证需真实运行并通过。
- 状态判定金标：0 false-qualified（当前固定 adversarial fixture 范围内）。
- OpenAPI schema 校验、静态类型检查、lint、组件与 E2E、可访问性 smoke test 均通过。
- 必须保存 `test-results/`、fixture hash、依赖锁定、运行命令与退出码；CI 运行后方可声称远端验证完成。

## TDD 工作流
`Write fixture & expected state → Red test → Minimal implementation → Refactor → Negative/mutation cases → CI evidence → Review`。
