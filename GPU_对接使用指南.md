# TeyMCP-Server + NVIDIA GPU 对接使用指南

## 📋 目录

- [系统概述](#系统概述)
- [对接架构](#对接架构)
- [快速对接](#快速对接)
- [API 对接方式](#api-对接方式)
- [GPU 加速配置](#gpu-加速配置)
- [MCP 工具使用](#mcp-工具使用)
- [常见对接场景](#常见对接场景)
- [故障排查](#故障排查)

---

## 系统概述

**TeyMCP-Server** 是一个支持 GPU 加速的 MCP（Model Context Protocol）工具聚合服务器，提供 125 个工具和 17 个服务器集成。

### 核心特性

- ✅ **GPU 加速支持**: 基于 NVIDIA CUDA 12.3，支持容器内 GPU 访问
- ✅ **工具聚合**: 125 个工具统一 API 访问
- ✅ **容器化部署**: Docker + GPU 完整打包
- ✅ **端口隔离**: 避免冲突的端口映射策略
- ✅ **健康监控**: 实时状态检查和日志记录

### 系统要求

| 组件 | 要求 |
|------|------|
| GPU | NVIDIA GPU (已测试: Tesla P100) |
| 驱动 | NVIDIA Driver ≥ 450.80.02 |
| CUDA | 支持 CUDA 12.3+ |
| Docker | ≥ 20.10 |
| NVIDIA Container Toolkit | ≥ 1.14.0 |
| 系统 | Linux (已测试: Ubuntu 22.04) |

---

## 对接架构

### 网络拓扑

```
┌─────────────────────────────────────────────────────────────┐
│                         宿主机 (Host)                        │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │       Docker Network: teymcp-network (bridge)         │ │
│  │                   172.28.0.0/16                       │ │
│  │                                                       │ │
│  │  ┌──────────────────────┐    ┌───────────────────┐  │ │
│  │  │  TeyMCP-Server       │    │  Ollama (可选)    │  │ │
│  │  │  GPU Container       │◄──►│  LLM Container    │  │ │
│  │  │                      │    │                   │  │ │
│  │  │  内部: 8080          │    │  内部: 11434      │  │ │
│  │  │  外部: 1215          │    │  外部: 11434      │  │ │
│  │  │  GPU: NVIDIA All     │    │  GPU: NVIDIA All  │  │ │
│  │  └──────┬───────────────┘    └───────────────────┘  │ │
│  │         │                                            │ │
│  └─────────┼────────────────────────────────────────────┘ │
│            │                                              │
│    ┌───────▼─────────┐                                   │
│    │   Port 1215     │  ◄─── 外部访问入口                 │
│    │   Port 1216     │  ◄─── 预留端口                    │
│    │   Port 11434    │  ◄─── Ollama (可选)              │
│    └─────────────────┘                                   │
│                                                           │
│    GPU: /dev/nvidia0, /dev/nvidiactl, /dev/nvidia-uvm   │
└───────────────────────────────────────────────────────────┘
```

### 端口映射策略

| 外部端口 | 容器端口 | 服务 | 用途 |
|---------|---------|------|------|
| 1215 | 8080 | TeyMCP-Server | 主 API 服务 |
| 1216 | - | 预留 | 未来扩展 |
| 11434 | 11434 | Ollama | GPU LLM 推理 (可选) |

### 数据卷映射

| 宿主机路径 | 容器路径 | 类型 | 说明 |
|-----------|---------|------|------|
| `./config` | `/app/config` | 只读 | 配置文件 |
| `teymcp-logs` (volume) | `/app/data/logs` | 读写 | 日志持久化 |
| `teymcp-metrics` (volume) | `/app/data/metrics` | 读写 | 监控数据 |
| `gpu-cache` (volume) | `/root/.cache` | 读写 | GPU 模型缓存 |

---

## 快速对接

### 方式 1: 一键启动脚本（推荐）

```bash
cd /home/sun/TeyMCP-Server

# 步骤 1: 安装 NVIDIA Container Toolkit（首次运行）
sudo bash install_nvidia_container_toolkit.sh

# 步骤 2: 启动 GPU 服务
bash start_gpu.sh

# 步骤 3: 验证服务
curl http://localhost:1215/api/status
```

### 方式 2: Docker Compose 手动启动

```bash
cd /home/sun/TeyMCP-Server

# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 验证 GPU 访问
docker exec teymcp-server-gpu nvidia-smi

# 检查服务状态
curl http://localhost:1215/api/status
```

### 方式 3: 原生 Docker 运行

```bash
# 构建镜像
docker build -t teymcp-server:gpu-latest .

# 运行容器
docker run -d \
  --name teymcp-server-gpu \
  --runtime=nvidia \
  --gpus all \
  -p 1215:8080 \
  -v $(pwd)/config:/app/config:ro \
  -v teymcp-logs:/app/data/logs \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e NVIDIA_DRIVER_CAPABILITIES=compute,utility \
  --restart unless-stopped \
  teymcp-server:gpu-latest

# 验证运行
docker ps | grep teymcp
docker exec teymcp-server-gpu nvidia-smi
```

---

## API 对接方式

### 基础 HTTP API

#### 1. 健康检查

```bash
curl http://localhost:1215/health
```

响应示例：
```json
{
  "status": "healthy",
  "timestamp": "2025-11-05T13:15:00Z"
}
```

#### 2. 获取服务状态

```bash
curl http://localhost:1215/api/status
```

响应示例：
```json
{
  "servers": [
    {
      "name": "filesystem",
      "status": "healthy",
      "tools_count": 14
    },
    {
      "name": "github",
      "status": "healthy",
      "tools_count": 13
    }
    // ... 共 17 个服务器
  ]
}
```

#### 3. 获取工具列表

```bash
curl http://localhost:1215/api/tools
```

响应示例：
```json
{
  "tools": [
    {
      "name": "puppeteer_navigate",
      "description": "Navigate to a URL",
      "server": "puppeteer",
      "inputSchema": { ... }
    },
    {
      "name": "mysql_query",
      "description": "Execute SQL query",
      "server": "mysql",
      "inputSchema": { ... }
    }
    // ... 共 125 个工具
  ]
}
```

#### 4. 调用 MCP 工具

```bash
curl -X POST http://localhost:1215/api/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "filesystem_read_file",
    "arguments": {
      "path": "/app/README.md"
    }
  }'
```

### Python SDK 对接示例

```python
import requests
import json

class TeyMCPClient:
    def __init__(self, base_url="http://localhost:1215"):
        self.base_url = base_url
    
    def get_status(self):
        """获取服务状态"""
        response = requests.get(f"{self.base_url}/api/status")
        return response.json()
    
    def list_tools(self):
        """列出所有工具"""
        response = requests.get(f"{self.base_url}/api/tools")
        return response.json()
    
    def call_tool(self, tool_name, arguments):
        """调用工具"""
        response = requests.post(
            f"{self.base_url}/api/tools/call",
            json={
                "tool": tool_name,
                "arguments": arguments
            }
        )
        return response.json()

# 使用示例
client = TeyMCPClient()

# 1. 检查服务状态
status = client.get_status()
print(f"服务器数量: {len(status['servers'])}")

# 2. 列出工具
tools = client.list_tools()
print(f"工具数量: {len(tools['tools'])}")

# 3. 调用文件系统工具
result = client.call_tool(
    "filesystem_list_directory",
    {"path": "/app"}
)
print(f"文件列表: {result}")

# 4. 调用 GitHub 工具
result = client.call_tool(
    "github_search_repositories",
    {"query": "MCP server", "limit": 5}
)
print(f"仓库搜索结果: {result}")

# 5. 调用数据库工具
result = client.call_tool(
    "mysql_query",
    {
        "connection_id": "main_db",
        "query": "SELECT * FROM users LIMIT 10"
    }
)
print(f"查询结果: {result}")
```

### JavaScript/Node.js 对接示例

```javascript
const axios = require('axios');

class TeyMCPClient {
  constructor(baseURL = 'http://localhost:1215') {
    this.client = axios.create({ baseURL });
  }

  async getStatus() {
    const response = await this.client.get('/api/status');
    return response.data;
  }

  async listTools() {
    const response = await this.client.get('/api/tools');
    return response.data;
  }

  async callTool(toolName, args) {
    const response = await this.client.post('/api/tools/call', {
      tool: toolName,
      arguments: args
    });
    return response.data;
  }
}

// 使用示例
(async () => {
  const client = new TeyMCPClient();

  // 检查状态
  const status = await client.getStatus();
  console.log(`服务器数量: ${status.servers.length}`);

  // 调用浏览器自动化工具
  const screenshot = await client.callTool('puppeteer_screenshot', {
    url: 'https://example.com',
    fullPage: true
  });
  console.log('截图结果:', screenshot);

  // 调用媒体生成工具
  const image = await client.callTool('generate_image_dalle', {
    prompt: 'A beautiful sunset over mountains',
    size: '1024x1024'
  });
  console.log('生成的图片:', image);
})();
```

---

## GPU 加速配置

### 启用 GPU 工具

编辑 `config/servers.yaml` 启用 GPU 加速的 MCP 服务器：

```yaml
servers:
  # Ollama 本地 LLM (GPU 加速)
  ollama:
    enabled: true
    command: "node"
    args: ["/path/to/ollama-mcp-server.js"]
    env:
      OLLAMA_HOST: "http://ollama-gpu:11434"
      CUDA_VISIBLE_DEVICES: "0"
  
  # HuggingFace 官方服务器 (GPU 推理)
  huggingface_official:
    enabled: true
    command: "uvx"
    args: ["--from", "mcp-server-huggingface", "mcp-server-huggingface"]
    env:
      CUDA_VISIBLE_DEVICES: "0"
      HF_TOKEN: "your_token_here"
  
  # DeepSeek MCP (GPU 推理)
  deepseek_mcp:
    enabled: true
    command: "uvx"
    args: ["deepseek-mcp"]
    env:
      CUDA_VISIBLE_DEVICES: "0"
      DEEPSEEK_API_KEY: "your_key_here"
```

### GPU 工具调用示例

```python
# 使用 Ollama 进行本地推理
result = client.call_tool(
    "ollama_generate",
    {
        "model": "llama2",
        "prompt": "Explain quantum computing in simple terms",
        "stream": False
    }
)

# 使用 HuggingFace 模型
result = client.call_tool(
    "huggingface_inference",
    {
        "model": "meta-llama/Llama-2-7b-chat-hf",
        "inputs": "What is the meaning of life?",
        "parameters": {
            "max_length": 200,
            "temperature": 0.7
        }
    }
)

# 使用媒体生成工具 (GPU 加速)
result = client.call_tool(
    "generate_image_sd",  # Stable Diffusion
    {
        "prompt": "A futuristic city with flying cars",
        "width": 1024,
        "height": 1024,
        "steps": 50
    }
)
```

---

## MCP 工具使用

### 工具分类 (125 个工具)

#### 📂 文件系统工具 (14 个)
- `filesystem_list_directory` - 列出目录
- `filesystem_read_file` - 读取文件
- `filesystem_write_file` - 写入文件
- `filesystem_create_directory` - 创建目录
- `filesystem_delete_file` - 删除文件
- `filesystem_move_file` - 移动文件
- `filesystem_copy_file` - 复制文件
- `filesystem_get_file_info` - 获取文件信息
- ...等 14 个工具

#### 🌐 浏览器自动化 (15 个)
**Puppeteer (14 个工具):**
- `puppeteer_navigate` - 导航到 URL
- `puppeteer_screenshot` - 截图
- `puppeteer_click` - 点击元素
- `puppeteer_type` - 输入文本
- `puppeteer_evaluate` - 执行 JavaScript
- `puppeteer_select` - 选择下拉框
- `puppeteer_hover` - 悬停元素
- ...等 14 个工具

**Playwright (1 个工具):**
- `playwright_action` - Playwright 自动化

#### 🐙 GitHub 集成 (13 个)
- `github_create_repository` - 创建仓库
- `github_search_repositories` - 搜索仓库
- `github_get_file_contents` - 获取文件内容
- `github_create_issue` - 创建问题
- `github_create_pull_request` - 创建 PR
- `github_list_commits` - 列出提交
- `github_create_branch` - 创建分支
- ...等 13 个工具

#### 🗄️ 数据库管理 (28 个)
**MySQL (11 个工具):**
- `mysql_connect` - 连接数据库
- `mysql_query` - 执行查询
- `mysql_execute` - 执行 SQL
- `mysql_list_databases` - 列出数据库
- `mysql_list_tables` - 列出表
- `mysql_describe_table` - 描述表结构
- `mysql_explain` - 分析查询计划
- ...等 11 个工具

**SQLite (8 个工具):**
- `sqlite_query` - 查询数据
- `sqlite_list_tables` - 列出表
- `sqlite_create_record` - 创建记录
- ...等 8 个工具

**PostgreSQL (9 个工具):**
- `postgres_query` - 查询数据
- `postgres_list_schemas` - 列出模式
- ...等 9 个工具

#### 🔍 搜索引擎 (2 个)
- `brave_search` - Brave 搜索
- `exa_search` - Exa 搜索

#### 🧠 知识图谱 (9 个)
- `memory_create_entities` - 创建实体
- `memory_add_observations` - 添加观察
- `memory_create_relations` - 创建关系
- `memory_read_graph` - 读取图谱
- ...等 9 个工具

#### 🎨 媒体生成 (8 个)
- `generate_image_dalle` - DALL-E 图像生成
- `generate_image_sd` - Stable Diffusion 生成
- `edit_image` - 编辑图像
- `convert_image` - 转换图像格式
- `generate_video` - 生成视频
- `add_watermark` - 添加水印
- ...等 8 个工具

#### 🤖 本地自动化 (7 个)
- `create_file` - 创建文件
- `compress_files` - 压缩文件
- `generate_code` - 生成代码
- `batch_rename` - 批量重命名
- `create_project` - 创建项目
- `remote_edit` - 远程编辑
- ...等 7 个工具

#### ⏰ 时间和 Git (6 个)
- `time_get_current_time` - 获取当前时间
- `time_add_reminder` - 添加提醒
- `git_status` - Git 状态
- `git_commit` - Git 提交
- ...等 6 个工具

---

## 常见对接场景

### 场景 1: AI 助手对接

**需求**: 让 AI 助手能访问文件、浏览网页、查询数据库

```python
from teymcp_client import TeyMCPClient

client = TeyMCPClient("http://localhost:1215")

class AIAssistant:
    def __init__(self):
        self.mcp = client
    
    def read_document(self, path):
        """读取文档"""
        return self.mcp.call_tool("filesystem_read_file", {"path": path})
    
    def search_web(self, query):
        """搜索网页"""
        return self.mcp.call_tool("brave_search", {"query": query})
    
    def query_database(self, sql):
        """查询数据库"""
        return self.mcp.call_tool("mysql_query", {
            "connection_id": "main",
            "query": sql
        })
    
    def take_screenshot(self, url):
        """网页截图"""
        return self.mcp.call_tool("puppeteer_screenshot", {
            "url": url,
            "fullPage": True
        })

# 使用
assistant = AIAssistant()
content = assistant.read_document("/app/data/report.txt")
results = assistant.search_web("latest AI news")
data = assistant.query_database("SELECT * FROM users LIMIT 10")
screenshot = assistant.take_screenshot("https://example.com")
```

### 场景 2: 自动化测试对接

**需求**: 自动化 Web 测试和 API 测试

```python
import time

def automated_test_suite():
    client = TeyMCPClient()
    
    # 1. 导航到登录页面
    client.call_tool("puppeteer_navigate", {
        "url": "https://myapp.com/login"
    })
    
    # 2. 输入用户名
    client.call_tool("puppeteer_type", {
        "selector": "#username",
        "text": "testuser"
    })
    
    # 3. 输入密码
    client.call_tool("puppeteer_type", {
        "selector": "#password",
        "text": "testpass123"
    })
    
    # 4. 点击登录按钮
    client.call_tool("puppeteer_click", {
        "selector": "#login-button"
    })
    
    time.sleep(2)
    
    # 5. 验证登录成功
    result = client.call_tool("puppeteer_evaluate", {
        "script": "document.querySelector('.welcome-message').innerText"
    })
    
    assert "Welcome" in result
    
    # 6. 截图保存
    client.call_tool("puppeteer_screenshot", {
        "path": "/app/test-results/login-success.png"
    })
    
    print("✅ 测试通过")

# 运行测试
automated_test_suite()
```

### 场景 3: 数据分析对接

**需求**: 从多个数据源收集数据并分析

```python
def data_analysis_pipeline():
    client = TeyMCPClient()
    
    # 1. 从 MySQL 获取销售数据
    sales_data = client.call_tool("mysql_query", {
        "connection_id": "sales_db",
        "query": """
            SELECT product_id, SUM(amount) as total_sales
            FROM sales
            WHERE date >= '2025-01-01'
            GROUP BY product_id
        """
    })
    
    # 2. 从 SQLite 获取产品信息
    products = client.call_tool("sqlite_query", {
        "database": "products.db",
        "query": "SELECT id, name, category FROM products"
    })
    
    # 3. 从文件系统读取配置
    config = client.call_tool("filesystem_read_file", {
        "path": "/app/config/analysis_config.json"
    })
    
    # 4. 合并数据并保存结果
    # ... 数据处理逻辑 ...
    
    # 5. 写入分析报告
    client.call_tool("filesystem_write_file", {
        "path": "/app/reports/sales_analysis.txt",
        "content": analysis_report
    })
    
    # 6. 创建 GitHub Issue 通知团队
    client.call_tool("github_create_issue", {
        "owner": "myorg",
        "repo": "reports",
        "title": "Sales Analysis Report Ready",
        "body": f"New report available at: /app/reports/sales_analysis.txt"
    })
    
    print("✅ 数据分析完成")

# 运行分析
data_analysis_pipeline()
```

### 场景 4: 内容生成对接

**需求**: AI 生成内容并自动发布

```python
def content_generation_workflow():
    client = TeyMCPClient()
    
    # 1. 使用 Ollama 生成文章
    article = client.call_tool("ollama_generate", {
        "model": "llama2",
        "prompt": "Write a blog post about the benefits of containerization",
        "stream": False
    })
    
    # 2. 生成配图
    image = client.call_tool("generate_image_dalle", {
        "prompt": "Containerization technology concept art",
        "size": "1024x1024"
    })
    
    # 3. 添加水印
    watermarked = client.call_tool("add_watermark", {
        "image_path": image["path"],
        "text": "© MyCompany 2025"
    })
    
    # 4. 保存到文件系统
    client.call_tool("filesystem_write_file", {
        "path": "/app/content/blog_post.md",
        "content": article["text"]
    })
    
    # 5. 提交到 Git
    client.call_tool("git_commit", {
        "message": "Add new blog post about containerization",
        "files": ["/app/content/blog_post.md"]
    })
    
    # 6. 创建 Pull Request
    client.call_tool("github_create_pull_request", {
        "owner": "myorg",
        "repo": "blog",
        "title": "New blog post: Containerization",
        "body": "Auto-generated content for review",
        "head": "content/new-post",
        "base": "main"
    })
    
    print("✅ 内容生成并提交完成")

# 运行工作流
content_generation_workflow()
```

---

## 故障排查

### 问题 1: GPU 无法访问

**症状**: 容器内 `nvidia-smi` 失败

**解决方案**:
```bash
# 检查 GPU 驱动
nvidia-smi

# 检查 NVIDIA Container Toolkit
nvidia-ctk --version

# 重新配置 Docker Runtime
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# 验证 GPU 访问
docker run --rm --runtime=nvidia --gpus all nvidia/cuda:12.3.0-base-ubuntu22.04 nvidia-smi
```

### 问题 2: 端口冲突

**症状**: `docker-compose up` 报端口已被占用

**解决方案**:
```bash
# 检查端口占用
sudo netstat -tlnp | grep 1215

# 停止占用端口的进程
sudo kill <PID>

# 或修改 docker-compose.yml 端口映射
ports:
  - "新端口:8080"  # 改为未占用的端口
```

### 问题 3: MCP 工具调用失败

**症状**: API 返回 500 错误

**解决方案**:
```bash
# 查看容器日志
docker logs teymcp-server-gpu --tail 100

# 检查 MCP 服务状态
curl http://localhost:1215/api/status

# 重启服务
docker-compose restart

# 检查配置文件
cat config/servers.yaml
```

### 问题 4: 内存不足

**症状**: 容器 OOM (Out of Memory)

**解决方案**:
```bash
# 检查 GPU 内存使用
nvidia-smi

# 增加容器内存限制 (编辑 docker-compose.yml)
services:
  teymcp:
    deploy:
      resources:
        limits:
          memory: 16G  # 增加内存限制
```

### 问题 5: 服务启动慢

**症状**: `docker-compose up` 长时间无响应

**解决方案**:
```bash
# 增加 healthcheck 启动时间
healthcheck:
  start_period: 120s  # 增加到 120 秒

# 查看启动日志
docker-compose logs -f teymcp

# 检查 GPU 初始化
docker exec teymcp-server-gpu nvidia-smi
```

---

## 监控和维护

### 实时监控

```bash
# 使用监控脚本（推荐）
bash monitor_gpu.sh

# 手动监控 GPU
watch -n 1 nvidia-smi

# 监控容器资源
docker stats teymcp-server-gpu

# 查看 MCP 服务状态
watch -n 5 'curl -s http://localhost:1215/api/status | jq'
```

### 日志管理

```bash
# 查看实时日志
docker logs -f teymcp-server-gpu

# 查看最近 100 行日志
docker logs teymcp-server-gpu --tail 100

# 导出日志
docker logs teymcp-server-gpu > teymcp.log

# 清理旧日志
docker-compose down
docker volume rm teymcp-logs
```

### 备份和恢复

```bash
# 备份配置
tar -czf teymcp-backup-$(date +%Y%m%d).tar.gz config/

# 备份数据卷
docker run --rm -v teymcp-logs:/data -v $(pwd):/backup \
  ubuntu tar -czf /backup/logs-backup.tar.gz /data

# 恢复配置
tar -xzf teymcp-backup-20251105.tar.gz

# 恢复数据卷
docker run --rm -v teymcp-logs:/data -v $(pwd):/backup \
  ubuntu tar -xzf /backup/logs-backup.tar.gz -C /
```

---

## 性能优化

### GPU 优化

```yaml
# docker-compose.yml
services:
  teymcp:
    environment:
      # 优化 CUDA 设置
      - CUDA_VISIBLE_DEVICES=0  # 使用特定 GPU
      - CUDA_LAUNCH_BLOCKING=1  # 调试模式
      - CUDA_CACHE_PATH=/root/.cache/cuda
    
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1  # 限制 GPU 数量
              capabilities: [gpu, compute]  # 最小权限
```

### 内存优化

```yaml
services:
  teymcp:
    deploy:
      resources:
        limits:
          memory: 8G
        reservations:
          memory: 4G
```

### 并发优化

```bash
# 增加 worker 数量（编辑 src/main.py）
uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8080,
    workers=4  # 增加 worker 数量
)
```

---

## 安全建议

1. **API 访问控制**: 配置 API 密钥认证
2. **网络隔离**: 使用 Docker 网络隔离
3. **权限最小化**: 容器以非 root 用户运行
4. **日志审计**: 定期检查访问日志
5. **定期更新**: 保持 NVIDIA 驱动和工具链最新

---

## 技术支持

- **文档**: `docs/GPU_SETUP.md` - 完整配置指南
- **快速开始**: `GPU_QUICKSTART.md` - 5 分钟快速上手
- **测试报告**: `GPU_TEST_REPORT.md` - 测试结果和验证
- **脚本工具**: 
  - `start_gpu.sh` - 启动脚本
  - `test_gpu.sh` - 测试脚本
  - `monitor_gpu.sh` - 监控脚本

---

## 更新日志

### v1.0.0 (2025-11-05)

- ✅ 完成 NVIDIA Container Toolkit 集成
- ✅ 实现 GPU 容器化部署
- ✅ 配置端口映射策略 (1215, 1216, 11434)
- ✅ 集成 125 个 MCP 工具
- ✅ 创建完整文档体系
- ✅ 实现监控和管理脚本
- ✅ 通过全部 8 项测试
- ✅ 支持 Ollama 本地 LLM (可选)

---

**版本**: v1.0.0  
**测试状态**: ✅ 100% 通过  
**GPU 支持**: ✅ Tesla P100 验证  
**工具数量**: 125 个  
**服务器数量**: 17 个  
**就绪状态**: 🚀 生产就绪
