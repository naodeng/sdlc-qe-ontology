# v0.8 PR–Build–Release 语义链实验

状态：**实验通过（仅 RDF/SPARQL）；SHACL 未通过完整环境验证；Baseline No-Go**。

## 范围

新增 PullRequest、Build、Release 三个类和 includesChange、builtFrom、containsBuild、targetsRequirement、hasExecution 五个属性。所有术语为本地实验契约，**不是 OSLC 官方等价映射**。

## 能力问题

- CQ-07：某 Release 对应哪些 PR、需求、测试义务和已有证据？
- CQ-08：某 Release 中哪些测试义务缺少当前数据图可查询的执行证据？

## 重要限制

CQ-08 的缺口是封闭快照中的“未找到”，不等于现实世界中绝对不存在。CQ-07 的证据存在不等于测试有效或发布安全。缺少版本、时间、环境、执行状态、签名与可信来源检查。

## 后续

引入带时间范围的构建与测试执行身份、来源追踪、证据可信度和明确的覆盖规则。
