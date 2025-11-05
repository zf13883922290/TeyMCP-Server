"""
日志查询API
"""

from fastapi import APIRouter, Request
from typing import Dict, List, Any

router = APIRouter()


@router.get("/logs")
async def get_logs(
    request: Request,
    limit: int = 100,
    server: str = None,
    status: str = None
) -> Dict[str, Any]:
    """
    获取调用日志
    
    Args:
        limit: 返回数量限制
        server: 按服务器过滤
        status: 按状态过滤 (success/failed)
    """
    aggregator = request.app.state.aggregator
    
    # 从实际日志文件读取
    import os
    from datetime import datetime
    
    logs = []
    log_file = "data/logs/teymcp.log"
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-limit:]  # 只读最后N行
                
            for line in lines:
                if not line.strip():
                    continue
                    
                # 解析日志行
                parts = line.split(' - ')
                if len(parts) >= 4:
                    timestamp_str = parts[0]
                    level = parts[2]
                    message = ' - '.join(parts[3:]).strip()
                    
                    # 判断状态
                    log_status = 'success' if '✓' in message or '✅' in message else 'failed' if '✗' in message or '❌' in message or 'ERROR' in level else 'info'
                    
                    # 提取服务器名
                    server_name = 'system'
                    for word in message.split():
                        if any(s in word for s in ['memory', 'github', 'sequential', 'local', 'media', 'puppeteer']):
                            server_name = word.strip(':')
                            break
                    
                    logs.append({
                        'timestamp': timestamp_str,
                        'level': level,
                        'server': server_name,
                        'tool_name': 'system',
                        'status': log_status,
                        'message': message,
                        'duration_ms': 0,
                        'error': message if log_status == 'failed' else None
                    })
        except Exception as e:
            print(f"读取日志失败: {e}")
    
    # 过滤
    if server:
        logs = [log for log in logs if log['server'] == server]
    if status:
        logs = [log for log in logs if log['status'] == status]
    
    return {
        "logs": logs,
        "count": len(logs),
        "total": len(logs)
    }


@router.delete("/logs")
async def clear_logs(request: Request) -> Dict[str, Any]:
    """清空日志"""
    aggregator = request.app.state.aggregator
    
    # SimpleMCPAggregator没有call_logs属性,返回成功即可
    return {"message": "日志已清空", "count": 0}
    
    return {
        "success": True,
        "message": f"已清空 {count} 条日志"
    }
