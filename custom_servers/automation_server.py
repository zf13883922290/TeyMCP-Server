#!/usr/bin/env python3
"""
自动化MCP服务器
提供文件创建、打包、压缩、代码生成等自动化功能
"""

import asyncio
import os
import sys
import json
import tarfile
import zipfile
import shutil
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime

# 添加MCP SDK路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("错误: 需要安装 mcp 包")
    print("运行: pip install mcp")
    sys.exit(1)


# 创建MCP服务器实例
server = Server("automation-server")


# ============================================================
# 工具1: 创建文件
# ============================================================

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="create_file",
            description="创建文件或目录",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "文件或目录路径"
                    },
                    "content": {
                        "type": "string",
                        "description": "文件内容(如果创建文件)"
                    },
                    "is_directory": {
                        "type": "boolean",
                        "description": "是否创建目录",
                        "default": False
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="compress_files",
            description="压缩文件或目录为zip或tar.gz格式",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_path": {
                        "type": "string",
                        "description": "要压缩的文件或目录路径"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "输出压缩包路径"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["zip", "tar.gz"],
                        "description": "压缩格式",
                        "default": "tar.gz"
                    }
                },
                "required": ["source_path", "output_path"]
            }
        ),
        Tool(
            name="generate_code",
            description="根据模板生成代码文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_type": {
                        "type": "string",
                        "enum": [
                            "python_script",
                            "python_class",
                            "fastapi_app",
                            "react_component",
                            "bash_script",
                            "dockerfile",
                            "makefile"
                        ],
                        "description": "代码模板类型"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "输出文件路径"
                    },
                    "params": {
                        "type": "object",
                        "description": "模板参数",
                        "additionalProperties": True
                    }
                },
                "required": ["template_type", "output_path"]
            }
        ),
        Tool(
            name="batch_rename",
            description="批量重命名文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "目录路径"
                    },
                    "pattern": {
                        "type": "string",
                        "description": "匹配模式(支持glob)"
                    },
                    "rename_rule": {
                        "type": "string",
                        "description": "重命名规则,如: {name}_{index}{ext}"
                    }
                },
                "required": ["directory", "pattern", "rename_rule"]
            }
        ),
        Tool(
            name="create_project",
            description="创建完整的项目结构",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_type": {
                        "type": "string",
                        "enum": [
                            "python",
                            "fastapi",
                            "react",
                            "nodejs",
                            "flask",
                            "django"
                        ],
                        "description": "项目类型"
                    },
                    "project_name": {
                        "type": "string",
                        "description": "项目名称"
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "输出目录"
                    }
                },
                "required": ["project_type", "project_name", "output_dir"]
            }
        ),
        Tool(
            name="remote_edit",
            description="通过SSH远程编辑文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "远程主机地址"
                    },
                    "port": {
                        "type": "integer",
                        "description": "SSH端口",
                        "default": 22
                    },
                    "username": {
                        "type": "string",
                        "description": "用户名"
                    },
                    "remote_path": {
                        "type": "string",
                        "description": "远程文件路径"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["read", "write", "append"],
                        "description": "操作类型"
                    },
                    "content": {
                        "type": "string",
                        "description": "文件内容(write/append时需要)"
                    }
                },
                "required": ["host", "username", "remote_path", "action"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """处理工具调用"""
    
    try:
        if name == "create_file":
            return await create_file_tool(arguments)
        elif name == "compress_files":
            return await compress_files_tool(arguments)
        elif name == "generate_code":
            return await generate_code_tool(arguments)
        elif name == "batch_rename":
            return await batch_rename_tool(arguments)
        elif name == "create_project":
            return await create_project_tool(arguments)
        elif name == "remote_edit":
            return await remote_edit_tool(arguments)
        else:
            return [TextContent(
                type="text",
                text=f"❌ 未知工具: {name}"
            )]
            
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 执行失败: {str(e)}"
        )]


# ============================================================
# 工具实现
# ============================================================

async def create_file_tool(args: dict) -> list[TextContent]:
    """创建文件或目录"""
    path = Path(args["path"])
    is_directory = args.get("is_directory", False)
    content = args.get("content", "")
    
    try:
        if is_directory:
            path.mkdir(parents=True, exist_ok=True)
            return [TextContent(
                type="text",
                text=f"✅ 目录创建成功: {path}"
            )]
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            return [TextContent(
                type="text",
                text=f"✅ 文件创建成功: {path}\n大小: {len(content)} 字节"
            )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 创建失败: {e}"
        )]


async def compress_files_tool(args: dict) -> list[TextContent]:
    """压缩文件或目录"""
    source = Path(args["source_path"])
    output = Path(args["output_path"])
    format_type = args.get("format", "tar.gz")
    
    if not source.exists():
        return [TextContent(
            type="text",
            text=f"❌ 源路径不存在: {source}"
        )]
    
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        
        if format_type == "zip":
            with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if source.is_file():
                    zipf.write(source, source.name)
                else:
                    for file in source.rglob('*'):
                        if file.is_file():
                            zipf.write(file, file.relative_to(source.parent))
        
        elif format_type == "tar.gz":
            with tarfile.open(output, 'w:gz') as tar:
                tar.add(source, arcname=source.name)
        
        size_mb = output.stat().st_size / (1024 * 1024)
        return [TextContent(
            type="text",
            text=f"✅ 压缩完成: {output}\n格式: {format_type}\n大小: {size_mb:.2f} MB"
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 压缩失败: {e}"
        )]


async def generate_code_tool(args: dict) -> list[TextContent]:
    """生成代码"""
    template_type = args["template_type"]
    output_path = Path(args["output_path"])
    params = args.get("params", {})
    
    # 代码模板
    templates = {
        "python_script": """#!/usr/bin/env python3
\"\"\"
{description}
\"\"\"

def main():
    print("Hello from {name}!")

if __name__ == "__main__":
    main()
""",
        "python_class": """\"\"\"
{description}
\"\"\"

class {class_name}:
    def __init__(self):
        pass
    
    def method(self):
        pass
""",
        "fastapi_app": """from fastapi import FastAPI

app = FastAPI(title=\"{name}\")

@app.get(\"/\")
async def root():
    return {{\"message\": \"Hello World\"}}

if __name__ == \"__main__\":
    import uvicorn
    uvicorn.run(app, host=\"0.0.0.0\", port=8000)
""",
        "bash_script": """#!/bin/bash

# {description}

set -e

echo "Running {name}..."
""",
        "dockerfile": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [\"python\", \"main.py\"]
""",
    }
    
    try:
        template = templates.get(template_type, "")
        code = template.format(
            name=params.get("name", "MyApp"),
            description=params.get("description", "自动生成的代码"),
            class_name=params.get("class_name", "MyClass")
        )
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(code, encoding='utf-8')
        
        # 如果是可执行文件,添加执行权限
        if template_type in ["python_script", "bash_script"]:
            os.chmod(output_path, 0o755)
        
        return [TextContent(
            type="text",
            text=f"✅ 代码生成成功: {output_path}\n类型: {template_type}\n大小: {len(code)} 字节"
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 生成失败: {e}"
        )]


async def batch_rename_tool(args: dict) -> list[TextContent]:
    """批量重命名文件"""
    directory = Path(args["directory"])
    pattern = args["pattern"]
    rename_rule = args["rename_rule"]
    
    if not directory.exists():
        return [TextContent(
            type="text",
            text=f"❌ 目录不存在: {directory}"
        )]
    
    try:
        files = list(directory.glob(pattern))
        renamed_count = 0
        
        for index, file in enumerate(files, 1):
            if file.is_file():
                new_name = rename_rule.format(
                    name=file.stem,
                    index=index,
                    ext=file.suffix
                )
                new_path = file.parent / new_name
                file.rename(new_path)
                renamed_count += 1
        
        return [TextContent(
            type="text",
            text=f"✅ 重命名完成\n处理文件: {renamed_count} 个"
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 重命名失败: {e}"
        )]


async def create_project_tool(args: dict) -> list[TextContent]:
    """创建项目结构"""
    project_type = args["project_type"]
    project_name = args["project_name"]
    output_dir = Path(args["output_dir"]) / project_name
    
    # 项目结构定义
    structures = {
        "python": {
            "dirs": ["src", "tests", "docs"],
            "files": {
                "README.md": f"# {project_name}\n",
                "requirements.txt": "",
                ".gitignore": "__pycache__/\n*.pyc\nvenv/\n",
                "src/__init__.py": "",
                "src/main.py": "def main():\n    pass\n"
            }
        },
        "fastapi": {
            "dirs": ["src", "tests", "docs"],
            "files": {
                "README.md": f"# {project_name}\n",
                "requirements.txt": "fastapi\nuvicorn[standard]\n",
                ".gitignore": "__pycache__/\n*.pyc\nvenv/\n",
                "src/main.py": "from fastapi import FastAPI\n\napp = FastAPI()\n"
            }
        }
    }
    
    try:
        structure = structures.get(project_type, structures["python"])
        
        # 创建目录
        for dir_name in structure["dirs"]:
            (output_dir / dir_name).mkdir(parents=True, exist_ok=True)
        
        # 创建文件
        for file_path, content in structure["files"].items():
            file = output_dir / file_path
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(content)
        
        return [TextContent(
            type="text",
            text=f"✅ 项目创建成功: {output_dir}\n类型: {project_type}"
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 创建项目失败: {e}"
        )]


async def remote_edit_tool(args: dict) -> list[TextContent]:
    """远程编辑文件 (需要paramiko库)"""
    try:
        import paramiko
    except ImportError:
        return [TextContent(
            type="text",
            text="❌ 需要安装paramiko: pip install paramiko"
        )]
    
    host = args["host"]
    port = args.get("port", 22)
    username = args["username"]
    remote_path = args["remote_path"]
    action = args["action"]
    content = args.get("content", "")
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username)
        
        sftp = ssh.open_sftp()
        
        if action == "read":
            with sftp.file(remote_path, 'r') as f:
                file_content = f.read().decode('utf-8')
            result = f"✅ 读取成功\n内容:\n{file_content[:500]}..."
            
        elif action == "write":
            with sftp.file(remote_path, 'w') as f:
                f.write(content.encode('utf-8'))
            result = f"✅ 写入成功: {remote_path}"
            
        elif action == "append":
            with sftp.file(remote_path, 'a') as f:
                f.write(content.encode('utf-8'))
            result = f"✅ 追加成功: {remote_path}"
        
        sftp.close()
        ssh.close()
        
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 远程操作失败: {e}"
        )]


# ============================================================
# 主函数
# ============================================================

async def main():
    """启动MCP服务器"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="automation-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
