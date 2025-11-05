#!/usr/bin/env python3
"""HuggingFace MCP Server"""
import asyncio, os, json
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("huggingface")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="search_models", description="搜索HuggingFace模型", 
             inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
        Tool(name="search_datasets", description="搜索HuggingFace数据集", 
             inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]})
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    token = os.getenv("HUGGINGFACE_TOKEN", "")
    return [TextContent(type="text", text=json.dumps({
        "tool": name,
        "status": "HuggingFace服务器已就绪" if token else "需要配置HUGGINGFACE_TOKEN",
        "message": f"工具 {name} 可用"
    }, ensure_ascii=False, indent=2))]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
