#!/usr/bin/env python3
"""
简单的本地MCP服务器 - 提供基本工具用于测试
"""

import json
import sys
from datetime import datetime
import os

def get_server_info():
    """返回服务器信息"""
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {}
        },
        "serverInfo": {
            "name": "local-test-server",
            "version": "1.0.0"
        }
    }

def list_tools():
    """列出可用工具"""
    return {
        "tools": [
            {
                "name": "get_time",
                "description": "获取当前时间",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "echo",
                "description": "回显输入的文本",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "要回显的消息"
                        }
                    },
                    "required": ["message"]
                }
            },
            {
                "name": "list_files",
                "description": "列出指定目录的文件",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "目录路径"
                        }
                    },
                    "required": ["path"]
                }
            }
        ]
    }

def call_tool(name, arguments):
    """调用工具"""
    if name == "get_time":
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"当前时间: {datetime.now().isoformat()}"
                }
            ]
        }
    elif name == "echo":
        message = arguments.get("message", "")
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"回显: {message}"
                }
            ]
        }
    elif name == "list_files":
        path = arguments.get("path", ".")
        try:
            files = os.listdir(path)
            file_list = "\n".join(f"- {f}" for f in files[:20])  # 限制20个
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"目录 {path} 的文件:\n{file_list}"
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"错误: {str(e)}"
                    }
                ],
                "isError": True
            }
    else:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"未知工具: {name}"
                }
            ],
            "isError": True
        }

def handle_request(request):
    """处理JSON-RPC请求"""
    method = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")
    
    if method == "initialize":
        result = get_server_info()
    elif method == "tools/list":
        result = list_tools()
    elif method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments", {})
        result = call_tool(name, arguments)
    else:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }
    
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result
    }

def main():
    """主函数 - 处理stdio通信"""
    print("Local Test MCP Server running on stdio", file=sys.stderr)
    sys.stderr.flush()
    
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line)
            response = handle_request(request)
            
            print(json.dumps(response), flush=True)
            
        except json.JSONDecodeError as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {e}"
                }
            }
            print(json.dumps(error_response), flush=True)
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {e}"
                }
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    main()
