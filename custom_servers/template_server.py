#!/usr/bin/env python3
"""
MCP服务器开发模板
基于官方Python SDK开发的MCP服务器模板

功能:
- 完整的MCP协议实现
- 工具、资源、提示词支持
- 异步IO优化
- 错误处理和日志
- 可扩展架构

使用方式:
1. 复制此文件作为新服务器的起点
2. 修改SERVER_NAME和SERVER_VERSION
3. 添加你的工具实现
4. 在servers.yaml中配置
5. 测试和部署

官方文档: https://github.com/modelcontextprotocol/python-sdk
"""

import asyncio
import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# 添加MCP SDK路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        Tool,
        TextContent,
        ImageContent,
        EmbeddedResource,
        Prompt,
        PromptArgument,
        Resource,
        ResourceContents,
        ResourceTemplate
    )
except ImportError:
    print("❌ 错误: 需要安装 mcp 包")
    print("运行: pip install mcp")
    sys.exit(1)


# ============================================================
# 配置
# ============================================================

# 服务器信息
SERVER_NAME = "custom-template"
SERVER_VERSION = "1.0.0"
SERVER_DESCRIPTION = "自定义MCP服务器模板"

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(SERVER_NAME)


# ============================================================
# 创建MCP服务器实例
# ============================================================

server = Server(SERVER_NAME)


# ============================================================
# 1. 工具 (Tools)
# MCP的主要功能 - LLM可以调用的函数
# ============================================================

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    列出所有可用工具
    
    工具是MCP服务器的核心功能,LLM可以调用这些工具来执行任务
    """
    return [
        Tool(
            name="example_tool",
            description="示例工具 - 展示如何定义工具",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_text": {
                        "type": "string",
                        "description": "输入文本"
                    },
                    "option": {
                        "type": "string",
                        "enum": ["option1", "option2", "option3"],
                        "description": "选择选项",
                        "default": "option1"
                    }
                },
                "required": ["input_text"]
            }
        ),
        Tool(
            name="async_operation",
            description="异步操作示例 - 展示如何处理异步任务",
            inputSchema={
                "type": "object",
                "properties": {
                    "duration": {
                        "type": "integer",
                        "description": "持续时间(秒)",
                        "default": 1
                    }
                }
            }
        ),
        Tool(
            name="data_processing",
            description="数据处理示例 - 展示如何处理复杂数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "value": {"type": "number"}
                            }
                        },
                        "description": "要处理的数据"
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["sum", "average", "max", "min"],
                        "description": "操作类型"
                    }
                },
                "required": ["data", "operation"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    处理工具调用
    
    根据工具名称路由到对应的实现函数
    """
    logger.info(f"调用工具: {name}, 参数: {arguments}")
    
    try:
        if name == "example_tool":
            return await example_tool_impl(arguments)
        elif name == "async_operation":
            return await async_operation_impl(arguments)
        elif name == "data_processing":
            return await data_processing_impl(arguments)
        else:
            return [TextContent(
                type="text",
                text=f"❌ 未知工具: {name}"
            )]
            
    except Exception as e:
        logger.error(f"工具执行失败: {name}, 错误: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=f"❌ 执行失败: {str(e)}"
        )]


# ============================================================
# 工具实现
# ============================================================

async def example_tool_impl(args: dict) -> list[TextContent]:
    """示例工具实现"""
    input_text = args["input_text"]
    option = args.get("option", "option1")
    
    result = f"处理结果:\n输入: {input_text}\n选项: {option}\n时间: {datetime.now()}"
    
    return [TextContent(
        type="text",
        text=f"✅ {result}"
    )]


async def async_operation_impl(args: dict) -> list[TextContent]:
    """异步操作实现"""
    duration = args.get("duration", 1)
    
    logger.info(f"开始异步操作,持续 {duration} 秒")
    await asyncio.sleep(duration)
    logger.info("异步操作完成")
    
    return [TextContent(
        type="text",
        text=f"✅ 异步操作完成 (持续 {duration} 秒)"
    )]


async def data_processing_impl(args: dict) -> list[TextContent]:
    """数据处理实现"""
    data = args["data"]
    operation = args["operation"]
    
    values = [item["value"] for item in data]
    
    if operation == "sum":
        result = sum(values)
    elif operation == "average":
        result = sum(values) / len(values) if values else 0
    elif operation == "max":
        result = max(values) if values else 0
    elif operation == "min":
        result = min(values) if values else 0
    else:
        result = 0
    
    return [TextContent(
        type="text",
        text=f"✅ {operation.upper()} 结果: {result}\n处理数据量: {len(data)}"
    )]


# ============================================================
# 2. 资源 (Resources)
# 提供给LLM的上下文数据
# ============================================================

@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """
    列出所有可用资源
    
    资源是MCP服务器提供的数据,可以被LLM读取和使用
    """
    return [
        Resource(
            uri="example://static-data",
            name="静态数据示例",
            description="展示如何提供静态数据",
            mimeType="text/plain"
        ),
        Resource(
            uri="example://dynamic-data",
            name="动态数据示例",
            description="展示如何提供动态数据",
            mimeType="application/json"
        )
    ]


@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """
    读取资源内容
    
    根据URI返回对应的资源数据
    """
    logger.info(f"读取资源: {uri}")
    
    if uri == "example://static-data":
        return "这是静态数据示例\n可以包含任何文本内容"
    
    elif uri == "example://dynamic-data":
        data = {
            "timestamp": datetime.now().isoformat(),
            "server": SERVER_NAME,
            "version": SERVER_VERSION,
            "status": "running"
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    else:
        raise ValueError(f"未知资源: {uri}")


# ============================================================
# 3. 提示词 (Prompts)
# 预定义的提示词模板
# ============================================================

@server.list_prompts()
async def handle_list_prompts() -> list[Prompt]:
    """
    列出所有可用提示词
    
    提示词是预定义的模板,可以帮助LLM更好地完成任务
    """
    return [
        Prompt(
            name="example_prompt",
            description="示例提示词",
            arguments=[
                PromptArgument(
                    name="topic",
                    description="话题",
                    required=True
                ),
                PromptArgument(
                    name="style",
                    description="风格",
                    required=False
                )
            ]
        )
    ]


@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict | None) -> str:
    """
    获取提示词内容
    
    根据提示词名称和参数返回生成的提示词
    """
    logger.info(f"获取提示词: {name}, 参数: {arguments}")
    
    if name == "example_prompt":
        topic = arguments.get("topic", "通用话题") if arguments else "通用话题"
        style = arguments.get("style", "专业") if arguments else "专业"
        
        prompt = f"""
请以{style}的风格讨论以下话题:

话题: {topic}

要求:
1. 内容准确
2. 结构清晰
3. 语言流畅

请开始你的分析:
"""
        return prompt.strip()
    
    else:
        raise ValueError(f"未知提示词: {name}")


# ============================================================
# 4. 资源模板 (Resource Templates)
# 动态资源的模板
# ============================================================

@server.list_resource_templates()
async def handle_list_resource_templates() -> list[ResourceTemplate]:
    """
    列出所有资源模板
    
    资源模板允许动态生成资源URI
    """
    return [
        ResourceTemplate(
            uriTemplate="example://data/{id}",
            name="动态数据模板",
            description="根据ID获取数据",
            mimeType="application/json"
        )
    ]


# ============================================================
# 主函数
# ============================================================

async def main():
    """
    启动MCP服务器
    
    使用stdio transport与客户端通信
    """
    logger.info(f"启动 {SERVER_NAME} v{SERVER_VERSION}")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=SERVER_NAME,
                server_version=SERVER_VERSION,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


# ============================================================
# 入口点
# ============================================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("服务器被用户中断")
    except Exception as e:
        logger.error(f"服务器错误: {e}", exc_info=True)
        sys.exit(1)


# ============================================================
# 📚 开发指南
# ============================================================

"""
## 如何使用此模板

### 1. 创建新的MCP服务器

```bash
# 复制模板
cp template_server.py my_server.py

# 编辑配置
nano my_server.py
# 修改 SERVER_NAME, SERVER_VERSION, SERVER_DESCRIPTION
```

### 2. 添加工具

在 `handle_list_tools()` 中添加新工具:

```python
Tool(
    name="my_tool",
    description="我的工具描述",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "参数1"},
            "param2": {"type": "integer", "description": "参数2"}
        },
        "required": ["param1"]
    }
)
```

在 `handle_call_tool()` 中添加路由:

```python
elif name == "my_tool":
    return await my_tool_impl(arguments)
```

实现工具函数:

```python
async def my_tool_impl(args: dict) -> list[TextContent]:
    # 你的实现
    return [TextContent(type="text", text="结果")]
```

### 3. 添加资源

在 `handle_list_resources()` 中添加:

```python
Resource(
    uri="my://resource",
    name="我的资源",
    description="资源描述",
    mimeType="text/plain"
)
```

在 `handle_read_resource()` 中处理:

```python
if uri == "my://resource":
    return "资源内容"
```

### 4. 配置服务器

在 `servers.yaml` 中添加:

```yaml
my_server:
  server_type: stdio
  command: python
  args:
    - "/path/to/my_server.py"
  env:
    API_KEY: ${MY_API_KEY}
  enabled: true
```

### 5. 测试

```bash
# 使用MCP Inspector测试
npx @modelcontextprotocol/inspector python my_server.py

# 在TeyMCP-Server中测试
python src/main.py
```

## 最佳实践

1. **错误处理**: 总是使用try-except包裹工具实现
2. **日志记录**: 使用logger记录关键操作
3. **异步IO**: 对IO操作使用async/await
4. **输入验证**: 验证工具参数的有效性
5. **文档**: 为每个工具添加清晰的描述

## 常见问题

Q: 如何添加环境变量?
A: 使用 `os.getenv("VAR_NAME")` 读取环境变量

Q: 如何返回图片?
A: 使用 ImageContent 类型

Q: 如何处理大文件?
A: 使用流式处理,避免一次性加载到内存

## 更多资源

- Python SDK文档: https://github.com/modelcontextprotocol/python-sdk
- MCP协议: https://modelcontextprotocol.io
- 示例服务器: https://github.com/modelcontextprotocol/servers
"""
