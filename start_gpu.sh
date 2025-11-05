#!/bin/bash
# TeyMCP-Server GPU 版本启动脚本

set -e

cd "$(dirname "$0")"

echo "======================================"
echo "  TeyMCP-Server GPU 启动脚本"
echo "======================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 NVIDIA GPU
check_gpu() {
    echo -e "${YELLOW}🔍 检查 NVIDIA GPU...${NC}"
    if command -v nvidia-smi &> /dev/null; then
        nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
        echo -e "${GREEN}✅ GPU 检查通过${NC}"
    else
        echo -e "${RED}❌ 未检测到 NVIDIA 驱动${NC}"
        echo -e "${YELLOW}提示: 请先运行 sudo bash install_nvidia_container_toolkit.sh${NC}"
        exit 1
    fi
    echo ""
}

# 检查 NVIDIA Container Toolkit
check_nvidia_toolkit() {
    echo -e "${YELLOW}🔍 检查 NVIDIA Container Toolkit...${NC}"
    if docker run --rm --gpus all nvidia/cuda:12.3.0-base-ubuntu22.04 nvidia-smi &> /dev/null; then
        echo -e "${GREEN}✅ NVIDIA Container Toolkit 正常${NC}"
    else
        echo -e "${RED}❌ NVIDIA Container Toolkit 未配置${NC}"
        echo -e "${YELLOW}提示: 请先运行 sudo bash install_nvidia_container_toolkit.sh${NC}"
        exit 1
    fi
    echo ""
}

# 检查端口
check_ports() {
    echo -e "${YELLOW}🔍 检查端口占用...${NC}"
    
    ports=(1215 1216)
    for port in "${ports[@]}"; do
        if sudo lsof -i :$port &> /dev/null; then
            echo -e "${RED}❌ 端口 $port 已被占用${NC}"
            echo -e "${YELLOW}占用进程:${NC}"
            sudo lsof -i :$port
            echo ""
            read -p "是否强制停止占用进程? (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                pid=$(sudo lsof -t -i:$port)
                sudo kill -9 $pid
                echo -e "${GREEN}✅ 进程已停止${NC}"
            else
                echo -e "${RED}❌ 请手动处理端口冲突后重试${NC}"
                exit 1
            fi
        else
            echo -e "${GREEN}✅ 端口 $port 可用${NC}"
        fi
    done
    echo ""
}

# 检查配置文件
check_config() {
    echo -e "${YELLOW}🔍 检查配置文件...${NC}"
    
    if [ ! -f "config/servers.yaml" ]; then
        echo -e "${RED}❌ 配置文件不存在: config/servers.yaml${NC}"
        exit 1
    fi
    
    if [ ! -f "config/.env" ]; then
        echo -e "${YELLOW}⚠️  警告: config/.env 不存在，将使用默认配置${NC}"
        echo "创建默认 .env 文件..."
        cp config/.env.example config/.env 2>/dev/null || touch config/.env
    fi
    
    echo -e "${GREEN}✅ 配置文件检查通过${NC}"
    echo ""
}

# 构建镜像
build_image() {
    echo -e "${YELLOW}🔨 构建 Docker 镜像...${NC}"
    docker-compose build
    echo -e "${GREEN}✅ 镜像构建完成${NC}"
    echo ""
}

# 启动服务
start_services() {
    echo -e "${YELLOW}🚀 启动服务...${NC}"
    docker-compose up -d
    echo -e "${GREEN}✅ 服务已启动${NC}"
    echo ""
}

# 等待服务就绪
wait_for_service() {
    echo -e "${YELLOW}⏳ 等待服务启动...${NC}"
    
    max_attempts=30
    attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s http://localhost:1215/health &> /dev/null; then
            echo -e "${GREEN}✅ 服务已就绪${NC}"
            return 0
        fi
        
        attempt=$((attempt + 1))
        echo -n "."
        sleep 2
    done
    
    echo ""
    echo -e "${RED}❌ 服务启动超时${NC}"
    echo -e "${YELLOW}查看日志:${NC}"
    docker-compose logs --tail=50
    return 1
}

# 显示服务信息
show_service_info() {
    echo ""
    echo "======================================"
    echo "  🎉 TeyMCP-Server GPU 已启动！"
    echo "======================================"
    echo ""
    echo -e "${GREEN}📊 服务信息:${NC}"
    echo ""
    
    # GPU 信息
    echo -e "${YELLOW}GPU 状态:${NC}"
    docker exec teymcp-server-gpu nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null || echo "GPU 信息获取失败"
    echo ""
    
    # 服务状态
    echo -e "${YELLOW}MCP 服务状态:${NC}"
    curl -s http://localhost:1215/api/status | jq -r '.servers | to_entries[] | select(.value.enabled) | "\(.key): \(.value.status)"' 2>/dev/null || echo "状态获取失败"
    echo ""
    
    # 访问地址
    echo -e "${YELLOW}访问地址:${NC}"
    echo "  - 主服务: http://localhost:1215"
    echo "  - API 文档: http://localhost:1215/docs"
    echo "  - 健康检查: http://localhost:1215/health"
    echo "  - 状态查询: http://localhost:1215/api/status"
    echo ""
    
    # 常用命令
    echo -e "${YELLOW}常用命令:${NC}"
    echo "  - 查看日志: docker-compose logs -f"
    echo "  - 停止服务: docker-compose down"
    echo "  - 重启服务: docker-compose restart"
    echo "  - GPU 监控: docker exec teymcp-server-gpu nvidia-smi"
    echo "  - 服务状态: curl http://localhost:1215/api/status | jq"
    echo ""
    echo "======================================"
}

# 主流程
main() {
    check_gpu
    check_nvidia_toolkit
    check_ports
    check_config
    build_image
    start_services
    
    if wait_for_service; then
        show_service_info
    else
        echo ""
        echo -e "${RED}启动失败，请检查日志${NC}"
        exit 1
    fi
}

# 运行主流程
main
