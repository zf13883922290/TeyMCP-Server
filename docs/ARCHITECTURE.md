# TeyMCP-Server 架构设计

## 项目定位

**TeyMCP-Server** 是一个 MCP 聚合器(MCP Aggregator),用于统一管理和聚合多个上游 MCP 服务器。

### 与单个 MCP 服务器的区别

```
单个 MCP 服务器架构:
┌─────────────┐
│ MCP Client  │ (Claude Desktop, Cursor, etc.)
│ (Claude等)  │
└──────┬──────┘
       │ MCP Protocol
       ▼
┌─────────────┐
│ MCP Server  │ (提供特定功能的工具)
│ (天气服务器) │
└─────────────┘

TeyMCP-Server 聚合器架构:
┌─────────────┐
│ MCP Client  │ (Claude Desktop, Cursor, etc.)
│ (Claude等)  │
└──────┬──────┘
       │ MCP Protocol
       ▼
┌──────────────────────────────────┐
│     TeyMCP-Server (聚合器)        │
│  - 统一的 MCP 接口                │
│  - 工具注册和路由                 │
│  - 请求转发和响应聚合              │
└──────┬───────────────────────┬──┘
       │                       │
       ▼                       ▼
┌─────────────┐         ┌─────────────┐
│ MCP Server 1│         │ MCP Server 2│
│  (GitHub)   │         │  (filesystem)│
└─────────────┘         └─────────────┘
       │                       │
       ▼                       ▼
┌─────────────┐         ┌─────────────┐
│ MCP Server 3│         │ MCP Server 4│
│  (memory)   │         │  (brave搜索) │
└─────────────┘         └─────────────┘
```

## 核心组件

### 1. SimpleMCPAggregator (src/core/simple_aggregator.py)

**职责**: 核心聚合器,管理所有上游 MCP 服务器连接

**支持的连接类型**:
- **STDIO**: 通过标准输入/输出与本地 MCP 服务器通信
- **HTTP/SSE**: 通过 HTTP 端点与远程 MCP 服务器通信

**主要方法**:
```python
# 添加 STDIO 方式的 MCP 服务器
await aggregator.add_server(
    name="github",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={"GITHUB_TOKEN": "..."}
)

# 添加 HTTP 方式的 MCP 服务器
await aggregator.add_http_server(
    name="remote_service",
    url="https://api.example.com/mcp",
    headers={"Authorization": "Bearer token"}
)
```

### 2. HTTPMCPClient (src/core/http_client.py)

**职责**: HTTP/SSE 方式的 MCP 客户端实现

**功能**:
- 支持 Bearer Token 认证
- 实现完整的 MCP 协议方法(initialize, list_tools, call_tool)
- SSE 事件流支持
- 请求超时控制

### 3. SimpleMCPClient (src/core/simple_aggregator.py)

**职责**: STDIO 方式的 MCP 客户端实现

**功能**:
- 管理子进程生命周期
- 处理 JSON-RPC 消息
- 错误恢复机制

### 4. FastAPI Web Server (src/main.py)

**职责**: 提供 REST API 和管理界面

**端点**:
- `/api/tools` - 查询所有可用工具
- `/api/call` - 调用特定工具
- `/api/servers` - 查询服务器状态
- `/dashboard` - Web 管理界面
- `/ws` - WebSocket 实时通信

## MCP 服务器类型

### STDIO 服务器(推荐)

大多数 MCP 服务器使用 STDIO 方式,这是 MCP 的标准实现方式。

**特点**:
- ✅ 本地运行,安全可控
- ✅ 官方 SDK 支持完善
- ✅ 大多数开源 MCP 服务器采用此方式
- ❌ 不支持日志输出到 stdout(会破坏 JSON-RPC 消息)
- ❌ 需要本地安装依赖

**配置示例**:
```yaml
github:
  command: npx
  args:
    - "-y"
    - "@modelcontextprotocol/server-github"
  env:
    GITHUB_PERSONAL_ACCESS_TOKEN: ${GITHUB_TOKEN}
  enabled: true
```

**日志注意事项**:
```python
# ❌ 错误: STDIO 服务器不能使用 print()
print("Processing request")

# ✅ 正确: 使用 logging 输出到 stderr
import logging
logging.info("Processing request")
```

### HTTP/SSE 服务器

少数 MCP 服务器提供 HTTP/SSE 端点,适用于远程托管的服务。

**特点**:
- ✅ 可远程访问
- ✅ 无需本地安装
- ✅ 支持标准日志输出
- ❌ 需要网络连接
- ❌ 安全性依赖于认证机制
- ❌ 较少的开源实现

**配置示例**:
```yaml
backdocket:
  type: http
  url: https://ai.backdocket.com/mcp
  headers:
    Authorization: "Bearer ${BACKDOCKET_TOKEN}"
  enabled: true
```

## 配置文件结构

### servers.yaml

```yaml
servers:
  # STDIO 类型服务器
  github:
    command: npx                    # 执行命令
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:                            # 环境变量
      GITHUB_TOKEN: ${GITHUB_TOKEN}
    working_dir: /path/to/dir       # 可选: 工作目录
    enabled: true                   # 是否启用
    critical: false                 # 是否关键(失败时是否阻止启动)
    description: "GitHub MCP服务器"
  
  # HTTP 类型服务器
  remote_service:
    type: http                      # 指定类型为 http
    url: https://api.example.com/mcp
    headers:                        # HTTP 请求头
      Authorization: "Bearer token"
    timeout: 30.0                   # 请求超时(秒)
    enabled: true
```

### .env

```bash
# GitHub Token
GITHUB_TOKEN=ghp_xxxxx

# HuggingFace Token
HUGGINGFACE_TOKEN=hf_xxxxx

# 其他服务的 Token
BRAVE_API_KEY=xxxxx
```

## 添加新的 MCP 服务器

### 方式 1: 添加 STDIO 服务器(推荐)

1. **查找服务器包名**:
   - 官方服务器: https://github.com/modelcontextprotocol/servers
   - 社区服务器: https://github.com/punkpeye/awesome-mcp-servers

2. **安装依赖** (如果需要):
```bash
# TypeScript/Node.js 服务器
npm install -g @modelcontextprotocol/server-github

# Python 服务器  
pip install mcp-server-git
```

3. **配置 servers.yaml**:
```yaml
new_server:
  command: npx  # 或 python, uvx 等
  args:
    - "-y"
    - "@modelcontextprotocol/server-name"
  env:
    API_KEY: ${API_KEY}
  enabled: true
  description: "服务器描述"
```

4. **重启 TeyMCP-Server**

### 方式 2: 添加 HTTP 服务器

1. **获取 API 端点和认证信息**

2. **配置 servers.yaml**:
```yaml
http_server:
  type: http
  url: https://api.service.com/mcp
  headers:
    Authorization: "Bearer ${TOKEN}"
  enabled: true
```

3. **重启 TeyMCP-Server**

## 安全性考虑

### STDIO 服务器

- ✅ 运行在本地,相对安全
- ⚠️ 需要信任执行的代码
- ⚠️ 注意环境变量泄露(使用 .env 文件)

### HTTP 服务器

- ✅ 使用 HTTPS 加密传输
- ⚠️ Token 需要妥善保管
- ⚠️ 注意速率限制和配额

### 容器化部署(推荐)

为了更好的隔离和安全性,建议使用 Docker 容器:

```yaml
version: '3.8'
services:
  teymcp-server:
    build: .
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    volumes:
      - ./config:/app/config:ro
      - ./data:/app/data
    ports:
      - "8080:8080"
```

## 工具路由机制

```python
# 客户端调用
POST /api/call
{
  "tool": "github_create_issue",
  "arguments": {...}
}

# TeyMCP-Server 处理流程
1. 解析工具名称 "github_create_issue"
2. 查找工具注册表,找到对应的上游服务器 "github"
3. 转发请求到 github MCP 服务器
4. 接收响应
5. 返回给客户端
```

## 扩展性

### 自定义 MCP 服务器

您可以创建自己的 MCP 服务器并集成到 TeyMCP-Server:

1. **使用 FastMCP 创建服务器**:
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-custom-server")

@mcp.tool()
async def my_tool(arg1: str, arg2: int) -> str:
    """工具描述"""
    return f"Result: {arg1} - {arg2}"

if __name__ == "__main__":
    mcp.run(transport='stdio')
```

2. **配置到 TeyMCP-Server**:
```yaml
my_custom:
  command: python
  args:
    - "/path/to/my_server.py"
  enabled: true
```

## 监控和调试

### 日志位置

- **主日志**: `data/logs/teymcp.log`
- **访问日志**: `data/logs/access.log`
- **各服务器日志**: `data/logs/servers/{server_name}.log`

### 调试工具

```bash
# 查看所有可用工具
curl http://localhost:8080/api/tools

# 查看服务器状态
curl http://localhost:8080/api/servers

# 测试工具调用
curl -X POST http://localhost:8080/api/call \
  -H "Content-Type: application/json" \
  -d '{"tool": "tool_name", "arguments": {}}'
```

### MCP Inspector

官方提供了 MCP Inspector 用于调试:

```bash
npx @modelcontextprotocol/inspector npx -y @modelcontextprotocol/server-name
```

## 性能优化

1. **并发连接**: SimpleMCPAggregator 支持并发连接多个服务器
2. **连接池**: HTTP 客户端使用连接池
3. **缓存**: 工具列表和服务器状态缓存
4. **异步处理**: 所有 I/O 操作都是异步的

## 未来计划

- [ ] 支持工具组合和链式调用
- [ ] 添加工具调用历史和统计
- [ ] 支持动态添加/删除服务器(无需重启)
- [ ] 添加 Rate Limiting 和配额管理
- [ ] 支持多租户和权限控制
- [ ] 提供 Prometheus metrics
- [ ] 支持更多传输协议(gRPC, WebSocket)

## 参考资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [构建 MCP 服务器](https://modelcontextprotocol.io/docs/develop/build-server)
- [MCP 服务器列表](https://github.com/modelcontextprotocol/servers)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)
