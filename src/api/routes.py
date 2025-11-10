"""
API路由配置
"""

from fastapi import FastAPI

from src.api.status import router as status_router
from src.api.servers import router as servers_router
from src.api.tools import router as tools_router
from src.api.logs import router as logs_router
from src.api.websocket import router as websocket_router
from src.web.dashboard import router as dashboard_router


def setup_routes(app: FastAPI, aggregator):
    """
    设置所有路由
    
    Args:
        app: FastAPI应用实例
        aggregator: MCP聚合器实例
    """
    # 将aggregator注入到app.state中，供各个路由使用
    app.state.aggregator = aggregator
    
    # 注册路由
    app.include_router(dashboard_router, tags=["Web界面"])
    app.include_router(status_router, prefix="/api", tags=["状态"])
    app.include_router(servers_router, prefix="/api", tags=["服务器管理"])
    app.include_router(tools_router, prefix="/api", tags=["工具管理"])
    app.include_router(logs_router, prefix="/api", tags=["日志"])
    app.include_router(websocket_router, tags=["实时通讯"])
