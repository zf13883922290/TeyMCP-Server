"""
简化的MCP聚合器 - 使用subprocess和直接JSON-RPC通信
避免MCP SDK stdio_client的超时问题
支持stdio和HTTP/SSE两种连接方式
"""

import asyncio
import json
import subprocess
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import logging

logger = logging.getLogger("teymcp")

# 导入HTTP客户端
try:
    from src.core.http_client import HTTPMCPClient
except ImportError:
    HTTPMCPClient = None
    logger.warning("HTTP客户端未安装,仅支持stdio连接")


class SimpleMCPClient:
    """简单的MCP客户端 - 使用subprocess和JSON-RPC"""
    
    def __init__(self, name: str, command: str, args: List[str], env: Optional[Dict[str, str]] = None, working_dir: Optional[str] = None):
        self.name = name
        self.command = command
        self.args = args
        self.env = env or {}
        self.working_dir = working_dir
        self.process: Optional[subprocess.Popen] = None
        self.request_id = 0
        self.tools: List[Dict[str, Any]] = []
        
    async def start(self) -> bool:
        """启动MCP服务器进程"""
        try:
            cmd_str = f"{self.command} {' '.join(self.args)}"
            if self.working_dir:
                logger.info(f"🚀 启动 {self.name} (工作目录: {self.working_dir}): {cmd_str}")
            else:
                logger.info(f"🚀 启动 {self.name}: {cmd_str}")
            
            # 启动子进程
            self.process = subprocess.Popen(
                [self.command] + self.args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**self.env},
                cwd=self.working_dir,  # 设置工作目录
                text=False,  # 使用字节模式
                bufsize=0
            )
            
            # 等待进程启动
            await asyncio.sleep(0.5)
            
            if self.process.poll() is not None:
                stderr = self.process.stderr.read().decode('utf-8', errors='ignore')
                logger.error(f"❌ {self.name} 进程启动失败: {stderr}")
                return False
            
            # 发送initialize请求
            init_success = await self._initialize()
            if not init_success:
                return False
            
            # 获取工具列表
            tools_success = await self._list_tools()
            if not tools_success:
                return False
            
            logger.info(f"✅ {self.name} 启动成功,提供 {len(self.tools)} 个工具")
            return True
            
        except Exception as e:
            logger.error(f"❌ {self.name} 启动异常: {e}")
            return False
    
    async def _initialize(self) -> bool:
        """发送initialize请求"""
        try:
            request = {
                "jsonrpc": "2.0",
                "id": self._next_id(),
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
            
            response = await self._send_request(request, timeout=10.0)
            if response and "result" in response:
                logger.info(f"✓ {self.name} 初始化成功")
                return True
            else:
                logger.error(f"✗ {self.name} 初始化失败: {response}")
                return False
                
        except asyncio.TimeoutError:
            logger.error(f"✗ {self.name} 初始化超时")
            return False
        except Exception as e:
            logger.error(f"✗ {self.name} 初始化异常: {e}")
            return False
    
    async def _list_tools(self) -> bool:
        """获取工具列表"""
        try:
            request = {
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "tools/list",
                "params": {}
            }
            
            response = await self._send_request(request, timeout=5.0)
            if response and "result" in response:
                self.tools = response["result"].get("tools", [])
                logger.info(f"✓ {self.name} 获取到 {len(self.tools)} 个工具")
                return True
            else:
                logger.error(f"✗ {self.name} 获取工具列表失败: {response}")
                return False
                
        except asyncio.TimeoutError:
            logger.error(f"✗ {self.name} 获取工具列表超时")
            return False
        except Exception as e:
            logger.error(f"✗ {self.name} 获取工具列表异常: {e}")
            return False
    
    async def _send_request(self, request: Dict[str, Any], timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """发送JSON-RPC请求并等待响应"""
        if not self.process or self.process.poll() is not None:
            return None
        
        try:
            # 发送请求
            request_line = json.dumps(request) + "\n"
            self.process.stdin.write(request_line.encode('utf-8'))
            self.process.stdin.flush()
            
            # 等待响应(带超时)
            response_data = await asyncio.wait_for(
                self._read_response(),
                timeout=timeout
            )
            
            if response_data:
                return json.loads(response_data)
            return None
            
        except asyncio.TimeoutError:
            raise
        except Exception as e:
            logger.error(f"发送请求异常: {e}")
            return None
    
    async def _read_response(self) -> Optional[str]:
        """从stdout读取一行响应（优化版本，使用asyncio streams）"""
        if not self.process:
            return None
        
        try:
            # Use asyncio.create_subprocess_exec for truly async I/O in future
            # For now, run blocking I/O in thread pool executor but with timeout
            loop = asyncio.get_event_loop()
            
            def read_line():
                try:
                    # Read with a small buffer to avoid excessive memory usage
                    line = self.process.stdout.readline()
                    if line:
                        return line.decode('utf-8', errors='ignore').strip()
                    return None
                except Exception:
                    return None
            
            # Add timeout to prevent indefinite blocking
            return await asyncio.wait_for(
                loop.run_in_executor(None, read_line),
                timeout=30.0
            )
        except asyncio.TimeoutError:
            logger.warning(f"{self.name}: Read response timeout")
            return None
        except Exception:
            return None
    
    def _next_id(self) -> int:
        """生成下一个请求ID"""
        self.request_id += 1
        return self.request_id
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """调用工具"""
        try:
            request = {
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            response = await self._send_request(request, timeout=30.0)
            return response.get("result") if response else None
            
        except Exception as e:
            logger.error(f"调用工具 {tool_name} 失败: {e}")
            return None
    
    def stop(self):
        """停止MCP服务器进程"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
            self.process = None


class SimpleMCPAggregator:
    """简化的MCP聚合器 - 支持stdio和HTTP两种连接方式"""
    
    def __init__(self):
        self.clients: Dict[str, Any] = {}  # Union[SimpleMCPClient, HTTPMCPClient]
        self.tool_registry: Dict[str, str] = {}  # tool_name -> server_name
        self.client_types: Dict[str, str] = {}  # server_name -> "stdio" or "http"
    
    async def add_server(self, name: str, command: str, args: List[str], 
                        env: Optional[Dict[str, str]] = None, working_dir: Optional[str] = None) -> bool:
        """添加并启动stdio方式的MCP服务器"""
        client = SimpleMCPClient(name, command, args, env, working_dir)
        
        success = await client.start()
        if success:
            self.clients[name] = client
            self.client_types[name] = "stdio"
            
            # 注册工具(添加命名空间前缀)
            for tool in client.tools:
                tool_name = tool.get("name", "")
                namespaced_name = f"{name}_{tool_name}"
                self.tool_registry[namespaced_name] = name
            
            return True
        
        return False
    
    async def add_http_server(
        self,
        name: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0
    ) -> bool:
        """
        添加HTTP/SSE方式的MCP服务器
        
        Args:
            name: 服务器名称
            url: HTTP端点URL
            headers: HTTP请求头
            timeout: 请求超时时间
        """
        if HTTPMCPClient is None:
            logger.error("HTTP客户端未安装,无法添加HTTP服务器")
            return False
        
        try:
            logger.info(f"🌐 连接 HTTP MCP: {name} ({url})...")
            
            # 创建HTTP客户端
            client = HTTPMCPClient(url=url, headers=headers, timeout=timeout)
            
            # 初始化连接
            await client.initialize()
            logger.info(f"✓ {name} HTTP初始化成功")
            
            # 获取工具列表
            tools_result = await client.list_tools()
            tools = tools_result.get("tools", [])
            
            # 保存客户端
            self.clients[name] = client
            self.client_types[name] = "http"
            
            # 注册工具(添加命名空间前缀)
            for tool in tools:
                tool_name = tool.get("name", "") if isinstance(tool, dict) else str(tool)
                namespaced_name = f"{name}_{tool_name}"
                self.tool_registry[namespaced_name] = name
            
            logger.info(f"✅ {name} HTTP连接成功,提供 {len(tools)} 个工具")
            return True
            
        except Exception as e:
            logger.error(f"❌ {name} HTTP连接失败: {e}")
            return False
    
    def get_all_tools(self) -> List[Dict[str, Any]]:
        """获取所有工具（优化版本，减少循环和字符串操作）"""
        all_tools = []
        
        # Pre-compute server prefix for faster lookups
        for server_name, client in self.clients.items():
            client_type = self.client_types.get(server_name, "stdio")
            server_prefix = f"{server_name}_"
            
            if client_type == "http":
                # HTTP客户端：只处理属于此服务器的工具
                # Use list comprehension for better performance
                http_tools = [
                    {
                        "server": server_name,
                        "name": namespaced_name,
                        "original_name": namespaced_name[len(server_prefix):],  # Faster than replace
                        "description": f"HTTP MCP工具: {namespaced_name[len(server_prefix):]}",
                        "inputSchema": {}
                    }
                    for namespaced_name, srv_name in self.tool_registry.items()
                    if srv_name == server_name
                ]
                all_tools.extend(http_tools)
            else:
                # stdio客户端：直接从tools列表获取（使用列表推导提升性能）
                stdio_tools = [
                    {
                        "server": server_name,
                        "name": f"{server_prefix}{tool.get('name', '')}",
                        "original_name": tool.get("name", ""),
                        "description": tool.get("description", ""),
                        "inputSchema": tool.get("inputSchema", {})
                    }
                    for tool in client.tools
                ]
                all_tools.extend(stdio_tools)
        
        return all_tools
    
    async def call_tool(self, namespaced_name: str, arguments: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """调用工具（支持stdio和HTTP两种方式）"""
        server_name = self.tool_registry.get(namespaced_name)
        if not server_name:
            return None
        
        client = self.clients.get(server_name)
        if not client:
            return None
        
        # 提取原始工具名称
        original_name = namespaced_name.replace(f"{server_name}_", "", 1)
        
        # 根据客户端类型调用
        client_type = self.client_types.get(server_name, "stdio")
        
        try:
            if client_type == "http":
                # HTTP方式调用
                result = await client.call_tool(original_name, arguments)
                return result
            else:
                # stdio方式调用
                return await client.call_tool(original_name, arguments)
        except Exception as e:
            logger.error(f"调用工具失败 [{namespaced_name}]: {e}")
            return None
    
    async def shutdown(self):
        """关闭所有MCP服务器"""
        for server_name, client in self.clients.items():
            client_type = self.client_types.get(server_name, "stdio")
            
            if client_type == "http":
                # HTTP客户端异步关闭
                try:
                    await client.close()
                except Exception as e:
                    logger.error(f"关闭HTTP客户端 {server_name} 失败: {e}")
            else:
                # stdio客户端同步关闭
                client.stop()
        
        self.clients.clear()
        self.tool_registry.clear()
        self.client_types.clear()
