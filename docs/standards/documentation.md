# 文档治理：过程文档与事实文档

`docs/features/`：版本化需求与验收（变更可提新版本，保留历史）；`docs/plans/`：一次任务一份 Plan，审批后冻结，修订创建新文件；`docs/designs/`：**当前批准的事实**（API、领域、数据模型、ADR）；`docs/standards/`：当前工程规范；`docs/qa/`：可追溯测试用例及执行证据。

变更检查：API→`docs/designs/api.yaml`；本体→模型/SHACL/SPARQL/CQ；导入→Mapping schema/预检/快照；UI→Arco token/页面/可访问性；状态规则→golden/决策 ADR；每个 PR 必须说明 `docs/` 同步情况。

旧版 `ui-design/v011–v018` 仅用于历史追溯，不应直接视为最新审批契约；以事实文件+正式 ADR 为唯一实施依据。
