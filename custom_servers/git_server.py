#!/usr/bin/env python3
"""Git MCP Server - 基础Git操作 (使用github服务器代替)"""
import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent
import subprocess

app = Server("git")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="git_status", description="查看Git状态", inputSchema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}),
        Tool(name="git_log", description="查看Git日志", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "limit": {"type": "number", "default": 10}}, "required": ["path"]})
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    path = arguments.get("path", ".")
    if name == "git_status":
        try:
            result = subprocess.run(["git", "-C", path, "status"], capture_output=True, text=True)
            return [TextContent(type="text", text=result.stdout)]
        except Exception as e:
            return [TextContent(type="text", text=f"错误: {e}")]
    elif name == "git_log":
        limit = arguments.get("limit", 10)
        try:
            result = subprocess.run(["git", "-C", path, "log", f"-{limit}", "--oneline"], capture_output=True, text=True)
            return [TextContent(type="text", text=result.stdout)]
        except Exception as e:
            return [TextContent(type="text", text=f"错误: {e}")]
    return [TextContent(type="text", text="未知工具")]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
