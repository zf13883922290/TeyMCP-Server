#!/usr/bin/env python3
"""捕获MCP SDK发送的请求"""

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def capture_mcp_communication():
    """捕获MCP通信"""
    
    server_params = StdioServerParameters(
        command="python3",
        args=["/home/sun/TeyMCP-Server/local_mcp_server.py"],
        env={}
    )
    
    print("开始捕获MCP通信...")
    
    try:
        stdio_ctx = stdio_client(server_params)
        read, write = await stdio_ctx.__aenter__()
        
        print("✅ stdio连接已建立\n")
        
        session = ClientSession(read, write)
        print("✅ ClientSession已创建\n")
        
        print("发送initialize请求...")
        print("等待响应 (5秒超时)...\n")
        
        init_result = await asyncio.wait_for(
            session.initialize(),
            timeout=5.0
        )
        
        print("✅ 收到响应!")
        print(f"协议版本: {init_result.protocolVersion}")
        print(f"服务器信息: {init_result.serverInfo}")
        
        await stdio_ctx.__aexit__(None, None, None)
        return True
        
    except asyncio.TimeoutError:
        print("❌ 超时 - 5秒内没有收到响应")
        print("\n可能的原因:")
        print("1. MCP SDK的请求格式与服务器不兼容")
        print("2. 请求/响应的JSON-RPC格式不匹配")
        print("3. stdio缓冲问题")
        return False
        
    except Exception as e:
        print(f"❌ 错误: {type(e).__name__}")
        print(f"   {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(capture_mcp_communication())
    sys.exit(0 if success else 1)
