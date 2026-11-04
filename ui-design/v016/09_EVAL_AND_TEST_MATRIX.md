# Eval 与验收矩阵

## 金标集合
至少覆盖：完整合格、全部失败、无证据但全集完整、缺截止时间、缺环境、跨 build、跨 snapshot、混合证据、来源未确认、过期证据、重复执行、SHACL 未运行、义务全集不完整、损坏 RDF、未知 policyVersion。每个 fixture 提供预期 assessment、assurance、reasonCodes。

## 指标
- **False Qualified = 0**（强制门禁，优先级高于整体准确率）。
- Unknown→Qualified 错误 = 0；跨快照关联 = 0；mandatory skipped = 0。
- 每条 release 结果可回溯 snapshotId、policyVersion、规则版本和证据标识。
- 图谱节点上限与截断提示一致；API p95 目标值需在固定硬件/数据规模下先测基线再确定。
- WCAG 2.2 AA 检查：键盘、焦点、文本对比度、状态非颜色唯一表达、200% 缩放、reduced motion。

## 测试金字塔
Unit：policy truth table / preference schema；Contract：OpenAPI schema / reason codes；Integration：RDFLib + SHACL + snapshot；E2E：Playwright theme/locale/quality status；Security：CORS/path/XSS；Performance：固定图谱规模和查询时延。每类测试至少一条负例。

**对照实验**：B0 Python 确定性关系查询 vs B1 RDF+SPARQL vs B2 SHACL+policy。评估相同数据和金标，不以 RDF 查询通过推断 ontology 有独特价值。
