#!/usr/bin/env python3
"""
Time MCP Server - 时间和时区工具
提供时间查询、转换、计算等功能
"""

import asyncio
import json
from datetime import datetime, timezone, timedelta
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
import pytz

# 创建服务器实例
app = Server("time")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="get_current_time",
            description="获取当前时间(支持时区)",
            inputSchema={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "时区名称，如: UTC, Asia/Shanghai, America/New_York",
                        "default": "UTC"
                    },
                    "format": {
                        "type": "string", 
                        "description": "时间格式: iso/unix/readable",
                        "default": "iso"
                    }
                }
            }
        ),
        Tool(
            name="convert_timezone",
            description="转换时区",
            inputSchema={
                "type": "object",
                "properties": {
                    "time": {
                        "type": "string",
                        "description": "时间字符串(ISO格式)"
                    },
                    "from_tz": {
                        "type": "string",
                        "description": "源时区"
                    },
                    "to_tz": {
                        "type": "string",
                        "description": "目标时区"
                    }
                },
                "required": ["time", "from_tz", "to_tz"]
            }
        ),
        Tool(
            name="time_difference",
            description="计算两个时间的差值",
            inputSchema={
                "type": "object",
                "properties": {
                    "time1": {
                        "type": "string",
                        "description": "第一个时间(ISO格式)"
                    },
                    "time2": {
                        "type": "string",
                        "description": "第二个时间(ISO格式)"
                    }
                },
                "required": ["time1", "time2"]
            }
        ),
        Tool(
            name="add_time",
            description="时间加减运算",
            inputSchema={
                "type": "object",
                "properties": {
                    "time": {
                        "type": "string",
                        "description": "基准时间(ISO格式)"
                    },
                    "days": {
                        "type": "number",
                        "description": "增加的天数(可为负数)",
                        "default": 0
                    },
                    "hours": {
                        "type": "number",
                        "description": "增加的小时数(可为负数)",
                        "default": 0
                    },
                    "minutes": {
                        "type": "number",
                        "description": "增加的分钟数(可为负数)",
                        "default": 0
                    }
                },
                "required": ["time"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """处理工具调用"""
    
    if name == "get_current_time":
        tz_name = arguments.get("timezone", "UTC")
        fmt = arguments.get("format", "iso")
        
        try:
            tz = pytz.timezone(tz_name)
            now = datetime.now(tz)
            
            if fmt == "unix":
                result = str(int(now.timestamp()))
            elif fmt == "readable":
                result = now.strftime("%Y年%m月%d日 %H:%M:%S %Z")
            else:  # iso
                result = now.isoformat()
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "time": result,
                    "timezone": tz_name,
                    "format": fmt
                }, ensure_ascii=False, indent=2)
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"错误: {str(e)}")]
    
    elif name == "convert_timezone":
        try:
            time_str = arguments["time"]
            from_tz = pytz.timezone(arguments["from_tz"])
            to_tz = pytz.timezone(arguments["to_tz"])
            
            # 解析时间
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            if dt.tzinfo is None:
                dt = from_tz.localize(dt)
            
            # 转换时区
            converted = dt.astimezone(to_tz)
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "original": time_str,
                    "from_timezone": arguments["from_tz"],
                    "to_timezone": arguments["to_tz"],
                    "result": converted.isoformat()
                }, ensure_ascii=False, indent=2)
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"错误: {str(e)}")]
    
    elif name == "time_difference":
        try:
            time1 = datetime.fromisoformat(arguments["time1"].replace('Z', '+00:00'))
            time2 = datetime.fromisoformat(arguments["time2"].replace('Z', '+00:00'))
            
            diff = abs(time2 - time1)
            days = diff.days
            hours, remainder = divmod(diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "time1": arguments["time1"],
                    "time2": arguments["time2"],
                    "difference": {
                        "days": days,
                        "hours": hours,
                        "minutes": minutes,
                        "seconds": seconds,
                        "total_seconds": diff.total_seconds()
                    }
                }, ensure_ascii=False, indent=2)
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"错误: {str(e)}")]
    
    elif name == "add_time":
        try:
            base_time = datetime.fromisoformat(arguments["time"].replace('Z', '+00:00'))
            days = arguments.get("days", 0)
            hours = arguments.get("hours", 0)
            minutes = arguments.get("minutes", 0)
            
            delta = timedelta(days=days, hours=hours, minutes=minutes)
            new_time = base_time + delta
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "original": arguments["time"],
                    "added": {
                        "days": days,
                        "hours": hours,
                        "minutes": minutes
                    },
                    "result": new_time.isoformat()
                }, ensure_ascii=False, indent=2)
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"错误: {str(e)}")]
    
    return [TextContent(type="text", text=f"未知工具: {name}")]

async def main():
    """运行服务器"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
