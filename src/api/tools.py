"""
工具管理API
"""

from fastapi import APIRouter, Request, HTTPException
from typing import Dict, List, Any
from pydantic import BaseModel

router = APIRouter()


class ToolCallRequest(BaseModel):
    """工具调用请求模型"""
    arguments: Dict[str, Any] = {}


@router.get("/tools")
async def list_tools(request: Request) -> Dict[str, Any]:
    """列出所有可用工具"""
    aggregator = request.app.state.aggregator
    
    tools = aggregator.get_all_tools()
    
    return {
        "tools": tools,
        "count": len(tools)
    }


@router.get("/tools/{tool_name}")
async def get_tool(tool_name: str, request: Request) -> Dict[str, Any]:
    """获取工具详情"""
    aggregator = request.app.state.aggregator
    
    if tool_name not in aggregator.tool_registry:
        raise HTTPException(status_code=404, detail="工具不存在")
    
    server_name = aggregator.tool_registry[tool_name]
    
    return {
        "name": tool_name,
        "server": server_name,
        "status": "healthy" if server_name in aggregator.clients else "unhealthy"
    }


@router.post("/tools/{tool_name}/call")
async def call_tool(
    tool_name: str,
    request_data: ToolCallRequest,
    request: Request
) -> Dict[str, Any]:
    """调用工具"""
    aggregator = request.app.state.aggregator
    
    if tool_name not in aggregator.tool_registry:
        raise HTTPException(status_code=404, detail="工具不存在")
    
    result = await aggregator.call_tool(tool_name, request_data.arguments)
    
    return {
        "success": True,
        "result": [item.dict() if hasattr(item, 'dict') else str(item) for item in result]
    }


@router.post("/tools/{tool_name}/test")
async def test_tool(
    tool_name: str,
    request_data: ToolCallRequest,
    request: Request
) -> Dict[str, Any]:
    """测试工具调用"""
    import time
    start_time = time.time()
    
    aggregator = request.app.state.aggregator
    
    if tool_name not in aggregator.tool_registry:
        raise HTTPException(status_code=404, detail="工具不存在")
    
    try:
        result = await aggregator.call_tool(tool_name, request_data.arguments)
        duration_ms = int((time.time() - start_time) * 1000)
        
        return {
            "success": True,
            "result": [item.dict() if hasattr(item, 'dict') else str(item) for item in result],
            "duration_ms": duration_ms
        }
    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        return {
            "success": False,
            "error": str(e),
            "duration_ms": duration_ms
        }
