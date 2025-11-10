"""
工具相关数据模型
"""

from pydantic import BaseModel
from typing import Dict, Any, Optional


class ToolCallLog(BaseModel):
    """工具调用日志模型"""
    timestamp: str
    tool_name: str
    server: str
    arguments: Dict[str, Any]
    status: str  # "success", "failed"
    duration_ms: int
    error: Optional[str] = None
