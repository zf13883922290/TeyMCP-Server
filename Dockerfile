# TeyMCP-Server Dockerfile with NVIDIA GPU Support
FROM nvidia/cuda:12.3.0-base-ubuntu22.04

# 设置元数据
LABEL maintainer="zf13883922290"
LABEL description="TeyMCP-Server - The One MCP to Rule Them All (GPU-Enabled)"
LABEL version="1.0.0"
LABEL gpu.support="enabled"

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility

# 设置工作目录
WORKDIR /app

# 安装 Python 3.11 和系统依赖
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    python3-pip \
    nodejs \
    npm \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 设置 Python 3.11 为默认版本
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# 升级 pip
RUN python3 -m pip install --upgrade pip setuptools wheel

# 复制requirements.txt
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/

# 创建数据目录
RUN mkdir -p data/logs data/metrics

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# 设置启动命令
CMD ["python", "src/main.py"]
