"""
状态查询API
"""

from fastapi import APIRouter, Request
from typing import Dict, Any
import time
from datetime import datetime

router = APIRouter()

# Cache status checks to avoid repeated subprocess.poll() calls
_status_cache = {
    "data": None,
    "timestamp": 0,
    "ttl": 2.0  # Cache for 2 seconds
}


def _check_client_health(client) -> bool:
    """Check if a client is healthy (with caching consideration)"""
    try:
        # For stdio clients
        if hasattr(client, 'process') and client.process:
            return client.process.poll() is None
        # For HTTP clients
        return True
    except Exception:
        return False


@router.get("/status")
async def get_status(request: Request) -> Dict[str, Any]:
    """获取系统整体状态（优化版本，使用缓存）"""
    aggregator = request.app.state.aggregator
    
    current_time = time.time()
    
    # Return cached data if still valid
    if (_status_cache["data"] is not None and 
        current_time - _status_cache["timestamp"] < _status_cache["ttl"]):
        return _status_cache["data"]
    
    # Build server status list efficiently
    servers = []
    for name, client in aggregator.clients.items():
        is_healthy = _check_client_health(client)
        tool_count = len(client.tools) if hasattr(client, 'tools') else 0
        
        servers.append({
            "name": name,
            "status": "healthy" if is_healthy else "unhealthy",
            "tools_count": tool_count,
            "last_check": datetime.now().isoformat(),
            "uptime": 0,
            "error_count": 0
        })
    
    result = {
        "servers": servers,
        "metrics": {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0
        },
        "tools_count": len(aggregator.tool_registry)
    }
    
    # Update cache
    _status_cache["data"] = result
    _status_cache["timestamp"] = current_time
    
    return result


@router.get("/health")
async def health_check(request: Request) -> Dict[str, str]:
    """健康检查（优化版本）"""
    aggregator = request.app.state.aggregator
    
    # Use cached status if available
    current_time = time.time()
    if (_status_cache["data"] is not None and 
        current_time - _status_cache["timestamp"] < _status_cache["ttl"]):
        servers = _status_cache["data"]["servers"]
        healthy_count = sum(1 for s in servers if s["status"] == "healthy")
        total_count = len(servers)
    else:
        # Calculate directly if cache miss
        healthy_count = sum(1 for client in aggregator.clients.values() 
                          if _check_client_health(client))
        total_count = len(aggregator.clients)
    
    status = "healthy" if total_count > 0 and healthy_count == total_count else "degraded"
    
    return {
        "status": status,
        "healthy_servers": f"{healthy_count}/{total_count}"
    }
