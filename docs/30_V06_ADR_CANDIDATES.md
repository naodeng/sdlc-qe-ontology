# v0.6 待审架构决策

| ADR | 候选决策 | 状态 | 验证要求 |
|---|---|---|---|
| ADR-06 | 共享核心 + SDLC + QE 三模块 | Proposed | 模块依赖和跨模块 CQ |
| ADR-07 | 复用 PROV-O 溯源语义，不以证据存在推断证据充分 | Proposed | 正反数据与溯源查询 |
| ADR-08 | OSLC 先映射再扩展，禁止无依据 `owl:equivalentClass` | Proposed | 官方术语审计 |
| ADR-09 | SHACL 是强制门禁，依赖缺失即失败 | Implemented candidate | 完整环境实测 |
| ADR-10 | 保持 Local-first，暂不引入图数据库服务 | Proposed | 样本查询性能测量 |

## 开发准入

所有阻断 ADR 必须有审查人、日期、证据路径和批准记录。自动化检查成功只是必要条件，不自动代表模型语义正确。
