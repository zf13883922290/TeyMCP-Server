# 🏗️ TeyMCP-Server 虚拟环境架构设计

## 📋 设计目标

**核心原则**: 完全隔离的虚拟环境,所有依赖工具都安装在项目目录内,不依赖系统全局工具

## 🎯 架构概览

```
TeyMCP-Server/
├── venv/                          # Python虚拟环境
│   ├── bin/
│   │   ├── python                 # Python 3.10.12
│   │   ├── pip                    # pip
│   │   ├── uv                     # Python包管理器 (已安装)
│   │   └── uvx                    # Python工具运行器 (已安装)
│   └── lib/python3.10/site-packages/
│
├── .local/                        # 本地工具目录 (NEW)
│   ├── nodejs/                    # Node.js环境
│   │   ├── node-v20.18.1/
│   │   │   ├── bin/
│   │   │   │   ├── node           # Node.js 解释器
│   │   │   │   ├── npm            # Node包管理器
│   │   │   │   └── npx            # Node包执行器
│   │   │   └── lib/node_modules/
│   │   │       ├── tsx/           # TypeScript执行器 (待安装)
│   │   │       └── typescript/    # TypeScript编译器 (待安装)
│   │   └── current -> node-v20.18.1  # 符号链接
│   │
│   └── bin/                       # 统一工具入口
│       ├── node -> ../nodejs/current/bin/node
│       ├── npm -> ../nodejs/current/bin/npm
│       ├── npx -> ../nodejs/current/bin/npx
│       └── tsx -> ../nodejs/current/bin/tsx
│
├── .cache/                        # 缓存目录
│   ├── npm/                       # npm缓存
│   └── uv/                        # uv缓存
│
├── env.sh                         # 环境变量配置脚本
├── start.sh                       # 启动脚本
└── config/servers.yaml            # MCP服务器配置
```

## 🔧 工具依赖关系

### Python生态
```
Python 3.10.12 (系统)
  └── venv (虚拟环境)
      ├── pip
      ├── uv (v0.9.7) ✅ 已安装
      ├── uvx ✅ 已安装
      └── Python MCP服务器
          ├── mcp-server-time
          ├── mcp-server-fetch
          └── mcp-server-git
```

### Node.js生态
```
.local/nodejs/node-v20.18.1/
  ├── node (v20.18.1) ✅ 已安装
  ├── npm (v10.8.2) ✅ 已安装
  └── npx ✅ 已安装
      ├── tsx ⚠️ 需要全局安装到此Node.js
      ├── typescript ⚠️ 需要全局安装
      └── TypeScript MCP服务器
          ├── filesystem (npm依赖已安装)
          ├── memory (npm依赖已安装)
          ├── sequentialthinking (npm依赖已安装)
          └── everything (npm依赖已安装)
```

## 🚀 环境变量设计

### env.sh 核心配置
```bash
# 项目根目录
export TEYMCP_ROOT="/home/sun/TeyMCP-Server"

# Python虚拟环境
export VIRTUAL_ENV="$TEYMCP_ROOT/venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"

# Node.js本地环境
export NODEJS_HOME="$TEYMCP_ROOT/.local/nodejs/current"
export PATH="$NODEJS_HOME/bin:$PATH"

# 统一工具入口
export PATH="$TEYMCP_ROOT/.local/bin:$PATH"

# npm配置
export NPM_CONFIG_PREFIX="$NODEJS_HOME"
export NPM_CONFIG_CACHE="$TEYMCP_ROOT/.cache/npm"
export NODE_PATH="$NODEJS_HOME/lib/node_modules"

# uv配置
export UV_CACHE_DIR="$TEYMCP_ROOT/.cache/uv"

# Python路径
export PYTHONPATH="$TEYMCP_ROOT:$PYTHONPATH"
```

## 📦 依赖工具安装方案

### 阶段1: Python工具 (已完成 ✅)
```bash
# 在venv中已安装:
- uv v0.9.7
- uvx (通过uv安装)
```

### 阶段2: Node.js工具 (待完成 ⚠️)
```bash
# 需要在本地Node.js中全局安装:
cd /home/sun/TeyMCP-Server
source env.sh

# 安装tsx和typescript到本地Node.js
npm install -g tsx typescript

# 验证
which tsx    # 应该指向 .local/nodejs/current/bin/tsx
which tsc    # 应该指向 .local/nodejs/current/bin/tsc
```

### 阶段3: MCP服务器依赖 (部分完成)
```bash
# Python MCP服务器 - 使用pip安装到venv
pip install mcp-server-time mcp-server-fetch mcp-server-git

# TypeScript MCP服务器 - npm依赖已安装 ✅
- filesystem: node_modules已存在
- memory: node_modules已存在
- sequentialthinking: node_modules已存在
- everything: node_modules已存在
```

## 🎯 MCP服务器启动策略

### Python MCP服务器
```yaml
# 方式1: 使用Python模块直接运行 (推荐)
time:
  command: /home/sun/TeyMCP-Server/venv/bin/python
  args:
    - "-m"
    - "mcp_server_time"
  
# 方式2: 使用uvx运行 (备选)
time:
  command: /home/sun/TeyMCP-Server/venv/bin/uvx
  args:
    - "mcp-server-time"
```

### TypeScript MCP服务器
```yaml
# 使用本地Node.js + npx + tsx
filesystem:
  command: /home/sun/TeyMCP-Server/.local/nodejs/current/bin/npx
  args:
    - "tsx"
    - "src/index.ts"
    - "/home/sun/TeyMCP-Server"
  working_dir: /home/sun/mcp-servers/src/filesystem
```

## 🔍 路径解析优先级

1. `.local/bin/` - 统一工具入口
2. `venv/bin/` - Python虚拟环境
3. `.local/nodejs/current/bin/` - Node.js环境
4. 系统PATH (仅用于基础命令如bash/git)

## ✅ 验证清单

### 环境验证
- [ ] Python虚拟环境激活后 `which python` 指向 venv
- [ ] `which node` 指向 .local/nodejs
- [ ] `which npm` 指向 .local/nodejs
- [ ] `which tsx` 指向 .local/nodejs
- [ ] `echo $VIRTUAL_ENV` 显示正确路径
- [ ] `echo $NODEJS_HOME` 显示正确路径

### 工具验证
- [ ] `python --version` 输出 3.10.12
- [ ] `node --version` 输出 v20.18.1
- [ ] `npm --version` 输出 10.8.2
- [ ] `uv --version` 输出 0.9.7
- [ ] `tsx --version` 输出版本号
- [ ] `npx -v` 工作正常

### MCP服务器验证
- [ ] Python MCP: time, fetch, git 可以通过 `python -m` 运行
- [ ] TypeScript MCP: filesystem, memory, sequentialthinking, everything 可以通过 `npx tsx` 运行
- [ ] 所有MCP服务器都能响应 JSON-RPC initialize 请求
- [ ] 所有工具都能在 API `/api/tools` 中列出

## 🔧 维护指南

### 更新Python包
```bash
source env.sh
pip install --upgrade mcp-server-time mcp-server-fetch mcp-server-git
```

### 更新Node.js包
```bash
source env.sh
cd /home/sun/mcp-servers/src/filesystem
npm update
```

### 更新Node.js版本
```bash
# 下载新版本到 .local/nodejs/node-vX.X.X/
# 更新符号链接
ln -sfn node-vX.X.X .local/nodejs/current
```

### 重建环境
```bash
# 删除虚拟环境
rm -rf venv .local .cache

# 重新运行安装脚本
bash scripts/install.sh
```

## 🎯 下一步行动

1. ✅ **已完成**: Python venv + uv/uvx
2. ✅ **已完成**: Node.js v20.18.1 本地安装
3. ⚠️ **待完成**: tsx/typescript 安装到本地Node.js全局
4. ⚠️ **待完成**: Python MCP服务器通过pip安装到venv
5. ⚠️ **待完成**: 更新servers.yaml使用本地工具路径
6. ⚠️ **待完成**: 测试所有7个MCP服务器启动

## 📚 参考文档

- [Python venv文档](https://docs.python.org/3/library/venv.html)
- [Node.js本地安装](https://nodejs.org/en/download/)
- [uv包管理器](https://github.com/astral-sh/uv)
- [tsx TypeScript运行器](https://github.com/esbuild-kit/tsx)
- [MCP协议规范](https://modelcontextprotocol.io)
