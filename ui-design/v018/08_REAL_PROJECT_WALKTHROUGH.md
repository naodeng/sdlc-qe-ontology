# 真实项目试点：退款 PR 质量分析（示例，不是已验证数据）

## 准备
准备 5 份脱敏 CSV：requirements、changes、builds、test_obligations、test_executions，以及可选 evidence。确保每条记录有稳定外部 ID、来源、版本和时间戳。MVP UI 使用标准模板或逐字段映射；每张表必须选择 entity type。

## 使用流程
1. 在 Workspaces 创建 `refund-demo`；显示工作区位置与权限提示。
2. Import Wizard 上传 `requirements.csv`，预览 `req_key` → Requirement.id、`title` → Requirement.title；人工确认。
3. 上传 PR/build/obligation/execution，配置 `requirement_ref`、`build_ref` 等引用字段，检查孤立引用。
4. 运行 DQ + SHACL；若缺少 build reference 或执行时间时区，显示阻断或 Unknown，不能强行视为通过。
5. 确认验证摘要、mapping hash、来源 hash 后 Commit，生成 snapshotId。
6. Overview 选择 PR-128 → Quality Decision；显示退款功能测试证据与权限测试义务缺口。
7. 导出报告：关联 Requirement、TestObligation、Build、Evidence、reasonCode、assessmentStatus、assuranceStatus、snapshotId。

## 用户价值验收
在同一组人工标注数据上对比：变更影响分析耗时、已知缺口召回、误报率、证据追溯完整率、错误 Qualified 数量。记录原始结果，不能预设改善百分比。
