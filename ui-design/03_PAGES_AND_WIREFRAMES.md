# Pages, Navigation & Wireframes / 页面与线框

## IA
`Overview | Ontology Explorer | Relationship Graph | Evidence Explorer | Quality Decision | Validation Status`
全局：数据集选择（MVP 仅预置只读数据集）、snapshot、语言 EN/中文、状态图例、帮助。

## 1 Overview
```text
┌──────────────────────────────────────────────────────────────┐
│ SDLC-QE Workbench    Dataset: demo-v010  Snapshot: abcd…  EN │
├──────────────┬───────────────────────────────────────────────┤
│ Overview     │ Dataset status: PARTIAL / Validation: BLOCKED │
│ Ontology     │ Requirements  PRs  Builds  Obligations        │
│ Graph        │ Qualified | Unqualified | Unknown             │
│ Evidence     │ [Open unknown obligations] [Explore graph]    │
│ Decisions    │ Last evaluated · Policy version · Source      │
│ Validation   │ Note: advisory, not a release approval        │
└──────────────┴───────────────────────────────────────────────┘
```

## 2 Ontology Explorer
左侧：Class/Property 列表 + 搜索；右侧：label (EN/中文)、IRI、description、domain/range、superclass、mapped standards、mapping review status；空字段显示 Not specified。点击关系跳转 Graph。

## 3 Relationship Graph
左：起点类型与 ID、深度 1–2；中：可缩放关系图；右：节点详情与 provenance；底部：表格/无障碍替代视图。超过上限显示“已截断”，不可误当完整图。

## 4 Evidence Explorer
过滤器：Release / Build / Obligation / status / reason。列表列：Obligation、Build、Execution、Evidence、Result、Reason。详情面板展示 `executedAt`, `releaseCutoff`, `executionEnvironment`, `buildEnvironment`, `digestPresent`, provenance links；未知字段明确标注 Missing。

## 5 Quality Decision
```text
Release R-001  |  Policy evidence-qualification-v1 | Snapshot abcd…
Overall: UNKNOWN (manual decision required)
┌───────────────────┬───────────────┬─────────────────────────┐
│ Obligation        │ Assessment    │ Why                     │
├───────────────────┼───────────────┼─────────────────────────┤
│ OB-1              │ Qualified     │ Valid matched evidence  │
│ OB-2              │ Unknown       │ MISSING_RELEASE_CUTOFF  │
│ OB-3              │ Unqualified   │ EXECUTION_FAILED        │
└───────────────────┴───────────────┴─────────────────────────┘
[Inspect evidence]  [Show policy]  [View validation status]
```
颜色之外始终显示文字+图标；Unknown 不用绿色；整体汇总：存在 Unknown → Unknown（即使同时存在 Unqualified，按策略可配置但必须解释）；全部 Qualified 才显示 Qualified（仅表示规则资格，不是 Go）。

## 6 Validation Status
展示 parse、SHACL、CQ、contract test 的 `passed|failed|not_run|unavailable` 和日志位置；依赖缺失显示 unavailable，不转化为 passed。

## UX 边界与错误态
- Loading / Empty / Partial / Error / Truncated / Stale 五种状态必须有专门文案。
- “No results” 与 “No gaps” 不同；未知或未运行时禁止显示“全部通过”。
- Graph 点击节点可回到列表，支持键盘、focus、屏幕阅读器说明。
