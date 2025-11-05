# 🚀 快速入门

5分钟快速部署TeyMCP-Server！

---

## 📦 一键安装

```bash
# 1. 克隆项目
git clone https://github.com/zf13883922290/TeyMCP-Server.git
cd TeyMCP-Server

# 2. 运行安装脚本（自动安装所有依赖）
bash scripts/install.sh

# 3. 配置环境变量
cp config/.env.example config/.env
# 编辑 config/.env 填入你的API密钥

# 4. 启动服务
bash scripts/start.sh
```

**就这么简单！** 🎉

---

## 🌐 访问服务

启动成功后，打开浏览器访问：

- **Web管理面板**: http://localhost:8080
- **API文档**: http://localhost:8080/docs
- **健康检查**: http://localhost:8080/health

---

## 🔧 配置MCP服务器

编辑 `config/servers.yaml`：

```yaml
servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_TOKEN: ${GITHUB_TOKEN}
    critical: true
    
  gitee:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-gitee"]
    env:
      GITEE_TOKEN: ${GITEE_TOKEN}
    critical: false
```

在 `config/.env` 中设置密钥：

```bash
GITHUB_TOKEN=ghp_your_token_here
GITEE_TOKEN=your_gitee_token_here
```

---

## 📡 测试API

### 查看所有工具

```bash
curl http://localhost:8080/api/tools
```

### 调用GitHub工具

```bash
curl -X POST http://localhost:8080/api/tools/github_create_repository/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-repo",
    "description": "Test repository",
    "private": false
  }'
```

### 查看服务器状态

```bash
curl http://localhost:8080/api/servers
```

---

## 🎯 常用命令

```bash
# 启动服务
bash scripts/start.sh

# 停止服务
bash scripts/stop.sh

# 重启服务
bash scripts/restart.sh

# 查看日志
tail -f data/logs/app.log

# 查看实时状态
watch -n 1 curl -s http://localhost:8080/api/status
```

---

## 🐳 Docker快速部署

```bash
# 使用Docker Compose
cd docker
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 🔍 验证安装

运行验证脚本：

```bash
bash verify.sh
```

检查项目：
- ✅ Python虚拟环境
- ✅ Node.js和npm
- ✅ 配置文件
- ✅ MCP服务器连接
- ✅ API响应

---

## ⚠️ 常见问题

### 问题1: 端口被占用

```bash
# 修改端口
vim config/app.yaml
# 将 port: 8080 改为其他端口
```

### 问题2: MCP服务器连接失败

```bash
# 检查环境变量
cat config/.env

# 手动测试MCP连接
npx -y @modelcontextprotocol/server-github
```

### 问题3: 权限不足

```bash
# 给脚本添加执行权限
chmod +x scripts/*.sh
```

---

## 📚 下一步

- [完整配置说明](CONFIGURATION.md) - 详细配置选项
- [API文档](API.md) - 完整API参考
- [部署指南](DEPLOYMENT.md) - 生产环境部署
- [故障排查](TROUBLESHOOTING.md) - 问题解决方案

---

## 💡 提示

- 首次启动会自动安装npm依赖，可能需要几分钟
- 确保8080端口未被占用
- 日志文件在 `data/logs/app.log`
- 配置修改后需要重启服务

---

## 🆘 需要帮助？

- [GitHub Issues](https://github.com/zf13883922290/TeyMCP-Server/issues)
- [FAQ](FAQ.md)
- [故障排查指南](TROUBLESHOOTING.md)

---

**现在开始使用TeyMCP-Server吧！** 🚀
