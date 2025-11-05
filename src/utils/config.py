"""
配置加载工具
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

from src.utils.logger import logger


def load_app_config() -> Dict[str, Any]:
    """加载应用配置"""
    config_file = Path("config/app.yaml")
    
    if not config_file.exists():
        logger.warning(f"配置文件不存在: {config_file}，使用默认配置")
        return {
            "host": "0.0.0.0",
            "port": 8080,
            "log_level": "INFO",
            "reload": False
        }
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config.get("app", {})


def load_servers_config() -> Dict[str, Any]:
    """
    加载服务器配置
    
    Returns:
        服务器配置字典
    """
    # 加载环境变量
    load_dotenv("config/.env")
    
    config_file = Path("config/servers.yaml")
    
    if not config_file.exists():
        logger.warning(f"服务器配置文件不存在: {config_file}")
        return {"servers": {}}
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 替换环境变量
    config = _replace_env_vars(config)
    
    return config


def _replace_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    递归替换配置中的环境变量
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
