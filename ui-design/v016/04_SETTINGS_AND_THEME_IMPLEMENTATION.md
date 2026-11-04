# Sprint 0 设置系统实施规范

`PreferencesV1 = {schemaVersion:1, theme:'system'|'light'|'dark', language:'system'|'en'|'zh-CN'}`；默认 theme=system, language=system；非英文/中文系统语言回退 English。只保存非敏感偏好在 localStorage，不存 token、原始证据或本地文件路径。

初始化顺序：读配置 → Zod/等效 schema 校验 → 版本迁移或安全回退 → 解析系统主题与语言 → 在首屏绘制前设置根节点 `data-theme`/`lang` → 渲染。`matchMedia('(prefers-color-scheme: dark)')` 仅在 theme=system 时更新。手动主题不受系统变动覆盖。存储不可用时使用内存偏好，显示非阻断提示。

Animal Island UI 主题令牌必须通过适配层统一映射，禁止业务页面直接覆盖组件内部类名；验证 dark/light 对比度、focus ring、portal/drawer、toast、graph canvas。主题状态不影响 API 结果或缓存键。

版本信息：只读 GET /system/info，显示 app / ontology / dataset / policy / snapshot / commit；无法读取显示 Unavailable，不使用设计文档版本冒充应用版本。重置偏好仅清除 preferences key；不得删除本体、RDF、快照、日志或导入历史。

TDD: 首启、系统切换、手动覆盖、刷新持久化、配置损坏、未来 schemaVersion、存储异常、语言回退、RTL 非支持提示、深色可访问性、重置边界、版本接口失败、跨标签页 storage 同步（如实现则必须测）。
