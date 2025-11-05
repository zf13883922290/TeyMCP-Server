#!/usr/bin/env python3
"""
HuggingFace MCP Server - 自定义实现

提供 HuggingFace Hub 的模型、数据集和空间访问能力。
使用 FastMCP 框架和 HuggingFace Hub API。
"""

import os
import sys
from typing import Optional, Dict, List, Any

try:
    from mcp.server.fastmcp import FastMCP
    from huggingface_hub import HfApi, hf_hub_download, list_models, list_datasets
    from huggingface_hub.utils import HfHubHTTPError
except ImportError as e:
    print(f"❌ 缺少依赖: {e}", file=sys.stderr)
    print("请运行: pip install mcp huggingface-hub", file=sys.stderr)
    sys.exit(1)

# 创建 MCP 服务器实例
mcp = FastMCP("huggingface")

# 初始化 HuggingFace API 客户端
token = os.getenv("HUGGINGFACE_TOKEN")
if not token:
    print("⚠️  警告: HUGGINGFACE_TOKEN 未设置,某些功能可能受限", file=sys.stderr)

api = HfApi(token=token)


@mcp.tool()
def search_models(
    query: str,
    limit: int = 10,
    sort: str = "downloads",
    direction: int = -1
) -> List[Dict[str, Any]]:
    """
    搜索 HuggingFace 模型
    
    Args:
        query: 搜索关键词
        limit: 返回结果数量限制 (默认: 10)
        sort: 排序字段 (downloads/likes/trending/created_at)
        direction: 排序方向 (-1=降序, 1=升序)
    
    Returns:
        模型列表,包含 id、作者、下载量、点赞数等信息
    """
    try:
        models = list(api.list_models(
            search=query,
            limit=limit,
            sort=sort,
            direction=direction
        ))
        
        return [{
            "id": model.id,
            "author": model.author if hasattr(model, 'author') else None,
            "downloads": model.downloads if hasattr(model, 'downloads') else 0,
            "likes": model.likes if hasattr(model, 'likes') else 0,
            "tags": model.tags if hasattr(model, 'tags') else [],
            "pipeline_tag": model.pipeline_tag if hasattr(model, 'pipeline_tag') else None,
            "created_at": str(model.created_at) if hasattr(model, 'created_at') else None,
        } for model in models]
    except Exception as e:
        return {"error": f"搜索模型失败: {str(e)}"}


@mcp.tool()
def get_model_info(model_id: str) -> Dict[str, Any]:
    """
    获取模型详细信息
    
    Args:
        model_id: 模型ID (例如: bert-base-uncased, gpt2)
    
    Returns:
        模型的详细信息,包括元数据、文件列表、标签等
    """
    try:
        info = api.model_info(model_id)
        
        return {
            "id": info.id,
            "author": info.author if hasattr(info, 'author') else None,
            "sha": info.sha if hasattr(info, 'sha') else None,
            "downloads": info.downloads if hasattr(info, 'downloads') else 0,
            "likes": info.likes if hasattr(info, 'likes') else 0,
            "tags": info.tags if hasattr(info, 'tags') else [],
            "pipeline_tag": info.pipeline_tag if hasattr(info, 'pipeline_tag') else None,
            "library_name": info.library_name if hasattr(info, 'library_name') else None,
            "created_at": str(info.created_at) if hasattr(info, 'created_at') else None,
            "last_modified": str(info.last_modified) if hasattr(info, 'last_modified') else None,
            "card_data": info.card_data.to_dict() if hasattr(info, 'card_data') and info.card_data else {},
            "siblings": [{"rfilename": f.rfilename, "size": f.size} for f in info.siblings] if hasattr(info, 'siblings') else []
        }
    except HfHubHTTPError as e:
        return {"error": f"模型不存在或无法访问: {str(e)}"}
    except Exception as e:
        return {"error": f"获取模型信息失败: {str(e)}"}


@mcp.tool()
def search_datasets(
    query: str,
    limit: int = 10,
    sort: str = "downloads",
    direction: int = -1
) -> List[Dict[str, Any]]:
    """
    搜索 HuggingFace 数据集
    
    Args:
        query: 搜索关键词
        limit: 返回结果数量限制 (默认: 10)
        sort: 排序字段 (downloads/likes/trending/created_at)
        direction: 排序方向 (-1=降序, 1=升序)
    
    Returns:
        数据集列表,包含 id、作者、下载量、点赞数等信息
    """
    try:
        datasets = list(api.list_datasets(
            search=query,
            limit=limit,
            sort=sort,
            direction=direction
        ))
        
        return [{
            "id": dataset.id,
            "author": dataset.author if hasattr(dataset, 'author') else None,
            "downloads": dataset.downloads if hasattr(dataset, 'downloads') else 0,
            "likes": dataset.likes if hasattr(dataset, 'likes') else 0,
            "tags": dataset.tags if hasattr(dataset, 'tags') else [],
            "created_at": str(dataset.created_at) if hasattr(dataset, 'created_at') else None,
        } for dataset in datasets]
    except Exception as e:
        return {"error": f"搜索数据集失败: {str(e)}"}


@mcp.tool()
def get_dataset_info(dataset_id: str) -> Dict[str, Any]:
    """
    获取数据集详细信息
    
    Args:
        dataset_id: 数据集ID (例如: squad, imdb)
    
    Returns:
        数据集的详细信息,包括元数据、文件列表、标签等
    """
    try:
        info = api.dataset_info(dataset_id)
        
        return {
            "id": info.id,
            "author": info.author if hasattr(info, 'author') else None,
            "sha": info.sha if hasattr(info, 'sha') else None,
            "downloads": info.downloads if hasattr(info, 'downloads') else 0,
            "likes": info.likes if hasattr(info, 'likes') else 0,
            "tags": info.tags if hasattr(info, 'tags') else [],
            "created_at": str(info.created_at) if hasattr(info, 'created_at') else None,
            "last_modified": str(info.last_modified) if hasattr(info, 'last_modified') else None,
            "card_data": info.card_data.to_dict() if hasattr(info, 'card_data') and info.card_data else {},
            "siblings": [{"rfilename": f.rfilename, "size": f.size} for f in info.siblings] if hasattr(info, 'siblings') else []
        }
    except HfHubHTTPError as e:
        return {"error": f"数据集不存在或无法访问: {str(e)}"}
    except Exception as e:
        return {"error": f"获取数据集信息失败: {str(e)}"}


@mcp.tool()
def list_model_files(model_id: str) -> List[Dict[str, Any]]:
    """
    列出模型仓库中的所有文件
    
    Args:
        model_id: 模型ID
    
    Returns:
        文件列表,包含文件名和大小
    """
    try:
        info = api.model_info(model_id)
        files = []
        
        if hasattr(info, 'siblings'):
            files = [{
                "filename": f.rfilename,
                "size": f.size,
                "size_mb": round(f.size / (1024 * 1024), 2) if f.size else 0
            } for f in info.siblings]
        
        return files
    except Exception as e:
        return {"error": f"列出模型文件失败: {str(e)}"}


@mcp.tool()
def list_dataset_files(dataset_id: str) -> List[Dict[str, Any]]:
    """
    列出数据集仓库中的所有文件
    
    Args:
        dataset_id: 数据集ID
    
    Returns:
        文件列表,包含文件名和大小
    """
    try:
        info = api.dataset_info(dataset_id)
        files = []
        
        if hasattr(info, 'siblings'):
            files = [{
                "filename": f.rfilename,
                "size": f.size,
                "size_mb": round(f.size / (1024 * 1024), 2) if f.size else 0
            } for f in info.siblings]
        
        return files
    except Exception as e:
        return {"error": f"列出数据集文件失败: {str(e)}"}


@mcp.tool()
def download_model_file(
    model_id: str,
    filename: str,
    local_dir: Optional[str] = None
) -> Dict[str, str]:
    """
    下载模型文件
    
    Args:
        model_id: 模型ID
        filename: 要下载的文件名
        local_dir: 本地保存目录 (可选)
    
    Returns:
        下载文件的本地路径和相关信息
    """
    if not token:
        return {"error": "需要 HUGGINGFACE_TOKEN 才能下载文件"}
    
    try:
        path = hf_hub_download(
            repo_id=model_id,
            filename=filename,
            repo_type="model",
            local_dir=local_dir,
            token=token
        )
        
        return {
            "success": True,
            "path": path,
            "model_id": model_id,
            "filename": filename
        }
    except Exception as e:
        return {"error": f"下载文件失败: {str(e)}"}


@mcp.tool()
def download_dataset_file(
    dataset_id: str,
    filename: str,
    local_dir: Optional[str] = None
) -> Dict[str, str]:
    """
    下载数据集文件
    
    Args:
        dataset_id: 数据集ID
        filename: 要下载的文件名
        local_dir: 本地保存目录 (可选)
    
    Returns:
        下载文件的本地路径和相关信息
    """
    if not token:
        return {"error": "需要 HUGGINGFACE_TOKEN 才能下载文件"}
    
    try:
        path = hf_hub_download(
            repo_id=dataset_id,
            filename=filename,
            repo_type="dataset",
            local_dir=local_dir,
            token=token
        )
        
        return {
            "success": True,
            "path": path,
            "dataset_id": dataset_id,
            "filename": filename
        }
    except Exception as e:
        return {"error": f"下载文件失败: {str(e)}"}


@mcp.tool()
def get_user_info(username: str) -> Dict[str, Any]:
    """
    获取用户信息
    
    Args:
        username: HuggingFace 用户名
    
    Returns:
        用户的详细信息
    """
    try:
        info = api.whoami(token=token) if username == "me" and token else None
        
        if info:
            return {
                "name": info.get("name"),
                "fullname": info.get("fullname"),
                "email": info.get("email"),
                "orgs": [org.get("name") for org in info.get("orgs", [])],
                "auth": info.get("auth", {})
            }
        else:
            # 对于其他用户,返回基本信息
            return {"error": "需要认证才能查看用户信息,或使用 'me' 查看当前用户"}
    except Exception as e:
        return {"error": f"获取用户信息失败: {str(e)}"}


def main():
    """主函数 - 运行 MCP 服务器"""
    print("🚀 启动 HuggingFace MCP 服务器...", file=sys.stderr)
    
    if token:
        print(f"✅ 使用 HuggingFace Token: {token[:10]}...", file=sys.stderr)
    else:
        print("⚠️  未设置 HUGGINGFACE_TOKEN,某些功能将受限", file=sys.stderr)
    
    print("📡 服务器运行在 STDIO 模式", file=sys.stderr)
    print("🔧 提供 10 个工具:", file=sys.stderr)
    print("   - search_models: 搜索模型", file=sys.stderr)
    print("   - get_model_info: 获取模型信息", file=sys.stderr)
    print("   - search_datasets: 搜索数据集", file=sys.stderr)
    print("   - get_dataset_info: 获取数据集信息", file=sys.stderr)
    print("   - list_model_files: 列出模型文件", file=sys.stderr)
    print("   - list_dataset_files: 列出数据集文件", file=sys.stderr)
    print("   - download_model_file: 下载模型文件", file=sys.stderr)
    print("   - download_dataset_file: 下载数据集文件", file=sys.stderr)
    print("   - get_user_info: 获取用户信息", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    
    # 运行服务器 (STDIO 模式)
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
