"""
MCP聚合器核心逻辑
"""

import asyncio
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import Tool, TextContent

from src.utils.logger import logger
from src.models.server import ServerStatus
from src.models.tool import ToolCallLog
from src.core.http_client import HTTPMCPClient, SSEMCPClient


class MCPAggregator:
    """
    MCP聚合器
    统一管理和调用多个上游MCP服务器
    支持 stdio 和 HTTP/SSE 两种连接方式
    """
    
    def __init__(self):
        self.upstream_clients: Dict[str, Union[ClientSession, HTTPMCPClient]] = {}
        self.client_contexts: Dict[str, Any] = {}  # 保存context managers (仅stdio)
        self.client_types: Dict[str, str] = {}  # 记录客户端类型: "stdio" 或 "http"
        self.tool_registry: Dict[str, str] = {}  # tool_name -> server_name
        self.server_status: Dict[str, ServerStatus] = {}
        self.call_logs: List[ToolCallLog] = []
        self.metrics = {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0
        }
    
    async def add_upstream_mcp_http(
        self,
        name: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        critical: bool = False,
        timeout: float = 30.0
    ) -> bool:
        """
        添加HTTP/SSE方式的上游MCP服务器
        
        Args:
            name: 服务器名称
            url: HTTP端点URL
            headers: HTTP请求头（如Authorization）
            critical: 是否为关键服务
            timeout: 请求超时时间
            
        Returns:
            是否成功连接
        """
        try:
            logger.info(f"🌐 正在连接 HTTP MCP: {name} ({url})...")
            
            # 创建HTTP客户端
            http_client = HTTPMCPClient(url=url, headers=headers, timeout=timeout)
            
            # 初始化连接
            logger.info(f"🔄 正在初始化 HTTP MCP: {name}...")
            await asyncio.wait_for(http_client.initialize(), timeout=timeout)
            logger.info(f"✅ {name} HTTP初始化完成")
            
            # 获取工具列表
            logger.info(f"📋 获取 {name} 工具列表...")
            tools_result = await asyncio.wait_for(http_client.list_tools(), timeout=10.0)
            
            # 解析工具列表
            tools = tools_result.get("tools", [])
            
            # 注册工具（添加命名空间前缀）
            for tool in tools:
                tool_name = tool.get("name") if isinstance(tool, dict) else tool.name
                namespaced_name = f"{name}_{tool_name}"
                self.tool_registry[namespaced_name] = name
            
            self.upstream_clients[name] = http_client
            self.client_types[name] = "http"
            
            # 更新状态
            self.server_status[name] = ServerStatus(
                name=name,
                status="healthy",
                tools_count=len(tools),
                last_check=datetime.now().isoformat(),
                uptime=0,
                error_count=0
            )
            
            logger.info(f"✅ {name} HTTP连接成功 ({len(tools)} 个工具)")
            return True
            
        except asyncio.TimeoutError:
            error_msg = f"HTTP连接超时"
            logger.error(f"❌ {name} {error_msg}")
            self._update_error_status(name, error_msg)
            if critical:
                raise RuntimeError(f"关键服务 {name} 启动失败: {error_msg}")
            return False
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ {name} HTTP连接失败: {error_msg}")
            self._update_error_status(name, error_msg)
            if critical:
                raise RuntimeError(f"关键服务 {name} 启动失败: {error_msg}")
            return False
    
    async def add_upstream_mcp(
        self,
        name: str,
        command: str,
        args: List[str],
        env: Optional[Dict[str, str]] = None,
        critical: bool = False
    ) -> bool:
        """
        添加stdio方式的上游MCP服务器
        
        Args:
            name: 服务器名称
            command: 启动命令
            args: 命令参数
            env: 环境变量
            critical: 是否为关键服务（失败时是否中断）
            
        Returns:
            是否成功连接
        """
        try:
            # 创建服务器参数
            server_params = StdioServerParameters(
                command=command,
                args=args,
                env=env or {}
            )
            
            # 建立连接
            logger.info(f"📡 正在连接 stdio MCP: {name}...")
            
            # 使用 stdio_client 创建连接
            stdio_ctx = stdio_client(server_params)
            read, write = await stdio_ctx.__aenter__()
            
            # 保存context manager以便后续清理
            self.client_contexts[name] = stdio_ctx
            
            client_session = ClientSession(read, write)
            
            # 初始化会话 (30秒超时)
            logger.info(f"🔄 正在初始化 stdio MCP: {name}...")
            init_task = client_session.initialize()
            await asyncio.wait_for(init_task, timeout=30.0)
            logger.info(f"✅ {name} stdio初始化完成")
            
            # 获取工具列表 (10秒超时)
            logger.info(f"📋 获取 {name} 工具列表...")
            list_task = client_session.list_tools()
            tools_result = await asyncio.wait_for(list_task, timeout=10.0)
            
            # 注册工具（添加命名空间前缀）
            for tool in tools_result.tools:
                namespaced_name = f"{name}_{tool.name}"
                self.tool_registry[namespaced_name] = name
            
            self.upstream_clients[name] = client_session
            self.client_types[name] = "stdio"
            
            # 更新状态
            self.server_status[name] = ServerStatus(
                name=name,
                status="healthy",
                tools_count=len(tools_result.tools),
                last_check=datetime.now().isoformat(),
                uptime=0,
                error_count=0
            )
            
            logger.info(f"✅ {name} stdio连接成功 ({len(tools_result.tools)} 个工具)")
            return True
            
        except asyncio.TimeoutError:
            error_msg = f"stdio连接超时"
            logger.error(f"❌ {name} {error_msg}")
            self._update_error_status(name, error_msg)
            if critical:
                raise RuntimeError(f"关键服务 {name} 启动失败: {error_msg}")
            return False
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ {name} stdio连接失败: {error_msg}")
            self._update_error_status(name, error_msg)
            if critical:
                raise RuntimeError(f"关键服务 {name} 启动失败: {error_msg}")
            return False
    
    def _update_error_status(self, name: str, error: str):
        """更新错误状态"""
        self.server_status[name] = ServerStatus(
            name=name,
            status="unhealthy",
            tools_count=0,
            last_check=datetime.now().isoformat(),
            uptime=0,
            error_count=1,
            last_error=error
        )
    
    async def remove_upstream_mcp(self, name: str) -> bool:
        """移除上游MCP服务器"""
        if name not in self.upstream_clients:
            return False
        
        # 断开连接
        try:
            client_type = self.client_types.get(name, "stdio")
            
            if client_type == "http":
                # HTTP客户端直接关闭
                client = self.upstream_clients[name]
                if isinstance(client, HTTPMCPClient):
                    await client.close()
            else:
                # stdio客户端需要清理上下文管理器
                if name in self.client_contexts:
                    ctx = self.client_contexts.pop(name)
                    try:
                        await ctx.__aexit__(None, None, None)
                    except:
                        pass
            
            # 清理客户端和类型记录
            self.upstream_clients.pop(name)
            self.client_types.pop(name, None)
        except Exception as e:
            logger.error(f"断开 {name} 时出错: {e}")
        
        # 清理工具注册
        self.tool_registry = {
            k: v for k, v in self.tool_registry.items()
            if v != name
        }
        
        # 清理状态
        self.server_status.pop(name, None)
        
        logger.info(f"🗑️  已移除服务器: {name}")
        return True
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """列出所有可用工具（优化版本，使用列表推导）"""
        # Use list comprehension for better performance
        return [
            {
                "name": tool_name,
                "server": server_name,
                "status": (
                    self.server_status[server_name].status 
                    if server_name in self.server_status and isinstance(self.server_status[server_name], ServerStatus)
                    else "unknown"
                )
            }
            for tool_name, server_name in self.tool_registry.items()
        ]
    
    async def call_tool(
        self,
        name: str,
        arguments: Dict[str, Any]
    ) -> List[TextContent]:
        """
        调用工具（支持stdio和HTTP两种方式）
        
        Args:
            name: 工具名称（带命名空间）
            arguments: 工具参数
            
        Returns:
            工具执行结果
        """
        import time
        start_time = time.time()
        
        # 查找对应的服务器
        server_name = self.tool_registry.get(name)
        if not server_name:
            return self._create_error_response(name, "工具未找到", 0)
        
        # 获取客户端
        client = self.upstream_clients.get(server_name)
        if not client:
            return self._create_error_response(name, "服务不可用", 0)
        
        try:
            # 移除命名空间前缀
            original_tool_name = name.replace(f"{server_name}_", "", 1)
            
            # 根据客户端类型调用工具
            client_type = self.client_types.get(server_name, "stdio")
            
            if client_type == "http":
                # HTTP方式调用
                result_dict = await client.call_tool(original_tool_name, arguments)
                # 将HTTP响应转换为TextContent格式
                content = result_dict.get("content", [])
                if isinstance(content, list):
                    result_content = [
                        TextContent(type="text", text=item.get("text", str(item)))
                        if isinstance(item, dict) else TextContent(type="text", text=str(item))
                        for item in content
                    ]
                else:
                    result_content = [TextContent(type="text", text=str(content))]
            else:
                # stdio方式调用
                result = await client.call_tool(original_tool_name, arguments)
                result_content = result.content
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            # 记录成功日志
            self._log_call(name, server_name, arguments, "success", duration_ms)
            
            # 更新服务器状态
            if server_name in self.server_status:
                self.server_status[server_name].status = "healthy"
                self.server_status[server_name].last_check = datetime.now().isoformat()
            
            return result_content
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_msg = str(e)
            
            # 记录失败日志
            self._log_call(name, server_name, arguments, "failed", duration_ms, error_msg)
            
            # 更新服务器错误状态
            if server_name in self.server_status:
                status = self.server_status[server_name]
                status.status = "unhealthy"
                status.error_count += 1
                status.last_error = error_msg
                status.last_check = datetime.now().isoformat()
            
            return self._create_error_response(name, error_msg, duration_ms)
    
    def _create_error_response(
        self,
        tool_name: str,
        error: str,
        duration_ms: int
    ) -> List[TextContent]:
        """创建错误响应"""
        return [TextContent(
            type="text",
            text=f"❌ 工具调用失败\n工具: {tool_name}\n错误: {error}\n耗时: {duration_ms}ms"
        )]
    
    def _log_call(
        self,
        tool_name: str,
        server_name: str,
        arguments: Dict[str, Any],
        status: str,
        duration_ms: int,
        error: Optional[str] = None
    ):
        """记录工具调用日志"""
        log = ToolCallLog(
            timestamp=datetime.now().isoformat(),
            tool_name=tool_name,
            server=server_name,
            arguments=arguments,
            status=status,
            duration_ms=duration_ms,
            error=error
        )
        
        self.call_logs.append(log)
        
        # 只保留最近1000条日志
        if len(self.call_logs) > 1000:
            self.call_logs = self.call_logs[-1000:]
        
        # 更新指标
        self.metrics["total_calls"] += 1
        if status == "success":
            self.metrics["successful_calls"] += 1
        else:
            self.metrics["failed_calls"] += 1
    
    async def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            "servers": {
                name: status.dict()
                for name, status in self.server_status.items()
            },
            "metrics": self.metrics,
            "tools_count": len(self.tool_registry)
        }
