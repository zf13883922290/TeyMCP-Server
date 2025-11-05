# 🔧 故障排查指南

TeyMCP-Server问题诊断和解决方案。

---

## 📋 目录

- [诊断工具](#诊断工具)
- [启动问题](#启动问题)
- [连接问题](#连接问题)
- [性能问题](#性能问题)
- [日志分析](#日志分析)
- [常见错误码](#常见错误码)

---

## 诊断工具

### 🔍 运行自动诊断

```bash
# 运行完整诊断
bash verify.sh

# 检查项目：
# ✅ Python环境
# ✅ Node.js环境
# ✅ 配置文件
# ✅ 端口可用性
# ✅ MCP服务器连接
```

### 📊 手动检查清单

```bash
# 1. 检查Python
python3 --version
which python3

# 2. 检查虚拟环境
source venv/bin/activate
pip list | grep fastapi

# 3. 检查Node.js
node --version
npm --version

# 4. 检查进程
ps aux | grep "python.*main.py"

# 5. 检查端口
netstat -tlnp | grep 8080

# 6. 检查日志
tail -f data/logs/app.log

# 7. 检查配置
cat config/servers.yaml
cat config/.env
```

---

## 启动问题

### ❌ 问题: 脚本执行失败

**错误**:
```
bash: scripts/start.sh: Permission denied
```

**解决方案**:
```bash
# 添加执行权限
chmod +x scripts/*.sh

# 或直接使用bash执行
bash scripts/start.sh
```

---

### ❌ 问题: 虚拟环境未激活

**错误**:
```
ModuleNotFoundError: No module named 'fastapi'
```

**解决方案**:
```bash
# 激活虚拟环境
source venv/bin/activate

# 确认激活成功（命令提示符会显示(venv)）
which python  # 应该指向 venv/bin/python

# 重新安装依赖
pip install -r requirements.txt
```

---

### ❌ 问题: 端口被占用

**错误**:
```
Error: Address already in use: ('0.0.0.0', 8080)
```

**解决方案**:
```bash
# 方案1: 杀死占用进程
sudo lsof -i :8080
sudo kill -9 <PID>

# 方案2: 修改端口
vim config/app.yaml
# 修改 port: 8080 为其他端口

# 方案3: 使用stop脚本
bash scripts/stop.sh
bash scripts/start.sh
```

---

### ❌ 问题: 配置文件未找到

**错误**:
```
FileNotFoundError: config/servers.yaml not found
```

**解决方案**:
```bash
# 检查配置文件
ls -la config/

# 如果缺失，复制示例
cp config/servers.yaml.example config/servers.yaml
cp config/.env.example config/.env

# 编辑配置
vim config/.env
```

---

## 连接问题

### ❌ 问题: MCP服务器连接失败

**错误**:
```
Failed to connect to MCP server: github
Error: spawn npx ENOENT
```

**诊断步骤**:
```bash
# 1. 检查Node.js
node --version
npm --version

# 2. 手动测试MCP服务器
npx -y @modelcontextprotocol/server-github

# 3. 检查环境变量
cat config/.env | grep GITHUB_TOKEN
echo $GITHUB_TOKEN

# 4. 测试网络连接
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

**解决方案**:
```bash
# 安装Node.js (如果未安装)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 清除npm缓存
npm cache clean --force

# 重新安装MCP包
npx -y @modelcontextprotocol/server-github

# 检查配置
vim config/servers.yaml
# 确保 command 和 args 正确
```

---

### ❌ 问题: API Token无效

**错误**:
```
HTTP 401: Bad credentials
```

**解决方案**:
```bash
# 1. 重新生成Token
# GitHub: https://github.com/settings/tokens
# 权限: repo, read:org

# 2. 更新配置
vim config/.env
GITHUB_TOKEN=ghp_新的token

# 3. 重启服务
bash scripts/restart.sh

# 4. 验证Token
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

---

### ❌ 问题: 网络超时

**错误**:
```
TimeoutError: Request timeout after 30s
```

**解决方案**:
```bash
# 增加超时时间
vim config/app.yaml

# 添加:
timeout:
  connect: 60
  read: 60
  
# 检查网络
ping api.github.com
curl -v https://api.github.com

# 使用代理（如果需要）
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

---

## 性能问题

### 🐌 问题: 响应速度慢

**诊断**:
```bash
# 1. 检查系统负载
top
htop

# 2. 检查内存
free -h

# 3. 检查磁盘IO
iostat -x 1

# 4. 测试API响应时间
time curl http://localhost:8080/api/health
```

**优化方案**:
```yaml
# config/app.yaml
performance:
  workers: 4              # 根据CPU核心数调整
  threads: 2              # 每个worker的线程数
  timeout: 30             # 请求超时
  max_connections: 100    # 最大连接数

cache:
  enabled: true           # 启用缓存
  ttl: 300               # 缓存时间(秒)
  max_size: 1000         # 最大缓存条目

logging:
  level: WARNING         # 减少日志级别
```

---

### 💾 问题: 内存占用高

**诊断**:
```bash
# 查看进程内存
ps aux --sort=-%mem | grep python

# 详细内存分析
python3 -m memory_profiler src/main.py
```

**解决方案**:
```bash
# 1. 减少worker数量
vim config/app.yaml
# workers: 2

# 2. 限制缓存大小
# cache.max_size: 100

# 3. 定期重启
crontab -e
# 0 3 * * * /path/to/scripts/restart.sh

# 4. 使用生产配置
export PRODUCTION=true
bash scripts/start.sh
```

---

### 📊 问题: CPU使用率高

**诊断**:
```bash
# 查看CPU占用
top -p $(pgrep -f "python.*main.py")

# 查看线程
ps -eLf | grep python
```

**解决方案**:
```bash
# 1. 检查死循环或频繁请求
tail -f data/logs/app.log | grep ERROR

# 2. 减少轮询频率
vim config/app.yaml
# health_check_interval: 60  # 从30秒改为60秒

# 3. 异步处理
# 确保config/app.yaml中:
async:
  enabled: true
```

---

## 日志分析

### 📝 日志位置

```bash
# 应用日志
data/logs/app.log

# 访问日志
data/logs/access.log

# 错误日志
data/logs/error.log

# MCP日志
data/logs/mcp/
```

### 🔍 日志分析命令

```bash
# 查看最新日志
tail -n 100 data/logs/app.log

# 实时监控
tail -f data/logs/app.log

# 查找错误
grep ERROR data/logs/app.log

# 查找特定时间
grep "2025-01-04 10:" data/logs/app.log

# 统计错误类型
grep ERROR data/logs/app.log | cut -d':' -f3 | sort | uniq -c

# 查看最频繁的错误
grep ERROR data/logs/app.log | sort | uniq -c | sort -rn | head -10
```

### 📊 日志级别调整

```yaml
# config/app.yaml
logging:
  level: DEBUG           # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format: detailed       # simple, detailed, json
  rotation: daily        # daily, size
  max_size: 100MB       # 单文件最大大小
  backup_count: 7       # 保留日志数量
```

---

## 常见错误码

### HTTP错误码

| 错误码 | 含义 | 可能原因 | 解决方案 |
|-------|------|---------|---------|
| 400 | Bad Request | 请求参数错误 | 检查API文档，验证参数 |
| 401 | Unauthorized | 认证失败 | 检查API Key或Token |
| 403 | Forbidden | 权限不足 | 检查Token权限 |
| 404 | Not Found | 资源不存在 | 检查URL和资源名称 |
| 429 | Too Many Requests | 请求过多 | 等待或增加限流阈值 |
| 500 | Internal Server Error | 服务器内部错误 | 查看日志，重启服务 |
| 502 | Bad Gateway | 上游服务器错误 | 检查MCP服务器 |
| 503 | Service Unavailable | 服务不可用 | 检查服务状态 |
| 504 | Gateway Timeout | 网关超时 | 增加超时时间 |

### MCP错误码

```python
# MCP特定错误
MCP_CONNECTION_ERROR    = "连接MCP服务器失败"
MCP_TIMEOUT_ERROR       = "MCP请求超时"
MCP_INVALID_RESPONSE    = "MCP响应格式错误"
TOOL_NOT_FOUND          = "工具不存在"
TOOL_EXECUTION_ERROR    = "工具执行失败"
```

**排查步骤**:
```bash
# 1. 检查MCP服务器状态
curl http://localhost:8080/api/servers

# 2. 测试特定服务器
curl http://localhost:8080/api/servers/github

# 3. 查看详细日志
grep "MCP ERROR" data/logs/app.log -A 10

# 4. 重新连接
curl -X POST http://localhost:8080/api/servers/github/reconnect
```

---

## Docker故障排查

### 🐳 容器无法启动

```bash
# 查看容器日志
docker logs teymcp-server

# 查看容器状态
docker ps -a | grep teymcp

# 进入容器调试
docker exec -it teymcp-server /bin/bash

# 检查容器资源
docker stats teymcp-server

# 重建容器
docker-compose down
docker-compose up --build -d
```

### 🔗 容器网络问题

```bash
# 检查网络
docker network ls
docker network inspect teymcp_network

# 测试容器间连接
docker exec teymcp-server ping other-container

# 重建网络
docker-compose down
docker network prune
docker-compose up -d
```

---

## 高级诊断

### 🔬 性能分析

```bash
# Python性能分析
pip install py-spy
sudo py-spy top --pid $(pgrep -f "python.*main.py")

# 生成火焰图
sudo py-spy record -o profile.svg --pid $(pgrep -f "python.*main.py")
```

### 🧪 压力测试

```bash
# 安装工具
pip install locust

# 创建测试脚本
cat > locustfile.py << 'EOF'
from locust import HttpUser, task

class TeyMCPUser(HttpUser):
    @task
    def health_check(self):
        self.client.get("/health")
    
    @task(3)
    def list_tools(self):
        self.client.get("/api/tools")
EOF

# 运行压测
locust -f locustfile.py --host=http://localhost:8080
```

---

## 数据恢复

### 💾 备份

```bash
# 自动备份脚本
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_${DATE}.tar.gz config/ data/ .env
find . -name "backup_*.tar.gz" -mtime +7 -delete
EOF

chmod +x backup.sh

# 添加到crontab
crontab -e
# 每天凌晨3点备份
0 3 * * * /path/to/backup.sh
```

### 🔄 恢复

```bash
# 停止服务
bash scripts/stop.sh

# 恢复数据
tar -xzf backup_20250104_030000.tar.gz

# 启动服务
bash scripts/start.sh

# 验证
curl http://localhost:8080/health
```

---

## 紧急恢复

### 🚨 完全重置

```bash
# ⚠️ 警告: 这会删除所有数据！

# 1. 备份重要数据
cp config/.env ~/.env.backup
tar -czf logs_backup.tar.gz data/logs/

# 2. 停止服务
bash scripts/stop.sh

# 3. 清理数据
rm -rf data/logs/*
rm -rf data/metrics/*
rm -rf venv/

# 4. 重新安装
bash scripts/install.sh

# 5. 恢复配置
cp ~/.env.backup config/.env

# 6. 启动服务
bash scripts/start.sh
```

---

## 获取帮助

### 📞 联系方式

- **GitHub Issues**: https://github.com/zf13883922290/TeyMCP-Server/issues
- **讨论区**: https://github.com/zf13883922290/TeyMCP-Server/discussions
- **邮件**: support@example.com

### 📤 报告问题时请提供

1. **系统信息**:
```bash
uname -a
python3 --version
node --version
```

2. **错误日志**:
```bash
tail -n 100 data/logs/app.log
```

3. **配置信息** (隐藏敏感信息):
```bash
cat config/servers.yaml | sed 's/token:.*/token: ***/'
```

4. **复现步骤**: 详细的操作步骤

---

## 📚 相关文档

- [快速入门](QUICKSTART.md)
- [FAQ](FAQ.md)
- [API文档](API.md)
- [配置说明](CONFIGURATION.md)

---

**遇到问题不要慌，按照步骤排查！** 🔧
