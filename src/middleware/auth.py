"""
认证中间件
处理API密钥验证（可选功能）
"""

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os


security = HTTPBearer(auto_error=False)


class AuthMiddleware:
    """API密钥认证中间件"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化认证中间件
        
        Args:
            api_key: API密钥，如果为None则从环境变量读取
        """
        self.api_key = api_key or os.getenv("API_SECRET_KEY")
        self.enabled = bool(self.api_key)
    
    async def verify_token(self, request: Request) -> bool:
        """
        验证请求的Token
        
        Args:
            request: FastAPI请求对象
            
        Returns:
            是否验证通过
            
        Raises:
            HTTPException: 验证失败时抛出
        """
        if not self.enabled:
            return True
        
        # 获取Authorization header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="缺少认证信息",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # 验证格式: Bearer <token>
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="认证格式错误",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        token = parts[1]
        
        # 验证token
        if token != self.api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="认证失败",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return True


def verify_api_key(api_key: str = None):
    """
    API密钥验证装饰器
    
    用法:
        @app.get("/protected")
        async def protected_route(authorized: bool = Depends(verify_api_key)):
            return {"message": "Success"}
    
    Args:
        api_key: 可选的API密钥，如果不提供则使用环境变量
    """
    expected_key = api_key or os.getenv("API_SECRET_KEY")
    
    async def verify(credentials: Optional[HTTPAuthorizationCredentials] = security):
        if not expected_key:
            # 如果没有配置密钥，则不验证
            return True
        
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="缺少认证信息",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        if credentials.credentials != expected_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="认证失败",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return True
    
    return verify


# 简单的IP白名单验证
class IPWhitelist:
    """IP白名单中间件"""
    
    def __init__(self, allowed_ips: list[str] = None):
        """
        初始化IP白名单
        
        Args:
            allowed_ips: 允许的IP地址列表
        """
        self.allowed_ips = allowed_ips or []
        self.enabled = bool(self.allowed_ips)
    
    async def verify_ip(self, request: Request) -> bool:
        """
        验证请求IP
        
        Args:
            request: FastAPI请求对象
            
        Returns:
            是否验证通过
            
        Raises:
            HTTPException: IP不在白名单时抛出
        """
        if not self.enabled:
            return True
        
        client_ip = request.client.host
        
        if client_ip not in self.allowed_ips:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"IP地址 {client_ip} 无权访问"
            )
        
        return True
