#!/bin/bash
# TeyMCP-Server 完整自动安装脚本
# 支持 Ubuntu/Debian 系统

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示欢迎信息
show_welcome() {
    cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          TeyMCP-Server 全自动安装脚本                         ║
║          GPU 加速 + 125 个工具 + 17 个服务器                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo ""
    log_info "本脚本将自动安装以下组件:"
    echo "  ✓ Python 3.11 及依赖"
    echo "  ✓ Node.js 20.x"
    echo "  ✓ Docker 及 Docker Compose"
    echo "  ✓ NVIDIA Container Toolkit (GPU 支持)"
    echo "  ✓ TeyMCP-Server 所有依赖"
    echo ""
}

# 检查系统
check_system() {
    log_info "检查系统环境..."
    
    # 检查是否是 Linux
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        log_error "此脚本仅支持 Linux 系统"
        exit 1
    fi
    
    # 检查发行版
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        VER=$VERSION_ID
        log_success "检测到系统: $NAME $VERSION"
    else
        log_error "无法检测系统发行版"
        exit 1
    fi
    
    # 检查是否有 sudo 权限
    if ! sudo -n true 2>/dev/null; then
        log_warning "需要 sudo 权限，请输入密码"
        sudo -v
    fi
    
    echo ""
}

# 检查并安装 Python 3.11
install_python() {
    log_info "检查 Python 3.11..."
    
    if command -v python3.11 &> /dev/null; then
        log_success "Python 3.11 已安装: $(python3.11 --version)"
    else
        log_warning "Python 3.11 未安装，开始安装..."
        
        # 添加 deadsnakes PPA
        sudo apt-get update
        sudo apt-get install -y software-properties-common
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        sudo apt-get update
        
        # 安装 Python 3.11 及相关工具
        sudo apt-get install -y \
            python3.11 \
            python3.11-venv \
            python3.11-dev \
            python3-pip \
            python3-setuptools
        
        log_success "Python 3.11 安装完成"
    fi
    
    # 创建虚拟环境
    if [ ! -d "venv" ]; then
        log_info "创建 Python 虚拟环境..."
        python3.11 -m venv venv
        log_success "虚拟环境创建完成"
    else
        log_info "虚拟环境已存在"
    fi
    
    echo ""
}

# 安装 Node.js
install_nodejs() {
    log_info "检查 Node.js..."
    
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
        if [ "$NODE_VERSION" -ge 18 ]; then
            log_success "Node.js 已安装: $(node --version)"
            return
        else
            log_warning "Node.js 版本过低 (需要 >= 18), 正在升级..."
        fi
    else
        log_warning "Node.js 未安装，开始安装..."
    fi
    
    # 安装 Node.js 20.x
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
    
    log_success "Node.js 安装完成: $(node --version)"
    echo ""
}

# 安装 Docker
install_docker() {
    log_info "检查 Docker..."
    
    if command -v docker &> /dev/null; then
        log_success "Docker 已安装: $(docker --version)"
    else
        log_warning "Docker 未安装，开始安装..."
        
        # 安装 Docker
        curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
        sudo sh /tmp/get-docker.sh
        rm /tmp/get-docker.sh
        
        # 将当前用户添加到 docker 组
        sudo usermod -aG docker $USER
        
        log_success "Docker 安装完成"
        log_warning "请注意: 需要重新登录以使 docker 组生效"
    fi
    
    # 安装 Docker Compose
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
        log_success "Docker Compose 已安装"
    else
        log_warning "安装 Docker Compose..."
        sudo apt-get install -y docker-compose-plugin
        log_success "Docker Compose 安装完成"
    fi
    
    echo ""
}

# 检查 GPU 和 NVIDIA 驱动
check_gpu() {
    log_info "检查 NVIDIA GPU..."
    
    if lspci | grep -i nvidia > /dev/null; then
        log_success "检测到 NVIDIA GPU:"
        lspci | grep -i nvidia | sed 's/^/  /'
        
        # 检查 NVIDIA 驱动
        if command -v nvidia-smi &> /dev/null; then
            log_success "NVIDIA 驱动已安装:"
            nvidia-smi --query-gpu=name,driver_version --format=csv,noheader | sed 's/^/  /'
            return 0
        else
            log_warning "NVIDIA 驱动未安装"
            log_info "请访问 https://www.nvidia.com/Download/index.aspx 安装驱动"
            return 1
        fi
    else
        log_warning "未检测到 NVIDIA GPU，将跳过 GPU 支持"
        return 1
    fi
    
    echo ""
}

# 安装 NVIDIA Container Toolkit
install_nvidia_toolkit() {
    log_info "安装 NVIDIA Container Toolkit..."
    
    # 检查是否已安装
    if command -v nvidia-ctk &> /dev/null; then
        log_success "NVIDIA Container Toolkit 已安装: $(nvidia-ctk --version | head -1)"
        return
    fi
    
    # 配置 apt 源
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    
    log_info "配置 NVIDIA 软件源..."
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
        sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    
    curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    
    # 安装
    log_info "安装 NVIDIA Container Toolkit 包..."
    sudo apt-get update
    sudo apt-get install -y nvidia-container-toolkit
    
    # 配置 Docker Runtime
    log_info "配置 Docker Runtime..."
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker
    
    log_success "NVIDIA Container Toolkit 安装完成"
    
    # 验证
    log_info "验证 GPU 容器访问..."
    if docker run --rm --runtime=nvidia --gpus all nvidia/cuda:12.3.0-base-ubuntu22.04 nvidia-smi &> /dev/null; then
        log_success "GPU 容器访问验证成功"
    else
        log_warning "GPU 容器访问验证失败，但这不影响基础功能"
    fi
    
    echo ""
}

# 安装 Python 依赖
install_python_dependencies() {
    log_info "安装 Python 依赖..."
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 升级 pip
    log_info "升级 pip..."
    pip install --upgrade pip setuptools wheel
    
    # 安装依赖
    if [ -f "requirements.txt" ]; then
        log_info "从 requirements.txt 安装依赖..."
        pip install -r requirements.txt
        log_success "Python 依赖安装完成"
    else
        log_warning "requirements.txt 未找到，跳过依赖安装"
    fi
    
    # 停用虚拟环境
    deactivate
    
    echo ""
}

# 安装系统依赖
install_system_dependencies() {
    log_info "安装系统依赖..."
    
    sudo apt-get update
    sudo apt-get install -y \
        curl \
        wget \
        git \
        build-essential \
        libssl-dev \
        libffi-dev \
        ca-certificates \
        gnupg \
        lsb-release \
        jq \
        net-tools
    
    log_success "系统依赖安装完成"
    echo ""
}

# 创建配置文件
setup_config() {
    log_info "配置文件检查..."
    
    # 检查配置目录
    if [ ! -d "config" ]; then
        mkdir -p config
        log_info "创建 config 目录"
    fi
    
    # 创建 .env 示例文件
    if [ ! -f "config/.env" ] && [ ! -f "config/.env.example" ]; then
        cat > config/.env.example << 'EOF'
# TeyMCP-Server 环境变量配置示例

# 服务器配置
HOST=0.0.0.0
PORT=8080

# GPU 配置
NVIDIA_VISIBLE_DEVICES=all
NVIDIA_DRIVER_CAPABILITIES=compute,utility

# 日志配置
LOG_LEVEL=INFO
LOG_PATH=/app/data/logs

# 时区
TZ=Asia/Shanghai

# API 认证 (推荐配置)
# API_KEY=your_secure_api_key_here

# 数据库配置 (如需要)
# MYSQL_HOST=localhost
# MYSQL_PORT=3306
# MYSQL_USER=user
# MYSQL_PASSWORD=password

# GitHub 配置 (如需要)
# GITHUB_TOKEN=your_github_token

# HuggingFace 配置 (如需要)
# HF_TOKEN=your_huggingface_token
EOF
        log_info "创建 config/.env.example 文件"
    fi
    
    # 如果 .env 不存在，从示例复制
    if [ ! -f "config/.env" ] && [ -f "config/.env.example" ]; then
        cp config/.env.example config/.env
        log_info "从 .env.example 创建 config/.env"
    fi
    
    log_success "配置文件准备完成"
    echo ""
}

# 验证安装
verify_installation() {
    log_info "验证安装..."
    echo ""
    
    local all_ok=true
    
    # 检查 Python
    if command -v python3.11 &> /dev/null && [ -d "venv" ]; then
        log_success "✓ Python 3.11 和虚拟环境"
    else
        log_error "✗ Python 3.11 或虚拟环境缺失"
        all_ok=false
    fi
    
    # 检查 Node.js
    if command -v node &> /dev/null; then
        log_success "✓ Node.js $(node --version)"
    else
        log_error "✗ Node.js 未安装"
        all_ok=false
    fi
    
    # 检查 Docker
    if command -v docker &> /dev/null; then
        log_success "✓ Docker $(docker --version | cut -d' ' -f3 | tr -d ',')"
    else
        log_error "✗ Docker 未安装"
        all_ok=false
    fi
    
    # 检查 GPU 支持
    if command -v nvidia-smi &> /dev/null && command -v nvidia-ctk &> /dev/null; then
        log_success "✓ GPU 支持 (NVIDIA Driver + Container Toolkit)"
    else
        log_warning "○ GPU 支持未配置 (可选)"
    fi
    
    # 检查配置文件
    if [ -f "config/.env" ]; then
        log_success "✓ 配置文件"
    else
        log_warning "○ 配置文件未找到"
    fi
    
    echo ""
    
    if [ "$all_ok" = true ]; then
        log_success "所有必要组件安装完成！"
        return 0
    else
        log_error "部分组件安装失败，请检查错误信息"
        return 1
    fi
}

# 显示下一步操作
show_next_steps() {
    cat << "EOF"

╔══════════════════════════════════════════════════════════════╗
║                    安装完成！                                 ║
╚══════════════════════════════════════════════════════════════╝

📝 下一步操作:

1. 配置环境变量:
   vim config/.env

2. 启动服务 (三种方式任选其一):

   方式 A - 使用启动脚本 (推荐):
   bash start_gpu.sh

   方式 B - 使用 Docker Compose:
   docker-compose build
   docker-compose up -d

   方式 C - 直接运行 (开发模式):
   source venv/bin/activate
   python src/main.py

3. 验证服务:
   curl http://localhost:1215/health
   curl http://localhost:1215/api/status

4. 查看文档:
   - 快速开始: cat GPU_QUICKSTART.md
   - 完整指南: cat docs/GPU_SETUP.md
   - 对接文档: cat GPU_对接使用指南.md

5. 测试系统 (可选):
   bash test_gpu.sh

6. 监控服务 (可选):
   bash monitor_gpu.sh

EOF

    if ! groups $USER | grep -q docker; then
        log_warning "⚠️  重要提示: 请重新登录以使 Docker 组权限生效"
        log_info "或运行: newgrp docker"
    fi
    
    echo ""
    log_success "祝使用愉快！🚀"
    echo ""
}

# 主函数
main() {
    # 显示欢迎信息
    show_welcome
    
    # 检查系统
    check_system
    
    # 安装系统依赖
    install_system_dependencies
    
    # 安装 Python
    install_python
    
    # 安装 Node.js
    install_nodejs
    
    # 安装 Docker
    install_docker
    
    # 检查 GPU 并安装 NVIDIA Container Toolkit
    if check_gpu; then
        read -p "是否安装 NVIDIA Container Toolkit? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            install_nvidia_toolkit
        else
            log_info "跳过 NVIDIA Container Toolkit 安装"
        fi
    fi
    
    # 安装 Python 依赖
    install_python_dependencies
    
    # 配置文件
    setup_config
    
    # 验证安装
    if verify_installation; then
        show_next_steps
        exit 0
    else
        log_error "安装过程中出现错误，请检查日志"
        exit 1
    fi
}

# 捕获错误
trap 'log_error "脚本执行失败，请检查错误信息"; exit 1' ERR

# 执行主函数
main "$@"
