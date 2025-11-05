#!/bin/bash
# GPU 监控脚本 - 实时监控 GPU 和服务状态

cd "$(dirname "$0")"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 清屏函数
clear_screen() {
    clear
    echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}   TeyMCP-Server GPU 实时监控 (Ctrl+C 退出)${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
    echo ""
}

# 显示时间
show_time() {
    echo -e "${YELLOW}⏰ 更新时间: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
    echo ""
}

# GPU 状态
show_gpu_status() {
    echo -e "${BLUE}═══ GPU 状态 ═══${NC}"
    
    if docker exec teymcp-server-gpu nvidia-smi --query-gpu=index,name,temperature.gpu,power.draw,power.limit,utilization.gpu,utilization.memory,memory.used,memory.total --format=csv,noheader,nounits 2>/dev/null | \
        awk -F', ' '{
            printf "GPU %s: %s\n", $1, $2
            printf "  温度: %s°C | 功耗: %s/%sW | GPU使用率: %s%% | 显存使用率: %s%%\n", $3, $4, $5, $6, $7
            printf "  显存: %sMB / %sMB (%.1f%% used)\n\n", $8, $9, ($8/$9)*100
        }'; then
        :
    else
        echo -e "${RED}❌ GPU 信息获取失败${NC}"
        echo ""
    fi
}

# 容器状态
show_container_status() {
    echo -e "${BLUE}═══ 容器状态 ═══${NC}"
    
    if docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}" 2>/dev/null | grep -E "NAME|teymcp|ollama"; then
        :
    else
        echo -e "${RED}❌ 容器状态获取失败${NC}"
    fi
    echo ""
}

# MCP 服务状态
show_mcp_status() {
    echo -e "${BLUE}═══ MCP 服务状态 ═══${NC}"
    
    if status_json=$(curl -s http://localhost:1215/api/status 2>/dev/null); then
        # 统计信息
        total=$(echo "$status_json" | jq '.servers | length' 2>/dev/null)
        enabled=$(echo "$status_json" | jq '[.servers | to_entries[] | select(.value.enabled)] | length' 2>/dev/null)
        running=$(echo "$status_json" | jq '[.servers | to_entries[] | select(.value.status == "running")] | length' 2>/dev/null)
        
        echo "总服务器: $total | 已启用: $enabled | 运行中: $running"
        echo ""
        
        # 显示启用的服务器状态
        echo "启用的服务器:"
        echo "$status_json" | jq -r '.servers | to_entries[] | select(.value.enabled) | 
            if .value.status == "running" then
                "  ✅ \(.key): \(.value.status)"
            else
                "  ❌ \(.key): \(.value.status)"
            end' 2>/dev/null || echo "  解析失败"
    else
        echo -e "${RED}❌ 无法连接到 TeyMCP-Server (http://localhost:1215)${NC}"
    fi
    echo ""
}

# 工具统计
show_tool_stats() {
    echo -e "${BLUE}═══ 工具统计 ═══${NC}"
    
    if tools_json=$(curl -s http://localhost:1215/api/tools 2>/dev/null); then
        total_tools=$(echo "$tools_json" | jq '. | length' 2>/dev/null)
        echo "可用工具总数: $total_tools"
        
        # 按服务器分组统计
        echo ""
        echo "各服务器工具数:"
        echo "$tools_json" | jq -r 'group_by(.server) | .[] | "  \(.[0].server): \(length) 个工具"' 2>/dev/null | head -10
        
        if [ $(echo "$tools_json" | jq -r 'group_by(.server) | length' 2>/dev/null) -gt 10 ]; then
            echo "  ..."
        fi
    else
        echo -e "${RED}❌ 工具信息获取失败${NC}"
    fi
    echo ""
}

# 最近日志
show_recent_logs() {
    echo -e "${BLUE}═══ 最近日志 (最后 5 行) ═══${NC}"
    
    docker logs --tail 5 teymcp-server-gpu 2>&1 | while IFS= read -r line; do
        if echo "$line" | grep -qi "error"; then
            echo -e "${RED}$line${NC}"
        elif echo "$line" | grep -qi "warn"; then
            echo -e "${YELLOW}$line${NC}"
        elif echo "$line" | grep -qi "success\|ok\|done"; then
            echo -e "${GREEN}$line${NC}"
        else
            echo "$line"
        fi
    done
    echo ""
}

# Ollama 状态（如果启用）
show_ollama_status() {
    if docker ps | grep ollama-gpu &> /dev/null; then
        echo -e "${BLUE}═══ Ollama GPU 状态 ═══${NC}"
        
        if curl -s http://localhost:11434/api/version &> /dev/null; then
            version=$(curl -s http://localhost:11434/api/version 2>/dev/null | jq -r .version)
            echo -e "${GREEN}✅ Ollama 运行中 (版本: $version)${NC}"
            
            echo ""
            echo "已安装的模型:"
            docker exec ollama-gpu ollama list 2>/dev/null | head -6 || echo "  查询失败"
        else
            echo -e "${RED}❌ Ollama 服务无响应${NC}"
        fi
        echo ""
    fi
}

# 系统资源
show_system_resources() {
    echo -e "${BLUE}═══ 系统资源 ═══${NC}"
    
    # CPU 和内存
    echo "CPU & 内存:"
    top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/  CPU使用率: \1%/" | awk '{print "  CPU使用率: " 100-$2 "%"}'
    free -h | awk 'NR==2{printf "  内存: %s / %s (%.1f%%)\n", $3, $2, $3*100/$2}'
    
    # 磁盘
    echo ""
    echo "磁盘使用:"
    df -h / | awk 'NR==2{printf "  根目录: %s / %s (%s)\n", $3, $2, $5}'
    
    # Docker 磁盘
    docker_size=$(docker system df --format "{{.Size}}" 2>/dev/null | head -1)
    [ -n "$docker_size" ] && echo "  Docker: $docker_size"
    echo ""
}

# 主循环
main_loop() {
    while true; do
        clear_screen
        show_time
        show_gpu_status
        show_container_status
        show_mcp_status
        show_tool_stats
        show_ollama_status
        show_system_resources
        show_recent_logs
        
        echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
        echo -e "${YELLOW}提示: Ctrl+C 退出 | 每 5 秒自动刷新${NC}"
        
        sleep 5
    done
}

# 捕获 Ctrl+C
trap 'echo ""; echo "监控已停止"; exit 0' INT

# 检查容器是否运行
if ! docker ps | grep teymcp-server-gpu &> /dev/null; then
    echo -e "${RED}❌ TeyMCP-Server GPU 容器未运行${NC}"
    echo ""
    echo "请先启动服务:"
    echo "  bash start_gpu.sh"
    echo "或"
    echo "  docker-compose up -d"
    exit 1
fi

# 运行主循环
main_loop
