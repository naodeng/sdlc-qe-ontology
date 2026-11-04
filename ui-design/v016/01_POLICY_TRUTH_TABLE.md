# 三态判定：可实现的规则与冲突消解

## 输入与输出
每个 obligation 在固定 snapshotId、policyVersion 下评估。输入包含 `catalogComplete`、`requiredMetadataComplete`、`provenanceTrusted`、`validationState`、`evidence[]`。每条证据的 eligibility 为 `eligible` / `ineligible` / `indeterminate`，附 machine-readable reasonCodes。输出 `assessmentStatus` = `qualified` / `unqualified` / `unknown`，另有 `assuranceStatus` = `verified` / `unverified` / `blocked`。

## 明确的决策顺序（候选，待产品审批）
1. 数据集不可解析、义务全集不完整或策略版本不可识别：assessment=unknown，assurance=blocked。
2. 关键元数据缺失、证据来源不可信或关联不确定：assessment=unknown；不得被其它“看似合格”的证据覆盖。
3. 完整且可信的数据集中，如存在至少一条符合所有规则的证据：assessment=qualified。历史失败不自动否决，除非策略显式要求 latest-only；该策略 MVP 不启用。
4. 数据集完整且证据全集已声明，所有已知证据均明确不合格（或确认无证据）：assessment=unqualified。
5. 其它情况：assessment=unknown。

**重要边界**：SHACL `passed` 是结构合规，不证明证据真实或测试有效。assurance=verified 仅表示指定的验证清单已执行并通过，不等于发布批准。SHACL 未运行/失败时 assurance=blocked；可以展示 computed assessment，但必须带未验证标识，不能作为 Go 依据。

## 发布级聚合
- 义务全集不完整：unknown。
- 在全集完整前提下，存在 confirmed unqualified → unqualified；否则存在 unknown → unknown；全部 qualified → qualified。
- `assuranceStatus` 由验证清单汇总，任何 mandatory check 失败/未运行 → blocked；验证不全 → unverified；全部通过 → verified。
- 发布级 `qualified + blocked` 允许作为**计算结果**返回，但 UI 禁止标记为“已验证通过”。

## 反例矩阵
| 输入 | 义务判定 | 原因 |
|---|---|---|
| 截止时间缺失 | unknown | MISSING_RELEASE_CUTOFF |
| Build 环境缺失 | unknown | MISSING_BUILD_ENV |
| 义务全集不明 | unknown | CATALOG_INCOMPLETE |
| 证据全部明确失败且全集完整 | unqualified | NO_ELIGIBLE_EVIDENCE |
| 一条有效、一条失败且元数据完整 | qualified | ELIGIBLE_EVIDENCE_FOUND |
| 证据链接指向其他 build | unqualified（若全集完整） | BUILD_MISMATCH |
| 证据签名/来源未确认 | unknown | PROVENANCE_UNVERIFIED |
| 结构校验未执行 | computed 结果不变，assurance=blocked | SHACL_NOT_RUN |

对不确定的“证据全集是否完整”，默认 unknown 而非 unqualified。不要将开放世界假设下的 SPARQL NOT EXISTS 当作真实世界的不存在证明。
