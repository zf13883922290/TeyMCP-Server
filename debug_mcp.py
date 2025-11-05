#!/usr/bin/env python3
"""详细调试MCP服务器连接"""

import asyncio
import sys
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def debug_mcp_connection(name: str, command: str, args: list):
    """详细调试MCP服务器连接过程"""
    print(f"\n{'='*60}")
    print(f"测试 MCP 服务器: {name}")
    print(f"命令: {command} {' '.join(args)}")
    print(f"{'='*60}\n")
    
    try:
        # 创建服务器参数
        server_params = StdioServerParameters(
            command=command,
            args=args,
            env={}
        )
        
        print("步骤 1: 创建 stdio_client...")
        stdio_ctx = stdio_client(server_params)
        
        print("步骤 2: 进入上下文管理器...")
        read, write = await stdio_ctx.__aenter__()
        print("✅ stdio 连接已建立")
        
        print("\n步骤 3: 创建 ClientSession...")
        session = ClientSession(read, write)
        print("✅ ClientSession 已创建")
        
        print("\n步骤 4: 初始化会话 (10秒超时)...")
        try:
            init_result = await asyncio.wait_for(
                session.initialize(),
                timeout=10.0
            )
            print(f"✅ 初始化成功!")
            print(f"   服务器信息: {init_result}")
            
            print("\n步骤 5: 列出工具 (5秒超时)...")
            tools_result = await asyncio.wait_for(
                session.list_tools(),
                timeout=5.0
            )
            print(f"✅ 获取到 {len(tools_result.tools)} 个工具:")
            for tool in tools_result.tools:
                print(f"   - {tool.name}: {tool.description}")
            
            # 清理
            await stdio_ctx.__aexit__(None, None, None)
            return True
            
        except asyncio.TimeoutError as e:
            print(f"❌ 超时: {e}")
            print("   可能原因:")
            print("   1. MCP服务器没有响应initialize请求")
            print("   2. MCP服务器需要额外的配置参数")
            print("   3. stdio通信问题")
            await stdio_ctx.__aexit__(None, None, None)
            return False
            
    except Exception as e:
        print(f"❌ 错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """测试多个MCP服务器"""
    
    tests = [
        ("fetch", "uvx", ["mcp-server-fetch"]),
        ("git", "uvx", ["mcp-server-git", "--repository", "/home/sun"]),
        ("time", "uvx", ["mcp-server-time"]),
    ]
    
    results = []
    for name, command, args in tests:
        success = await debug_mcp_connection(name, command, args)
        results.append((name, success))
        await asyncio.sleep(2)  # 等待一下再测试下一个
    
    print(f"\n{'='*60}")
    print("测试总结:")
    print(f"{'='*60}")
    for name, success in results:
        status = "✅ 成功" if success else "❌ 失败"
        print(f"{status} - {name}")
    
    success_count = sum(1 for _, s in results if s)
    print(f"\n总计: {success_count}/{len(results)} 成功")

if __name__ == "__main__":
    asyncio.run(main())
