# MCP 服务器开发指南

## 📚 概述

TeyMCP-Server 已经集成了 MCP (Model Context Protocol) SDK,您可以直接开发自己的 MCP 服务器!

## ✅ 已安装的 SDK

| SDK | 版本 | 用途 | 文档 |
|-----|------|------|------|
| **Python SDK** | 1.12.4 | 开发 Python MCP 服务器 | https://github.com/modelcontextprotocol/python-sdk |
| **TypeScript SDK** | 最新 (via npx) | 开发 TypeScript MCP 服务器 | https://github.com/modelcontextprotocol/typescript-sdk |

## 🚀 快速开始

### 方式一: Python MCP 服务器 (推荐)

#### 1. 创建服务器文件

```python
# custom_servers/my_new_server.py
from mcp.server import Server
from mcp.types import Tool, TextContent

# 创建服务器实例
server = Server("my-new-server")

@server.list_tools()
async def list_tools():
    """列出可用工具"""
    return [
        Tool(
            name="my_tool",
            description="我的自定义工具",
            inputSchema={
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "输入参数"
                    }
                },
                "required": ["input"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """执行工具"""
    if name == "my_tool":
        result = f"处理结果: {arguments.get('input', '')}"
        return [TextContent(type="text", text=result)]
    raise ValueError(f"未知工具: {name}")

# 启动服务器
if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    
    asyncio.run(main())
```

#### 2. 添加到 servers.yaml

```yaml
servers:
  my_new_server:
    server_type: stdio
    command: python
    args:
      - "custom_servers/my_new_server.py"
    enabled: true
    critical: false
    description: "我的自定义MCP服务器"
```

#### 3. 重启服务

```bash
bash service.sh restart
```

#### 4. 验证工具

```bash
curl http://localhost:1215/api/tools | jq '.tools[] | select(.server_name=="my_new_server")'
```

---

### 方式二: TypeScript MCP 服务器

#### 1. 创建 TypeScript 服务器

```bash
# 创建目录
mkdir -p custom_servers_ts/my-ts-server
cd custom_servers_ts/my-ts-server

# 初始化项目
npm init -y

# 安装依赖
npm install @modelcontextprotocol/sdk express zod
npm install -D tsx typescript @types/node @types/express
```

#### 2. 创建服务器文件 (server.ts)

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

// 创建 MCP 服务器
const server = new McpServer({
    name: 'my-ts-server',
    version: '1.0.0'
});

// 注册工具
server.registerTool(
    'my_ts_tool',
    {
        title: 'My TypeScript Tool',
        description: 'TypeScript开发的示例工具',
        inputSchema: {
            message: z.string().describe('输入消息')
        },
        outputSchema: {
            result: z.string()
        }
    },
    async ({ message }) => {
        const output = {
            result: `TS处理结果: ${message}`
        };
        return {
            content: [
                {
                    type: 'text',
                    text: JSON.stringify(output)
                }
            ],
            structuredContent: output
        };
    }
);

// 连接 stdio 传输
const transport = new StdioServerTransport();
await server.connect(transport);
```

#### 3. 添加启动脚本到 package.json

```json
{
  "name": "my-ts-server",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "tsx server.ts"
  }
}
```

#### 4. 添加到 servers.yaml

```yaml
servers:
  my_ts_server:
    server_type: stdio
    command: /home/sun/TeyMCP-Server/.local/bin/npx
    args:
      - "tsx"
      - "custom_servers_ts/my-ts-server/server.ts"
    enabled: true
    critical: false
    description: "TypeScript开发的自定义MCP服务器"
```

---

## 🛠️ 现有自定义服务器示例

您的项目中已经有几个自定义服务器可以参考:

### 1. time_server.py (完整实现)
- **位置**: `custom_servers/time_server.py`
- **工具**: 4个 (时间、时区转换、时间差、时间计算)
- **特点**: 完整的 Python MCP 服务器实现,带 pytz 依赖

```bash
# 查看代码
cat custom_servers/time_server.py
```

### 2. git_server.py (subprocess 示例)
- **位置**: `custom_servers/git_server.py`
- **工具**: 2个 (git status, git log)
- **特点**: 展示如何调用外部命令

```bash
# 查看代码
cat custom_servers/git_server.py
```

### 3. huggingface_server.py (HTTP API 示例)
- **位置**: `custom_servers/huggingface_server.py`
- **工具**: 2个 (搜索模型、搜索数据集)
- **特点**: 展示如何集成外部 API

---

## 📖 MCP 服务器核心概念

### 1. Tools (工具)
- **用途**: 让 LLM 执行操作 (计算、获取数据、副作用)
- **特点**: 模型驱动 - AI 决定何时调用
- **示例**: 计算器、数据库查询、发送消息

### 2. Resources (资源)
- **用途**: 向 LLM 暴露数据 (无副作用)
- **特点**: 应用驱动 - 客户端决定如何使用
- **示例**: 配置文件、用户资料、文档

### 3. Prompts (提示词)
- **用途**: 可重用的提示词模板
- **特点**: 用户驱动 - 可能作为斜杠命令
- **示例**: 代码审查、翻译、总结

---

## 🔧 开发工具

### 1. MCP Inspector (调试工具)
```bash
# 安装
npm install -g @modelcontextprotocol/inspector

# 测试 Python 服务器
npx @modelcontextprotocol/inspector python custom_servers/my_new_server.py

# 测试 TypeScript 服务器
npx @modelcontextprotocol/inspector npx tsx custom_servers_ts/my-ts-server/server.ts
```

### 2. 日志调试
```bash
# 查看启动日志
tail -f /tmp/teymcp_startup.log

# 查看运行日志
tail -f data/logs/teymcp.log

# 查看特定服务器日志
grep "my_new_server" data/logs/teymcp.log
```

### 3. API 测试
```bash
# 查看所有工具
curl http://localhost:1215/api/tools

# 查看特定服务器的工具
curl http://localhost:1215/api/tools | jq '.tools[] | select(.server_name=="my_new_server")'

# 调用工具 (如果API支持)
curl -X POST http://localhost:1215/api/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "server": "my_new_server",
    "tool": "my_tool",
    "arguments": {"input": "test"}
  }'
```

---

## 📚 官方文档

### Python SDK
- **GitHub**: https://github.com/modelcontextprotocol/python-sdk
- **PyPI**: https://pypi.org/project/mcp/
- **示例**: https://github.com/modelcontextprotocol/python-sdk/tree/main/examples

### TypeScript SDK
- **GitHub**: https://github.com/modelcontextprotocol/typescript-sdk
- **npm**: https://www.npmjs.com/package/@modelcontextprotocol/sdk
- **文档**: 您提供的完整 TypeScript SDK 文档

### MCP 协议规范
- **规范**: https://spec.modelcontextprotocol.io/
- **社区**: https://github.com/modelcontextprotocol

---

## 🌟 最佳实践

### 1. 命名规范
- **服务器名**: 小写下划线 (my_server)
- **工具名**: 小写下划线 (my_tool)
- **文件名**: 与服务器名一致 (my_server.py)

### 2. 错误处理
```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        # 工具逻辑
        result = process(arguments)
        return [TextContent(type="text", text=result)]
    except Exception as e:
        # 返回错误信息
        return [TextContent(type="text", text=f"错误: {str(e)}")]
```

### 3. 输入验证
```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    # 验证必需参数
    if "required_param" not in arguments:
        raise ValueError("缺少必需参数: required_param")
    
    # 验证参数类型
    if not isinstance(arguments["required_param"], str):
        raise TypeError("required_param 必须是字符串")
    
    # 执行工具逻辑
    ...
```

### 4. 异步操作
```python
import asyncio
import httpx

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "fetch_data":
        async with httpx.AsyncClient() as client:
            response = await client.get(arguments["url"])
            return [TextContent(type="text", text=response.text)]
```

### 5. 资源管理
```python
# 使用上下文管理器
async with httpx.AsyncClient() as client:
    # 自动清理资源
    response = await client.get(url)

# 或手动清理
try:
    resource = open_resource()
    # 使用资源
finally:
    close_resource(resource)
```

---

## 🔗 集成到 TeyMCP-Server

### 服务器生命周期

1. **启动阶段**
   - TeyMCP-Server 启动 (service.sh start)
   - 读取 config/servers.yaml
   - 为每个启用的服务器创建子进程

2. **连接阶段**
   - SimpleMCPAggregator 连接各服务器
   - 通过 stdio 建立 JSON-RPC 通信
   - 获取服务器能力 (capabilities)

3. **工具发现**
   - 调用 tools/list 获取工具列表
   - 缓存工具信息
   - 暴露给 API (http://localhost:1215/api/tools)

4. **运行阶段**
   - 接收工具调用请求
   - 路由到对应服务器
   - 返回执行结果

5. **关闭阶段**
   - service.sh stop
   - 发送终止信号
   - 清理子进程

### 工具调用流程

```
用户请求
  ↓
FastAPI (/api/tools/call)
  ↓
SimpleMCPAggregator
  ↓
路由到对应服务器
  ↓
MCP Server (您的自定义服务器)
  ↓
执行工具逻辑
  ↓
返回结果
  ↓
格式化响应
  ↓
返回给用户
```

---

## 🎓 学习路径

### 阶段一: 基础 (1-2天)
1. ✅ 理解 MCP 协议概念 (Tools, Resources, Prompts)
2. ✅ 阅读现有自定义服务器代码
3. 🔧 修改一个现有服务器,添加新工具
4. 🔧 测试修改后的服务器

### 阶段二: 进阶 (3-5天)
1. 🔧 创建简单的自定义服务器 (Hello World)
2. 🔧 集成外部 API (示例: 天气API)
3. 🔧 添加错误处理和输入验证
4. 🔧 编写完整的工具文档

### 阶段三: 高级 (1-2周)
1. 🔧 实现复杂的工具逻辑 (数据库、文件操作)
2. 🔧 添加 Resources 和 Prompts
3. 🔧 实现工具链 (一个工具调用另一个工具)
4. 🔧 性能优化和并发处理

---

## 🐛 常见问题

### Q1: 服务器启动失败
```bash
# 检查日志
grep "my_server" /tmp/teymcp_startup.log

# 常见原因:
# 1. Python 路径错误 - 使用完整路径
# 2. 依赖缺失 - pip install <package>
# 3. 语法错误 - python custom_servers/my_server.py 测试
```

### Q2: 工具不显示
```bash
# 检查工具列表
curl http://localhost:1215/api/tools | jq '.tools[] | select(.server_name=="my_server")'

# 常见原因:
# 1. list_tools 未正确实现
# 2. 服务器未启动成功
# 3. enabled: false 在 servers.yaml
```

### Q3: 工具调用失败
```bash
# 查看详细错误
tail -20 data/logs/teymcp.log

# 常见原因:
# 1. 参数验证失败
# 2. 未捕获的异常
# 3. 返回格式错误
```

### Q4: TypeScript 服务器找不到 module
```bash
# 确保使用 ES modules
# package.json 中添加:
{
  "type": "module"
}

# 使用 .js 后缀导入:
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
```

---

## 📝 示例项目

### 完整示例: 天气查询服务器

```python
# custom_servers/weather_server.py
from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx
import os

server = Server("weather-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_weather",
            description="获取指定城市的天气信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称 (例如: Beijing, Shanghai)"
                    }
                },
                "required": ["city"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_weather":
        city = arguments.get("city", "")
        
        # 调用天气API (示例使用 OpenWeatherMap)
        api_key = os.getenv("WEATHER_API_KEY", "demo")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                
                # 格式化结果
                weather_info = {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"]
                }
                
                result = (
                    f"🌍 {weather_info['city']} 天气\n"
                    f"🌡️ 温度: {weather_info['temperature']}°C "
                    f"(体感 {weather_info['feels_like']}°C)\n"
                    f"☁️ 天气: {weather_info['description']}\n"
                    f"💧 湿度: {weather_info['humidity']}%\n"
                    f"💨 风速: {weather_info['wind_speed']} m/s"
                )
                
                return [TextContent(type="text", text=result)]
                
        except httpx.HTTPError as e:
            return [TextContent(type="text", text=f"❌ 获取天气失败: {str(e)}")]
        except KeyError as e:
            return [TextContent(type="text", text=f"❌ 解析天气数据失败: {str(e)}")]
    
    raise ValueError(f"未知工具: {name}")

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    
    asyncio.run(main())
```

**配置环境变量** (config/app.yaml 或 .env):
```yaml
servers:
  weather_server:
    server_type: stdio
    command: python
    args:
      - "custom_servers/weather_server.py"
    enabled: true
    critical: false
    description: "天气查询服务器"
    env:
      WEATHER_API_KEY: "your_api_key_here"
```

---

## 🚀 下一步

1. **立即开始**: 复制现有的 `time_server.py`,修改为您自己的逻辑
2. **查看文档**: 阅读官方 Python SDK 文档和示例
3. **加入社区**: https://github.com/modelcontextprotocol/servers
4. **分享您的服务器**: 发布到 MCP Registry

---

## 🎉 总结

您的 TeyMCP-Server 项目**已经完全具备 MCP 开发能力**:

- ✅ Python MCP SDK 已安装 (1.12.4)
- ✅ TypeScript MCP SDK 可通过 npx 使用
- ✅ 现有 4 个自定义服务器作为参考
- ✅ 完整的测试和调试工具链
- ✅ 13 个运行中的服务器,105 个工具

**现在就可以开始开发您自己的 MCP 服务器了!** 🚀
