# v0.4 质量门禁与架构决策复核

## 已决定的实验约束

- 范围：Shared Core + SDLC + QE；行业业务本体、Agent 平台不进入 v0.1。
- 本体可脱离 LLM 独立使用。
- 实验阶段使用 RDFLib 与 SHACL；不强制引入图数据库。
- TestObligation 与 TestCase 分离；TestEvidence 与 QualityClaim 分离。

## 严格门禁

执行 `python -m pip install -r requirements-validation.txt` 后运行 `python scripts/verify_baseline.py`。缺少 pySHACL 时必须返回非零状态；任何失败或跳过的测试不得计入通过。正式 CI 应使用仓库根目录的 `.github/workflows/ontology-quality-gate.yml`，本包提供可复制的示例文件。

## 阻断项

| 编号 | 阻断项 | 解除条件 |
|---|---|---|
| G01 | 标准 URI/Shape 未逐项核验 | 提交来源和精确术语映射证据 |
| G02 | SHACL 验证未有通过证据 | 正反样本在完整依赖环境通过 |
| G03 | 稳定命名空间未确定 | 确认域名、版本与弃用政策 |
| G04 | 许可证未审计 | 记录每项复用资产的许可 |
| G05 | CQ 覆盖不足 | 为 v0.1 必要 CQ 建立 golden fixture |
| G06 | 真实研发项目数据缺失 | 建立匿名或合成端到端 SDLC/QE 样本 |

## Go / No-Go

当前：**NO-GO for v0.1 baseline freeze**。可以继续技术 Spike 和文档评审，不应把实验模型描述为稳定标准。
