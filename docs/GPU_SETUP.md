# TeyMCP-Server GPU 配置指南

## 📋 目录

- [系统要求](#系统要求)
- [安装步骤](#安装步骤)
- [端口规划](#端口规划)
- [使用方法](#使用方法)
- [GPU 服务对接](#gpu-服务对接)
- [故障排除](#故障排除)

---

## 🖥️ 系统要求

### 硬件要求
- ✅ NVIDIA GPU（支持 CUDA 12.3+）
- ✅ 至少 8GB 系统内存
- ✅ 20GB+ 可用磁盘空间

### 软件要求
- ✅ Ubuntu 20.04+ / Debian 11+
- ✅ NVIDIA 驱动 >= 525.60.11
- ✅ Docker >= 20.10
- ✅ Docker Compose >= 2.0

---

## 🚀 安装步骤

### 第一步：检查 NVIDIA 驱动

```bash
# 检查驱动是否安装
nvidia-smi

# 预期输出应显示 GPU 信息和驱动版本
# 如未安装，请访问: https://www.nvidia.com/Download/index.aspx
```

### 第二步：安装 NVIDIA Container Toolkit

```bash
cd /home/sun/TeyMCP-Server

# 运行自动安装脚本
sudo bash install_nvidia_container_toolkit.sh
```

安装脚本会自动完成：
1. ✅ 检查 NVIDIA GPU 和驱动
2. ✅ 检查/安装 Docker
3. ✅ 安装 NVIDIA Container Toolkit
4. ✅ 配置 Docker Runtime
5. ✅ 验证 GPU 容器访问

### 第三步：验证安装

```bash
# 测试 GPU 容器访问
docker run --rm --gpus all nvidia/cuda:12.3.0-base-ubuntu22.04 nvidia-smi

# 应该显示 GPU 信息，说明容器可以访问 GPU
```

---

## 🔌 端口规划

为避免端口冲突，TeyMCP-Server 使用以下端口分配：

| 服务名称 | 容器内端口 | 宿主机端口 | 用途 | 状态 |
|---------|-----------|-----------|------|------|
| TeyMCP-Server | 8080 | **1215** | MCP 聚合服务主端口 | ✅ 必需 |
| Ollama (可选) | 11434 | **11434** | 本地 LLM 推理服务 | 🔄 可选 |
| 预留端口 | - | **1216** | 未来 GPU 服务扩展 | 🔄 可选 |

### 端口冲突检查

```bash
# 检查端口占用情况
sudo netstat -tlnp | grep -E '1215|1216|11434'

# 或使用 lsof
sudo lsof -i :1215
sudo lsof -i :1216
sudo lsof -i :11434
```

### 端口配置说明

**为什么选择 1215 端口？**
- 原服务端口 8080 常被其他服务占用
- 1215 端口范围较少冲突
- 容器内仍使用 8080，外部映射到 1215

**如何修改端口？**
编辑 `docker-compose.yml`:
```yaml
ports:
  - "您的端口:8080"  # 修改冒号前的端口号
```

---

## 📦 使用方法

### 方式一：使用 Docker Compose（推荐）

```bash
cd /home/sun/TeyMCP-Server

# 1. 构建 GPU 镜像
docker-compose build

# 2. 启动服务（GPU 模式）
docker-compose up -d

# 3. 查看日志
docker-compose logs -f teymcp

# 4. 检查 GPU 使用情况
docker exec teymcp-server-gpu nvidia-smi

# 5. 停止服务
docker-compose down
```

### 方式二：直接使用 Docker

```bash
cd /home/sun/TeyMCP-Server

# 构建镜像
docker build -t teymcp-server:gpu-latest .

# 运行容器（单独运行）
docker run -d \
  --name teymcp-server-gpu \
  --gpus all \
  -p 1215:8080 \
  -v $(pwd)/config:/app/config:ro \
  -v teymcp-logs:/app/data/logs \
  -v teymcp-metrics:/app/data/metrics \
  -e NVIDIA_VISIBLE_DEVICES=all \
  --restart unless-stopped \
  teymcp-server:gpu-latest

# 查看日志
docker logs -f teymcp-server-gpu

# 停止容器
docker stop teymcp-server-gpu
docker rm teymcp-server-gpu
```

### 方式三：启用 Ollama 本地 LLM（可选）

如果需要本地 GPU 推理服务：

```bash
# 1. 编辑 docker-compose.yml，取消 Ollama 部分的注释
vim docker-compose.yml
# 找到 ollama 服务定义，删除前面的 # 注释符号

# 2. 启动所有服务
docker-compose up -d

# 3. 验证 Ollama
curl http://localhost:11434/api/version

# 4. 拉取模型（例如 llama2）
docker exec -it ollama-gpu ollama pull llama2

# 5. 测试推理
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Hello, how are you?"
}'
```

---

## 🔗 GPU 服务对接

### 对接架构

```
┌─────────────────────────────────────────────────────┐
│                    宿主机（Host）                    │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │         Docker Network (teymcp-network)       │ │
│  │                                               │ │
│  │  ┌─────────────────────┐  ┌────────────────┐ │ │
│  │  │  TeyMCP-Server      │  │  Ollama (可选) │ │ │
│  │  │  Container          │  │  Container     │ │ │
│  │  │                     │  │                │ │ │
│  │  │  Port: 8080→1215    │  │  Port: 11434  │ │ │
│  │  │  GPU: ✅ Enabled    │  │  GPU: ✅ All   │ │ │
│  │  │                     │  │                │ │ │
│  │  │  MCP Servers:       │◄─┤  API Endpoint  │ │ │
│  │  │  - Ollama MCP       │  │                │ │ │
│  │  │  - HuggingFace      │  └────────────────┘ │ │
│  │  │  - DeepSeek         │                     │ │
│  │  │  - ...其他66个       │                     │ │
│  │  └─────────────────────┘                     │ │
│  │           ▲                                   │ │
│  │           │ GPU Access                        │ │
│  │           ▼                                   │ │
│  │  ┌─────────────────────┐                     │ │
│  │  │   NVIDIA GPU        │                     │ │
│  │  │   (via nvidia-ctk)  │                     │ │
│  │  └─────────────────────┘                     │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  External Access: http://YOUR_IP:1215               │
└─────────────────────────────────────────────────────┘
```

### 1. TeyMCP-Server 内部对接

TeyMCP-Server 可以通过 MCP 协议调用 GPU 加速的服务：

#### 配置 Ollama MCP Server

编辑 `config/servers.yaml`:

```yaml
servers:
  # Ollama 本地 LLM（GPU 加速）
  ollama:
    enabled: true  # 启用
    command: "npx"
    args:
      - "-y"
      - "ollama-mcp-server"
    env:
      OLLAMA_HOST: "http://ollama:11434"  # Docker 网络内访问
      # 或如果 Ollama 在宿主机: "http://host.docker.internal:11434"
```

#### 配置其他 GPU 服务

```yaml
  # DeepSeek MCP（GPU 推理）
  deepseek_mcp:
    enabled: true
    command: "npx"
    args:
      - "-y"
      - "deepseek-mcp-server"
    env:
      DEEPSEEK_API_KEY: "${DEEPSEEK_API_KEY}"
      USE_GPU: "true"

  # HuggingFace（GPU 推理）
  huggingface_official:
    enabled: true
    command: "npx"
    args:
      - "-y"
      - "@llmindset/hf-mcp-server"
    env:
      HUGGINGFACE_TOKEN: "${HUGGINGFACE_TOKEN}"
      DEVICE: "cuda"  # 使用 GPU
```

### 2. 外部应用对接

#### Claude Desktop 配置

编辑 `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "teymcp-gpu": {
      "command": "curl",
      "args": [
        "-X", "POST",
        "http://YOUR_SERVER_IP:1215/api/tools/call",
        "-H", "Content-Type: application/json",
        "-d", "{\"server\":\"ollama\",\"tool\":\"generate\",\"params\":{\"prompt\":\"YOUR_PROMPT\"}}"
      ]
    }
  }
}
```

#### Python SDK 对接

```python
import requests

class TeyMCPClient:
    def __init__(self, base_url="http://localhost:1215"):
        self.base_url = base_url
    
    def call_gpu_tool(self, server, tool, params):
        """调用 GPU 加速的工具"""
        response = requests.post(
            f"{self.base_url}/api/tools/call",
            json={
                "server": server,
                "tool": tool,
                "params": params
            }
        )
        return response.json()
    
    def ollama_generate(self, prompt, model="llama2"):
        """使用 Ollama GPU 推理"""
        return self.call_gpu_tool(
            server="ollama",
            tool="generate",
            params={
                "model": model,
                "prompt": prompt
            }
        )

# 使用示例
client = TeyMCPClient("http://YOUR_IP:1215")
result = client.ollama_generate("What is AI?")
print(result)
```

#### curl 命令对接

```bash
# 查看所有可用工具
curl http://localhost:1215/api/tools | jq

# 调用 Ollama 生成
curl -X POST http://localhost:1215/api/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "server": "ollama",
    "tool": "generate",
    "params": {
      "model": "llama2",
      "prompt": "Explain quantum computing"
    }
  }' | jq

# 检查服务状态
curl http://localhost:1215/api/status | jq
```

### 3. 容器间通信

在 Docker Compose 环境中，服务可以直接通过服务名访问：

```yaml
# TeyMCP-Server 访问 Ollama
OLLAMA_HOST: "http://ollama:11434"

# 而不是
# OLLAMA_HOST: "http://localhost:11434"
```

如果需要从容器访问宿主机服务：
```yaml
environment:
  - EXTERNAL_SERVICE: "http://host.docker.internal:PORT"
```

---

## 🔍 验证和测试

### 基础验证

```bash
# 1. 检查容器运行状态
docker ps | grep teymcp

# 2. 检查 GPU 可见性
docker exec teymcp-server-gpu nvidia-smi

# 3. 检查服务健康
curl http://localhost:1215/health

# 4. 查看服务状态
curl http://localhost:1215/api/status | jq

# 5. 查看日志
docker logs -f teymcp-server-gpu
```

### GPU 功能测试

```bash
# 测试 CUDA 是否可用
docker exec teymcp-server-gpu python3 -c "
import torch
print(f'CUDA Available: {torch.cuda.is_available()}')
print(f'CUDA Device: {torch.cuda.get_device_name(0)}')
"

# 测试 GPU 内存
docker exec teymcp-server-gpu nvidia-smi --query-gpu=memory.total,memory.used,memory.free --format=csv
```

### MCP 工具测试

```bash
# 查看所有 MCP 工具
curl http://localhost:1215/api/tools | jq '.[] | select(.server == "ollama")'

# 测试 Ollama 工具调用
curl -X POST http://localhost:1215/api/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "server": "ollama",
    "tool": "list_models",
    "params": {}
  }' | jq
```

---

## 🐛 故障排除

### 问题 1: GPU 不可见

**症状**: `nvidia-smi` 在容器内无法运行

**解决方案**:
```bash
# 检查 NVIDIA Container Toolkit
sudo systemctl status docker
sudo nvidia-ctk --version

# 重新配置 Docker Runtime
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# 重新构建容器
docker-compose down
docker-compose up -d
```

### 问题 2: 端口冲突

**症状**: `Error starting userland proxy: listen tcp4 0.0.0.0:1215: bind: address already in use`

**解决方案**:
```bash
# 查找占用端口的进程
sudo lsof -i :1215
sudo netstat -tlnp | grep 1215

# 杀死占用进程
sudo kill -9 <PID>

# 或修改 docker-compose.yml 使用其他端口
vim docker-compose.yml
# 修改 ports: "1215:8080" 为 "YOUR_PORT:8080"
```

### 问题 3: GPU 内存不足

**症状**: CUDA out of memory

**解决方案**:
```bash
# 查看 GPU 内存使用
nvidia-smi

# 限制 GPU 内存（修改 docker-compose.yml）
environment:
  - CUDA_VISIBLE_DEVICES=0  # 只使用第一个 GPU
  # 或在应用层面限制
  - TF_FORCE_GPU_ALLOW_GROWTH=true
```

### 问题 4: Ollama 无法连接

**症状**: Connection refused to ollama:11434

**解决方案**:
```bash
# 检查 Ollama 容器状态
docker ps | grep ollama

# 检查网络连接
docker exec teymcp-server-gpu ping ollama

# 查看 Ollama 日志
docker logs ollama-gpu

# 测试 Ollama API
curl http://localhost:11434/api/version
```

### 问题 5: 权限问题

**症状**: Permission denied accessing GPU

**解决方案**:
```bash
# 添加当前用户到 docker 组
sudo usermod -aG docker $USER

# 重新登录或运行
newgrp docker

# 或临时使用 sudo
sudo docker-compose up -d
```

---

## 📊 性能监控

### 实时监控脚本

创建 `monitor_gpu.sh`:

```bash
#!/bin/bash
watch -n 1 '
echo "=== GPU Status ==="
nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.used,memory.free --format=csv,noheader,nounits

echo ""
echo "=== Container Stats ==="
docker stats --no-stream teymcp-server-gpu

echo ""
echo "=== TeyMCP Status ==="
curl -s http://localhost:1215/api/status | jq -r ".servers | to_entries[] | select(.value.enabled) | \"\(.key): \(.value.status)\""
'
```

使用:
```bash
chmod +x monitor_gpu.sh
./monitor_gpu.sh
```

---

## 🔐 安全建议

1. **不要使用 privileged 模式**: 已在 docker-compose.yml 中禁用
2. **限制 GPU 访问**: 可以使用 `count: 1` 限制 GPU 数量
3. **使用只读挂载**: 配置文件使用 `:ro` 标志
4. **配置防火墙**: 限制 1215 端口的访问
```bash
sudo ufw allow from YOUR_TRUSTED_IP to any port 1215
```
5. **定期更新**: 保持 NVIDIA 驱动和 Container Toolkit 最新

---

## 📚 更多资源

- **NVIDIA Container Toolkit 文档**: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/
- **Docker GPU 支持**: https://docs.docker.com/config/containers/resource_constraints/#gpu
- **Ollama 文档**: https://github.com/ollama/ollama
- **TeyMCP-Server 主文档**: [README.md](../README.md)

---

## ✅ 快速启动清单

- [ ] 安装 NVIDIA 驱动
- [ ] 运行 `install_nvidia_container_toolkit.sh`
- [ ] 验证 GPU 容器访问
- [ ] 检查端口 1215 是否可用
- [ ] 配置 `config/servers.yaml` 启用 GPU 服务
- [ ] 配置 `config/.env` 添加 API 密钥
- [ ] 运行 `docker-compose up -d`
- [ ] 验证服务: `curl http://localhost:1215/api/status`
- [ ] 测试 GPU: `docker exec teymcp-server-gpu nvidia-smi`
- [ ] 测试 MCP 工具调用

---

**🎉 恭喜！您的 TeyMCP-Server 现在已经支持 GPU 加速了！**
