"""
HTTP/SSE MCP客户端
支持通过HTTP连接到MCP服务器
"""

import asyncio
import json
from typing import Dict, Any, Optional, AsyncIterator
import httpx
from mcp.types import (
    JSONRPCRequest,
    JSONRPCResponse,
    JSONRPCNotification,
    JSONRPCMessage
)
from src.utils.logger import logger


class HTTPMCPClient:
    """
    HTTP/SSE方式的MCP客户端
    用于连接支持HTTP协议的MCP服务器（如HuggingFace MCP）
    """
    
    def __init__(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0
    ):
        """
        初始化HTTP MCP客户端
        
        Args:
            url: MCP服务器的HTTP端点
            headers: HTTP请求头（如Authorization）
            timeout: 请求超时时间（秒）
        """
        self.url = url.rstrip('/')
        self.headers = headers or {}
        self.timeout = timeout
        # Use connection pooling with limits for better performance
        self.client = httpx.AsyncClient(
            headers=self.headers,
            timeout=timeout,
            follow_redirects=True,
            limits=httpx.Limits(
                max_keepalive_connections=20,
                max_connections=100,
                keepalive_expiry=30.0
            ),
            http2=True  # Enable HTTP/2 for better performance
        )
        self._request_id = 0
        
    def _next_request_id(self) -> int:
        """生成下一个请求ID"""
        self._request_id += 1
        return self._request_id
    
    async def initialize(self) -> Dict[str, Any]:
        """
        初始化连接
        发送 initialize 请求
        """
        try:
            request = {
                "jsonrpc": "2.0",
                "id": self._next_request_id(),
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "TeyMCP-Server",
                        "version": "1.0.0"
                    }
                }
            }
            
            response = await self.client.post(
                f"{self.url}/message",
                json=request
            )
            response.raise_for_status()
            
            result = response.json()
            if "error" in result:
                raise RuntimeError(f"初始化失败: {result['error']}")
            
            logger.info(f"✅ HTTP MCP 初始化成功: {self.url}")
            return result.get("result", {})
            
        except Exception as e:
            logger.error(f"❌ HTTP MCP 初始化失败: {e}")
            raise
    
    async def list_tools(self) -> Dict[str, Any]:
        """
        列出所有可用工具
        """
        try:
            request = {
                "jsonrpc": "2.0",
                "id": self._next_request_id(),
                "method": "tools/list",
                "params": {}
            }
            
            response = await self.client.post(
                f"{self.url}/message",
                json=request
            )
            response.raise_for_status()
            
            result = response.json()
            if "error" in result:
                raise RuntimeError(f"获取工具列表失败: {result['error']}")
            
            return result.get("result", {})
            
        except Exception as e:
            logger.error(f"❌ 获取工具列表失败: {e}")
            raise
    
    async def call_tool(
        self,
        name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        调用工具
        
        Args:
            name: 工具名称
            arguments: 工具参数
            
        Returns:
            工具执行结果
        """
        try:
            request = {
                "jsonrpc": "2.0",
                "id": self._next_request_id(),
                "method": "tools/call",
                "params": {
                    "name": name,
                    "arguments": arguments
                }
            }
            
            response = await self.client.post(
                f"{self.url}/message",
                json=request
            )
            response.raise_for_status()
            
            result = response.json()
            if "error" in result:
                raise RuntimeError(f"工具调用失败: {result['error']}")
            
            return result.get("result", {})
            
        except Exception as e:
            logger.error(f"❌ 工具调用失败 [{name}]: {e}")
            raise
    
    async def close(self):
        """关闭客户端连接"""
        try:
            await self.client.aclose()
            logger.info(f"🔌 HTTP MCP 客户端已关闭: {self.url}")
        except Exception as e:
            logger.error(f"关闭客户端时出错: {e}")


class SSEMCPClient(HTTPMCPClient):
    """
    SSE (Server-Sent Events) 方式的MCP客户端
    支持服务器推送事件流
    """
    
    async def stream_events(self) -> AsyncIterator[Dict[str, Any]]:
        """
        订阅SSE事件流
        
        Yields:
            服务器推送的事件
        """
        try:
            async with self.client.stream(
                "GET",
                f"{self.url}/sse",
                headers={"Accept": "text/event-stream"}
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]  # 移除 "data: " 前缀
                        try:
                            data = json.loads(data_str)
                            yield data
                        except json.JSONDecodeError:
                            logger.warning(f"无法解析SSE数据: {data_str}")
                            
        except Exception as e:
            logger.error(f"SSE流处理错误: {e}")
            raise
