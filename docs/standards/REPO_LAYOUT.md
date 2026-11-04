# 推荐目标仓库结构（项目基线）

```text
repo/
  AGENTS.md
  README.md / README.zh-CN.md
  CONTRIBUTING.md
  frontend/              # React + Arco
  backend/               # FastAPI / application / domain / adapters
  ontology/              # TTL, SHACL, CQ, mappings
  e2e/                   # Playwright
  scripts/               # Local lifecycle and validation
  docs/
    features/            # Requirements
    plans/               # Frozen approved plans
    designs/             # Current approved facts + ADRs
    standards/           # Enforced engineering standards
    qa/                  # Case / evidence index
  .agent/skills/          # dev-plan/dev-build/dev-debug
  .github/               # PR template / CI
  tests/                 # Python/API/ontology tests
```

当前仓库已经使用此根目录结构，并把 Python/API/ontology tests 放在根级 `tests/`。浏览器 E2E 测试位于 `e2e/tests/`。

仓库历史交付包中的 `01_project/` 与 `02_blog/` 不是部署仓库根目录；项目资料已按职责迁入当前目录，历史 UI 设计保存在根级 `ui-design/` 以维持来源与链接追溯。
