#!/usr/bin/env python3
"""简单测试git MCP服务器"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_git_mcp():
    """测试git MCP"""
    
    # 使用当前TeyMCP-Server仓库
    repo_path = "/home/sun/TeyMCP-Server"
    
    print(f"测试 git MCP 服务器")
    print(f"仓库路径: {repo_path}\n")
    
    server_params = StdioServerParameters(
        command="uvx",
        args=["mcp-server-git", "--repository", repo_path],
        env={}
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            print("✅ stdio 连接已建立")
            
            session = ClientSession(read, write)
            print("✅ ClientSession 已创建")
            
            print("\n初始化会话...")
            init_result = await asyncio.wait_for(
                session.initialize(),
                timeout=15.0
            )
            print(f"✅ 初始化成功!")
            print(f"   协议版本: {init_result.protocolVersion}")
            print(f"   服务器信息: {init_result.serverInfo}")
            
            print("\n列出工具...")
            tools_result = await asyncio.wait_for(
                session.list_tools(),
                timeout=10.0
            )
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

if __name__ == "__main__":
    success = asyncio.run(test_git_mcp())
    exit(0 if success else 1)
