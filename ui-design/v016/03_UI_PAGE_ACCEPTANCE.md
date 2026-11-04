# 七个页面：组件、状态与可验收交互

| 页面 | 主组件 | 加载/空/失败 | 验收重点 |
|---|---|---|---|
| Overview | KPI Card、status strip、snapshot banner | loading skeleton / no data / degraded | 计数有 snapshot 来源；partial 不伪装总数 |
| Ontology Explorer | search、concept list、detail drawer | no concepts / 404 / mapping unknown | IRI 可复制；中英文 fallback；长词折行 |
| Relationship Graph | bounded graph、list fallback、details | truncated badge / no edges / graph error | 图和列表同一 edge set；键盘可达；节点上限 |
| Evidence Explorer | obligations table、evidence drawer | no evidence ≠ pass / invalid provenance | reason codes 可见，支持来源追溯 |
| Quality Decision | tri-state cards、assurance banner、reasons | Unknown prominent / blocked / stale | `qualified+blocked` 不出现绿色已验证通过 |
| Validation Status | checks table、last run、hash | not run / failed / passed | 真实时间与报告哈希；不伪造通过 |
| Settings | theme cards、language select、version table | corrupted prefs / info unavailable | 三主题、语言持久化、重置不删数据 |

## 全局 UI 状态机
`booting → ready | degraded | error`；`snapshot-stale` 为覆盖状态；切换快照必须重新获取所有业务数据。Error boundary 提供重试而不重写数据。

## 视觉约束
使用 Animal Island UI 的色彩和圆角语义，但数据密集页优先可读性；图谱节点和三态标签必须同时使用文本/图标，不仅靠颜色；支持 `prefers-reduced-motion`、200% 缩放、键盘焦点、WCAG 2.2 AA。深色模式必须覆盖弹窗、图谱、滚动条、代码块、空态。不得硬编码“已验证”状态。

## 页面验收例
- Given release assessment=qualified, assurance=blocked; When 打开 Quality Decision; Then 显示“计算符合条件 / 验证阻断”，不显示“已验证通过”。
- Given graph 300 nodes; When 请求两跳关系; Then 返回至多 200 nodes 且 `truncated=true`，并提供列表视图。
- Given 语言切换到 zh-CN; When 刷新; Then 导航、reason code 的人类可读说明保留中文，原始 reason code 不变。
