# Plan: 20261104-workbench-all-pages-visual-polish
Status: Completed
Linked Requirement: REQ-BOOT-001

## 目标、现状与预期用户价值
优化前端工作台四个页面（项目总览、本体模型、数据导入、质量分析）、共享导航及跨页面交互，让数据状态更易读、页面重心更平衡、桌面与移动端阅读顺序更清楚。保留当前森林绿/薄荷色、双语文案、路由和“候选/未运行/未知”证据边界。

## 技术方案与架构边界
仅调整 React 页面结构、双语无障碍标签与 CSS。维持浅色品牌框架，让总览结论和示例规模保持两个清晰摘要面板，缩短次级页面阅读宽度，并让导入说明与质量报告各自形成更清晰的构图；添加键盘跳转入口和尊重减少动态偏好的轻量过渡。路径图仍可交互，导入步骤仍是静态计划说明。不得新增数据、评估结论、导入行为或 API/本体语义。

## 受影响文件（路径）
- `frontend/src/App.tsx`
- `frontend/src/styles.css`
- `docs/plans/20261104-workbench-all-pages-visual-polish.md`

## API / 本体 / 映射 / 快照变化
无。

## 时序图或数据流
无数据流变化。页面继续从现有本地 metadata API 读取只读示例数据。

## TDD: RED 测试、GREEN 实现、REFACTOR
改动限于呈现与可访问性，不增加产品运行逻辑。第二轮先保存当前四条路由在 1440、768、390 CSS 像素下的基线截图，再在相同环境比较，并检查路径选择、语言切换、路由链接和键盘跳转。

## 单元 / API / SPARQL / SHACL / E2E / 安全测试
- `npm --prefix frontend run build`
- `npm --prefix frontend run e2e`
- ego-browser：四条路由在 1440、768、390 宽度检查布局、溢出、字号和交互。
- 后端、本体、映射和安全逻辑不变；与本次呈现改动无关的门禁不纳入本次验证声明。

执行结果：
- `npm --prefix frontend run build` 通过。
- Design Taste Skill app lint 通过：0 FAIL、0 WARN。
- ego-browser 检查四条路由在 1440、768、390 及 320px 宽度的布局，均无横向溢出；在桌面验证模型路径选择，在手机验证导航和中英文切换。
- Playwright E2E 在沙箱内首次未能启动 Chromium，浏览器进程因 `MachPortRendezvousServer: Permission denied` 在测试执行前退出。按项目规则停止沙箱内重试；随后通过一次性沙箱外运行现有 E2E suite，2 项通过（Playwright 随附 headless Chromium，使用隔离本地预览配置）。
- Design Taste Skill 的 headless `inspect.mjs --app` 同样无法启动 Chrome；已改用 ego-browser 完成全路由截图和手动检查。

## 风险、回滚、可观测证据
风险限于样式覆盖、断点布局或焦点可见性。基线/复查截图保存在 `/private/tmp/`；如出现问题，回退本计划涉及的前端呈现改动，不动用户数据或其他工作区文件。

## 文档同步清单
本计划记录范围和验证方式；产品基线、API 契约与本体文档无需修改。

## 人工审批与执行结果
本任务由用户明确授权为全页面视觉优化；不改变产品语义、数据或服务行为，因此无需额外的语义/高风险审批。视觉实现、构建、样式 lint、浏览器手动检查和现有 E2E suite 均已完成。

## 最终复查记录
- 四个路由均在 1440、768、390 CSS 像素视口检查截图；另外在 320px 检查横向溢出，均为 0。768px 下导入步骤与分析报告改为单列，390px 下路径图转为垂直阅读；最终通过减少描边、以相邻底色与间距分组。
- 键盘首个 Tab 聚焦“跳到主要内容”，Enter 后焦点进入 `main`；语言按钮可切换英文且手机端无溢出；选择“测试用例”后更新详情并点亮此前三个连接段。
- `prefers-reduced-motion: reduce` 下页面与路径详情动画计算值均为 `none`。动效限于页面进入、详情切换及可见的细微状态变化。
- `npm --prefix frontend run build` 通过；Design Taste 源码 lint 为 0 FAIL、0 WARN。正文和状态色在最终浅色面板上的对比度均达到 4.5:1；次级色调微加深后仍保持原有森林绿与浅纸色方向。
- 仓库现有 Playwright E2E 在最终 CSS 版本上 2/2 通过，使用临时隔离配置连接当前本地预览和 API，并在测试后移除临时配置。Playwright 使用随附 headless Chromium。
- 截图、键盘、语言切换和 reduced-motion 检查由 ego-browser 执行；最终截图保存在 `/private/tmp/sdlc-qe-round3-final-*`。本轮未提交或推送。
