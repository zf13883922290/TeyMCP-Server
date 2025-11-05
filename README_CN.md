<div align="center">

# 🚀 TeyMCP-Server

### *一个MCP统治所有工具* 

**The One MCP to Rule Them All** 🔥

[![许可证: MIT](https://img.shields.io/badge/许可证-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-00C7B7.svg)](https://fastapi.tiangolo.com/)
[![GPU Support](https://img.shields.io/badge/GPU-NVIDIA%20CUDA-76B900.svg)](https://developer.nvidia.com/cuda-toolkit)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

[English](README.md) | [简体中文](README_CN.md)

</div>

---

## 💡 TeyMCP-Server 是什么？

TeyMCP-Server 是一个强大的 MCP 聚合器，专为中国开发者设计。

- ✅ 同时支持 GitHub 和 Gitee
- ✅ 完整中文文档和界面
- ✅ 国内加速优化
- ✅ 一键部署脚本
- 🎮 **GPU 加速支持**（NEW！）
- 🐳 **Docker 容器化**（NEW！）

### 为什么选择 TeyMCP-Server？

传统方式你需要配置：
```json
{
  "mcpServers": {
    "github": {...},
    "gitee": {...},
    "filesystem": {...},
    "postgres": {...},
    "slack": {...}
    // 10+ 个配置...
  }
}
```

使用 TeyMCP-Server：
```json
{
  "mcpServers": {
    "tey": {
      "command": "python",
      "args": ["~/.teymcp/src/main.py"]
    }
  }
}
```

就这么简单！✨

---

## 🎬 快速开始

### 标准部署

#### 方式一：一键安装（推荐）
```bash
curl -fsSL https://gitee.com/zf13883922290/TeyMCP-Server/raw/main/scripts/install.sh | bash
```

#### 方式二：Gitee 源（国内加速）
```bash
git clone https://gitee.com/zf13883922290/TeyMCP-Server.git
cd TeyMCP-Server
bash scripts/install.sh
```

### 🎮 GPU 加速部署（NEW！）

如果您有 NVIDIA GPU，可以启用 GPU 加速以支持本地 LLM 推理：

```bash
cd /home/sun/TeyMCP-Server

# 1. 安装 NVIDIA Container Toolkit
sudo bash install_nvidia_container_toolkit.sh

# 2. 启动 GPU 服务
bash start_gpu.sh

# 3. 测试 GPU 功能
bash test_gpu.sh

# 4. 实时监控（可选）
bash monitor_gpu.sh
```

**GPU 功能特性：**
- 🚀 NVIDIA CUDA 12.3+ 支持
- 🤖 Ollama 本地 LLM 推理（可选）
- 📦 完整容器化部署
- 🔌 端口自动协调（避免冲突）
- 📊 实时 GPU 监控工具

**查看详细文档：**
- [GPU 快速开始](GPU_QUICKSTART.md) - 5 分钟上手
- [GPU 完整配置指南](docs/GPU_SETUP.md) - 详细文档

---

## 📖 完整文档

### 基础文档
- [快速入门](docs/QUICKSTART_CN.md)
- [配置指南](docs/CONFIG_CN.md)
- [API 文档](docs/API_CN.md)
- [常见问题](docs/FAQ_CN.md)

### GPU 相关（NEW！）
- [GPU 快速开始](GPU_QUICKSTART.md) ⭐️
- [GPU 完整配置](docs/GPU_SETUP.md)
- [Docker 容器化](docs/DEPLOYMENT.md)

---

<div align="center">

**用 ❤️ 制作 by [zf13883922290](https://github.com/zf13883922290)**

</div>
