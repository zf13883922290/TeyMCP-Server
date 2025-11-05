"""
状态查询API
"""

from fastapi import APIRouter, Request
from typing import Dict, Any

router = APIRouter()


@router.get("/status")
async def get_status(request: Request) -> Dict[str, Any]:
    """获取系统整体状态"""
    aggregator = request.app.state.aggregator
    
    # 构建服务器状态列表
    servers = []
    for name, client in aggregator.clients.items():
        servers.append({
            "name": name,
            "status": "healthy" if client.process and client.process.poll() is None else "unhealthy",
            "tools_count": len(client.tools),
            "last_check": "",
            "uptime": 0,
            "error_count": 0
        })
    
    return {
        "servers": servers,
        "metrics": {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0
        },
        "tools_count": len(aggregator.tool_registry)
    }


@router.get("/health")
async def health_check(request: Request) -> Dict[str, str]:
    """健康检查"""
    aggregator = request.app.state.aggregator
    
    healthy_count = sum(
        1 for client in aggregator.clients.values()
        if client.process and client.process.poll() is None
    )
    total_count = len(aggregator.clients)
    
    status = "healthy" if total_count > 0 and healthy_count == total_count else "degraded"
    
    return {
        "status": status,
        "healthy_servers": f"{healthy_count}/{total_count}"
    }
