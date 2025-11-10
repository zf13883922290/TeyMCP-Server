"""
配置加载工具（优化版本，支持异步加载和缓存）
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
import asyncio
from functools import lru_cache

from src.utils.logger import logger

# Configuration cache
_config_cache: Dict[str, Any] = {}


def load_app_config() -> Dict[str, Any]:
    """加载应用配置（同步版本，用于启动）"""
    if "app" in _config_cache:
        return _config_cache["app"]
    
    config_file = Path("config/app.yaml")
    
    if not config_file.exists():
        logger.warning(f"配置文件不存在: {config_file}，使用默认配置")
        default_config = {
            "host": "0.0.0.0",
            "port": 8080,
            "log_level": "INFO",
            "reload": False
        }
        _config_cache["app"] = default_config
        return default_config
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    app_config = config.get("app", {})
    _config_cache["app"] = app_config
    return app_config


async def load_app_config_async() -> Dict[str, Any]:
    """异步加载应用配置"""
    if "app" in _config_cache:
        return _config_cache["app"]
    
    config_file = Path("config/app.yaml")
    
    if not config_file.exists():
        logger.warning(f"配置文件不存在: {config_file}，使用默认配置")
        default_config = {
            "host": "0.0.0.0",
            "port": 8080,
            "log_level": "INFO",
            "reload": False
        }
        _config_cache["app"] = default_config
        return default_config
    
    # Read file asynchronously
    loop = asyncio.get_event_loop()
    
    def read_config():
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    config = await loop.run_in_executor(None, read_config)
    app_config = config.get("app", {})
    _config_cache["app"] = app_config
    return app_config


def load_servers_config() -> Dict[str, Any]:
    """
    加载服务器配置（同步版本）
    
    Returns:
        服务器配置字典
    """
    if "servers" in _config_cache:
        return _config_cache["servers"]
    
    # 加载环境变量
    load_dotenv("config/.env")
    
    config_file = Path("config/servers.yaml")
    
    if not config_file.exists():
        logger.warning(f"服务器配置文件不存在: {config_file}")
        default_config = {"servers": {}}
        _config_cache["servers"] = default_config
        return default_config
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 替换环境变量
    config = _replace_env_vars(config)
    _config_cache["servers"] = config
    
    return config


async def load_servers_config_async() -> Dict[str, Any]:
    """
    异步加载服务器配置
    
    Returns:
        服务器配置字典
    """
    if "servers" in _config_cache:
        return _config_cache["servers"]
    
    # 加载环境变量
    load_dotenv("config/.env")
    
    config_file = Path("config/servers.yaml")
    
    if not config_file.exists():
        logger.warning(f"服务器配置文件不存在: {config_file}")
        default_config = {"servers": {}}
        _config_cache["servers"] = default_config
        return default_config
    
    # Read file asynchronously
    loop = asyncio.get_event_loop()
    
    def read_config():
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    config = await loop.run_in_executor(None, read_config)
    
    # 替换环境变量
    config = _replace_env_vars(config)
    _config_cache["servers"] = config
    
    return config


def clear_config_cache():
    """清除配置缓存（用于热重载）"""
    _config_cache.clear()


@lru_cache(maxsize=128)
def _replace_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    递归替换配置中的环境变量（带缓存）
    ${VAR_NAME} -> 环境变量值
    """
    if isinstance(config, dict):
        return {
            key: _replace_env_vars(value)
            for key, value in config.items()
        }
    elif isinstance(config, list):
        return [_replace_env_vars(item) for item in config]
    elif isinstance(config, str):
        # 替换 ${VAR_NAME} 格式的环境变量
        if config.startswith("${") and config.endswith("}"):
            var_name = config[2:-1]
            return os.getenv(var_name, config)
        return config
    else:
        return config
