# TeyMCP-Server 2.0

```
  _____         __  __  ____ ____  
 |_   _|__ _   _|  \/  |/ ___|  _ \ 
   | |/ _ \ | | | |\/| | |   | |_) |
   | |  __/ |_| | |  | | |___|  __/ 
   |_|\___|\__, |_|  |_|\____|_|    
           |___/                     
    ____                            
   / ___|  ___ _ ____   _____ _ __  
   \___ \ / _ \ '__\ \ / / _ \ '__| 
    ___) |  __/ |   \ V /  __/ |    
   |____/ \___|_|    \_/ \___|_|    

  🌟 The One MCP to Rule Them All 🌟
```

**版本**: 2.0  
**作者**: zf13883922290  
**许可**: MIT  

## 📋 项目简介

TeyMCP-Server 是一个强大的 MCP (Model Context Protocol) 聚合服务器,能够统一管理和调用多个上游 MCP 服务器,为 AI 应用提供统一的工具和资源接口。

### ✨ 核心特性

- 🔌 **多服务器聚合**: 支持40+个MCP服务器同时运行
- 🚀 **双协议支持**: STDIO 和 HTTP/SSE 两种连接方式
- 🎯 **统一接口**: 一个端点访问所有MCP工具
- 📊 **实时监控**: Web管理面板实时查看状态
- 🔧 **易于扩展**: 简单添加自定义MCP服务器
- 🛡️ **自动管理**: 进程自动清理和重启

## 🚀 快速开始

### 1. 启动服务器

```bash
bash start.sh
```

服务器将自动:
- ✅ 清理旧进程
- ✅ 启动新服务 (端口: 1215)
- ✅ 加载所有MCP服务器
- ✅ 显示完整的访问信息

### 2. 访问服务

启动后访问以下地址:

| 功能 | 地址 | 说明 |
|------|------|------|
| 🏠 管理面板 | http://localhost:1215 | Web管理界面 |
| 📚 API文档 | http://localhost:1215/api/docs | Swagger文档 |
| 📊 状态监控 | http://localhost:1215/api/status | 服务器状态 |
| 📝 日志接口 | http://localhost:1215/api/logs | 实时日志 |
| 🔧 工具列表 | http://localhost:1215/api/tools | 所有可用工具 |
| 🖥️ 服务器列表 | http://localhost:1215/api/servers | MCP服务器列表 |

## 🛠️ 管理命令

```bash
# 启动服务器
bash start.sh

# 查看状态
bash service.sh status

# 实时日志
bash view_logs.sh

# 停止服务
bash service.sh stop

# 重启服务
bash service.sh restart

# 查看最近日志
bash service.sh logs
```

## 📦 已集成的MCP服务器

### ✅ 当前运行中 (6个服务器, 55个工具)

| 服务器 | 工具数 | 说明 |
|--------|--------|------|
| **memory** | 9 | 知识图谱记忆系统 |
| **sequential_thinking** | 1 | 思维链推理 |
| **github** | 26 | GitHub集成 |
| **puppeteer** | 7 | 浏览器自动化 |
| **local_automation** | 6 | 文件自动化 (自定义) |
| **media_generator** | 6 | 媒体生成 (自定义) |

### 📋 已配置但未启用的服务器

查看 `config/servers.yaml` 了解完整的40+服务器列表,包括:
- 官方服务器: fetch, filesystem, git, time 等
- 官方集成: Microsoft Azure, Slack, GitLab 等
- 社区服务器: Playwright, Database集成等

## ⚙️ 配置文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 应用配置 | `config/app.yaml` | 端口、日志等设置 |
| MCP服务器 | `config/servers.yaml` | 服务器配置 |
| 环境变量 | `config/.env` | API密钥和令牌 |

### 🔑 已配置的TOKEN

- ✅ GitHub Token - 26个工具可用
- ✅ Gitee Token (个人+企业)
- ✅ HuggingFace Token

## 📝 日志文件

- **启动日志**: `/tmp/teymcp_startup.log` - 服务器启动和初始化
- **持久日志**: `data/logs/teymcp.log` - 完整运行日志

## 🔥 防火墙配置

端口 **1215** 已自动开启:

```bash
# 如需手动配置
sudo ufw allow 1215/tcp
```

## 🌐 外部访问

如需从其他设备访问,替换 `localhost` 为服务器IP:

```
http://YOUR_SERVER_IP:1215
```

## 📚 项目资源

- 🔗 **GitHub仓库**: https://github.com/zf13883922290/TeyMCP-Server
- 🐛 **问题反馈**: https://github.com/zf13883922290/TeyMCP-Server/issues
- 📖 **Wiki文档**: https://github.com/zf13883922290/TeyMCP-Server/wiki
- 🤝 **贡献指南**: [CONTRIBUTING.md](CONTRIBUTING.md)
- ⚡ **快速开始**: [QUICKSTART.md](QUICKSTART.md)

## 👥 社区与支持

### 联系方式

- **作者**: zf13883922290
- **GitHub**: [@zf13883922290](https://github.com/zf13883922290)
- **邮箱**: 在GitHub Profile查看

### 贡献

欢迎贡献代码、报告问题或提出建议!

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [Model Context Protocol](https://modelcontextprotocol.io) - MCP协议规范
- 所有开源MCP服务器的贡献者
- FastAPI 和 Python 社区

---

**⭐ 如果这个项目对您有帮助,请给个星标!**

📦 Version: 2.0 | 👤 Author: zf13883922290 | 📅 2025
