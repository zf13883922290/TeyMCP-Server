"""
指标收集工具
用于收集和统计系统性能指标
"""

from typing import Dict, Any, List
from datetime import datetime
import json
from pathlib import Path


class MetricsCollector:
    """指标收集器"""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {
            "requests": {
                "total": 0,
                "success": 0,
                "failed": 0
            },
            "response_times": [],
            "servers": {},
            "tools": {}
        }
        
        # 创建指标目录
        self.metrics_dir = Path("data/metrics")
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
    
    def record_request(self, success: bool, duration_ms: int):
        """
        记录请求
        
        Args:
            success: 是否成功
            duration_ms: 响应时间（毫秒）
        """
        self.metrics["requests"]["total"] += 1
        
        if success:
            self.metrics["requests"]["success"] += 1
        else:
            self.metrics["requests"]["failed"] += 1
        
        # 记录响应时间（只保留最近1000条）
        self.metrics["response_times"].append(duration_ms)
        if len(self.metrics["response_times"]) > 1000:
            self.metrics["response_times"] = self.metrics["response_times"][-1000:]
    
    def record_server_call(self, server_name: str, success: bool):
        """
        记录服务器调用
        
        Args:
            server_name: 服务器名称
            success: 是否成功
        """
        if server_name not in self.metrics["servers"]:
            self.metrics["servers"][server_name] = {
                "calls": 0,
                "success": 0,
                "failed": 0
            }
        
        self.metrics["servers"][server_name]["calls"] += 1
        
        if success:
            self.metrics["servers"][server_name]["success"] += 1
        else:
            self.metrics["servers"][server_name]["failed"] += 1
    
    def record_tool_call(self, tool_name: str, success: bool):
        """
        记录工具调用
        
        Args:
            tool_name: 工具名称
            success: 是否成功
        """
        if tool_name not in self.metrics["tools"]:
            self.metrics["tools"][tool_name] = {
                "calls": 0,
                "success": 0,
                "failed": 0
            }
        
        self.metrics["tools"][tool_name]["calls"] += 1
        
        if success:
            self.metrics["tools"][tool_name]["success"] += 1
        else:
            self.metrics["tools"][tool_name]["failed"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取当前指标"""
        return {
            **self.metrics,
            "avg_response_time": self._calculate_avg_response_time(),
            "success_rate": self._calculate_success_rate()
        }
    
    def _calculate_avg_response_time(self) -> float:
        """计算平均响应时间"""
        if not self.metrics["response_times"]:
            return 0.0
        return sum(self.metrics["response_times"]) / len(self.metrics["response_times"])
    
    def _calculate_success_rate(self) -> float:
        """计算成功率"""
        total = self.metrics["requests"]["total"]
        if total == 0:
            return 100.0
        return (self.metrics["requests"]["success"] / total) * 100
    
    def save_metrics(self):
        """保存指标到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.metrics_dir / f"metrics_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.get_metrics(), f, indent=2, ensure_ascii=False)
    
    def reset_metrics(self):
        """重置所有指标"""
        self.metrics = {
            "requests": {"total": 0, "success": 0, "failed": 0},
            "response_times": [],
            "servers": {},
            "tools": {}
        }


# 全局指标收集器实例
metrics_collector = MetricsCollector()
