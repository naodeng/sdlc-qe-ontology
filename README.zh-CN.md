# SDLC-QE Ontology Workbench

Local-first 研发质量工作台，用于追踪需求、交付活动与质量证据。

**当前状态：** 工作台默认显示简体中文，可在右上角切换为 English。现在支持创建、列出和只读查看本地工作区；仓库示例始终是独立的只读数据源。受限 JSON 已选为首个导入格式，但真实导入、映射审批、快照发布和质量评估流程尚未实现。示例数据不代表验证结果。

## 快速启动

环境要求：Python 3.12+、Node.js 22.12+ 和 npm。

~~~bash
make setup
make dev
~~~

打开本地工作台：http://127.0.0.1:5174

本地 API 文档：http://127.0.0.1:8000/api/docs

工作区文件保存在服务端本机数据目录：macOS 默认为 `~/Library/Application Support/SDLC-QE Ontology Workbench`，Windows 默认为 `%LOCALAPPDATA%/SDLC-QE Ontology Workbench`，其他系统优先使用 `$XDG_DATA_HOME/sdlc-qe-ontology-workbench`，否则使用 `~/.local/share/sdlc-qe-ontology-workbench`。可通过 `SDLC_QE_DATA_DIR` 覆盖；相对路径按 API 进程工作目录解析，`~` 会展开。服务启动和读取不会创建数据目录。

运行 Python、本体、映射 Schema 和前端构建检查：

~~~bash
make verify
~~~

首次运行浏览器冒烟检查前，安装 Playwright 自带的 Chromium：

~~~bash
cd frontend && npm run e2e:install
cd .. && make e2e
~~~

## 当前已有

- React + TypeScript + Vite + Arco Design React 工作台壳层。
- FastAPI 本地 health、metadata 和工作区 API；工作区写入只发生在用户创建时。
- 本地工作区创建、列表和只读详情，使用严格校验的 manifest 与原子目录发布。
- RDFLib 本体读取适配器；本地服务绑定 127.0.0.1。
- 候选本体、SHACL 正反例、SPARQL competency queries 和 mapping profile schema。
- Python、本体、Schema、UI 构建检查、Playwright Chromium 冒烟测试和 GitHub Actions 工作流。
- 页面明确显示 Unknown 和 not run，不会把未验证状态显示成通过。

## 尚未实现的 MVP 流程

- 全局当前工作区选择和工作区既有数据写入锁。
- 受限 JSON 首个导入器（profile 尚待定义），以及后续 CSV/受控 RDF 导入与字段预览。
- 可视化映射编辑、人工确认及审批失效。
- 数据预检、完整 SHACL/策略验证和不可变快照原子切换。
- 测试证据资格判定与带来源的质量报告。

## 文档入口

- [产品与实现基线](docs/designs/current-baseline.md)
- [本地工作区需求与实现计划](docs/features/REQ-WORKSPACE-001-local-workspaces.md)
- [最新工作区验证证据](docs/qa/pr-review-second-pass-20261105.md)
- [本次仓库搭建计划](docs/plans/20261104-repository-bootstrap.md)
- [工程标准](docs/standards/README.md)
- [实现中的 API 契约](docs/designs/api.yaml)
- [v0.18 产品决策](ui-design/v018/00_START_HERE_AND_DECISIONS.md)
- [QA 检查与证据状态](docs/qa/README.md)

evidence/ 内保留的日志来自早期版本，只用于历史追溯，不代表当前 checkout 已通过相同检查。项目尚未发布正式 LICENSE。
