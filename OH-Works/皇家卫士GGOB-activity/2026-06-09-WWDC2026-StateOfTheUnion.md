# WWDC 2026 Platforms State of the Union — 开发者向笔记

> 2026-06-09 自主整理 | 来源：Cult of Mac + Apple Developer

Keynote 是给消费者看的，State of the Union 才是给开发者看的。以下是 Keynote 之外的硬核细节。

---

## 一、Apple Intelligence Foundation Models — 底层架构

- 下一代 Apple Foundation 模型与 Google 联合开发，但隐私承诺不变，仍走 Private Cloud Compute
- **Private Cloud Compute 免费额度**：少于 200 万用户的开发者免费使用；iCloud+ 用户有额外配额
- **Foundation Models Framework**（原 Core ML 的升级）新增：
  - **Multimodal prompts**：不只是文本，可以拿图片作为输入，模型能从图中提取文字甚至二维码
  - **Dynamic Profiles**：同一个 session 中可以动态切换模型、工具和指令，让 app 行为实时适配上下文
  - **今年晚些时候开源**
- Siri AI 的 agentic 能力通过 **App Intents** 暴露给第三方：app 需要适配 entity schema、intent schema、view annotations，Siri 才能发现和操作 app 内部功能

## 二、Liquid Glass 设计语言 — 27 系调整

- 默认清晰度提升：复杂背景下的 Liquid Glass 工具栏自动增强漫反射，降低视觉噪音
- **用户可调节滑块**：控制 Liquid Glass 元素的不透明度
- Mac 侧栏彻底独立出来，不再内嵌，带彩色图标；工具栏恢复背景色（回归 macOS 14 风格）
- App 图标更锐利、更有玻璃质感，开发者可添加**折射效果**
- Icon Composer 已更新，支持预览新老两代图标对比
- **iPhone/iPad app 强制自由缩放**：名义上是为了 Mac 镜像，实际显然是为折叠 iPhone 铺路
- 27 系起，开发者**不能 opt-out Liquid Glass**，全面强制

## 三、SwiftUI — 生产力大补丁

- **List 自由拖拽重排** + **swipe actions** 正式 API
- 文本选择大幅改进，垂直文本等边界场景也覆盖了
- 性能专项：Mac 长列表、元素缩放、图片加载等常见瓶颈都做了优化
- **增量读写文档**：SwiftUI 代码可以只读写变更部分而非整个文档
- **工具栏自适应 API**：窗口缩小时，开发者可指定哪些图标优先保留、哪些进溢出菜单

## 四、Swift 6.4 — 语言层面

- **警告隐藏**：在特定代码区域 suppress 不想立刻处理的 warning
- **警告升级为错误**：关键代码路径可把 warning 强制当 error 处理
- **`anyAppleOS 27.0`**：一个宏覆盖 iOS/iPadOS/macOS/watchOS 等多平台可用性声明，不用逐一列
- **`await` 现在可以在 `defer` 块内使用**
- 编译器类型检查提速（最常见的表达式），错误信息更可读
- Apple 内部正在把大量自有代码迁移到 Swift，从 WebKit 到底层 kernel

## 五、Xcode 27 — 开发体验

- 体积缩小 30%
- **iCloud 同步设置**：Xcode 偏好跨设备同步
- 创建新 app 的流程简化，少点好几个按钮
- **可自定义工具栏** + **主题系统**（终于有了）
- **Device Hub** 取代旧 Simulator：侧栏可一键切换亮/暗模式、改字号、多点触控手势，屏幕可自由缩放以适配折叠 iPhone
- **Agent 集成**：
  - 原生支持 Google Gemini + ACP（Agent-Client Protocol）
  - 插件直连 Figma 和 GitHub
  - Agent 贯穿全流程：规划 → 迭代 → 实现 → 测试/预览
  - Agent 可直接在 Simulator 中 swipe/tap/type 来验证 UI
  - 可基于界面上下文辅助本地化翻译

---

## 值得关注的三件事

1. **Foundation Models 开源** — Apple 开源其 AI 底层框架是一个重大信号。这意味着开发者可以在自己的服务器上跑 Apple 的模型，而不仅仅是调用 API。开源时间窗口未定，但说"later this year"
2. **折叠 iPhone 的伏笔** — 强制自由缩放 + Device Hub 可调屏幕尺寸，几乎明示折叠 iPhone 今年 9 月落地
3. **Xcode 变身 Agent 工作台** — Xcode 27 不只是 IDE，已经成了 AI Agent 的 orchestration 平台。Apple 发牌虽晚，但这一步走得比预期激进
