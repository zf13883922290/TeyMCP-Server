"""
CORS中间件
处理跨域请求
"""

from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware
from typing import List


class CORSMiddleware:
    """
    CORS中间件配置
    """
    
    @staticmethod
    def get_default_config() -> dict:
        """
        获取默认CORS配置
        
        Returns:
            CORS配置字典
        """
        return {
            "allow_origins": ["*"],  # 生产环境应该指定具体域名
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }
    
    @staticmethod
    def get_production_config(allowed_origins: List[str]) -> dict:
        """
        获取生产环境CORS配置
        
        Args:
            allowed_origins: 允许的源列表
            
        Returns:
            CORS配置字典
        """
        return {
            "allow_origins": allowed_origins,
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["*"],
            "expose_headers": ["X-Request-ID"],
            "max_age": 3600,  # 预检请求缓存时间（秒）
        }
    
    @staticmethod
    def get_restricted_config() -> dict:
        """
        获取受限的CORS配置（最安全）
        
        Returns:
            CORS配置字典
        """
        return {
            "allow_origins": ["http://localhost:3000"],
            "allow_credentials": True,
            "allow_methods": ["GET", "POST"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": [],
            "max_age": 600,
        }


def setup_cors(app, allowed_origins: List[str] = None):
    """
    设置CORS中间件
    
    Args:
        app: FastAPI应用实例
        allowed_origins: 允许的源列表
    """
    if allowed_origins:
        config = CORSMiddleware.get_production_config(allowed_origins)
    else:
        config = CORSMiddleware.get_default_config()
    
    app.add_middleware(
        FastAPICORSMiddleware,
        **config
    )
