# 最小技术 Spike：本地运行

实验使用 `https://example.org/sdlc-qe/` 临时 IRI，**不得发布为稳定命名空间**。

```bash
python -m pip install 'rdflib>=7,<9'
python -m unittest discover -s tests -v
# S03 额外验证（需要 pySHACL）
python -m pip install 'pyshacl>=0.29,<1'
python -m unittest discover -s tests -v
```

注意：未安装 pySHACL 时，SHACL 测试会 **SKIP**，不是 PASS。必须在有依赖的 CI 中强制检查无跳过，才能视为 S03 通过。

当前示例只验证 CQ-01~04 的简化子集；CQ-03 尚未从组件追溯测试，CQ-04 尚未校验时间和版本。它们不是完整 CQ 验收。
