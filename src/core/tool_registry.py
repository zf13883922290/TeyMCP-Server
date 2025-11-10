"""
工具注册表
管理所有可用工具的注册和查询
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ToolInfo:
    """工具信息"""
    name: str                    # 工具名称
    server: str                  # 所属服务器
    description: str             # 工具描述
    input_schema: dict          # 输入schema
    full_name: str              # 完整名称 (server_name.tool_name)


class ToolRegistry:
    """工具注册表 - 管理所有工具的元数据"""
    
    def __init__(self):
        self.tools: Dict[str, ToolInfo] = {}  # full_name -> ToolInfo
        
    def register_tool(
        self,
        server_name: str,
        tool_name: str,
        description: str,
        input_schema: dict
    ) -> str:
        """
        注册一个工具
        
        Args:
            server_name: 服务器名称
            tool_name: 工具名称
            description: 工具描述
            input_schema: 输入schema
            
        Returns:
            工具的完整名称 (server_name.tool_name)
        """
        # 生成完整名称（带命名空间）
        full_name = f"{server_name}.{tool_name}"
        
        # 创建工具信息
        tool_info = ToolInfo(
            name=tool_name,
            server=server_name,
            description=description,
            input_schema=input_schema,
            full_name=full_name
        )
        
        # 注册到注册表
        self.tools[full_name] = tool_info
        
        logger.debug(f"注册工具: {full_name}")
        return full_name
        
    def unregister_tool(self, full_name: str) -> bool:
        """
        注销一个工具
        
        Args:
            full_name: 工具的完整名称
            
        Returns:
            True表示成功，False表示工具不存在
        """
        if full_name in self.tools:
            del self.tools[full_name]
            logger.debug(f"注销工具: {full_name}")
            return True
        return False
        
    def unregister_server_tools(self, server_name: str) -> int:
        """
        注销某个服务器的所有工具
        
        Args:
            server_name: 服务器名称
            
        Returns:
            注销的工具数量
        """
        # 找到所有属于该服务器的工具
        tools_to_remove = [
            full_name for full_name, tool_info in self.tools.items()
            if tool_info.server == server_name
        ]
        
        # 删除这些工具
        for full_name in tools_to_remove:
            del self.tools[full_name]
            
        count = len(tools_to_remove)
        if count > 0:
            logger.info(f"注销服务器 {server_name} 的 {count} 个工具")
            
        return count
        
    def get_tool_info(self, full_name: str) -> Optional[ToolInfo]:
        """
        获取工具信息
        
        Args:
            full_name: 工具的完整名称
            
        Returns:
            ToolInfo实例，如果不存在返回None
        """
        return self.tools.get(full_name)
        
    def list_all_tools(self) -> List[ToolInfo]:
        """
        列出所有工具
        
        Returns:
            ToolInfo列表
        """
        return list(self.tools.values())
        
    def list_server_tools(self, server_name: str) -> List[ToolInfo]:
        """
        列出某个服务器的所有工具
        
        Args:
            server_name: 服务器名称
            
        Returns:
            ToolInfo列表
        """
        return [
            tool_info for tool_info in self.tools.values()
            if tool_info.server == server_name
        ]
        
    def search_tools(self, keyword: str) -> List[ToolInfo]:
        """
        搜索工具（按名称或描述）
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的ToolInfo列表
        """
        keyword_lower = keyword.lower()
        results = []
        
        for tool_info in self.tools.values():
            if (keyword_lower in tool_info.name.lower() or
                keyword_lower in tool_info.description.lower()):
                results.append(tool_info)
                
        return results
        
    def get_tool_count(self) -> int:
        """
        获取工具总数
        
        Returns:
            工具数量
        """
        return len(self.tools)
        
    def get_server_tool_count(self, server_name: str) -> int:
        """
        获取某个服务器的工具数量
        
        Args:
            server_name: 服务器名称
            
        Returns:
            工具数量
        """
        return sum(
            1 for tool_info in self.tools.values()
            if tool_info.server == server_name
        )
        
    def clear_all(self) -> None:
        """清空所有工具"""
        count = len(self.tools)
        self.tools.clear()
        logger.info(f"清空所有工具注册表 ({count} 个工具)")
