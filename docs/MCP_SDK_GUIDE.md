# 🌐 MCP完整生态系统集成指南

Model Context Protocol (MCP) 官方SDK、服务器和开发指南

---

## 📋 目录

- [MCP协议概述](#mcp协议概述)
- [官方SDK](#官方sdk)
- [TeyMCP-Server兼容性](#teymcp-server兼容性)
- [服务器集成](#服务器集成)
- [开发新服务器](#开发新服务器)
- [社区资源](#社区资源)

---

## 🎯 MCP协议概述

### 什么是MCP?

**Model Context Protocol (MCP)** 是一个开放协议,实现LLM应用与外部数据源、工具的无缝集成。

### 核心仓库

1. **协议规范**: https://github.com/modelcontextprotocol/modelcontextprotocol
   - MCP协议的完整规范
   - 设计文档和RFC
   - 不需要直接使用,SDK已实现

2. **官方服务器集合**: https://github.com/modelcontextprotocol/servers
   - 40+个官方和社区MCP服务器
   - 参考实现和最佳实践
   - 定期更新

3. **MCP Registry**: https://github.com/modelcontextprotocol/registry
   - 社区驱动的MCP服务器注册中心
   - 类似应用商店
   - API: https://registry.modelcontextprotocol.io

---

## 🛠️ 官方SDK

### 1. Python SDK ✅ (TeyMCP-Server使用)

**仓库**: https://github.com/modelcontextprotocol/python-sdk

**安装**:
```bash
pip install mcp
```

**特性**:
- ✅ 完整的MCP协议实现
- ✅ stdio和HTTP transport
- ✅ 异步IO支持
- ✅ 类型提示
- ✅ 完整文档

**使用示例**:
```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("my-server")

@server.list_tools()
async def list_tools():
    return [...]

@server.call_tool()
async def call_tool(name, arguments):
    return [...]

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, ...)

asyncio.run(main())
```

**兼容性**: ✅ 完全兼容TeyMCP-Server

---

### 2. TypeScript SDK

**仓库**: https://github.com/modelcontextprotocol/typescript-sdk

**安装**:
```bash
npm install @modelcontextprotocol/sdk
```

**特性**:
- ✅ TypeScript类型安全
- ✅ stdio和HTTP transport
- ✅ Node.js和浏览器支持
- ✅ 完整文档

**使用示例**:
```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server({
  name: 'my-server',
  version: '1.0.0'
});

server.setRequestHandler('tools/list', async () => ({
  tools: [...]
}));

const transport = new StdioServerTransport();
await server.connect(transport);
```

**兼容性**: ✅ 通过npx调用的MCP服务器都使用此SDK

---

### 3. C# SDK (Microsoft维护)

**仓库**: https://github.com/modelcontextprotocol/csharp-sdk

**安装**:
```bash
dotnet add package ModelContextProtocol.SDK
```

**特性**:
- ✅ .NET 6+支持
- ✅ 异步/等待模式
- ✅ Microsoft官方维护

**兼容性**: ⚠️ 需要.NET运行时,TeyMCP-Server可通过进程调用

---

### 4. Kotlin SDK (JetBrains维护)

**仓库**: https://github.com/modelcontextprotocol/kotlin-sdk

**安装**:
```kotlin
implementation("com.anthropic:mcp-kotlin-sdk:1.0.0")
```

**特性**:
- ✅ Kotlin协程支持
- ✅ JetBrains官方维护
- ✅ Android兼容

**兼容性**: ⚠️ 需要JVM,TeyMCP-Server可通过进程调用

---

### 5. Go SDK (Google维护)

**仓库**: https://github.com/modelcontextprotocol/go-sdk

**安装**:
```bash
go get github.com/modelcontextprotocol/go-sdk
```

**特性**:
- ✅ Go原生实现
- ✅ 高性能
- ✅ Google官方维护

**兼容性**: ✅ 可编译为独立二进制,TeyMCP-Server可直接调用

---

### 6. PHP SDK

**仓库**: https://github.com/modelcontextprotocol/php-sdk

**安装**:
```bash
composer require modelcontextprotocol/php-sdk
```

**兼容性**: ⚠️ 需要PHP运行时

---

### 7. Java SDK

**仓库**: https://github.com/modelcontextprotocol/java-sdk

**安装**:
```xml
<dependency>
    <groupId>com.anthropic</groupId>
    <artifactId>mcp-java-sdk</artifactId>
    <version>1.0.0</version>
</dependency>
```

**兼容性**: ⚠️ 需要JVM

---

### 8. Swift SDK

**仓库**: https://github.com/modelcontextprotocol/swift-sdk

**特性**:
- ✅ Swift原生实现
- ✅ iOS/macOS支持

**兼容性**: ⚠️ 仅适用于Apple平台

---

### 9. Ruby SDK (Shopify维护)

**仓库**: https://github.com/modelcontextprotocol/ruby-sdk

**安装**:
```bash
gem install mcp
```

**兼容性**: ⚠️ 需要Ruby运行时

---

## ✅ TeyMCP-Server兼容性

### 完全兼容的SDK

1. **Python SDK** ✅
   - TeyMCP-Server核心使用
   - 自定义服务器开发首选
   - 零配置集成

2. **TypeScript SDK** ✅
   - 通过npx调用npm包
   - 所有官方和社区MCP服务器
   - 自动下载和运行

3. **Go SDK** ✅
   - 编译为独立二进制
   - 通过命令行调用
   - 高性能

### 需要包装的SDK

其他SDK (C#, Kotlin, PHP, Java等) 需要通过以下方式使用:

```yaml
# 示例: C# MCP服务器
csharp_server:
  server_type: stdio
  command: dotnet
  args:
    - "run"
    - "--project"
    - "/path/to/server.csproj"
  enabled: true
```

### 兼容性矩阵

| SDK | 直接兼容 | 需要运行时 | 推荐度 |
|-----|---------|-----------|-------|
| Python | ✅ | ❌ | ⭐⭐⭐⭐⭐ |
| TypeScript | ✅ | Node.js | ⭐⭐⭐⭐⭐ |
| Go | ✅ | ❌ | ⭐⭐⭐⭐ |
| C# | ⚠️ | .NET | ⭐⭐⭐ |
| Kotlin | ⚠️ | JVM | ⭐⭐⭐ |
| Java | ⚠️ | JVM | ⭐⭐⭐ |
| PHP | ⚠️ | PHP | ⭐⭐ |
| Swift | ⚠️ | macOS/iOS | ⭐⭐ |
| Ruby | ⚠️ | Ruby | ⭐⭐ |

---

## 🔧 服务器集成

### 集成方式对比

#### 方式1: npm包 (推荐) ⭐⭐⭐⭐⭐

```yaml
github:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@modelcontextprotocol/server-github"
  env:
    GITHUB_TOKEN: ${GITHUB_TOKEN}
  enabled: true
```

**优点**:
- ✅ 自动下载
- ✅ 版本管理
- ✅ 无需安装
- ✅ 社区丰富

**适用**:
- 所有TypeScript/JavaScript MCP服务器
- 官方服务器
- 大部分社区服务器

---

#### 方式2: Python脚本 ⭐⭐⭐⭐⭐

```yaml
my_server:
  server_type: stdio
  command: python
  args:
    - "/path/to/server.py"
  enabled: true
```

**优点**:
- ✅ 完全控制
- ✅ 易于开发
- ✅ 无额外依赖

**适用**:
- 自定义MCP服务器
- 内部工具
- 快速原型

---

#### 方式3: 独立二进制 ⭐⭐⭐⭐

```yaml
go_server:
  server_type: stdio
  command: /path/to/server
  args: []
  enabled: true
```

**优点**:
- ✅ 高性能
- ✅ 零依赖
- ✅ 易分发

**适用**:
- Go编译的服务器
- 性能关键场景

---

#### 方式4: Docker容器 ⭐⭐⭐

```yaml
docker_server:
  server_type: stdio
  command: docker
  args:
    - "run"
    - "-i"
    - "--rm"
    - "my-mcp-server"
  enabled: true
```

**优点**:
- ✅ 隔离环境
- ✅ 依赖封装

**缺点**:
- ⚠️ 需要Docker
- ⚠️ 性能开销

---

### 40+个可用MCP服务器

已在 `servers_ecosystem.yaml` 中配置:

**官方参考** (7个):
- everything, fetch, filesystem, git, memory, sequential_thinking, time

**官方集成** (10+个):
- GitHub, GitLab, Sentry, Slack, Microsoft (Azure, M365等)

**社区服务器** (20+个):
- Gitee, HuggingFace, Puppeteer, Playwright, Notion, Figma等

**自定义服务器** (3个):
- automation_server, media_server, template_server

---

## 🚀 开发新服务器

### 使用Python SDK (推荐)

#### 1. 从模板开始

```bash
cp template_server.py my_server.py
```

#### 2. 修改配置

```python
SERVER_NAME = "my-server"
SERVER_VERSION = "1.0.0"
SERVER_DESCRIPTION = "我的MCP服务器"
```

#### 3. 添加工具

```python
@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="my_tool",
            description="我的工具",
            inputSchema={...}
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    if name == "my_tool":
        return await my_tool_impl(arguments)
```

#### 4. 测试

```bash
# 使用MCP Inspector
npx @modelcontextprotocol/inspector python my_server.py

# 在TeyMCP-Server中
python src/main.py
```

#### 5. 发布

```bash
# 发布到npm (TypeScript)
npm publish

# 发布到PyPI (Python)
python -m build
twine upload dist/*

# 或提交到MCP Registry
# https://github.com/modelcontextprotocol/registry
```

---

### 使用TypeScript SDK

#### 1. 初始化项目

```bash
npm init -y
npm install @modelcontextprotocol/sdk
npm install -D typescript @types/node
```

#### 2. 创建服务器

```typescript
// server.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server({
  name: 'my-server',
  version: '1.0.0'
});

// 添加工具
server.setRequestHandler('tools/list', async () => ({
  tools: [{
    name: 'my_tool',
    description: 'My tool',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  }]
}));

// 启动
const transport = new StdioServerTransport();
await server.connect(transport);
```

#### 3. 编译和运行

```bash
tsc
node dist/server.js
```

---

## 📚 社区资源

### 官方资源

- **官方网站**: https://modelcontextprotocol.io
- **文档**: https://modelcontextprotocol.io/docs
- **GitHub组织**: https://github.com/modelcontextprotocol
- **Discord**: https://discord.gg/modelcontextprotocol

### 社区资源

- **Awesome MCP Servers**: https://github.com/wong2/awesome-mcp-servers
  - 精选的MCP服务器列表
  - 300+社区服务器
  - 按类别分类

- **MCP Registry**: https://registry.modelcontextprotocol.io
  - 官方服务器注册中心
  - API访问
  - 版本管理

### 开发工具

- **MCP Inspector**: 交互式MCP服务器调试工具
  ```bash
  npx @modelcontextprotocol/inspector python server.py
  ```

- **MCP Publisher**: 发布MCP服务器到Registry
  ```bash
  npx @modelcontextprotocol/publisher
  ```

---

## 🔐 最佳实践

### 安全

1. **API密钥管理**:
   - 使用环境变量
   - 不要硬编码密钥
   - 定期轮换

2. **输入验证**:
   - 验证所有用户输入
   - 使用类型检查
   - 防止注入攻击

3. **权限控制**:
   - 最小权限原则
   - 文件系统访问控制
   - 网络访问限制

### 性能

1. **异步IO**:
   - 使用async/await
   - 避免阻塞操作
   - 并发请求处理

2. **资源管理**:
   - 及时释放资源
   - 限制内存使用
   - 连接池复用

3. **错误处理**:
   - 完整的错误捕获
   - 有意义的错误消息
   - 日志记录

### 文档

1. **工具描述**:
   - 清晰的功能说明
   - 参数详细描述
   - 使用示例

2. **README**:
   - 安装说明
   - 配置指南
   - API文档

3. **变更日志**:
   - 版本历史
   - 破坏性更改
   - 迁移指南

---

## ❓ 常见问题

### Q1: 为什么TeyMCP-Server选择Python SDK?

**A**: Python SDK提供:
- 成熟稳定
- 完整文档
- 易于开发
- 丰富生态

### Q2: 可以混用多种SDK吗?

**A**: 可以! TeyMCP-Server支持:
- Python脚本 (Python SDK)
- npm包 (TypeScript SDK)
- 独立二进制 (Go SDK等)

### Q3: 如何选择SDK?

**推荐顺序**:
1. Python SDK - 自定义服务器首选
2. TypeScript SDK - 使用npm包
3. Go SDK - 高性能需求
4. 其他SDK - 特定场景

### Q4: 所有MCP服务器都兼容吗?

**A**: 只要使用stdio transport,就兼容TeyMCP-Server。HTTP transport需要额外配置。

### Q5: 如何贡献到社区?

1. 开发新的MCP服务器
2. 提交到GitHub
3. 发布到npm/PyPI
4. 提交到MCP Registry
5. 分享使用经验

---

## 📊 统计数据

- **官方SDK**: 9个 (Python, TS, C#, Kotlin, Go, PHP, Java, Swift, Ruby)
- **官方服务器**: 40+个
- **社区服务器**: 300+个
- **支持语言**: 所有主流编程语言
- **活跃开发者**: 1000+

---

## 🎯 下一步

1. ✅ 安装 `servers_ecosystem.yaml`
2. ✅ 配置需要的API密钥
3. ✅ 启用想要的MCP服务器
4. ✅ 使用 `template_server.py` 开发自定义服务器
5. ✅ 探索社区MCP服务器
6. ✅ 贡献你的MCP服务器

---

**祝你在MCP生态系统中开发愉快！** 🚀
