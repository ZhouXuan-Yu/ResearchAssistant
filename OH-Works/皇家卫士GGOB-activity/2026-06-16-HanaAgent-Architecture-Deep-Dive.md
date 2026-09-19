# HanaAgent 架构深度解析

## 核心架构洞察

基于代码结构图的分析，HanaAgent采用了**四层分离架构**：

1. **Desktop层** (Electron主进程)
   - 负责窗口管理、文件监听、IPC通信
   - 通过`bootstrap.cjs`管理服务器生命周期
   - 使用`file-watch-*.cjs`实现实时文件变更监听

2. **Server层** (Hono HTTP + WebSocket)
   - 独立Node.js进程，解耦前后端
   - REST API + WebSocket双协议支持
   - 通过`ws-protocol.ts`定义完整的WebSocket通信协议

3. **Core层** (引擎编排)
   - Facade模式：`engine.ts`统一暴露所有Manager
   - 关键Manager：AgentManager、ModelManager、SessionManager、ChannelManager
   - 安全边界：`execution-boundary.ts`实现四级访问控制

4. **Hub层** (后台调度)
   - 心跳巡检：`scheduler.ts`实现定时任务
   - 事件总线：`event-bus.ts`解耦组件通信
   - 频道路由：`channel-router.ts`处理消息分发

## 关键设计模式

### 1. 双进程架构
```
Electron Main Process → spawn → Server Process (Node.js)
         ↓                           ↓
      IPC通信 ←─── WebSocket ───→ REST API
```
这种设计实现了：
- 前后端完全解耦
- 服务器可独立重启/更新
- 更好的错误隔离

### 2. Facade + Manager模式
```typescript
// core/engine.ts 作为统一入口
class Engine {
  agentManager: AgentManager
  modelManager: ModelManager
  sessionManager: SessionManager
  // ...其他Manager
}
```
优点：
- 简化上层调用
- 便于单元测试
- 支持热插拔Manager

### 3. 事件驱动架构
Hub层的EventBus实现了：
- Agent间通信
- 频道消息广播
- DM路由
- 后台任务调度

### 4. 插件约定优先
插件通过目录结构贡献功能：
```
plugins/
  ├── beautify/     # Markdown美化
  ├── image-gen/    # 图片生成
  ├── mcp/          # MCP协议
  └── office/       # Office文档
```
每个插件可包含：
- 工具定义 (tools/)
- 技能 (skills/)
- 命令 (commands/)
- 路由 (routes/)

## 数据流优化

### 1. 流式渲染
```
用户输入 → React组件 → WebSocket → Server → Core → LLM API
    ↓                                           ↓
  流式输出 ←─── WebSocket ←─── 流式响应 ←─── 流式处理
```

### 2. SessionFile统一身份
跨平台文件引用机制：
- 桌面端：本地文件路径
- Bridge：远程文件引用
- Mobile PWA：云端文件标识

### 3. 双层沙盒安全
```
应用层：PathGuard (四级访问控制)
    ↓
操作系统层：macOS Seatbelt / Linux Bubblewrap / Windows Restricted Token
```

## 性能优化点

1. **连接池管理**
   - WebSocket连接复用
   - HTTP/2多路复用
   - 数据库连接池 (better-sqlite3 WAL模式)

2. **缓存策略**
   - 模型响应缓存
   - 文件内容缓存
   - 技能元数据缓存

3. **异步处理**
   - 后台任务队列
   - 延迟结果处理 (`deferred-result-*.ts`)
   - 流式处理避免阻塞

## 扩展性设计

### 1. 水平扩展
- Server层可部署多个实例
- 通过EventBus实现分布式通信
- 数据库支持读写分离

### 2. 垂直扩展
- 插件系统支持功能热插拔
- 技能系统支持动态加载
- 模型提供商支持多API适配

### 3. 协议扩展
- WebSocket协议版本管理
- REST API版本控制
- Bridge协议适配器

## 安全机制

1. **认证授权**
   - 设备注册 (`device-registry.ts`)
   - 用户账户管理 (`local-user-account.ts`)
   - 能力策略 (`capability-policy.ts`)

2. **数据保护**
   - 消息消毒 (`message-sanitizer.ts`)
   - 执行租约 (`execution-lease-*.ts`)
   - 授权注册表 (`grant-registry.ts`)

3. **审计日志**
   - 调试日志 (`debug-log.ts`)
   - 检查点 (`checkpoint-*.ts`)
   - 事件追踪

## 部署架构建议

### 开发环境
```bash
# 启动开发服务器
npm run dev

# 单独启动Server
npm run dev:server

# 单独启动Desktop
npm run dev:desktop
```

### 生产环境
```bash
# 构建所有组件
npm run build

# 启动生产服务器
npm run start:prod

# 启动Desktop应用
npm run start:desktop
```

### Docker部署
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY dist/ ./dist/
EXPOSE 3000
CMD ["node", "dist/server/index.js"]
```

## 监控与运维

1. **健康检查**
   - 服务器状态端点
   - 数据库连接检查
   - 外部API可用性检查

2. **性能指标**
   - 请求延迟
   - 内存使用
   - 并发连接数

3. **日志管理**
   - 结构化日志
   - 日志轮转
   - 错误报警

## 未来演进方向

1. **微服务化**
   - 将Core层拆分为独立服务
   - 使用消息队列解耦
   - 容器化部署

2. **云原生支持**
   - Kubernetes部署
   - 服务网格集成
   - 自动扩缩容

3. **AI增强**
   - 智能缓存策略
   - 预测性资源分配
   - 自适应负载均衡

---

*此分析基于2026-06-16的代码结构图，反映当前架构状态。*
