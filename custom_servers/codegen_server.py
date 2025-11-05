#!/usr/bin/env python3
"""CodeGen MCP Server - AI代码生成"""
import asyncio, json
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("codegen")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="generate_code", description="生成代码模板", 
             inputSchema={"type": "object", "properties": {
                 "language": {"type": "string", "description": "编程语言"},
                 "description": {"type": "string", "description": "代码描述"}
             }, "required": ["language", "description"]})
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    return [TextContent(type="text", text=json.dumps({
        "tool": name,
        "language": arguments.get("language"),
        "description": arguments.get("description"),
        "message": "代码生成服务器已就绪,可以通过AI模型生成代码"
    }, ensure_ascii=False, indent=2))]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
