# ⚙️ 配置详解

TeyMCP-Server 完整配置说明文档。

---

## 📋 目录

- [配置文件概览](#配置文件概览)
- [应用配置](#应用配置-appyaml)
- [服务器配置](#服务器配置-serversyaml)
- [环境变量](#环境变量-env)
- [日志配置](#日志配置)
- [性能配置](#性能配置)
- [安全配置](#安全配置)
- [配置示例](#配置示例)

---

## 📁 配置文件概览

TeyMCP-Server 使用多个配置文件管理不同方面的设置：

```
config/
├── app.yaml          # 应用主配置
├── servers.yaml      # MCP服务器配置  
├── .env              # 环境变量（敏感信息）
└── .env.example      # 环境变量示例
```

**配置优先级**:
1. 环境变量 (最高优先级)
2. `.env` 文件
3. YAML 配置文件
4. 默认值 (最低优先级)

---

## 🎛️ 应用配置 (app.yaml)

### 基础配置

```yaml
# 服务器配置
server:
  host: 0.0.0.0          # 监听地址，0.0.0.0 表示监听所有网络接口
  port: 8080             # 监听端口
  workers: 4             # Worker进程数，建议设置为CPU核心数
  
# 应用信息
app:
  name: TeyMCP-Server
  version: 1.0.0
  debug: false           # 调试模式，生产环境务必设置为 false
```

### 完整配置示例

```yaml
# ============================================
# TeyMCP-Server 应用配置
# ============================================

# 服务器配置
server:
  host: 0.0.0.0
  port: 8080
  workers: 4
  reload: false          # 热重载（仅开发环境）

# 日志配置
logging:
  level: INFO            # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format: json           # json 或 text
  file: data/logs/app.log
  rotation: daily        # daily, weekly, size
  max_size: 100MB        # 单文件最大大小（rotation=size时）
  backup_count: 7        # 保留日志文件数量

# 性能配置
performance:
  timeout: 30            # 请求超时时间（秒）
  max_connections: 100   # 最大并发连接数
  keep_alive: 60         # Keep-Alive 超时（秒）

# 缓存配置
cache:
  enabled: true          # 启用缓存
  ttl: 300              # 缓存过期时间（秒）
  max_size: 1000        # 最大缓存条目数

# 安全配置
security:
  enabled: false         # 启用API密钥认证
  api_key: ""           # API密钥（建议使用环境变量）
  cors:
    enabled: true        # 启用CORS
    origins:             # 允许的源
      - "*"
    methods:             # 允许的HTTP方法
      - GET
      - POST
      - PUT
      - DELETE
    headers:             # 允许的请求头
      - "*"

# 监控配置
monitoring:
  enabled: true          # 启用监控
  metrics_port: 9090     # Prometheus指标端口
  health_check_interval: 30  # 健康检查间隔（秒）

# 数据存储
storage:
  log_retention_days: 30      # 日志保留天数
  metrics_retention_days: 90   # 指标保留天数
  data_dir: data/              # 数据目录
```

---

## 🖥️ 服务器配置 (servers.yaml)

### 配置结构

```yaml
servers:
  <服务器名称>:
    command: <启动命令>
    args: [<参数列表>]
    env: {<环境变量>}
    critical: <true/false>
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `command` | string | ✅ | 启动命令（如 `npx`, `node`, `python`） |
| `args` | array | ✅ | 命令参数 |
| `env` | object | ❌ | 环境变量（可引用 `.env` 中的变量） |
| `critical` | boolean | ❌ | 是否为关键服务器（启动失败时是否中止）|

### 示例配置

```yaml
# ============================================
# MCP 服务器配置
# ============================================

servers:
  # GitHub MCP服务器
  github:
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-github"
    env:
      GITHUB_TOKEN: ${GITHUB_TOKEN}    # 从 .env 读取
    critical: true                      # 关键服务器
    
  # Gitee MCP服务器
  gitee:
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-gitee"
    env:
      GITEE_TOKEN: ${GITEE_TOKEN}
    critical: false
    
  # 文件系统MCP
  filesystem:
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-filesystem"
      - "/home/user/allowed-directory"  # 允许访问的目录
    critical: true
    
  # 内存MCP（知识存储）
  memory:
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-memory"
    critical: false
    
  # AWS MCP服务器
  aws:
    command: npx
    args:
      - "-y"
      - "@aws/mcp-server-aws"
    env:
      AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
      AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
      AWS_REGION: ${AWS_REGION}
    critical: false
    
  # 自定义Node.js MCP
  custom-nodejs:
    command: node
    args:
      - "/path/to/custom-mcp-server.js"
    env:
      CUSTOM_API_KEY: ${CUSTOM_API_KEY}
    critical: false
    
  # 自定义Python MCP
  custom-python:
    command: python
    args:
      - "/path/to/custom_mcp_server.py"
    env:
      PYTHON_API_KEY: ${PYTHON_API_KEY}
    critical: false
```

### 环境变量引用

在 `servers.yaml` 中，可以使用 `${VAR_NAME}` 语法引用环境变量：

```yaml
servers:
  github:
    env:
      # 直接引用 .env 中的变量
      GITHUB_TOKEN: ${GITHUB_TOKEN}
      
      # 带默认值
      API_ENDPOINT: ${API_ENDPOINT:-https://api.github.com}
      
      # 系统环境变量
      HOME: ${HOME}
```

---

## 🔐 环境变量 (.env)

### 创建配置文件

```bash
# 复制示例文件
cp config/.env.example config/.env

# 编辑配置
nano config/.env
```

### 完整示例

```bash
# ============================================
# TeyMCP-Server 环境变量配置
# ============================================

# -------------------- MCP服务器密钥 --------------------

# GitHub Personal Access Token
# 获取: https://github.com/settings/tokens
# 权限: repo, read:org, read:user
GITHUB_TOKEN=ghp_your_github_token_here

# Gitee Personal Access Token
# 获取: https://gitee.com/profile/personal_access_tokens
# 权限: projects, user_info
GITEE_TOKEN=your_gitee_token_here

# AWS凭证
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# -------------------- 应用配置 --------------------

# 服务器配置
HOST=0.0.0.0
PORT=8080

# 日志级别
LOG_LEVEL=INFO

# 环境
ENVIRONMENT=production

# -------------------- 安全配置 --------------------

# API密钥（如果启用认证）
API_KEY=your-secret-api-key-here

# CORS配置
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# -------------------- 性能配置 --------------------

# Worker数量
WORKERS=4

# 超时时间（秒）
TIMEOUT=30

# 最大连接数
MAX_CONNECTIONS=100

# -------------------- 缓存配置 --------------------

CACHE_ENABLED=true
CACHE_TTL=300
CACHE_MAX_SIZE=1000

# -------------------- 数据库配置 --------------------

# SQLite（默认）
DATABASE_URL=sqlite:///data/teymcp.db

# 或 PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost/teymcp

# -------------------- 监控配置 --------------------

# Prometheus指标
METRICS_PORT=9090
METRICS_ENABLED=true

# 健康检查
HEALTH_CHECK_ENABLED=true
HEALTH_CHECK_INTERVAL=30

# -------------------- 第三方服务 --------------------

# Sentry错误追踪
# SENTRY_DSN=https://xxx@sentry.io/xxx

# Redis缓存
# REDIS_URL=redis://localhost:6379/0

# -------------------- 自定义MCP配置 --------------------

# 自定义服务器1
CUSTOM_MCP_1_TOKEN=your_token_here
CUSTOM_MCP_1_ENDPOINT=https://api.example.com

# 自定义服务器2
CUSTOM_MCP_2_API_KEY=your_api_key_here
```

### 安全建议

⚠️ **重要**: 
- **不要提交** `.env` 文件到Git仓库
- 已添加到 `.gitignore`
- 生产环境使用**强密码**和**密钥**
- 定期**轮换密钥**

---

## 📝 日志配置

### 日志级别

```yaml
logging:
  level: INFO    # DEBUG | INFO | WARNING | ERROR | CRITICAL
```

| 级别 | 用途 | 输出量 |
|------|------|--------|
| `DEBUG` | 开发调试 | 最多 |
| `INFO` | 正常运行 | 中等 |
| `WARNING` | 警告信息 | 较少 |
| `ERROR` | 错误信息 | 很少 |
| `CRITICAL` | 严重错误 | 最少 |

### 日志格式

```yaml
logging:
  format: json    # json | text
```

**JSON格式** (推荐生产环境):
```json
{
  "timestamp": "2025-01-04T10:30:00Z",
  "level": "INFO",
  "message": "服务器启动成功",
  "server": "github",
  "pid": 12345
}
```

**文本格式** (适合开发环境):
```
2025-01-04 10:30:00 [INFO] 服务器启动成功 (server=github, pid=12345)
```

### 日志轮转

```yaml
logging:
  rotation: daily     # daily | weekly | size
  max_size: 100MB     # rotation=size 时生效
  backup_count: 7     # 保留文件数
```

---

## ⚡ 性能配置

### Worker配置

```yaml
performance:
  workers: 4    # 建议设置为 CPU 核心数
```

确定最佳worker数量:
```bash
# Linux/Mac
nproc

# 或
python -c "import os; print(os.cpu_count())"
```

### 超时配置

```yaml
performance:
  timeout: 30              # 请求超时（秒）
  mcp_connect_timeout: 10  # MCP连接超时
  mcp_call_timeout: 30     # 工具调用超时
```

### 连接池

```yaml
performance:
  max_connections: 100    # 最大并发连接数
  keep_alive: 60         # Keep-Alive超时
```

### 缓存配置

```yaml
cache:
  enabled: true           # 启用缓存
  ttl: 300               # 过期时间（秒）
  max_size: 1000         # 最大缓存条目
  strategy: lru          # 缓存策略: lru | lfu | fifo
```

---

## 🔒 安全配置

### API密钥认证

```yaml
security:
  enabled: true
  api_key: ${API_KEY}    # 从环境变量读取
```

使用方式:
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8080/api/status
```

### CORS配置

```yaml
security:
  cors:
    enabled: true
    origins:
      - "https://yourdomain.com"
      - "http://localhost:3000"
    methods:
      - GET
      - POST
      - PUT
      - DELETE
    headers:
      - "Content-Type"
      - "Authorization"
```

**开发环境** (允许所有源):
```yaml
security:
  cors:
    enabled: true
    origins: ["*"]
```

### 速率限制

```yaml
rate_limit:
  enabled: true
  requests_per_minute: 60    # 每分钟请求数
  burst: 10                  # 突发请求数
```

---

## 📊 监控配置

### Prometheus指标

```yaml
monitoring:
  enabled: true
  metrics_port: 9090
```

访问指标:
```bash
curl http://localhost:9090/metrics
```

### 健康检查

```yaml
monitoring:
  health_check_interval: 30    # 检查间隔（秒）
  health_check_timeout: 5      # 检查超时（秒）
```

---

## 🎯 配置示例

### 开发环境配置

```yaml
# config/app.yaml (开发环境)
server:
  host: 127.0.0.1
  port: 8080
  workers: 1
  reload: true         # 热重载

logging:
  level: DEBUG
  format: text

security:
  enabled: false
  cors:
    origins: ["*"]

cache:
  enabled: false
```

### 生产环境配置

```yaml
# config/app.yaml (生产环境)
server:
  host: 0.0.0.0
  port: 8080
  workers: 4
  reload: false

logging:
  level: WARNING
  format: json
  rotation: daily
  backup_count: 30

security:
  enabled: true
  api_key: ${API_KEY}
  cors:
    origins:
      - "https://yourdomain.com"

cache:
  enabled: true
  ttl: 300
  max_size: 1000

performance:
  timeout: 30
  max_connections: 100
```

---

## 🔄 配置热重载

修改配置后无需重启:

```bash
# 重新加载配置
curl -X POST http://localhost:8080/api/config/reload

# 或发送HUP信号
kill -HUP $(pgrep -f "python.*main.py")
```

---

## ✅ 配置验证

### 验证配置文件

```bash
# 验证YAML语法
python -c "import yaml; yaml.safe_load(open('config/app.yaml'))"
python -c "import yaml; yaml.safe_load(open('config/servers.yaml'))"

# 验证环境变量
python << 'EOF'
from dotenv import load_dotenv
import os

load_dotenv('config/.env')

required_vars = ['GITHUB_TOKEN', 'GITEE_TOKEN']
for var in required_vars:
    if os.getenv(var):
        print(f"✅ {var}: 已设置")
    else:
        print(f"❌ {var}: 未设置")
EOF
```

### 启动时验证

```bash
# 启动时会自动验证配置
python src/main.py

# 输出示例:
# ✅ 配置验证通过
# ✅ GitHub Token: 已设置
# ✅ Gitee Token: 已设置
# ⚠️  AWS Token: 未设置（非关键服务器）
```

---

## 🛠️ 故障排查

### 配置未生效

```bash
# 1. 检查配置文件路径
ls -la config/

# 2. 检查YAML语法
python -m yaml config/app.yaml

# 3. 检查环境变量
echo $GITHUB_TOKEN

# 4. 查看启动日志
tail -f data/logs/app.log
```

### 环境变量未加载

```bash
# 确认 .env 文件存在
ls -la config/.env

# 检查格式（不要有空格）
cat config/.env

# 正确: GITHUB_TOKEN=xxx
# 错误: GITHUB_TOKEN = xxx
```

---

## 📚 相关文档

- [快速入门](QUICKSTART.md) - 快速配置和启动
- [部署指南](DEPLOYMENT.md) - 生产环境配置
- [API文档](API.md) - API接口说明
- [故障排查](TROUBLESHOOTING.md) - 问题解决

---

**配置正确，运行顺畅！** ⚙️
