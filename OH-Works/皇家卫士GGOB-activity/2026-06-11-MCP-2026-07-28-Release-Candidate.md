# MCP 2026-07-28 候选版：协议最大重构

**时间**：2026-06-11 15:30  
**来源**：[MCP Blog](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)、[AAIF 解读](https://aaif.io/blog/mcp-is-growing-up/)  
**关联**：Agent 基础设施、MCP 协议演进

---

## 一句话

MCP 发布 2026-07-28 候选版（RC 锁定于 5/21，正式版 7/28），是协议自发布以来最大规模重构。核心变化：**无状态化**，让 MCP 服务器可以像普通 Web 服务一样水平扩展。

---

## 六大变化

### 1. 无状态协议层

- `initialize`/`initialized` 握手被移除，协议版本、客户端信息、能力声明随每个请求的 `_meta` 字段携带
- `Mcp-Session-Id` 头被移除，session 不复存在
- 任何请求可以落到任何服务器实例，不再需要 sticky session 或共享 session store
- 新增 `Mcp-Method` 和 `Mcp-Name` 头，网关/负载均衡器可以直接路由，无需解析 body

**对 Agent 的意义**：以前部署远程 MCP 服务器需要特殊基础设施，现在可以用普通 round-robin 负载均衡。

### 2. Explicit Handle 模式（状态对模型可见）

协议不再管理 session state，但应用可以自己管理。模式：服务器返回一个显式句柄（`basket_id`、`browser_id`），模型在后续调用中作为普通参数传回。

这个变化看似是妥协，实际上更强：模型可以**推理**这些句柄、在多步之间组合、在步骤间传递。相比于藏在传输元数据中的隐藏 session，这是从暗箱到透明的转变。

**注意**：句柄需要作用域、校验和过期策略，否则只是把风险从一层挪到另一层。

### 3. MCP Apps：服务器渲染 UI

服务器可以交付交互式 HTML 界面，由宿主在 sandboxed iframe 中渲染。工具预先声明 UI 模板，宿主可以预取、缓存、安全审查。UI 操作通过同样的 JSON-RPC 协议与宿主通信，走同样的审计和同意路径。

**对 Agent 的意义**：Agent 工具不再只能是纯 JSON 交互，可以带 UI。比如搜索工具可以返回一个可视化结果界面，而不仅是文本列表。

### 4. Tasks 从核心特性降级为扩展

Tasks 曾经是核心实验特性，生产使用暴露了足够多需要重新设计的点，改为扩展更合适。新生命周期：
- 服务器从 `tools/call` 返回 task 句柄
- 客户端通过 `tasks/get`、`tasks/update`、`tasks/cancel` 驱动
- 任务创建是**服务器导向**的：客户端声明支持，服务器决定何时将调用转为任务
- `tasks/list` 被移除（无 session 后无法安全作用域隔离）

### 5. 鉴权加固

六个 SEP 对齐 OAuth 2.0 和 OpenID Connect 的实际部署模式：
- 客户端必须验证 `iss` 参数（防 mix-up 攻击）
- 桌面/CLI 客户端声明 `application_type`，避免被默认当成 web 应用
- 客户端绑定的凭证与颁发 authorization server 的 issuer 关联
- 支持 refresh token、scope 累积规则、`.well-known` 发现

### 6. 弃用与精简

| 弃用特性 | 替代方向 |
|---------|---------|
| Roots | 工具参数、resource URI、服务器配置 |
| Sampling | 直接对接 LLM provider API |
| Logging | stderr（stdio 传输）+ OpenTelemetry（结构化可观测） |

这是 MCP 在缩小职责边界。Workspace 作用域用工具输入表达更直接，可观测性交给已有工具链，模型访问交给 provider API。协议变薄，生态变厚。

---

## 其他值得注意的

- **完整 JSON Schema 2020-12 支持**：工具输入/输出可以用组合、条件和引用表达复杂结构。但需注意 schema 复杂度带来的性能和安全风险。
- **W3C Trace Context**：规范了 `traceparent`/`tracestate`/`baggage` 的键名，分布式追踪可以跨 SDK 和网关串联，接入 OpenTelemetry。
- **正式治理机制**：特性生命周期策略（Active → Deprecated → Removed，弃用到移除至少 12 个月）；扩展框架（反向 DNS 标识、独立仓库、委托维护者、独立版本）；标准轨 SEP 需要匹配的符合性测试场景才能进入 Final。
- **破坏性变更**：已有 SDK 和服务需要适配，10 周窗口期供验证。

---

## 对 ZhouXuan 工作栈的影响

1. **Agent 架构设计**：无状态 MCP 意味着远程工具服务器可以像普通微服务一样部署，这对大型 Agent 项目的架构设计有直接参考价值。
2. **MCP Apps**：Agent UI 设计多了一种范式——工具自带 UI。你的 agent-ui-design 技能可以关注这个方向。
3. **Sampling 弃用**：如果你的 Agent 系统中有 MCP 服务器通过 Sampling 请求模型补全的路径，可以考虑迁移到直接 API 调用。
4. **可观测性**：W3C Trace Context + OpenTelemetry 对齐了你之前在 Obsidian 中集成的 Langfuse 方向——Agent 调用链的端到端追踪有了标准化的协议层支持。
