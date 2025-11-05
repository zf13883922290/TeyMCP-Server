# ❓ 常见问题 (FAQ)

关于TeyMCP-Server的常见问题解答。

---

## 📚 目录

- [基础问题](#基础问题)
- [安装问题](#安装问题)
- [配置问题](#配置问题)
- [运行问题](#运行问题)
- [性能问题](#性能问题)
- [集成问题](#集成问题)

---

## 基础问题

### Q1: TeyMCP-Server是什么？

**A:** TeyMCP-Server是一个MCP（Model Context Protocol）聚合服务器，可以：
- 🔗 统一管理多个上游MCP服务器
- 🛠️ 提供统一的工具调用接口
- 📊 提供Web管理面板
- 🔄 支持动态添加/移除MCP服务器

### Q2: 为什么需要MCP聚合器？

**A:** 主要优势：
- **统一管理**: 一个地方管理所有MCP服务器
- **命名空间**: 避免工具名称冲突
- **负载均衡**: 自动分发请求
- **监控告警**: 统一的健康检查和日志
- **简化集成**: 客户端只需连接一个服务器

### Q3: 支持哪些MCP服务器？

**A:** 支持所有标准MCP协议的服务器：
- ✅ @modelcontextprotocol/server-github
- ✅ @modelcontextprotocol/server-gitee
- ✅ @modelcontextprotocol/server-filesystem
- ✅ @modelcontextprotocol/server-memory
- ✅ 自定义MCP服务器

### Q4: 需要什么技术栈？

**A:**
- **后端**: Python 3.10+, FastAPI
- **前端**: 内嵌HTML (无需单独部署)
- **运行时**: Node.js 18+ (用于MCP服务器)
- **可选**: Docker, Kubernetes

---

## 安装问题

### Q5: 安装失败怎么办？

**A:** 按照以下步骤排查：

```bash
# 1. 检查Python版本
python3 --version  # 需要 3.10+

# 2. 检查pip
pip3 --version

# 3. 手动创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 4. 手动安装依赖
pip install -r requirements.txt

# 5. 检查Node.js
node --version  # 需要 18+
npm --version
```

### Q6: 虚拟环境创建失败？

**A:** 
```bash
# Ubuntu/Debian
sudo apt-get install python3-venv python3-dev

# CentOS/RHEL
sudo yum install python3-devel

# 手动创建
python3 -m venv venv --clear
```

### Q7: npm安装慢或失败？

**A:**
```bash
# 使用国内镜像
npm config set registry https://registry.npmmirror.com

# 或使用cnpm
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install
```

### Q8: 权限问题？

**A:**
```bash
# 给脚本添加执行权限
chmod +x scripts/*.sh

# 如果是系统级安装问题
sudo chown -R $USER:$USER .
```

---

## 配置问题

### Q9: 如何配置GitHub Token？

**A:**

1. **获取Token**: https://github.com/settings/tokens
2. **权限**: 勾选 `repo`, `read:org`
3. **配置**:
```bash
# config/.env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

### Q10: 如何添加新的MCP服务器？

**A:** 编辑 `config/servers.yaml`:

```yaml
servers:
  my_custom_mcp:
    command: node
    args: ["/path/to/mcp-server.js"]
    env:
      CUSTOM_API_KEY: ${CUSTOM_API_KEY}
    critical: false
```

然后重启服务：
```bash
bash scripts/restart.sh
```

### Q11: 如何修改端口？

**A:** 编辑 `config/app.yaml`:

```yaml
server:
  host: 0.0.0.0
  port: 9090  # 修改这里
```

### Q12: 环境变量不生效？

**A:**
```bash
# 1. 确认.env文件存在
ls -la config/.env

# 2. 检查格式（不要有空格）
# 正确: GITHUB_TOKEN=xxx
# 错误: GITHUB_TOKEN = xxx

# 3. 重启服务
bash scripts/restart.sh
```

---

## 运行问题

### Q13: 启动失败怎么办？

**A:** 查看日志：

```bash
# 查看完整日志
cat data/logs/app.log

# 实时监控日志
tail -f data/logs/app.log

# 检查进程
ps aux | grep "python.*main.py"

# 检查端口
netstat -tlnp | grep 8080
```

### Q14: 端口被占用？

**A:**
```bash
# 查看占用端口的进程
sudo lsof -i :8080

# 杀死进程
sudo kill -9 <PID>

# 或修改配置使用其他端口
vim config/app.yaml
```

### Q15: MCP服务器连接失败？

**A:**

```bash
# 1. 检查MCP服务器本身
npx -y @modelcontextprotocol/server-github

# 2. 检查环境变量
echo $GITHUB_TOKEN

# 3. 查看详细错误
# 在 config/app.yaml 中设置:
logging:
  level: DEBUG
```

### Q16: Web界面打不开？

**A:**
```bash
# 1. 确认服务正在运行
curl http://localhost:8080/health

# 2. 检查防火墙
sudo ufw status
sudo ufw allow 8080

# 3. 检查绑定地址
# config/app.yaml 中确保:
server:
  host: 0.0.0.0  # 不是 127.0.0.1
```

### Q17: API返回500错误？

**A:**
```bash
# 查看详细错误信息
curl -v http://localhost:8080/api/tools

# 检查日志
tail -n 100 data/logs/app.log

# 重启服务
bash scripts/restart.sh
```

---

## 性能问题

### Q18: 响应速度慢？

**A:** 优化建议：

```yaml
# config/app.yaml
performance:
  workers: 4              # 增加worker数量
  timeout: 30             # 调整超时时间
  max_connections: 100    # 最大连接数
```

### Q19: 内存占用高？

**A:**
```bash
# 查看进程内存
ps aux | grep python

# 优化配置
# config/app.yaml
cache:
  enabled: true
  max_size: 100  # 减小缓存大小
```

### Q20: 如何监控性能？

**A:**
```bash
# 访问指标端点
curl http://localhost:8080/api/metrics

# 使用Prometheus
# 参考 docs/DEPLOYMENT.md 的监控章节
```

---

## 集成问题

### Q21: 如何在Claude Desktop中使用？

**A:** 编辑Claude配置文件：

```json
{
  "mcpServers": {
    "teymcp": {
      "command": "curl",
      "args": [
        "-X", "POST",
        "http://localhost:8080/api/tools/{tool_name}/call",
        "-H", "Content-Type: application/json",
        "-d", "{}"
      ]
    }
  }
}
```

### Q22: 如何在代码中调用？

**A:**

**Python示例**:
```python
import requests

# 调用工具
response = requests.post(
    "http://localhost:8080/api/tools/github_create_repository/call",
    json={
        "name": "my-repo",
        "private": False
    }
)
print(response.json())
```

**JavaScript示例**:
```javascript
// 调用工具
const response = await fetch(
  'http://localhost:8080/api/tools/github_create_repository/call',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: 'my-repo',
      private: false
    })
  }
);
const data = await response.json();
console.log(data);
```

### Q23: 支持WebSocket吗？

**A:** 支持！实时获取状态更新：

```javascript
const ws = new WebSocket('ws://localhost:8080/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('状态更新:', data);
};
```

### Q24: 如何实现认证？

**A:** 
```yaml
# config/app.yaml
security:
  enabled: true
  api_key: your-secret-key

# 请求时添加header
curl -H "X-API-Key: your-secret-key" \
  http://localhost:8080/api/tools
```

---

## Docker问题

### Q25: Docker镜像构建失败？

**A:**
```bash
# 清理缓存重新构建
docker build --no-cache -t teymcp-server .

# 查看详细日志
docker build -t teymcp-server . --progress=plain
```

### Q26: 容器启动失败？

**A:**
```bash
# 查看日志
docker logs teymcp-server

# 进入容器调试
docker exec -it teymcp-server /bin/bash

# 检查环境变量
docker exec teymcp-server env
```

---

## 其他问题

### Q27: 如何升级版本？

**A:**
```bash
# 1. 备份数据
tar -czf backup.tar.gz config/ data/

# 2. 拉取最新代码
git pull origin main

# 3. 更新依赖
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 4. 重启服务
bash scripts/restart.sh
```

### Q28: 如何备份数据？

**A:**
```bash
# 备份配置和日志
tar -czf teymcp-backup-$(date +%Y%m%d).tar.gz \
  config/ data/ .env

# 恢复
tar -xzf teymcp-backup-20250104.tar.gz
```

### Q29: 如何贡献代码？

**A:** 参考 [CONTRIBUTING.md](../CONTRIBUTING.md)

### Q30: 如何报告Bug？

**A:** 
1. 在GitHub上 [创建Issue](https://github.com/zf13883922290/TeyMCP-Server/issues/new)
2. 提供以下信息：
   - 系统版本
   - Python版本
   - 错误日志
   - 复现步骤

---

## 📚 更多资源

- [快速入门](QUICKSTART.md)
- [配置说明](CONFIGURATION.md)
- [API文档](API.md)
- [故障排查](TROUBLESHOOTING.md)
- [部署指南](DEPLOYMENT.md)

---

## 🆘 还有问题？

- **GitHub Issues**: https://github.com/zf13883922290/TeyMCP-Server/issues
- **邮件**: support@example.com
- **讨论区**: https://github.com/zf13883922290/TeyMCP-Server/discussions

---

**找不到答案？别犹豫，直接提Issue！** 💬
