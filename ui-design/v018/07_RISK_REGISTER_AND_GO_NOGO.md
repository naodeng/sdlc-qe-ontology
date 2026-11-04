# 风险登记与 Go/No-Go

| ID | 严重度 | 风险 | 控制措施 | 所属门禁 |
|---|---|---|---|---|
| R01 | Blocker | 映射错误导致假关系/假 Qualified | 预览、显式审批、金标、Unknown fallback | G0/G1 |
| R02 | Blocker | SHACL 不可用但展示已验证 | assurance 单独建模、阻断 verified badge | G0 |
| R03 | Blocker | 导入失败污染 active | staging + atomic pointer + fault injection | G2 |
| R04 | High | 本地恶意文件解析/外部实体/远程 context | 限制格式、网络禁用、资源预算 | G1 |
| R05 | High | 数据来源与版本不匹配 | hash/manifest/ontology-policy-mapping versions | G2 |
| R06 | High | 同一字段映射冲突/重复键 | blocking diagnostics | G1 |
| R07 | High | Arco/Figma 视觉与依赖不一致 | 组件安装 Spike、目标节点核对 | G4 |
| R08 | High | 真实项目无法映射到受控 schema | 先选 pilot、定义扩展边界、失败案例归档 | G5 |
| R09 | Medium | PII 在日志/导出泄露 | 脱敏预览、最小化日志、导出确认 | G1/G5 |
| R10 | Medium | MVP 范围膨胀 | 0.2+ 延后增量/AI/云同步 | PM Gate |

## Go/No-Go 模板
每个 gate 记录：负责人、提交 SHA、测试命令、环境、测试报告、失败项、风险接受人、日期。无证据即 Not Run；不能仅凭文档检查标记 Passed。

当前状态：**Design Candidate / No-Go for full MVP**；仅批准 Sprint 0 的验证性工作。此包未执行浏览器、真实 SHACL、Figma 像素匹配、文件系统故障注入或真实项目试点。
