#!/usr/bin/env python3
"""
媒体生成MCP服务器
提供AI图片生成、视频生成、图片编辑等功能
"""

import asyncio
import os
import sys
import json
import base64
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime

# 添加MCP SDK路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
except ImportError:
    print("错误: 需要安装 mcp 包")
    print("运行: pip install mcp")
    sys.exit(1)


# 创建MCP服务器实例
server = Server("media-generator")


# ============================================================
# 工具列表
# ============================================================

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="generate_image_dalle",
            description="使用DALL-E生成图片",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "图片描述提示词"
                    },
                    "size": {
                        "type": "string",
                        "enum": ["1024x1024", "1792x1024", "1024x1792"],
                        "description": "图片尺寸",
                        "default": "1024x1024"
                    },
                    "quality": {
                        "type": "string",
                        "enum": ["standard", "hd"],
                        "description": "图片质量",
                        "default": "standard"
                    },
                    "style": {
                        "type": "string",
                        "enum": ["natural", "vivid"],
                        "description": "图片风格",
                        "default": "vivid"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "保存路径"
                    }
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="generate_image_sd",
            description="使用Stable Diffusion生成图片",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "正向提示词"
                    },
                    "negative_prompt": {
                        "type": "string",
                        "description": "负向提示词",
                        "default": "ugly, blurry, low quality"
                    },
                    "width": {
                        "type": "integer",
                        "description": "图片宽度",
                        "default": 1024
                    },
                    "height": {
                        "type": "integer",
                        "description": "图片高度",
                        "default": 1024
                    },
                    "steps": {
                        "type": "integer",
                        "description": "生成步数",
                        "default": 30
                    },
                    "cfg_scale": {
                        "type": "number",
                        "description": "CFG权重",
                        "default": 7.5
                    },
                    "output_path": {
                        "type": "string",
                        "description": "保存路径"
                    }
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="edit_image",
            description="编辑图片（裁剪、调整大小、滤镜）",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "输入图片路径"
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["crop", "resize", "rotate", "filter"],
                        "description": "操作类型"
                    },
                    "params": {
                        "type": "object",
                        "description": "操作参数",
                        "additionalProperties": True
                    },
                    "output_path": {
                        "type": "string",
                        "description": "输出路径"
                    }
                },
                "required": ["input_path", "operation", "output_path"]
            }
        ),
        Tool(
            name="convert_image",
            description="转换图片格式",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "输入图片路径"
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["png", "jpg", "webp", "gif", "bmp"],
                        "description": "输出格式"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "输出路径"
                    },
                    "quality": {
                        "type": "integer",
                        "description": "质量(1-100)",
                        "default": 90
                    }
                },
                "required": ["input_path", "output_format", "output_path"]
            }
        ),
        Tool(
            name="generate_video",
            description="生成视频（从图片序列或AI生成）",
            inputSchema={
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": ["from_images", "text_to_video"],
                        "description": "生成模式"
                    },
                    "input_source": {
                        "type": "string",
                        "description": "输入源（图片目录或提示词）"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "输出视频路径"
                    },
                    "fps": {
                        "type": "integer",
                        "description": "帧率",
                        "default": 30
                    },
                    "duration": {
                        "type": "number",
                        "description": "时长(秒,text_to_video模式)",
                        "default": 5
                    }
                },
                "required": ["mode", "input_source", "output_path"]
            }
        ),
        Tool(
            name="add_watermark",
            description="给图片添加水印",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "输入图片路径"
                    },
                    "watermark_text": {
                        "type": "string",
                        "description": "水印文字"
                    },
                    "position": {
                        "type": "string",
                        "enum": ["top-left", "top-right", "bottom-left", "bottom-right", "center"],
                        "description": "水印位置",
                        "default": "bottom-right"
                    },
                    "opacity": {
                        "type": "number",
                        "description": "透明度(0-1)",
                        "default": 0.5
                    },
                    "output_path": {
                        "type": "string",
                        "description": "输出路径"
                    }
                },
                "required": ["input_path", "watermark_text", "output_path"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """处理工具调用"""
    
    try:
        if name == "generate_image_dalle":
            return await generate_image_dalle(arguments)
        elif name == "generate_image_sd":
            return await generate_image_sd(arguments)
        elif name == "edit_image":
            return await edit_image(arguments)
        elif name == "convert_image":
            return await convert_image(arguments)
        elif name == "generate_video":
            return await generate_video(arguments)
        elif name == "add_watermark":
            return await add_watermark(arguments)
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

async def generate_image_dalle(args: dict) -> list[TextContent]:
    """使用DALL-E生成图片"""
    try:
        from openai import AsyncOpenAI
    except ImportError:
        return [TextContent(
            type="text",
            text="❌ 需要安装OpenAI SDK: pip install openai"
        )]
    
    prompt = args["prompt"]
    size = args.get("size", "1024x1024")
    quality = args.get("quality", "standard")
    style = args.get("style", "vivid")
    output_path = args.get("output_path")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return [TextContent(
            type="text",
            text="❌ 未设置 OPENAI_API_KEY 环境变量"
        )]
    
    try:
        client = AsyncOpenAI(api_key=api_key)
        
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            style=style,
            n=1
        )
        
        image_url = response.data[0].url
        
        # 下载图片
        if output_path:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    image_data = await resp.read()
                    Path(output_path).write_bytes(image_data)
            
            return [TextContent(
                type="text",
                text=f"✅ 图片生成成功\n保存位置: {output_path}\n提示词: {prompt}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"✅ 图片生成成功\nURL: {image_url}\n提示词: {prompt}"
            )]
            
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ DALL-E生成失败: {e}"
        )]


async def generate_image_sd(args: dict) -> list[TextContent]:
    """使用Stable Diffusion生成图片"""
    try:
        from stability_sdk import client
        import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
    except ImportError:
        return [TextContent(
            type="text",
            text="❌ 需要安装Stability SDK: pip install stability-sdk"
        )]
    
    prompt = args["prompt"]
    negative_prompt = args.get("negative_prompt", "")
    width = args.get("width", 1024)
    height = args.get("height", 1024)
    steps = args.get("steps", 30)
    cfg_scale = args.get("cfg_scale", 7.5)
    output_path = args.get("output_path")
    
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        return [TextContent(
            type="text",
            text="❌ 未设置 STABILITY_API_KEY 环境变量"
        )]
    
    try:
        stability_api = client.StabilityInference(
            key=api_key,
            engine="stable-diffusion-xl-1024-v1-0"
        )
        
        answers = stability_api.generate(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            steps=steps,
            cfg_scale=cfg_scale,
            samples=1
        )
        
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.type == generation.ARTIFACT_IMAGE:
                    if output_path:
                        Path(output_path).write_bytes(artifact.binary)
                        return [TextContent(
                            type="text",
                            text=f"✅ 图片生成成功\n保存位置: {output_path}\n尺寸: {width}x{height}"
                        )]
                        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Stable Diffusion生成失败: {e}"
        )]


async def edit_image(args: dict) -> list[TextContent]:
    """编辑图片"""
    try:
        from PIL import Image, ImageFilter, ImageEnhance
    except ImportError:
        return [TextContent(
            type="text",
            text="❌ 需要安装Pillow: pip install Pillow"
        )]
    
    input_path = Path(args["input_path"])
    operation = args["operation"]
    params = args.get("params", {})
    output_path = Path(args["output_path"])
    
    if not input_path.exists():
        return [TextContent(
            type="text",
            text=f"❌ 输入图片不存在: {input_path}"
        )]
    
    try:
        img = Image.open(input_path)
        
        if operation == "crop":
            # 裁剪: params = {"left": 0, "top": 0, "right": 500, "bottom": 500}
            box = (
                params.get("left", 0),
                params.get("top", 0),
                params.get("right", img.width),
                params.get("bottom", img.height)
            )
            img = img.crop(box)
            
        elif operation == "resize":
            # 调整大小: params = {"width": 800, "height": 600}
            width = params.get("width", img.width)
            height = params.get("height", img.height)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            
        elif operation == "rotate":
            # 旋转: params = {"angle": 90}
            angle = params.get("angle", 0)
            img = img.rotate(angle, expand=True)
            
        elif operation == "filter":
            # 滤镜: params = {"type": "blur", "radius": 2}
            filter_type = params.get("type", "blur")
            if filter_type == "blur":
                radius = params.get("radius", 2)
                img = img.filter(ImageFilter.GaussianBlur(radius))
            elif filter_type == "sharpen":
                img = img.filter(ImageFilter.SHARPEN)
            elif filter_type == "edge":
                img = img.filter(ImageFilter.FIND_EDGES)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path)
        
        return [TextContent(
            type="text",
            text=f"✅ 图片编辑成功\n操作: {operation}\n输出: {output_path}"
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 编辑失败: {e}"
        )]


async def convert_image(args: dict) -> list[TextContent]:
    """转换图片格式"""
    try:
        from PIL import Image
    except ImportError:
        return [TextContent(
            type="text",
            text="❌ 需要安装Pillow: pip install Pillow"
        )]
    
    input_path = Path(args["input_path"])
    output_format = args["output_format"]
    output_path = Path(args["output_path"])
    quality = args.get("quality", 90)
    
    if not input_path.exists():
        return [TextContent(
            type="text",
            text=f"❌ 输入图片不存在: {input_path}"
        )]
    
    try:
        img = Image.open(input_path)
        
        # 确保输出路径有正确的扩展名
        if not output_path.suffix:
            output_path = output_path.with_suffix(f".{output_format}")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存
        save_kwargs = {}
        if output_format in ["jpg", "jpeg"]:
            img = img.convert("RGB")
            save_kwargs["quality"] = quality
        elif output_format == "webp":
            save_kwargs["quality"] = quality
        
        img.save(output_path, format=output_format.upper(), **save_kwargs)
        
        return [TextContent(
            type="text",
            text=f"✅ 格式转换成功\n输入: {input_path}\n输出: {output_path}\n格式: {output_format}"
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 转换失败: {e}"
        )]


async def generate_video(args: dict) -> list[TextContent]:
    """生成视频"""
    mode = args["mode"]
    input_source = args["input_source"]
    output_path = Path(args["output_path"])
    fps = args.get("fps", 30)
    duration = args.get("duration", 5)
    
    if mode == "from_images":
        # 从图片序列生成视频
        try:
            import cv2
            import numpy as np
        except ImportError:
            return [TextContent(
                type="text",
                text="❌ 需要安装opencv: pip install opencv-python"
            )]
        
        try:
            image_dir = Path(input_source)
            if not image_dir.exists():
                return [TextContent(
                    type="text",
                    text=f"❌ 图片目录不存在: {image_dir}"
                )]
            
            images = sorted(image_dir.glob("*.png")) + sorted(image_dir.glob("*.jpg"))
            if not images:
                return [TextContent(
                    type="text",
                    text=f"❌ 目录中没有找到图片"
                )]
            
            # 读取第一张图片获取尺寸
            frame = cv2.imread(str(images[0]))
            height, width, _ = frame.shape
            
            # 创建视频写入器
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
            
            # 写入所有图片
            for image_path in images:
                frame = cv2.imread(str(image_path))
                video.write(frame)
            
            video.release()
            
            return [TextContent(
                type="text",
                text=f"✅ 视频生成成功\n输出: {output_path}\n帧数: {len(images)}\n帧率: {fps}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 视频生成失败: {e}"
            )]
    
    elif mode == "text_to_video":
        # AI文本生成视频 (需要API)
        return [TextContent(
            type="text",
            text="⚠️ text_to_video 模式需要配置视频生成API\n可用服务: Runway, Pika Labs, Stability AI"
        )]


async def add_watermark(args: dict) -> list[TextContent]:
    """添加水印"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return [TextContent(
            type="text",
            text="❌ 需要安装Pillow: pip install Pillow"
        )]
    
    input_path = Path(args["input_path"])
    watermark_text = args["watermark_text"]
    position = args.get("position", "bottom-right")
    opacity = args.get("opacity", 0.5)
    output_path = Path(args["output_path"])
    
    if not input_path.exists():
        return [TextContent(
            type="text",
            text=f"❌ 输入图片不存在: {input_path}"
        )]
    
    try:
        img = Image.open(input_path).convert("RGBA")
        
        # 创建水印层
        watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)
        
        # 尝试使用字体
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        # 计算文字位置
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        if position == "top-left":
            pos = (10, 10)
        elif position == "top-right":
            pos = (img.width - text_width - 10, 10)
        elif position == "bottom-left":
            pos = (10, img.height - text_height - 10)
        elif position == "bottom-right":
            pos = (img.width - text_width - 10, img.height - text_height - 10)
        else:  # center
            pos = ((img.width - text_width) // 2, (img.height - text_height) // 2)
        
        # 绘制水印
        alpha = int(255 * opacity)
        draw.text(pos, watermark_text, fill=(255, 255, 255, alpha), font=font)
        
        # 合并
        result = Image.alpha_composite(img, watermark)
        result = result.convert("RGB")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        result.save(output_path)
        
        return [TextContent(
            type="text",
            text=f"✅ 水印添加成功\n输出: {output_path}"
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 添加水印失败: {e}"
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
                server_name="media-generator",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
