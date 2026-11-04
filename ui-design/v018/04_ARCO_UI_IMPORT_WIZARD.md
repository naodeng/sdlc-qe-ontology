# Arco Design Pro 2.0 风格导入向导

## 新增页面与路由（候选）
`/workspaces` 工作区列表；`/workspaces/:id/import` 导入向导；`/workspaces/:id/import/:jobId/review` 验证与发布审批；`/workspaces/:id/snapshots` 历史快照。现有 Overview/Explorer/Graph/Evidence/Decision/Validation/Settings 不改变核心职责。

## 向导步骤
1. **Source**：选择 CSV/JSON/RDF、来源说明、工作区和模板。
2. **Preview**：文件大小、行数、列名、敏感字段提醒、错误示例。
3. **Map**：Arco Table 列出源字段、Select 选择目标概念/属性、表单校验、类型转换预览；保存草稿。
4. **Validate**：数据质量、SHACL、完整性、provenance、policy readiness；显示 Blocking/Warning。
5. **Review & Commit**：展示 diff、source hash、mapping hash、snapshot metadata、风险接受、确认提交。
6. **Explore**：跳转新快照的分析页，保留快照 ID。

## 组件适配
Arco Steps、Upload（限制类型/大小）、Table、Form、Select、Alert、Drawer、Modal、Tag、Result、Progress、Tabs；业务层包一层 adapter，避免组件 API 渗透 semantic domain。组件名称/能力属于候选，需要真实安装验证。

## 关键交互
- 有 Blocking error 时禁用 Commit；Warnings 必须展开查看并明确确认。
- 页面刷新后恢复 job 状态；审批失效时显示原因。
- 大文件预览分页，不在浏览器持有整个文件。
- 键盘操作、屏幕阅读器状态播报、色彩不作为唯一错误信号、深浅色与中文长文本验证。
- 导入进度、失败和取消应与后端真实状态同步，不使用假进度。

## Figma 约束
所给节点 `342:94144` 仅是“通知、我的👉”标题，不是完整导入页面。此处是依据 Arco 设计语言的产品设计规范，不声称像素级复刻。完整 dashboard/table/form 视觉对齐仍需对应节点与截图验收。
