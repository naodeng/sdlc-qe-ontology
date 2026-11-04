# v0.6 执行与门禁报告

## 本轮目标

将 SHACL 缺失从“跳过”改为“失败”，配置真实 GitHub Actions 入口，增加本体契约回归测试。保留 v0.5 的研究与博客资产。

## 已完成

- 将 `tests/test_shacl_optional.py` 修改为强制依赖，pySHACL 不存在时明确失败。
- 新增 `.github/workflows/validate.yml`，在 CI 安装声明的依赖并执行严格门禁。
- 新增 `tests/test_contract_regression.py`，检查 9 个类、5 个对象属性及类的中英标签。
- 保持 v0.5 的 ontology、SHACL 和 SPARQL 不变，避免未经证据的语义漂移。

## 验证限制与结论

当前容器已安装 RDFLib，但无法连接软件包索引安装 pySHACL。故此处只能执行 RDF/契约层测试，SHACL 真实验证未完成。CI 工作流是待远端执行的配置，不是 CI 已通过的证据。

**决策：No-Go。** 不得把 v0.6 视为正式 v0.1 语义基线。

## 解阻任务（按优先级）

| ID | 工作 | 完成证据 |
|---|---|---|
| G-01 | 在可联网环境安装 pySHACL 并运行严格门禁 | 完整日志、无失败和跳过、依赖锁定 |
| G-02 | 增加独立 SHACL 负样本（缺少验收标准、错误目标类型、缺少执行对象） | 每种故障都被准确检测 |
| G-03 | 核对 OSLC QM/CM/RM 术语及规范 URI | 官方来源、逐项映射、许可证记录 |
| G-04 | 核对 PROV-O 活动/实体语义与证据建模 | URI、示例与推理测试 |
| G-05 | 将 example.org 替换为获批准的持久命名空间 | ADR、迁移映射、兼容测试 |
| G-06 | 建立端到端 SDLC→QE→Release 样本 | 可复现查询、金标结果和反例 |

## 注意

当前 CQ 查询是实验样例，不构成影响分析准确率或质量证据充分性的实证证明。

## 本地执行记录

- unittest 退出码：`1`（缺失 pySHACL，预期失败）
- strict gate 退出码：`2`（缺失 pySHACL，预期阻断）
- 原始日志：`evidence/unittest-v06.txt`、`evidence/strict-gate-v06.txt`
