"""
数据验证工具
用于验证配置和输入数据
"""

import re
from typing import Dict, Any, List, Optional
from pathlib import Path


def validate_server_name(name: str) -> bool:
    """
    验证服务器名称
    只允许字母、数字、下划线、连字符
    
    Args:
        name: 服务器名称
        
    Returns:
        是否有效
    """
    if not name:
        return False
    
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, name))


def validate_command(command: str) -> bool:
    """
    验证命令
    
    Args:
        command: 命令字符串
        
    Returns:
        是否有效
    """
    if not command:
        return False
    
    # 检查常见的安全风险字符
    dangerous_chars = [';', '&&', '||', '|', '`', '$']
    return not any(char in command for char in dangerous_chars)


def validate_port(port: int) -> bool:
    """
    验证端口号
    
    Args:
        port: 端口号
        
    Returns:
        是否有效
    """
    return 1 <= port <= 65535


def validate_file_path(path: str, must_exist: bool = False) -> bool:
    """
    验证文件路径
    
    Args:
        path: 文件路径
        must_exist: 是否必须存在
        
    Returns:
        是否有效
    """
    try:
        p = Path(path)
        
        if must_exist:
            return p.exists()
        
        # 检查路径是否包含危险字符
        dangerous_patterns = ['..', '~', '$']
        return not any(pattern in str(p) for pattern in dangerous_patterns)
        
    except Exception:
        return False


def validate_env_var(name: str) -> bool:
    """
    验证环境变量名称
    
    Args:
        name: 环境变量名
        
    Returns:
        是否有效
    """
    if not name:
        return False
    
    pattern = r'^[A-Z][A-Z0-9_]*$'
    return bool(re.match(pattern, name))


def validate_server_config(config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    验证服务器配置
    
    Args:
        config: 服务器配置字典
        
    Returns:
        (是否有效, 错误信息)
    """
    # 必需字段
    required_fields = ['command', 'args']
    for field in required_fields:
        if field not in config:
            return False, f"缺少必需字段: {field}"
    
    # 验证命令
    if not validate_command(config['command']):
        return False, "无效的命令"
    
    # 验证参数
    if not isinstance(config['args'], list):
        return False, "args 必须是列表"
    
    # 验证环境变量
    if 'env' in config:
        if not isinstance(config['env'], dict):
            return False, "env 必须是字典"
        
        for key in config['env'].keys():
            if not isinstance(key, str):
                return False, f"环境变量名必须是字符串: {key}"
    
    return True, None


def validate_tool_arguments(arguments: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    验证工具参数
    
    Args:
        arguments: 工具参数字典
        
    Returns:
        (是否有效, 错误信息)
    """
    if not isinstance(arguments, dict):
        return False, "参数必须是字典"
    
    # 检查参数值的类型
    for key, value in arguments.items():
        if not isinstance(key, str):
            return False, f"参数名必须是字符串: {key}"
        
        # 参数值只能是基本类型
        if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
            return False, f"参数值类型不支持: {key}={type(value)}"
    
    return True, None


def sanitize_string(s: str, max_length: int = 1000) -> str:
    """
    清理字符串
    移除危险字符，限制长度
    
    Args:
        s: 输入字符串
        max_length: 最大长度
        
    Returns:
        清理后的字符串
    """
    # 限制长度
    s = s[:max_length]
    
    # 移除控制字符
    s = ''.join(char for char in s if ord(char) >= 32 or char in '\n\r\t')
    
    return s


def validate_yaml_syntax(yaml_string: str) -> tuple[bool, Optional[str]]:
    """
    验证YAML语法
    
    Args:
        yaml_string: YAML字符串
        
    Returns:
        (是否有效, 错误信息)
    """
    try:
        import yaml
        yaml.safe_load(yaml_string)
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)
    except Exception as e:
        return False, f"未知错误: {str(e)}"


def validate_json_syntax(json_string: str) -> tuple[bool, Optional[str]]:
    """
    验证JSON语法
    
    Args:
        json_string: JSON字符串
        
    Returns:
        (是否有效, 错误信息)
    """
    try:
        import json
        json.loads(json_string)
        return True, None
    except json.JSONDecodeError as e:
        return False, str(e)
    except Exception as e:
        return False, f"未知错误: {str(e)}"
