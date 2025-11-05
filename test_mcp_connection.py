#!/usr/bin/env python3
"""测试单个MCP服务器连接"""

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_server(command: str, args: list):
    """测试连接到MCP服务器"""
    print(f"测试命令: {command} {' '.join(args)}")
    
    try:
        # 创建服务器参数
        server_params = StdioServerParameters(
            command=command,
            args=args,
            env={}
        )
        
        print("1. 创建stdio客户端...")
        async with stdio_client(server_params) as (read, write):
            print("2. 创建客户端会话...")
            session = ClientSession(read, write)
            
            print("3. 初始化会话...")
            init_result = await asyncio.wait_for(session.initialize(), timeout=10.0)
            print(f"✅ 初始化成功: {init_result}")
            
            print("4. 列出工具...")
            tools_result = await asyncio.wait_for(session.list_tools(), timeout=5.0)
            print(f"✅ 获取到 {len(tools_result.tools)} 个工具:")
            for tool in tools_result.tools:
                print(f"   - {tool.name}: {tool.description}")
            
            return True
            
    except asyncio.TimeoutError:
        print("❌ 超时")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    # 测试git MCP服务器
    success = await test_mcp_server("uvx", ["mcp-server-git", "--repository", "/home/sun"])
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
