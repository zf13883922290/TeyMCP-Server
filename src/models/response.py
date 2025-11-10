"""
API响应模型
"""

from pydantic import BaseModel
from typing import Any, Optional


class APIResponse(BaseModel):
    """标准API响应"""
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """错误响应"""
    error: str
    detail: Optional[str] = None
