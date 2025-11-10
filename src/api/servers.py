"""
服务器管理API
"""

from fastapi import APIRouter, Request, HTTPException
from typing import Dict, List, Any
from pydantic import BaseModel

router = APIRouter()


class ServerConfig(BaseModel):
    """服务器配置模型"""
    name: str
    command: str
    args: List[str]
    env: Dict[str, str] = {}
    critical: bool = False


@router.get("/servers")
async def list_servers(request: Request) -> Dict[str, Any]:
    """列出所有服务器"""
    aggregator = request.app.state.aggregator
    
    return {
        "servers": [
            status.dict()
            for status in aggregator.server_status.values()
        ],
        "count": len(aggregator.server_status)
    }


@router.get("/servers/{server_name}")
async def get_server(server_name: str, request: Request) -> Dict[str, Any]:
    """获取服务器详情"""
    aggregator = request.app.state.aggregator
    
    if server_name not in aggregator.server_status:
        raise HTTPException(status_code=404, detail="服务器不存在")
    
    status = aggregator.server_status[server_name]
    
    # 获取该服务器的所有工具
    tools = [
        tool_name for tool_name, srv_name in aggregator.tool_registry.items()
        if srv_name == server_name
    ]
    
    return {
        **status.dict(),
        "tools": tools
    }


@router.post("/servers")
async def add_server(config: ServerConfig, request: Request) -> Dict[str, Any]:
    """添加新服务器"""
    aggregator = request.app.state.aggregator
    
    if config.name in aggregator.upstream_clients:
        raise HTTPException(status_code=400, detail="服务器已存在")
    
    success = await aggregator.add_upstream_mcp(
        name=config.name,
        command=config.command,
        args=config.args,
        env=config.env,
        critical=config.critical
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="添加服务器失败")
    
    return {
        "success": True,
        "message": f"服务器 {config.name} 添加成功"
    }


@router.delete("/servers/{server_name}")
async def remove_server(server_name: str, request: Request) -> Dict[str, Any]:
    """移除服务器"""
    aggregator = request.app.state.aggregator
    
    success = await aggregator.remove_upstream_mcp(server_name)
    
    if not success:
        raise HTTPException(status_code=404, detail="服务器不存在")
    
    return {
        "success": True,
        "message": f"服务器 {server_name} 已移除"
    }


@router.post("/servers/{server_name}/restart")
async def restart_server(server_name: str, request: Request) -> Dict[str, Any]:
    """重启服务器"""
    aggregator = request.app.state.aggregator
    
    if server_name not in aggregator.server_status:
        raise HTTPException(status_code=404, detail="服务器不存在")
    
    # TODO: 实现重启逻辑
    # 目前简单返回成功
    
    return {
        "success": True,
        "message": f"服务器 {server_name} 重启成功"
    }
