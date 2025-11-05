"""
MCP客户端管理器
负责管理与上游MCP服务器的连接
"""

import asyncio
import logging
from typing import Dict, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)


class ClientManager:
    """管理MCP客户端连接的生命周期"""
    
    def __init__(self):
        self.clients: Dict[str, ClientSession] = {}
        self.sessions: Dict[str, tuple] = {}  # 存储 (read, write) 元组
        
    async def connect_client(
        self,
        name: str,
        command: str,
        args: list,
        env: Optional[dict] = None
    ) -> ClientSession:
        """
        连接到MCP服务器
        
        Args:
            name: 服务器名称
            command: 启动命令
            args: 命令参数
            env: 环境变量
            
        Returns:
            ClientSession实例
            
        Raises:
            Exception: 连接失败时抛出
        """
        try:
            logger.info(f"正在连接MCP服务器: {name}")
            logger.debug(f"命令: {command} {' '.join(args)}")
            
            # 创建服务器参数
            server_params = StdioServerParameters(
                command=command,
                args=args,
                env=env or {}
            )
            
            # 建立stdio连接
            read, write = await stdio_client(server_params)
            
            # 创建客户端会话
            client = ClientSession(read, write)
            
            # 初始化会话
            await client.initialize()
            
            # 保存客户端和会话信息
            self.clients[name] = client
            self.sessions[name] = (read, write)
            
            logger.info(f"✅ MCP服务器 {name} 连接成功")
            return client
            
        except Exception as e:
            logger.error(f"❌ 连接MCP服务器 {name} 失败: {e}")
            raise
            
    async def disconnect_client(self, name: str) -> None:
        """
        断开与MCP服务器的连接
        
        Args:
            name: 服务器名称
        """
        try:
            if name in self.clients:
                client = self.clients[name]
                
                # 关闭客户端
                # await client.close()  # MCP SDK可能没有close方法，需要手动清理
                
                # 清理资源
                if name in self.sessions:
                    read, write = self.sessions[name]
                    # 关闭流
                    try:
                        write.close()
                        # await write.wait_closed()  # 如果支持异步关闭
                    except:
                        pass
                    
                    del self.sessions[name]
                
                del self.clients[name]
                logger.info(f"已断开MCP服务器: {name}")
                
        except Exception as e:
            logger.error(f"断开MCP服务器 {name} 时出错: {e}")
            
    async def reconnect_client(
        self,
        name: str,
        command: str,
        args: list,
        env: Optional[dict] = None
    ) -> ClientSession:
        """
        重新连接MCP服务器
        
        Args:
            name: 服务器名称
            command: 启动命令
            args: 命令参数
            env: 环境变量
            
        Returns:
            ClientSession实例
        """
        logger.info(f"正在重连MCP服务器: {name}")
        
        # 先断开现有连接
        await self.disconnect_client(name)
        
        # 等待一小段时间
        await asyncio.sleep(1)
        
        # 重新连接
        return await self.connect_client(name, command, args, env)
        
    def get_client(self, name: str) -> Optional[ClientSession]:
        """
        获取客户端实例
        
        Args:
            name: 服务器名称
            
        Returns:
            ClientSession实例，如果不存在返回None
        """
        return self.clients.get(name)
        
    def is_connected(self, name: str) -> bool:
        """
        检查服务器是否已连接
        
        Args:
            name: 服务器名称
            
        Returns:
            True表示已连接，False表示未连接
        """
        return name in self.clients
        
    async def disconnect_all(self) -> None:
        """断开所有客户端连接"""
        logger.info("正在断开所有MCP服务器连接...")
        
        names = list(self.clients.keys())
        for name in names:
            await self.disconnect_client(name)
            
        logger.info(f"已断开所有 {len(names)} 个MCP服务器连接")
        
    def get_all_clients(self) -> Dict[str, ClientSession]:
        """
        获取所有客户端
        
        Returns:
            服务器名称到ClientSession的映射
        """
        return self.clients.copy()
