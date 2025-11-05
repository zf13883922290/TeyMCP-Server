"""
服务器相关数据模型
"""

from pydantic import BaseModel
from typing import Optional


class ServerStatus(BaseModel):
    """服务器状态模型"""
    name: str
    status: str  # "healthy", "unhealthy", "disconnected"
    tools_count: int
    last_check: str
    uptime: int
    error_count: int
    last_error: Optional[str] = None
