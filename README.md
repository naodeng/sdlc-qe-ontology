# SDLC-QE Ontology Workbench

Local-first workbench for tracing software delivery and quality evidence.

工作台默认使用简体中文，可切换 English。现在可创建、列出并只读查看本地工作区；仓库示例始终作为独立只读数据源。受限 JSON 是选定的首个导入格式，但导入、映射审批、快照发布和质量评估流程尚未实现。示例数据不代表验证结果。

## Quick start

    make setup
    make dev

Open the UI at http://127.0.0.1:5174. API docs: http://127.0.0.1:8000/api/docs.

Run checks with make verify. First install Playwright Chromium with cd frontend && npm run e2e:install, then run make e2e.

## Entry points

- [简体中文使用说明](README.zh-CN.md)
- [English setup guide](README.en.md)
- [Product and implementation baseline](docs/designs/current-baseline.md)
- [Local workspace requirement and implementation plan](docs/features/REQ-WORKSPACE-001-local-workspaces.md)
- [Latest workspace verification evidence](docs/qa/pr-review-fixes-20261105.md)
- [Repository bootstrap plan](docs/plans/20261104-repository-bootstrap.md)
- [Repository engineering standards](docs/standards/README.md)
- [Current API contract](docs/designs/api.yaml)
- [v0.18 product decisions](ui-design/v018/00_START_HERE_AND_DECISIONS.md)

Use Python 3.12+ and Node.js 22.12+. The project has not selected a release license.
