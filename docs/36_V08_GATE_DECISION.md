# v0.8 Gate 决策

- RDF/SPARQL 正反样本：以 evidence 日志为准。
- SHACL：pySHACL 仍不可用，严格门禁必须失败；不得以 RDF 查询替代 SHACL。
- OSLC / PROV-O：术语 URI、定义、许可证复核未关闭。
- PR/Build/Release：已形成实验样例，尚未建立真实系统适配。

**结论：Candidate / No-Go。**

下一步：在可联网 CI 中安装锁定版本依赖并运行 SHACL；完成标准 URI 级映射审查；增加包含失败执行、过期证据、错误构建关联的反例；冻结版本化契约前执行 ADR 评审。
