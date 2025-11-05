# 📡 API 文档

TeyMCP-Server RESTful API 完整参考。

---

## 📋 目录

- [基础信息](#基础信息)
- [认证](#认证)
- [状态API](#状态api)
- [服务器管理API](#服务器管理api)
- [工具管理API](#工具管理api)
- [日志API](#日志api)
- [WebSocket API](#websocket-api)
- [错误码](#错误码)

---

## 🌐 基础信息

### Base URL
```
http://localhost:8080
```

### Content-Type
```
application/json
```

### API版本
```
v1.0.0
```

---

## 🔐 认证

### API Key认证（可选）

如果启用了认证，需要在请求头中添加：

```http
X-API-Key: your-api-key-here
```

示例：
```bash
curl -H "X-API-Key: sk-xxx" http://localhost:8080/api/status
```

---

## 📊 状态API

### 获取系统状态

获取系统整体运行状态。

**端点**: `GET /api/status`

**请求**:
```bash
curl http://localhost:8080/api/status
```

**响应**:
```json
{
  "status": "healthy",
  "uptime_seconds": 3600,
  "servers": {
    "total": 5,
    "healthy": 4,
    "unhealthy": 1
  },
  "tools": {
    "total": 42,
    "by_server": {
      "github": 15,
      "gitee": 12,
      "filesystem": 8,
      "memory": 7
    }
  },
  "metrics": {
    "total_calls": 1234,
    "success_rate": 0.98,
    "avg_response_ms": 156
  }
}
```

### 健康检查

简单的健康检查端点。

**端点**: `GET /health`

**请求**:
```bash
curl http://localhost:8080/health
```

**响应**:
```json
{
  "status": "ok",
  "timestamp": "2025-01-04T10:30:00Z"
}
```

---

## 🖥️ 服务器管理API

### 列出所有服务器

获取所有已连接的MCP服务器列表。

**端点**: `GET /api/servers`

**请求**:
```bash
curl http://localhost:8080/api/servers
```

**响应**:
```json
{
  "servers": [
    {
      "name": "github",
      "status": "connected",
      "tool_count": 15,
      "last_health_check": "2025-01-04T10:29:50Z",
      "uptime_seconds": 3580
    },
    {
      "name": "gitee",
      "status": "connected",
      "tool_count": 12,
      "last_health_check": "2025-01-04T10:29:51Z",
      "uptime_seconds": 3579
    }
  ],
  "count": 2
}
```

### 获取服务器详情

获取特定服务器的详细信息。

**端点**: `GET /api/servers/{server_name}`

**路径参数**:
- `server_name`: 服务器名称

**请求**:
```bash
curl http://localhost:8080/api/servers/github
```

**响应**:
```json
{
  "name": "github",
  "status": "connected",
  "config": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "critical": true
  },
  "tools": [
    {
      "name": "create_repository",
      "description": "Create a new GitHub repository",
      "full_name": "github.create_repository"
    }
  ],
  "metrics": {
    "total_calls": 145,
    "success_rate": 0.99,
    "avg_response_ms": 234
  }
}
```

### 添加服务器

动态添加新的MCP服务器。

**端点**: `POST /api/servers`

**请求体**:
```json
{
  "name": "custom-mcp",
  "command": "node",
  "args": ["/path/to/mcp-server.js"],
  "env": {
    "API_KEY": "xxx"
  },
  "critical": false
}
```

**请求**:
```bash
curl -X POST http://localhost:8080/api/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "custom-mcp",
    "command": "node",
    "args": ["/path/to/server.js"],
    "env": {"API_KEY": "xxx"},
    "critical": false
  }'
```

**响应**:
```json
{
  "success": true,
  "message": "服务器 custom-mcp 添加成功",
  "server": {
    "name": "custom-mcp",
    "status": "connected",
    "tool_count": 8
  }
}
```

### 删除服务器

移除MCP服务器。

**端点**: `DELETE /api/servers/{server_name}`

**请求**:
```bash
curl -X DELETE http://localhost:8080/api/servers/custom-mcp
```

**响应**:
```json
{
  "success": true,
  "message": "服务器 custom-mcp 已移除"
}
```

### 重启服务器

重启指定的MCP服务器。

**端点**: `POST /api/servers/{server_name}/restart`

**请求**:
```bash
curl -X POST http://localhost:8080/api/servers/github/restart
```

**响应**:
```json
{
  "success": true,
  "message": "服务器 github 重启成功"
}
```

---

## 🛠️ 工具管理API

### 列出所有工具

获取所有可用工具列表。

**端点**: `GET /api/tools`

**查询参数**:
- `server` (可选): 筛选特定服务器的工具
- `search` (可选): 搜索关键词

**请求**:
```bash
# 获取所有工具
curl http://localhost:8080/api/tools

# 只获取GitHub的工具
curl "http://localhost:8080/api/tools?server=github"

# 搜索工具
curl "http://localhost:8080/api/tools?search=repository"
```

**响应**:
```json
{
  "tools": [
    {
      "name": "create_repository",
      "full_name": "github.create_repository",
      "server": "github",
      "description": "Create a new GitHub repository",
      "input_schema": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "description": {"type": "string"},
          "private": {"type": "boolean"}
        },
        "required": ["name"]
      }
    }
  ],
  "count": 42
}
```

### 获取工具详情

获取特定工具的详细信息。

**端点**: `GET /api/tools/{tool_name}`

**请求**:
```bash
curl http://localhost:8080/api/tools/github.create_repository
```

**响应**:
```json
{
  "name": "create_repository",
  "full_name": "github.create_repository",
  "server": "github",
  "description": "Create a new GitHub repository",
  "input_schema": {
    "type": "object",
    "properties": {
      "name": {"type": "string", "description": "Repository name"},
      "description": {"type": "string"},
      "private": {"type": "boolean", "default": false}
    },
    "required": ["name"]
  },
  "stats": {
    "total_calls": 45,
    "success_rate": 0.98,
    "avg_response_ms": 456
  }
}
```

### 调用工具

执行工具调用。

**端点**: `POST /api/tools/{tool_name}/call`

**请求体**:
```json
{
  "arguments": {
    "name": "my-new-repo",
    "description": "A test repository",
    "private": false
  }
}
```

**请求**:
```bash
curl -X POST http://localhost:8080/api/tools/github.create_repository/call \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "name": "my-new-repo",
      "description": "Test repo",
      "private": false
    }
  }'
```

**响应**:
```json
{
  "success": true,
  "result": [
    {
      "type": "text",
      "text": "Repository created successfully: https://github.com/user/my-new-repo"
    }
  ],
  "duration_ms": 456
}
```

### 测试工具

测试工具调用（包含性能指标）。

**端点**: `POST /api/tools/{tool_name}/test`

**请求**:
```bash
curl -X POST http://localhost:8080/api/tools/github.search_repositories/test \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"query": "mcp"}}'
```

**响应**:
```json
{
  "success": true,
  "result": [...],
  "duration_ms": 234,
  "test_info": {
    "timestamp": "2025-01-04T10:30:00Z",
    "server_status": "healthy"
  }
}
```

---

## 📝 日志API

### 获取日志列表

获取工具调用日志。

**端点**: `GET /api/logs`

**查询参数**:
- `limit` (可选): 返回数量，默认100
- `offset` (可选): 偏移量，默认0
- `server` (可选): 筛选服务器
- `status` (可选): 筛选状态 (success/error)

**请求**:
```bash
# 获取最近100条日志
curl http://localhost:8080/api/logs

# 获取GitHub服务器的日志
curl "http://localhost:8080/api/logs?server=github&limit=50"

# 只获取错误日志
curl "http://localhost:8080/api/logs?status=error"
```

**响应**:
```json
{
  "logs": [
    {
      "id": "log_123",
      "tool": "github.create_repository",
      "server": "github",
      "arguments": {"name": "test-repo"},
      "status": "success",
      "duration_ms": 456,
      "timestamp": "2025-01-04T10:29:30Z"
    }
  ],
  "count": 100,
  "total": 1234
}
```

### 获取日志详情

获取特定日志的详细信息。

**端点**: `GET /api/logs/{log_id}`

**请求**:
```bash
curl http://localhost:8080/api/logs/log_123
```

**响应**:
```json
{
  "id": "log_123",
  "tool": "github.create_repository",
  "server": "github",
  "arguments": {
    "name": "test-repo",
    "private": false
  },
  "result": [
    {
      "type": "text",
      "text": "Repository created successfully"
    }
  ],
  "status": "success",
  "duration_ms": 456,
  "timestamp": "2025-01-04T10:29:30Z",
  "error": null
}
```

### 清空日志

清空所有日志记录。

**端点**: `DELETE /api/logs`

**请求**:
```bash
curl -X DELETE http://localhost:8080/api/logs
```

**响应**:
```json
{
  "success": true,
  "message": "已清空 1234 条日志"
}
```

---

## 🔄 WebSocket API

### 连接WebSocket

实时接收系统状态更新。

**端点**: `WS /ws`

**JavaScript示例**:
```javascript
const ws = new WebSocket('ws://localhost:8080/ws');

ws.onopen = () => {
  console.log('WebSocket connected');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Update:', data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('WebSocket disconnected');
};
```

**Python示例**:
```python
import asyncio
import websockets
import json

async def connect():
    uri = "ws://localhost:8080/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Update: {data}")

asyncio.run(connect())
```

**消息格式**:
```json
{
  "type": "status_update",
  "data": {
    "servers": {
      "github": "connected",
      "gitee": "connected"
    },
    "tool_count": 42,
    "timestamp": "2025-01-04T10:30:00Z"
  }
}
```

---

## ⚠️ 错误码

### HTTP状态码

| 状态码 | 含义 | 说明 |
|--------|------|------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未授权 |
| 403 | Forbidden | 禁止访问 |
| 404 | Not Found | 资源不存在 |
| 429 | Too Many Requests | 请求过多 |
| 500 | Internal Server Error | 服务器内部错误 |
| 502 | Bad Gateway | 上游服务器错误 |
| 503 | Service Unavailable | 服务不可用 |

### 错误响应格式

```json
{
  "error": {
    "code": "TOOL_NOT_FOUND",
    "message": "Tool 'invalid.tool' does not exist",
    "details": {
      "tool_name": "invalid.tool",
      "available_servers": ["github", "gitee"]
    }
  }
}
```

### 错误代码

| 错误码 | 说明 |
|--------|------|
| `TOOL_NOT_FOUND` | 工具不存在 |
| `SERVER_NOT_FOUND` | 服务器不存在 |
| `SERVER_UNAVAILABLE` | 服务器不可用 |
| `INVALID_ARGUMENTS` | 参数错误 |
| `TOOL_EXECUTION_ERROR` | 工具执行失败 |
| `AUTHENTICATION_ERROR` | 认证失败 |
| `RATE_LIMIT_EXCEEDED` | 超过速率限制 |

---

## 📚 SDK示例

### Python SDK

```python
import requests

class TeyMCPClient:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
    
    def get_status(self):
        """获取系统状态"""
        response = requests.get(f"{self.base_url}/api/status")
        return response.json()
    
    def list_tools(self):
        """列出所有工具"""
        response = requests.get(f"{self.base_url}/api/tools")
        return response.json()
    
    def call_tool(self, tool_name, arguments):
        """调用工具"""
        response = requests.post(
            f"{self.base_url}/api/tools/{tool_name}/call",
            json={"arguments": arguments}
        )
        return response.json()

# 使用示例
client = TeyMCPClient()
status = client.get_status()
print(f"系统状态: {status['status']}")

# 调用工具
result = client.call_tool(
    "github.create_repository",
    {"name": "my-repo", "private": False}
)
print(result)
```

### JavaScript SDK

```javascript
class TeyMCPClient {
  constructor(baseUrl = 'http://localhost:8080') {
    this.baseUrl = baseUrl;
  }

  async getStatus() {
    const response = await fetch(`${this.baseUrl}/api/status`);
    return await response.json();
  }

  async listTools() {
    const response = await fetch(`${this.baseUrl}/api/tools`);
    return await response.json();
  }

  async callTool(toolName, arguments) {
    const response = await fetch(
      `${this.baseUrl}/api/tools/${toolName}/call`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ arguments })
      }
    );
    return await response.json();
  }
}

// 使用示例
const client = new TeyMCPClient();

// 获取状态
const status = await client.getStatus();
console.log('系统状态:', status);

// 调用工具
const result = await client.callTool('github.create_repository', {
  name: 'my-repo',
  private: false
});
console.log(result);
```

---

## 🔍 高级用法

### 批量操作

```bash
# 批量调用工具
for repo in repo1 repo2 repo3; do
  curl -X POST http://localhost:8080/api/tools/github.create_repository/call \
    -H "Content-Type: application/json" \
    -d "{\"arguments\": {\"name\": \"$repo\"}}"
done
```

### 监控脚本

```bash
#!/bin/bash
# 监控系统状态

while true; do
  status=$(curl -s http://localhost:8080/api/status)
  health=$(echo $status | jq -r '.servers.healthy')
  total=$(echo $status | jq -r '.servers.total')
  
  echo "[$(date)] 健康服务器: $health/$total"
  
  if [ "$health" -lt "$total" ]; then
    echo "⚠️ 警告: 有服务器不健康!"
  fi
  
  sleep 30
done
```

---

## 📞 获取帮助

- [GitHub Issues](https://github.com/zf13883922290/TeyMCP-Server/issues)
- [讨论区](https://github.com/zf13883922290/TeyMCP-Server/discussions)
- [文档首页](README.md)

---

**祝你使用愉快！** 🚀
