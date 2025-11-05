# TeyMCP-Server 快速使用指南

## 🚀 快速启动

```bash
# 方法1: 使用快速启动脚本 (推荐)
bash start.sh

# 方法2: 使用服务管理脚本
bash service.sh start
```

## 🔌 访问地址

- **端口号**: `1215` (固定端口,避免冲突)
- **管理面板**: http://localhost:1215
- **API文档**: http://localhost:1215/api/docs
- **状态API**: http://localhost:1215/api/status

## 🛠️ 管理命令

```bash
# 启动服务器 (自动清理旧进程)
bash start.sh

# 查看服务状态
bash service.sh status

# 实时查看日志
bash view_logs.sh

# 停止服务器
bash service.sh stop

# 重启服务器
bash service.sh restart

# 查看最近日志
bash service.sh logs
```

## 📊 当前状态

运行 `bash service.sh status` 可以看到:
- ✅ 6个MCP服务器已加载
- 🔧 55个工具可用
- 包括: memory, sequential_thinking, github, puppeteer, local_automation, media_generator

## 🔑 已配置的TOKEN

- ✅ GitHub Token (26个工具)
- ✅ Gitee Token (个人+企业)
- ✅ HuggingFace Token

配置文件: `config/.env`

## 📝 日志文件

- **启动日志**: `/tmp/teymcp_startup.log`
- **持久日志**: `data/logs/teymcp.log`

## ⚙️ 配置文件

- **应用配置**: `config/app.yaml` (端口设置)
- **服务器配置**: `config/servers.yaml` (MCP服务器)
- **环境变量**: `config/.env` (API密钥)

## 🎯 特点

1. **自动进程管理**: 启动前自动清理旧进程
2. **固定端口**: 1215端口,避免与常见服务冲突
3. **完整生态**: 40+配置的MCP服务器
4. **便捷管理**: 多个管理脚本支持

## 🐛 故障排查

如果服务启动失败:

```bash
# 1. 查看错误日志
tail -50 /tmp/teymcp_startup.log

# 2. 确认端口未被占用
netstat -tlnp | grep 1215

# 3. 手动清理进程
pkill -9 -f "python.*src/main.py"

# 4. 重新启动
bash start.sh
```
