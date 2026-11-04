# 导入与字段映射规范（PRODUCT-ADR-008/009）

## 必须保留的工作流
`Upload → Quarantine → Preview → Map → Human Confirm → Preflight → SHACL → Build Snapshot → Atomic Activate`

- CSV、JSON 和受控 RDF：严格按显式允许的编码、媒体类型、尺寸和解析策略处理。
- 方案 B：标准模板 + 可视化字段映射；映射必须保留用户批准记录，输入变化或规则变化须使批准失效。
- 拒绝重复主键、循环或未解析引用、可疑 RDF、路径遍历、外部实体、不可信外部 URL；错误不得污染活动快照。
- 原始数据、映射配置、验证报告和来源哈希与 snapshot ID 绑定。字段语义不能由 AI 自动猜测并无确认写入。
- 预检的“未发现错误”不等于数据集已经完整；数据完整性另行证明。
