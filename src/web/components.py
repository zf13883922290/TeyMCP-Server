"""
Web组件
可复用的HTML组件
"""

from typing import Dict, Any, List


def create_status_badge(status: str) -> str:
    """
    创建状态徽章
    
    Args:
        status: 状态值 (healthy, unhealthy, disconnected)
        
    Returns:
        HTML字符串
    """
    colors = {
        "healthy": "green",
        "unhealthy": "red",
        "disconnected": "gray"
    }
    
    labels = {
        "healthy": "健康",
        "unhealthy": "异常",
        "disconnected": "断开"
    }
    
    color = colors.get(status, "gray")
    label = labels.get(status, status)
    
    return f'''
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-{color}-100 text-{color}-800">
            <span class="status-dot bg-{color}-500 mr-1"></span>
            {label}
        </span>
    '''


def create_metric_card(title: str, value: str, icon: str, color: str = "blue") -> str:
    """
    创建指标卡片
    
    Args:
        title: 标题
        value: 值
        icon: Font Awesome图标类名
        color: 颜色 (blue, green, purple, orange)
        
    Returns:
        HTML字符串
    """
    return f'''
        <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100 hover:shadow-md transition">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-sm text-gray-500 mb-1">{title}</p>
                    <p class="text-3xl font-bold text-gray-800">{value}</p>
                </div>
                <div class="w-12 h-12 bg-{color}-100 rounded-lg flex items-center justify-center">
                    <i class="{icon} text-{color}-600 text-xl"></i>
                </div>
            </div>
        </div>
    '''


def create_server_table_row(server: Dict[str, Any]) -> str:
    """
    创建服务器表格行
    
    Args:
        server: 服务器信息字典
        
    Returns:
        HTML字符串
    """
    status_badge = create_status_badge(server.get("status", "unknown"))
    
    return f'''
        <tr class="border-b border-gray-50 hover:bg-gray-50 transition">
            <td class="py-4">
                <span class="font-medium text-gray-800">{server.get("name", "")}</span>
            </td>
            <td class="py-4">{status_badge}</td>
            <td class="py-4 text-gray-600">{server.get("tools_count", 0)}</td>
            <td class="py-4 text-gray-600">{server.get("last_check", "-")}</td>
            <td class="py-4">
                <span class="{'text-red-600' if server.get('error_count', 0) > 0 else 'text-gray-600'}">
                    {server.get("error_count", 0)}
                </span>
            </td>
        </tr>
    '''


def create_log_entry(log: Dict[str, Any]) -> str:
    """
    创建日志条目
    
    Args:
        log: 日志信息字典
        
    Returns:
        HTML字符串
    """
    status = log.get("status", "unknown")
    bg_color = "bg-green-50 border-green-200" if status == "success" else "bg-red-50 border-red-200"
    
    error_html = ""
    if log.get("error"):
        error_html = f'<div class="text-xs text-red-600 mt-1">{log["error"]}</div>'
    
    return f'''
        <div class="log-entry p-3 rounded-lg border {bg_color}">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <span class="font-semibold">{log.get("tool_name", "")}</span>
                    <span class="text-gray-500 ml-2">{log.get("server", "")}</span>
                </div>
                <span class="text-gray-500">{log.get("duration_ms", 0)}ms</span>
            </div>
            <div class="text-xs text-gray-600 mt-1">
                {log.get("timestamp", "")}
            </div>
            {error_html}
        </div>
    '''


def create_alert(message: str, alert_type: str = "info") -> str:
    """
    创建警告框
    
    Args:
        message: 消息内容
        alert_type: 类型 (info, success, warning, error)
        
    Returns:
        HTML字符串
    """
    colors = {
        "info": "blue",
        "success": "green",
        "warning": "yellow",
        "error": "red"
    }
    
    icons = {
        "info": "fa-info-circle",
        "success": "fa-check-circle",
        "warning": "fa-exclamation-triangle",
        "error": "fa-times-circle"
    }
    
    color = colors.get(alert_type, "blue")
    icon = icons.get(alert_type, "fa-info-circle")
    
    return f'''
        <div class="bg-{color}-50 border-l-4 border-{color}-400 p-4 rounded">
            <div class="flex">
                <div class="flex-shrink-0">
                    <i class="fas {icon} text-{color}-400"></i>
                </div>
                <div class="ml-3">
                    <p class="text-sm text-{color}-700">{message}</p>
                </div>
            </div>
        </div>
    '''


def create_loading_spinner() -> str:
    """
    创建加载动画
    
    Returns:
        HTML字符串
    """
    return '''
        <div class="flex items-center justify-center py-8">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
    '''


def create_empty_state(message: str, icon: str = "fa-inbox") -> str:
    """
    创建空状态
    
    Args:
        message: 消息
        icon: 图标
        
    Returns:
        HTML字符串
    """
    return f'''
        <div class="text-center py-12">
            <i class="fas {icon} text-gray-300 text-5xl mb-4"></i>
            <p class="text-gray-400 text-lg">{message}</p>
        </div>
    '''


def create_button(text: str, onclick: str = "", btn_type: str = "primary") -> str:
    """
    创建按钮
    
    Args:
        text: 按钮文本
        onclick: 点击事件
        btn_type: 按钮类型 (primary, secondary, danger)
        
    Returns:
        HTML字符串
    """
    colors = {
        "primary": "bg-blue-600 hover:bg-blue-700 text-white",
        "secondary": "bg-gray-200 hover:bg-gray-300 text-gray-800",
        "danger": "bg-red-600 hover:bg-red-700 text-white"
    }
    
    color_class = colors.get(btn_type, colors["primary"])
    onclick_attr = f'onclick="{onclick}"' if onclick else ''
    
    return f'''
        <button {onclick_attr} 
                class="px-4 py-2 rounded-lg {color_class} transition duration-200">
            {text}
        </button>
    '''
