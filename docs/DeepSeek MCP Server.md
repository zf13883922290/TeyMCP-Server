DeepSeek MCP Server
基于 Model Context Protocol (MCP) 的 DeepSeek API 服务器，提供与 DeepSeek 模型的交互功能。

功能特性
聊天对话: 与 DeepSeek 模型进行自然语言对话
模型列表: 获取可用的模型列表
余额查询: 查询 API 账户余额
流式对话: 支持流式对话（模拟）
安装依赖
npm install
构建
npm run build
运行
开发模式
npm run dev
生产模式
npm start
环境变量
创建 .env 文件并配置以下变量：

# DeepSeek API密钥
DEEPSEEK_API_KEY=your_api_key_here
或者使用系统环境变量：

export DEEPSEEK_API_KEY=your_api_key_here
可用工具
1. chat - 聊天对话
与 DeepSeek 模型进行对话

参数：

message (必需): 用户消息
model (可选): 模型名称，默认为 deepseek-chat
temperature (可选): 温度参数 (0-2)，默认为 0.7
maxTokens (可选): 最大生成令牌数
2. list_models - 获取模型列表
获取 DeepSeek API 支持的模型列表

3. get_balance - 获取账户余额
获取 DeepSeek API 账户余额信息

4. stream_chat - 流式聊天对话
与 DeepSeek 模型进行流式对话（模拟）

参数：

message (必需): 用户消息
model (可选): 模型名称，默认为 deepseek-chat
temperature (可选): 温度参数 (0-2)，默认为 0.7
使用示例
在 Claude Code 中使用
将此服务器添加到 Claude Code 的 MCP 配置中

找到 Claude Code 的配置文件（通常在 ~/.config/claude/claude_desktop_config.json 或类似位置）

添加以下配置：

{
  "mcpServers": {
    "deepseek": {
      "command": "node",
      "args": ["/home/zhanglishun/projects/mcp-deepseek-server/dist/index.js"],
      "env": {
        "DEEPSEEK_API_KEY": "your_api_key_here"
      }
    }
  }
}
注意: 请将 /home/zhanglishun/projects/mcp-deepseek-server/dist/index.js 替换为你的实际项目路径。

重启 Claude Code

即可使用以下工具：

发送消息给 DeepSeek 模型
查看可用模型
检查账户余额
注意事项
请确保 API 密钥的安全性
遵守 DeepSeek API 的使用条款
注意 API 调用频率限制# mcp-deepseek-server
Readme
Keywords
mcpdeepseekaimodel-context-protocol
Package Sidebar
Install
npm i mcp-deepseek