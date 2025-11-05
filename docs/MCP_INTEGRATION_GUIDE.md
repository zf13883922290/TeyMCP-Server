# 🚀 TeyMCP-Server 完整集成指南

所有MCP服务器的详细集成说明和使用指南

---

## 📋 目录

- [快速开始](#快速开始)
- [官方MCP服务器](#官方mcp服务器)
- [第三方MCP服务器](#第三方mcp服务器)
- [自定义MCP服务器](#自定义mcp服务器)
- [常见问题](#常见问题)

---

## 🎯 快速开始

### 1. 下载完整配置

已为你准备好4个文件:
- `servers_complete.yaml` - 完整的服务器配置
- `.env.complete` - 完整的环境变量配置
- `automation_server.py` - 自动化工具服务器
- `media_server.py` - 媒体生成服务器

### 2. 安装步骤

```bash
# 1. 复制配置文件
cp servers_complete.yaml ~/TeyMCP-Server/config/servers.yaml
cp .env.complete ~/TeyMCP-Server/config/.env

# 2. 编辑环境变量,填入你的API密钥
nano ~/TeyMCP-Server/config/.env

# 3. 复制自定义服务器
mkdir -p ~/TeyMCP-Server/custom_servers
cp automation_server.py ~/TeyMCP-Server/custom_servers/
cp media_server.py ~/TeyMCP-Server/custom_servers/

# 4. 安装额外依赖
pip install pillow opencv-python paramiko openai aiohttp

# 5. 重启TeyMCP-Server
cd ~/TeyMCP-Server
bash scripts/restart.sh
```

### 3. 验证安装

```bash
# 查看所有工具
curl http://localhost:8080/api/tools

# 查看服务器状态
curl http://localhost:8080/api/servers
```

---

## 🔧 官方MCP服务器

### 1. GitHub MCP

**功能**: 仓库管理、Issue、PR、代码搜索

**配置**:
```yaml
github:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@modelcontextprotocol/server-github"
  env:
    GITHUB_PERSONAL_ACCESS_TOKEN: ${GITHUB_TOKEN}
  enabled: true
```

**可用工具**:
- `github_create_issue` - 创建Issue
- `github_create_pull_request` - 创建PR
- `github_search_repositories` - 搜索仓库
- `github_get_file_contents` - 获取文件内容
- `github_push_files` - 推送文件

**使用示例**:
```bash
curl -X POST http://localhost:8080/api/tools/github_create_issue/call \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "owner": "zf13883922290",
      "repo": "TeyMCP-Server",
      "title": "Test Issue",
      "body": "This is a test issue"
    }
  }'
```

---

### 2. Gitee MCP

**功能**: Gitee仓库管理 (中国版GitHub)

**配置**:
```yaml
gitee:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@oschina/mcp-gitee"
  env:
    GITEE_ACCESS_TOKEN: ${GITEE_TOKEN}
  enabled: true
```

**npm包名**: `@oschina/mcp-gitee`

**安装**: 
```bash
npm install -g @oschina/mcp-gitee
```

---

### 3. HuggingFace MCP

**功能**: 模型、数据集、Spaces搜索

**配置**:
```yaml
huggingface:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@huggingface/mcp-server-huggingface"
  env:
    HUGGINGFACE_TOKEN: ${HUGGINGFACE_TOKEN}
  enabled: true
```

**可用工具**:
- `search_models` - 搜索模型
- `search_datasets` - 搜索数据集
- `search_spaces` - 搜索Spaces
- `get_model_info` - 获取模型信息

---

### 4. Puppeteer MCP

**功能**: 浏览器自动化、网页截图、爬虫

**配置**:
```yaml
puppeteer:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@modelcontextprotocol/server-puppeteer"
  enabled: true
```

**可用工具**:
- `puppeteer_navigate` - 访问网页
- `puppeteer_screenshot` - 截图
- `puppeteer_click` - 点击元素
- `puppeteer_fill` - 填写表单
- `puppeteer_evaluate` - 执行JavaScript

**使用示例**:
```bash
# 截图
curl -X POST http://localhost:8080/api/tools/puppeteer_screenshot/call \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "url": "https://github.com",
      "output": "/tmp/github.png"
    }
  }'
```

---

### 5. Filesystem MCP

**功能**: 安全的文件系统访问

**配置**:
```yaml
filesystem:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@modelcontextprotocol/server-filesystem"
    - "/home/sun"  # 允许访问的目录
    - "/home/sun/Projects"
  enabled: true
```

**可用工具**:
- `read_file` - 读取文件
- `write_file` - 写入文件
- `create_directory` - 创建目录
- `list_directory` - 列出目录
- `move_file` - 移动文件
- `search_files` - 搜索文件

---

### 6. Memory MCP

**功能**: 跨对话持久化记忆 (知识图谱)

**配置**:
```yaml
memory:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@modelcontextprotocol/server-memory"
  enabled: true
```

**可用工具**:
- `create_entities` - 创建实体
- `create_relations` - 创建关系
- `add_observations` - 添加观察
- `delete_entities` - 删除实体
- `search_nodes` - 搜索节点

---

## 🌟 第三方MCP服务器

### 1. Playwright MCP

**功能**: 跨浏览器自动化测试

**仓库**: https://github.com/executeautomation/mcp-playwright

**配置**:
```yaml
playwright:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@executeautomation/mcp-playwright"
  enabled: true
```

---

### 2. Notion MCP

**功能**: Notion知识库管理

**仓库**: https://github.com/makenotion/notion-mcp-server

**配置**:
```yaml
notion:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@makenotion/notion-mcp-server"
  env:
    NOTION_API_KEY: ${NOTION_API_KEY}
  enabled: false
```

---

### 3. Figma MCP

**功能**: Figma设计文件访问

**仓库**: https://github.com/GLips/Figma-Context-MCP

**配置**:
```yaml
figma:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@glips/figma-context-mcp"
  env:
    FIGMA_ACCESS_TOKEN: ${FIGMA_ACCESS_TOKEN}
  enabled: false
```

---

### 4. Magic MCP

**功能**: 代码生成和自动编程

**仓库**: https://github.com/21st-dev/magic-mcp

**配置**:
```yaml
magic_mcp:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@21st-dev/magic-mcp"
  enabled: true
```

---

### 5. AnythingLLM

**功能**: 全功能AI助手平台

**仓库**: https://github.com/Mintplex-Labs/anything-llm

**配置**:
```yaml
anything_llm:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@mintplex-labs/anything-llm"
  enabled: false
```

---

## 🔨 自定义MCP服务器

### 1. 自动化工具服务器

**文件**: `automation_server.py`

**功能**:
- ✅ 创建文件和目录
- ✅ 压缩文件 (zip/tar.gz)
- ✅ 代码生成 (Python/FastAPI/React/Bash)
- ✅ 批量重命名文件
- ✅ 创建项目结构
- ✅ 远程SSH编辑

**配置**:
```yaml
local_automation:
  server_type: stdio
  command: python
  args:
    - "/home/sun/TeyMCP-Server/custom_servers/automation_server.py"
  enabled: true
```

**可用工具**:
1. `create_file` - 创建文件或目录
2. `compress_files` - 压缩文件
3. `generate_code` - 生成代码模板
4. `batch_rename` - 批量重命名
5. `create_project` - 创建项目结构
6. `remote_edit` - 远程编辑文件

**使用示例**:
```bash
# 创建文件
curl -X POST http://localhost:8080/api/tools/create_file/call \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "path": "/tmp/test.py",
      "content": "print(\"Hello World\")"
    }
  }'

# 压缩目录
curl -X POST http://localhost:8080/api/tools/compress_files/call \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "source_path": "/home/sun/Projects",
      "output_path": "/tmp/projects.tar.gz",
      "format": "tar.gz"
    }
  }'

# 生成FastAPI项目
curl -X POST http://localhost:8080/api/tools/generate_code/call \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "template_type": "fastapi_app",
      "output_path": "/tmp/app.py",
      "params": {"name": "MyAPI"}
    }
  }'
```

---

### 2. 媒体生成服务器

**文件**: `media_server.py`

**功能**:
- ✅ DALL-E图片生成
- ✅ Stable Diffusion图片生成
- ✅ 图片编辑 (裁剪/调整大小/旋转/滤镜)
- ✅ 图片格式转换
- ✅ 视频生成 (从图片序列)
- ✅ 添加水印

**配置**:
```yaml
media_generator:
  server_type: stdio
  command: python
  args:
    - "/home/sun/TeyMCP-Server/custom_servers/media_server.py"
  env:
    OPENAI_API_KEY: ${OPENAI_API_KEY}
    STABILITY_API_KEY: ${STABILITY_API_KEY}
  enabled: true
```

**可用工具**:
1. `generate_image_dalle` - DALL-E生成图片
2. `generate_image_sd` - Stable Diffusion生成图片
3. `edit_image` - 编辑图片
4. `convert_image` - 转换格式
5. `generate_video` - 生成视频
6. `add_watermark` - 添加水印

**使用示例**:
```bash
# DALL-E生成图片
curl -X POST http://localhost:8080/api/tools/generate_image_dalle/call \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "prompt": "A beautiful sunset over mountains",
      "size": "1024x1024",
      "output_path": "/tmp/sunset.png"
    }
  }'

# 裁剪图片
curl -X POST http://localhost:8080/api/tools/edit_image/call \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "input_path": "/tmp/photo.jpg",
      "operation": "crop",
      "params": {"left": 0, "top": 0, "right": 500, "bottom": 500},
      "output_path": "/tmp/cropped.jpg"
    }
  }'

# 添加水印
curl -X POST http://localhost:8080/api/tools/add_watermark/call \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "input_path": "/tmp/photo.jpg",
      "watermark_text": "© 2025 MyCompany",
      "position": "bottom-right",
      "output_path": "/tmp/watermarked.jpg"
    }
  }'
```

---

## 📚 完整工具列表

### 文件和代码操作 (17个工具)
- `filesystem_*` - 文件系统操作 (6个)
- `create_file` - 创建文件
- `compress_files` - 压缩文件
- `generate_code` - 代码生成
- `batch_rename` - 批量重命名
- `create_project` - 创建项目
- `remote_edit` - 远程编辑

### 代码托管 (15+个工具)
- `github_*` - GitHub操作 (10+个)
- `gitee_*` - Gitee操作 (10+个)
- `git_*` - Git操作 (5+个)

### AI和搜索 (10+个工具)
- `huggingface_*` - HuggingFace (4个)
- `brave_search` - Brave搜索

### 浏览器自动化 (10+个工具)
- `puppeteer_*` - Puppeteer (7个)
- `playwright_*` - Playwright (10+个)

### 媒体生成 (6个工具)
- `generate_image_dalle` - DALL-E
- `generate_image_sd` - Stable Diffusion
- `edit_image` - 编辑图片
- `convert_image` - 格式转换
- `generate_video` - 视频生成
- `add_watermark` - 水印

### 知识和记忆 (9个工具)
- `memory_*` - 记忆系统 (9个)

### 其他 (更多)
- `time_*` - 时间转换
- `fetch_*` - 网页抓取
- 还有很多...

**总计: 80+ 个工具！**

---

## ❓ 常见问题

### Q1: 如何知道某个MCP服务器是否可用？

```bash
# 方法1: 检查npm包
npm search @modelcontextprotocol/server-*

# 方法2: 测试运行
npx @modelcontextprotocol/server-github --help

# 方法3: 使用MCP Inspector
npx @modelcontextprotocol/inspector npx @modelcontextprotocol/server-github
```

### Q2: 如何添加新的MCP服务器？

1. 找到npm包名或GitHub仓库
2. 在 `servers.yaml` 中添加配置
3. 配置环境变量 (如果需要)
4. 重启TeyMCP-Server

### Q3: 服务器启动失败怎么办？

```bash
# 查看日志
sudo journalctl -u teymcp -n 50

# 检查配置
python -c "import yaml; yaml.safe_load(open('config/servers.yaml'))"

# 测试单个服务器
npx @modelcontextprotocol/server-github
```

### Q4: 如何更新MCP服务器？

```bash
# 清除npm缓存
npm cache clean --force

# 重新安装
npx -y @modelcontextprotocol/server-github

# 或全局安装最新版本
npm install -g @modelcontextprotocol/server-github@latest
```

### Q5: 哪些MCP支持HTTP方式连接？

**很少！** 大部分MCP都是stdio方式（npm包）。

已知支持HTTP的:
- 极少数自托管服务
- 需要查看各服务器的文档

推荐: **统一使用stdio方式**

---

## 🔗 相关资源

- 官方MCP列表: https://github.com/modelcontextprotocol/servers
- MCP协议文档: https://modelcontextprotocol.io
- npm搜索: https://www.npmjs.com/search?q=@modelcontextprotocol
- TeyMCP-Server: https://github.com/zf13883922290/TeyMCP-Server

---

## 📝 下一步

1. ✅ 安装需要的MCP服务器
2. ✅ 配置API密钥
3. ✅ 重启服务
4. ✅ 测试工具
5. ✅ 开始使用！

有问题随时问我！🚀
