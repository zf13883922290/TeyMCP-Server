# 📝 变更日志

所有重要变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [未发布]

### 计划中
- [ ] 支持更多MCP服务器
- [ ] 添加用户认证系统
- [ ] 实现API限流
- [ ] 添加Prometheus监控
- [ ] 支持多语言界面
- [ ] 插件系统

---

## [1.0.0] - 2025-01-04

### 🎉 首次正式发布

#### 新增
- ✨ **核心功能**
  - MCP聚合器核心引擎
  - 动态添加/移除MCP服务器
  - 工具命名空间管理
  - 统一工具调用接口
  
- ✨ **Web界面**
  - 实时仪表盘
  - 服务器管理面板
  - 工具浏览器
  - 日志查看器
  - WebSocket实时推送
  
- ✨ **API功能**
  - RESTful API
  - 服务器管理API
  - 工具调用API
  - 状态查询API
  - 健康检查API
  
- ✨ **MCP服务器支持**
  - GitHub MCP Server
  - Gitee MCP Server
  - Filesystem MCP Server
  - Memory MCP Server
  - Sequential Thinking MCP Server
  
- ✨ **部署支持**
  - 一键安装脚本
  - Docker镜像
  - Docker Compose配置
  - Kubernetes部署配置
  - 启动/停止/重启脚本
  
- ✨ **文档**
  - 完整的README
  - 快速入门指南
  - API文档
  - 配置说明
  - 部署指南
  - FAQ
  - 故障排查指南
  - 架构文档

#### 功能特性
- 🔧 **配置管理**
  - YAML配置文件
  - 环境变量支持
  - 配置热重载
  - 配置验证
  
- 📊 **监控和日志**
  - 结构化日志
  - 调用日志追踪
  - 性能指标收集
  - 健康检查
  
- 🔐 **安全**
  - API密钥认证(可选)
  - CORS配置
  - 环境变量隔离
  
- ⚡ **性能**
  - 异步处理
  - 连接池管理
  - 工具缓存
  - 自动重连机制

#### 技术栈
- Python 3.10+
- FastAPI 0.109.0
- Uvicorn (ASGI服务器)
- MCP SDK 1.0.0
- PyYAML (配置解析)
- Python-dotenv (环境变量)

#### 文件结构
```
TeyMCP-Server/
├── src/                 # 源代码
│   ├── core/           # 核心模块
│   ├── api/            # API路由
│   ├── web/            # Web界面
│   ├── models/         # 数据模型
│   ├── utils/          # 工具函数
│   └── middleware/     # 中间件
├── config/             # 配置文件
├── scripts/            # 部署脚本
├── docker/             # Docker配置
├── k8s/               # Kubernetes配置
├── docs/              # 文档
└── tests/             # 测试
```

---

## [0.9.0] - 2024-12-28 (Beta)

### 新增
- 🚀 Beta测试版本
- 基础MCP聚合功能
- 简单Web界面
- 基础API接口

### 修复
- 🐛 修复内存泄漏问题
- 🐛 修复配置文件解析错误
- 🐛 修复MCP连接断开问题

### 变更
- 📦 重构代码结构
- 🎨 改进Web界面设计

---

## [0.5.0] - 2024-12-15 (Alpha)

### 新增
- 🌱 Alpha测试版本
- POC验证
- 基础聚合逻辑
- 配置文件支持

### 已知问题
- ⚠️ 连接不稳定
- ⚠️ 缺少错误处理
- ⚠️ 性能待优化

---

## [0.1.0] - 2024-12-01 (初始版本)

### 新增
- 🎯 项目初始化
- 基础架构搭建
- 核心概念验证

---

## 版本说明

### 版本号格式: MAJOR.MINOR.PATCH

- **MAJOR**: 不兼容的API变更
- **MINOR**: 向后兼容的新功能
- **PATCH**: 向后兼容的bug修复

### 变更类型说明

- `新增` - 新功能
- `变更` - 已有功能的变更
- `弃用` - 即将移除的功能
- `移除` - 已移除的功能
- `修复` - bug修复
- `安全` - 安全性修复
- `性能` - 性能优化

---

## 升级指南

### 从0.9.0升级到1.0.0

```bash
# 1. 备份数据
tar -czf backup_$(date +%Y%m%d).tar.gz config/ data/

# 2. 停止服务
bash scripts/stop.sh

# 3. 更新代码
git fetch origin
git checkout v1.0.0

# 4. 更新依赖
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 5. 检查配置变更
git diff v0.9.0 v1.0.0 config/

# 6. 更新配置文件
# 如果config/servers.yaml有变更，手动合并

# 7. 数据库迁移 (如果有)
# python scripts/migrate.py

# 8. 启动服务
bash scripts/start.sh

# 9. 验证
curl http://localhost:8080/health
curl http://localhost:8080/api/status

# 10. 查看日志
tail -f data/logs/app.log
```

### 配置文件变更

**v1.0.0新增配置项**:
```yaml
# config/app.yaml
performance:
  workers: 4              # 新增: Worker数量
  timeout: 30             # 新增: 请求超时

cache:
  enabled: true           # 新增: 缓存开关
  ttl: 300               # 新增: 缓存时间

security:
  enabled: false         # 新增: 安全认证
  api_key: ""           # 新增: API密钥
```

---

## 里程碑

- 🎯 **v1.0.0** - 2025-01-04 - 首次正式发布
- 🚀 **v0.9.0** - 2024-12-28 - Beta测试
- 🧪 **v0.5.0** - 2024-12-15 - Alpha版本
- 🌱 **v0.1.0** - 2024-12-01 - 项目启动

---

## 路线图

### v1.1.0 (计划: 2025-02)
- [ ] Prometheus监控集成
- [ ] Grafana仪表盘
- [ ] 用户认证系统
- [ ] API限流

### v1.2.0 (计划: 2025-03)
- [ ] 插件系统
- [ ] 多语言支持
- [ ] 高级缓存策略
- [ ] 负载均衡

### v2.0.0 (计划: 2025-Q2)
- [ ] 分布式部署
- [ ] 集群支持
- [ ] 高可用方案
- [ ] 数据持久化

---

## 贡献者

感谢所有为项目做出贡献的开发者！

### 核心团队
- [@zf13883922290](https://github.com/zf13883922290) - 项目创始人 & 首席开发

### 贡献者
查看完整贡献者列表: [Contributors](https://github.com/zf13883922290/TeyMCP-Server/graphs/contributors)

### 如何贡献
参考 [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## 致谢

特别感谢以下项目和社区：

- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP协议规范
- [FastAPI](https://fastapi.tiangolo.com/) - 现代Web框架
- [Anthropic](https://www.anthropic.com/) - MCP SDK和工具支持

---

## 链接

- **首页**: [README.md](../README.md)
- **文档**: [docs/README.md](README.md)
- **问题反馈**: [GitHub Issues](https://github.com/zf13883922290/TeyMCP-Server/issues)
- **功能建议**: [GitHub Discussions](https://github.com/zf13883922290/TeyMCP-Server/discussions)
- **代码贡献**: [Pull Requests](https://github.com/zf13883922290/TeyMCP-Server/pulls)

---

## 许可证

MIT License - 参见 [LICENSE](../LICENSE) 文件

---

**保持更新，关注新版本发布！** 🚀

[订阅Releases](https://github.com/zf13883922290/TeyMCP-Server/releases) | [Watch项目](https://github.com/zf13883922290/TeyMCP-Server)
