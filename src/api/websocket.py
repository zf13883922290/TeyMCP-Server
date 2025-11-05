"""
WebSocket实时推送
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
import asyncio

router = APIRouter()

# 全局WebSocket连接池
active_connections: List[WebSocket] = []


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket连接端点"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # 接收客户端消息
            data = await websocket.receive_text()
            
            # 可以处理客户端请求
            # 这里简单echo回去
            await websocket.send_text(f"收到消息: {data}")
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)


async def broadcast_message(message: dict):
    """广播消息到所有连接的客户端"""
    dead_connections = []
    
    for connection in active_connections:
        try:
            await connection.send_text(json.dumps(message))
        except:
            dead_connections.append(connection)
    
    # 清理断开的连接
    for connection in dead_connections:
        active_connections.remove(connection)
