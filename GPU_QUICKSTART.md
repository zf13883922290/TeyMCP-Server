# TeyMCP-Server + NVIDIA GPU 快速开始指南

## 🚀 三步快速启动

### 步骤 1: 安装 NVIDIA Container Toolkit

```bash
cd /home/sun/TeyMCP-Server
sudo bash install_nvidia_container_toolkit.sh
```

这将自动完成：
- ✅ 检查 NVIDIA GPU 和驱动
- ✅ 安装 Docker（如未安装）
- ✅ 安装 NVIDIA Container Toolkit
- ✅ 配置 Docker Runtime
- ✅ 验证 GPU 容器访问

### 步骤 2: 启动 GPU 服务

```bash
bash start_gpu.sh
```

这将自动完成：
- ✅ 检查 GPU 和工具链
- ✅ 检查端口冲突
- ✅ 构建 GPU 镜像
- ✅ 启动服务
- ✅ 验证服务就绪

### 步骤 3: 验证和测试

```bash
bash test_gpu.sh
```

这将测试：
- ✅ Docker 和容器状态
- ✅ GPU 访问和功能
- ✅ MCP 服务和 API
- ✅ 端口和日志

---

## 📊 监控和管理

### 实时监控

```bash
bash monitor_gpu.sh
```

显示：
- 🖥️ GPU 状态（温度、功耗、显存）
- 📦 容器资源使用
- 🔧 MCP 服务状态
- 📈 工具统计
- 📝 实时日志
- 🖥️ 系统资源

### 查看日志

```bash
# 实时日志
docker-compose logs -f

# 只看主服务
docker-compose logs -f teymcp

# 最近 100 行
docker logs --tail 100 teymcp-server-gpu
```

### 停止服务

```bash
docker-compose down
```

### 重启服务

```bash
docker-compose restart
```

---

## 🔌 端口和访问

| 端口 | 服务 | 访问地址 |
|------|------|----------|
| 1215 | TeyMCP-Server 主服务 | http://localhost:1215 |
| 1215 | API 文档 | http://localhost:1215/docs |
| 1215 | 健康检查 | http://localhost:1215/health |
| 1215 | 服务状态 | http://localhost:1215/api/status |
| 11434 | Ollama (可选) | http://localhost:11434 |

### 测试连接

```bash
# 健康检查
curl http://localhost:1215/health

# 服务状态
curl http://localhost:1215/api/status | jq

# 工具列表
curl http://localhost:1215/api/tools | jq

# GPU 状态
docker exec teymcp-server-gpu nvidia-smi
```

---

## 🔧 配置 GPU 服务

### 1. 启用 Ollama 本地 LLM

编辑 `docker-compose.yml`，取消 Ollama 部分的注释：

```bash
vim docker-compose.yml
# 找到 "# ollama:" 开始的部分，删除所有 # 注释符号
```

然后重启：

```bash
docker-compose up -d
```

拉取模型：

```bash
docker exec ollama-gpu ollama pull llama2
docker exec ollama-gpu ollama pull codellama
```

测试：

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Hello, how are you?"
}'
```

### 2. 配置 MCP 服务器使用 GPU

编辑 `config/servers.yaml`:

```yaml
servers:
  # Ollama MCP（连接到容器内 Ollama）
  ollama:
    enabled: true
    command: "npx"
    args:
      - "-y"
      - "ollama-mcp-server"
    env:
      OLLAMA_HOST: "http://ollama:11434"  # Docker 网络内访问
```

添加 API 密钥到 `config/.env`:

```bash
# HuggingFace（使用 GPU）
HUGGINGFACE_TOKEN=your_token_here

# DeepSeek
DEEPSEEK_API_KEY=your_api_key_here

# Ollama（本地，无需密钥）
OLLAMA_HOST=http://ollama:11434
```

重启服务：

```bash
docker-compose restart
```

---

## 🎯 使用示例

### Python 客户端

```python
import requests

# 初始化客户端
BASE_URL = "http://localhost:1215"

# 1. 查看服务状态
response = requests.get(f"{BASE_URL}/api/status")
print(response.json())

# 2. 查看所有工具
response = requests.get(f"{BASE_URL}/api/tools")
tools = response.json()
print(f"总工具数: {len(tools)}")

# 3. 调用 Ollama 生成文本（如果启用）
response = requests.post(
    f"{BASE_URL}/api/tools/call",
    json={
        "server": "ollama",
        "tool": "generate",
        "params": {
            "model": "llama2",
            "prompt": "Explain quantum computing in simple terms"
        }
    }
)
print(response.json())

# 4. 使用 GitHub 工具
response = requests.post(
    f"{BASE_URL}/api/tools/call",
    json={
        "server": "github",
        "tool": "search_repositories",
        "params": {
            "query": "machine learning",
            "limit": 5
        }
    }
)
print(response.json())
```

### curl 命令

```bash
# 查看状态
curl http://localhost:1215/api/status | jq '.servers | keys'

# 查看 GPU 相关工具
curl http://localhost:1215/api/tools | jq '.[] | select(.server | contains("ollama") or contains("huggingface"))'

# 调用工具
curl -X POST http://localhost:1215/api/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "server": "ollama",
    "tool": "list_models",
    "params": {}
  }' | jq
```

### Claude Desktop 配置

编辑 `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "teymcp": {
      "url": "http://YOUR_SERVER_IP:1215",
      "headers": {
        "Content-Type": "application/json"
      }
    }
  }
}
```

---

## 🐛 常见问题

### GPU 不可见

```bash
# 检查驱动
nvidia-smi

# 重新配置
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# 重启容器
docker-compose restart
```

### 端口冲突

```bash
# 检查占用
sudo lsof -i :1215

# 杀死进程
sudo kill -9 <PID>

# 或修改端口
vim docker-compose.yml
# 修改 ports: "YOUR_PORT:8080"
```

### 服务无响应

```bash
# 查看日志
docker logs teymcp-server-gpu

# 检查容器状态
docker ps -a | grep teymcp

# 重启服务
docker-compose restart
```

### GPU 内存不足

```bash
# 查看 GPU 使用
nvidia-smi

# 限制使用的 GPU
vim docker-compose.yml
# 修改 count: 1  # 只使用一个 GPU

# 清理不用的容器
docker system prune -a
```

---

## 📚 脚本说明

| 脚本 | 用途 | 何时使用 |
|------|------|----------|
| `install_nvidia_container_toolkit.sh` | 安装 NVIDIA 工具 | 首次安装 |
| `start_gpu.sh` | 启动 GPU 服务 | 每次启动 |
| `test_gpu.sh` | 测试 GPU 功能 | 验证配置 |
| `monitor_gpu.sh` | 实时监控 | 日常监控 |

---

## 🔗 更多资源

- 📖 完整文档: `docs/GPU_SETUP.md`
- 📊 更新总结: `UPDATE_SUMMARY_20251105.md`
- 🔧 配置文件: `config/servers.yaml`
- 🌐 API 文档: http://localhost:1215/docs

---

## ✅ 快速检查清单

使用前请确认：

- [ ] NVIDIA 驱动已安装（`nvidia-smi` 可用）
- [ ] Docker 已安装并运行
- [ ] NVIDIA Container Toolkit 已安装
- [ ] 端口 1215 可用
- [ ] 配置文件 `config/servers.yaml` 存在
- [ ] 环境变量 `config/.env` 已配置（如需要）

---

**🎉 开始使用 TeyMCP-Server + GPU！**

```bash
# 一键启动
bash start_gpu.sh

# 一键测试
bash test_gpu.sh

# 一键监控
bash monitor_gpu.sh
```
