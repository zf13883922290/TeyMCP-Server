#!/usr/bin/env python3
"""
示例 MCP 服务器 - Hello World
展示最简单的 MCP 服务器实现

这个服务器提供 3 个工具:
1. hello - 简单的问候
2. echo - 回显输入
3. calculate - 简单计算器
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
import json

# 创建 MCP 服务器实例
server = Server("example-hello-server")

@server.list_tools()
async def list_tools():
    """列出所有可用工具"""
    return [
        Tool(
            name="hello",
            description="返回友好的问候语",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "要问候的名字"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="echo",
            description="回显输入的消息",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "要回显的消息"
                    }
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="calculate",
            description="执行简单的数学计算",
            inputSchema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "运算类型: add(加), subtract(减), multiply(乘), divide(除)"
                    },
                    "a": {
                        "type": "number",
                        "description": "第一个数字"
                    },
                    "b": {
                        "type": "number",
                        "description": "第二个数字"
                    }
                },
                "required": ["operation", "a", "b"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """执行工具调用"""
    
    # 工具 1: hello - 问候
    if name == "hello":
        user_name = arguments.get("name", "World")
        result = f"👋 你好, {user_name}! 欢迎使用 MCP 服务器!"
        return [TextContent(type="text", text=result)]
    
    # 工具 2: echo - 回显
    elif name == "echo":
        message = arguments.get("message", "")
        result = f"📢 回显: {message}"
        return [TextContent(type="text", text=result)]
    
    # 工具 3: calculate - 计算
    elif name == "calculate":
        try:
            operation = arguments.get("operation")
            a = float(arguments.get("a", 0))
            b = float(arguments.get("b", 0))
            
            if operation == "add":
                result = a + b
                symbol = "+"
            elif operation == "subtract":
                result = a - b
                symbol = "-"
            elif operation == "multiply":
                result = a * b
                symbol = "×"
            elif operation == "divide":
                if b == 0:
                    return [TextContent(
                        type="text",
                        text="❌ 错误: 除数不能为零"
                    )]
                result = a / b
                symbol = "÷"
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ 错误: 未知运算类型 '{operation}'"
                )]
            
            response = f"🔢 计算结果: {a} {symbol} {b} = {result}"
            return [TextContent(type="text", text=response)]
            
        except (ValueError, TypeError) as e:
            return [TextContent(
                type="text",
                text=f"❌ 错误: 参数类型错误 - {str(e)}"
            )]
    
    # 未知工具
    else:
        raise ValueError(f"未知工具: {name}")

# 启动服务器
if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        """主函数 - 启动 stdio 传输"""
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    
    # 运行服务器
    asyncio.run(main())
