# 风险登记与基线 Go/No-Go

| 风险 | 严重度 | 当前状态 | 解除证据 |
|---|---|---|---|
| R01 pySHACL 未实测 | Blocker | Open | 正反样本、完整日志、0 skip |
| R02 质量判定实现缺失 | Blocker | Open | 可执行真值表、mutation/adversarial tests |
| R03 OSLC/PROV-O 精确映射未签署 | Blocker（对正式本体冻结） | Open | URI/定义/许可审核记录 |
| R04 Animal Island UI 兼容性未知 | Blocker（对 UI 开发） | Open | npm install/build/a11y/license Spike |
| R05 snapshot 原子性未验证 | Blocker | Open | 并发切换与缓存隔离测试 |
| R06 localhost 安全未验证 | High | Open | Origin/path/SSRF 测试 |
| R07 深色主题与组件冲突 | High | Open | 视觉回归和可访问性测试 |
| R08 真实数据完整性证明困难 | High | Open | manifest 与 pilot 证据 |

**Go**：所有适用 Blocker 有可复现通过证据、负责人确认、版本冻结；**Conditional Go**：仅允许明确缩小范围且不影响质量可信度的非阻断任务；**No-Go**：任何 mandatory 验证跳过、false Qualified、快照混合或安全越权。
