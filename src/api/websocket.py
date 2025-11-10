"""
WebSocket实时推送（优化版本，支持消息批处理和速率限制）
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
import json
import asyncio
import time
from collections import deque

router = APIRouter()

# 全局WebSocket连接池
active_connections: List[WebSocket] = []

# Message queue for batching
_message_queue: deque = deque(maxlen=1000)
_last_broadcast_time = 0
_broadcast_interval = 0.1  # Broadcast every 100ms max
_broadcast_task = None


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
        if websocket in active_connections:
            active_connections.remove(websocket)


async def _broadcast_worker():
    """Background worker to batch and broadcast messages"""
    global _last_broadcast_time
    
    while True:
        try:
            await asyncio.sleep(_broadcast_interval)
            
            if not _message_queue:
                continue
            
            # Batch messages
            messages = []
            while _message_queue and len(messages) < 10:  # Max 10 messages per batch
                messages.append(_message_queue.popleft())
            
            if not messages:
                continue
            
            # Broadcast batch
            dead_connections = []
            batch_data = json.dumps({"batch": messages})
            
            # Send to all connections concurrently
            send_tasks = []
            for connection in active_connections:
                send_tasks.append(_send_safe(connection, batch_data, dead_connections))
            
            if send_tasks:
                await asyncio.gather(*send_tasks, return_exceptions=True)
            
            # Clean up dead connections
            for connection in dead_connections:
                if connection in active_connections:
                    active_connections.remove(connection)
            
            _last_broadcast_time = time.time()
            
        except Exception as e:
            print(f"Broadcast worker error: {e}")
            await asyncio.sleep(1)


async def _send_safe(connection: WebSocket, data: str, dead_connections: List[WebSocket]):
    """Send data to a connection safely"""
    try:
        await asyncio.wait_for(connection.send_text(data), timeout=1.0)
    except Exception:
        dead_connections.append(connection)


async def broadcast_message(message: dict):
    """
    广播消息到所有连接的客户端（优化版本，使用批处理）
    Messages are queued and sent in batches for better performance
    """
    global _broadcast_task
    
    # Add message to queue
    _message_queue.append(message)
    
    # Start broadcast worker if not running
    if _broadcast_task is None or _broadcast_task.done():
        _broadcast_task = asyncio.create_task(_broadcast_worker())


async def broadcast_message_immediate(message: dict):
    """
    Immediately broadcast a message (for critical updates)
    Use sparingly as it bypasses batching optimization
    """
    if not active_connections:
        return
    
    dead_connections = []
    data = json.dumps(message)
    
    # Send to all connections concurrently
    send_tasks = []
    for connection in active_connections:
        send_tasks.append(_send_safe(connection, data, dead_connections))
    
    if send_tasks:
        await asyncio.gather(*send_tasks, return_exceptions=True)
    
    # Clean up dead connections
    for connection in dead_connections:
        if connection in active_connections:
            active_connections.remove(connection)
