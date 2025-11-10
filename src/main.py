"""
TeyMCP-Server - 主入口
The One MCP to Rule Them All

Author: zf13883922290
License: MIT
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# 使用简化的聚合器
from src.core.simple_aggregator import SimpleMCPAggregator as MCPAggregator
from src.api.routes import setup_routes
from src.utils.logger import setup_logger, logger
from src.utils.config import load_app_config, load_servers_config

# Logo
LOGO = """
  _____         __  __  ____ ____  
 |_   _|__ _   _|  \/  |/ ___|  _ \ 
   | |/ _ \ | | | |\/| | |   | |_) |
   | |  __/ |_| | |  | | |___|  __/ 
   |_|\___|\__, |_|  |_|\____|_|    
           |___/                     
    ____                            
   / ___|  ___ _ ____   _____ _ __  
   \___ \ / _ \ '__\ \ / / _ \ '__| 
    ___) |  __/ |   \ V /  __/ |    
   |____/ \___|_|    \_/ \___|_|    
"""

# 创建FastAPI应用
app = FastAPI(
    title="TeyMCP-Server",
    description="The One MCP to Rule Them All - 统一管理所有MCP服务器的聚合器",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局聚合器实例
aggregator: MCPAggregator = None


@app.on_event("startup")
async def startup():
    """应用启动时初始化"""
    global aggregator
    
    print(LOGO)
    logger.info("🚀 启动 TeyMCP-Server...")
    
    # 设置日志
    setup_logger()
    
    # 加载应用配置
    app_config = load_app_config()
    
    # 创建聚合器实例
    aggregator = MCPAggregator()
    
    # 先设置路由，确保API可用
    setup_routes(app, aggregator)
    logger.info("✅ API路由已设置")
    
    # 加载服务器配置
    servers_config = load_servers_config()
    
    # 在后台异步初始化所有MCP服务器
    async def init_mcps():
        success_count = 0
        failed_count = 0
        
        for name, server_config in servers_config.get("servers", {}).items():
            if not server_config.get("enabled", True):
                logger.info(f"⏭️  跳过已禁用的服务器: {name}")
                continue
            
            # 检查服务器类型
            server_type = server_config.get("type", "stdio")
            
            logger.info(f"📡 连接服务器: {name} (类型: {server_type})")
            try:
                if server_type == "http":
                    # HTTP/SSE连接
                    success = await aggregator.add_http_server(
                        name=name,
                        url=server_config["url"],
                        headers=server_config.get("headers"),
                        timeout=server_config.get("timeout", 30.0)
                    )
                else:
                    # stdio连接
                    # 准备环境变量,为Node.js命令添加PATH
                    env = server_config.get("env") or {}
                    command = server_config["command"]
                    
                    # 如果是npx命令,添加Node.js到PATH
                    if "npx" in command or "node" in command:
                        import os
                        node_bin_dir = "/home/sun/TeyMCP-Server/.local/bin"
                        current_path = env.get("PATH", os.environ.get("PATH", ""))
                        env["PATH"] = f"{node_bin_dir}:{current_path}"
                    
                    success = await aggregator.add_server(
                        name=name,
                        command=command,
                        args=server_config["args"],
                        env=env,
                        working_dir=server_config.get("working_dir")
                    )
                
                if success:
                    success_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                logger.error(f"❌ {name} 初始化异常: {e}")
                failed_count += 1
        
        logger.info("=" * 50)
        logger.info(f"✅ 成功加载: {success_count} 个MCP服务器")
        if failed_count > 0:
            logger.warning(f"❌ 加载失败: {failed_count} 个MCP服务器")
        logger.info(f"🔧 提供工具: {len(aggregator.tool_registry)} 个")
        logger.info("=" * 50)
    
    # 启动后台任务初始化MCP
    asyncio.create_task(init_mcps())
    
    logger.info(f"🌐 访问管理面板: http://localhost:{app_config['port']}")
    logger.info(f"📚 API文档: http://localhost:{app_config['port']}/api/docs")
    logger.info("⏳ MCP服务器正在后台初始化...")


@app.on_event("shutdown")
async def shutdown():
    """应用关闭时清理"""
    logger.info("👋 关闭 TeyMCP-Server...")
    # 断开所有连接
    if aggregator:
        await aggregator.shutdown()


@app.get("/", include_in_schema=False)
async def root():
    """根路径重定向到管理面板"""
    return RedirectResponse(url="/dashboard")


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "servers": len(aggregator.upstream_clients) if aggregator else 0,
        "tools": len(aggregator.tool_registry) if aggregator else 0
    }


def main():
    """主函数"""
    # 加载配置
    config = load_app_config()
    
    # 启动服务
    uvicorn.run(
        "src.main:app",
        host=config.get("host", "0.0.0.0"),
        port=config.get("port", 8080),
        reload=config.get("reload", False),
        log_level=config.get("log_level", "info").lower()
    )


if __name__ == "__main__":
    main()
