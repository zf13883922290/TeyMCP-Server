#!/bin/bash
# NVIDIA Container Toolkit 安装脚本
# 支持 Ubuntu/Debian 系统

set -e

echo "======================================"
echo "NVIDIA Container Toolkit 安装脚本"
echo "======================================"
echo ""

# 检查是否有 NVIDIA GPU
check_nvidia_gpu() {
    echo "🔍 检查 NVIDIA GPU..."
    if lspci | grep -i nvidia > /dev/null; then
        echo "✅ 检测到 NVIDIA GPU"
        lspci | grep -i nvidia
    else
        echo "❌ 未检测到 NVIDIA GPU"
        echo "⚠️  警告: 系统中没有 NVIDIA GPU，但仍可继续安装工具包"
        read -p "是否继续安装? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    echo ""
}

# 检查 NVIDIA 驱动
check_nvidia_driver() {
    echo "🔍 检查 NVIDIA 驱动..."
    if command -v nvidia-smi &> /dev/null; then
        echo "✅ NVIDIA 驱动已安装"
        nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
    else
        echo "❌ NVIDIA 驱动未安装"
        echo "请先安装 NVIDIA 驱动: https://www.nvidia.com/Download/index.aspx"
        exit 1
    fi
    echo ""
}

# 检查 Docker
check_docker() {
    echo "🔍 检查 Docker..."
    if command -v docker &> /dev/null; then
        echo "✅ Docker 已安装: $(docker --version)"
    else
        echo "❌ Docker 未安装"
        echo "正在安装 Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        rm get-docker.sh
        echo "✅ Docker 安装完成"
    fi
    echo ""
}

# 安装 NVIDIA Container Toolkit
install_nvidia_container_toolkit() {
    echo "📦 安装 NVIDIA Container Toolkit..."
    
    # 配置 apt 源
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    
    curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    
    # 更新包列表
    sudo apt-get update
    
    # 安装 NVIDIA Container Toolkit
    sudo apt-get install -y nvidia-container-toolkit
    
    echo "✅ NVIDIA Container Toolkit 安装完成"
    echo ""
}

# 配置 Docker Runtime
configure_docker_runtime() {
    echo "⚙️  配置 Docker Runtime..."
    
    # 配置 NVIDIA runtime
    sudo nvidia-ctk runtime configure --runtime=docker
    
    # 重启 Docker
    sudo systemctl restart docker
    
    echo "✅ Docker Runtime 配置完成"
    echo ""
}

# 验证安装
verify_installation() {
    echo "🧪 验证安装..."
    
    # 测试 GPU 访问
    echo "运行测试容器..."
    if sudo docker run --rm --gpus all nvidia/cuda:12.3.0-base-ubuntu22.04 nvidia-smi; then
        echo ""
        echo "✅ NVIDIA Container Toolkit 验证成功！"
    else
        echo ""
        echo "❌ 验证失败，请检查配置"
        exit 1
    fi
    echo ""
}

# 显示使用信息
show_usage() {
    cat << EOF
====================================
✅ 安装完成！
====================================

📋 使用方法:

1. Docker 命令使用 GPU:
   docker run --gpus all your_image

2. Docker Compose 使用 GPU (已更新配置):
   docker-compose up -d

3. 查看 GPU 信息:
   nvidia-smi

4. 测试 GPU 容器:
   docker run --rm --gpus all nvidia/cuda:12.3.0-base-ubuntu22.04 nvidia-smi

5. 启动 TeyMCP-Server (带 GPU):
   cd /home/sun/TeyMCP-Server
   docker-compose up -d

====================================
📚 更多信息:
- NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/
- TeyMCP-Server GPU 配置: docs/GPU_SETUP.md
====================================
EOF
}

# 主流程
main() {
    check_nvidia_gpu
    check_nvidia_driver
    check_docker
    install_nvidia_container_toolkit
    configure_docker_runtime
    verify_installation
    show_usage
}

# 运行主流程
main
