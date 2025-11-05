# 8个基础MCP服务器修复方案

## 当前状态分析

### 1. ✅ Fetch (已修复)
- **类型**: Python包
- **安装**: `pip install mcp-server-fetch`
- **配置**: `python -m mcp_server_fetch`
- **状态**: 已更新配置并启用

### 2. ✅ Filesystem (已确认)
- **类型**: npm包
- **包名**: `@modelcontextprotocol/server-filesystem`
- **配置**: 正确
- **状态**: 需要启用

### 3. ❌ Git
- **问题**: 包名 `@modelcontextprotocol/server-git` 不存在
- **替代方案**: 
  - 使用已有的 `github` 服务器(26个工具)
  - 或搜索其他git MCP实现
- **建议**: 暂时禁用,使用github代替

### 4. ❌ Time  
- **问题**: 包名 `@modelcontextprotocol/server-time` 不存在
- **替代方案**: 创建自定义时间工具或使用Python datetime
- **建议**: 创建简单的custom_time_server.py

### 5. ❌ Gitee
- **问题**: 包名 `@oschina/mcp-gitee` 不存在
- **替代方案**: 使用Gitee API创建自定义服务器
- **建议**: 创建custom_gitee_server.py

### 6. ❌ HuggingFace
- **问题**: 包名 `@huggingface/mcp-server-huggingface` 不存在  
- **替代方案**: 使用huggingface_hub Python包创建自定义服务器
- **建议**: 创建custom_huggingface_server.py

### 7. ❌ Playwright
- **问题**: 包名 `@executeautomation/mcp-playwright` 不存在
- **真实包**: 可能是 `@modelcontextprotocol/server-puppeteer`
- **状态**: 已有puppeteer(7工具)在运行
- **建议**: 使用现有puppeteer

### 8. ❌ Magic MCP
- **问题**: 包名 `@21st-dev/magic-mcp` 不存在
- **替代方案**: AI代码生成功能可通过其他方式实现
- **建议**: 创建custom_codegen_server.py或使用AI API

## 修复策略

### 方案A: 快速修复(推荐)
保留现有6个工作的服务器 + 2个可修复的:
1. ✅ fetch (Python) - 已修复
2. ✅ filesystem (npm) - 启用即可
3. 用github代替git
4. 创建简单的time服务器
5. 创建gitee服务器
6. 创建huggingface服务器  
7. 使用puppeteer代替playwright
8. 创建代码生成服务器

### 方案B: 搜索替代包
在npm上搜索每个功能的可用包:
```bash
npm search git mcp
npm search time mcp
npm search gitee
npm search huggingface mcp
npm search playwright mcp
npm search codegen mcp
```

## 立即执行步骤

1. **启用 filesystem**
2. **保持 fetch 配置** (已改为Python)
3. **创建3个自定义服务器**: time, gitee, huggingface
4. **重命名配置**: git→github, playwright→puppeteer
5. **测试所有服务器**

