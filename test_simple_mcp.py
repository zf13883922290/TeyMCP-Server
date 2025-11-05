#!/usr/bin/env python3
"""最简单的MCP连接测试"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    print("1. 创建服务器参数...")
    server_params = StdioServerParameters(
        command="uvx",
        args=["mcp-server-time"]
    )
    
    print("2. 建立stdio连接...")
    try:
        async with stdio_client(server_params) as (read, write):
            print("3. 创建客户端会话...")
            session = ClientSession(read, write)
            
            print("4. 初始化会话(无超时)...")
            result = await session.initialize()
            print(f"✅ 初始化成功!")
            print(f"   Server名称: {result.serverInfo.name}")
            print(f"   版本: {result.serverInfo.version}")
            
            print("5. 列出工具...")
            tools = await session.list_tools()
            print(f"✅ 获取到 {len(tools.tools)} 个工具:")
            for tool in tools.tools:
                print(f"   - {tool.name}: {tool.description}")
                
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
