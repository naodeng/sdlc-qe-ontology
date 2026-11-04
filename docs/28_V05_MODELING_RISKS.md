# v0.5 语义建模风险与反例

1. **开放世界误解：** OWL 中没有某条关系不等于关系为假。完整性要求用 SHACL / 业务校验。
2. **错误等价：** `CodeChange` 不等于 `ChangeRequest`；`TestExecution` 不等于 `TestResult`。
3. **证据充分性：** `prov:wasGeneratedBy` 只描述来源，不能证明测试正确、断言有效或满足发布门禁。
4. **测试义务：** `TestObligation` 是必须得到验证的责任/目标，不应直接等同一条测试用例。
5. **变更影响：** `modifies` 关系只能构成潜在影响链，需人工标注基准测量误报与漏报。
6. **命名空间：** `https://example.org/sdlc-qe/` 是实验 URI，不能当作正式长期稳定 URI。
7. **供应链：** 未审核外部项目许可证前，不直接复制本体文件或大段定义。
