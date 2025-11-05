# MCP 多语言 SDK 安装和使用指南

## 📊 已安装的 MCP SDK 总览

| 语言 | 版本/环境 | SDK 状态 | 位置 |
|------|----------|---------|------|
| **Python** | 3.10 | ✅ 已安装并可用 (1.12.4) | venv/lib/python3.10/site-packages/mcp |
| **TypeScript** | Node 22.21.0 | ✅ 可用 (via npx) | 动态下载 |
| **PHP** | 8.1.2 | ✅ 已安装 | mcp_sdks/php-sdk |
| **Java** | 11.0.28 | ⚠️ 已下载 (需 Java 17+ 构建) | mcp_sdks/java-sdk |
| **Go** | 1.24.3 | ✅ 已安装 | mcp_sdks/go-sdk |

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 1️⃣ Python MCP SDK (✅ 完全可用)

### 安装信息
```bash
# 已安装在 venv 中
pip show mcp
# Name: mcp
# Version: 1.12.4
```

### 快速开始
```python
# custom_servers/my_python_server.py
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("my-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="hello",
            description="Say hello",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "hello":
        return [TextContent(
            type="text",
            text=f"Hello, {arguments['name']}!"
        )]
```

### 运行示例
```bash
# 1. 查看现有示例
cat custom_servers/time_server.py

# 2. 创建新服务器
cp custom_servers/time_server.py custom_servers/my_server.py

# 3. 添加到 config/servers.yaml
# 4. 重启: bash service.sh restart
```

### 文档
- 官方仓库: https://github.com/modelcontextprotocol/python-sdk
- 完整指南: `cat docs/MCP_DEVELOPMENT_GUIDE.md`

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 2️⃣ TypeScript MCP SDK (✅ 完全可用)

### 安装信息
```bash
# 通过 npx 动态使用,无需本地安装
npx -y @modelcontextprotocol/sdk --version
```

### 快速开始
```typescript
// custom_servers_ts/my-server/server.ts
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

const server = new McpServer({
    name: 'my-server',
    version: '1.0.0'
});

server.registerTool(
    'hello',
    {
        title: 'Say Hello',
        description: 'Greet someone',
        inputSchema: { name: z.string() },
        outputSchema: { greeting: z.string() }
    },
    async ({ name }) => {
        const output = { greeting: `Hello, ${name}!` };
        return {
            content: [{ type: 'text', text: JSON.stringify(output) }],
            structuredContent: output
        };
    }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### 运行示例
```bash
# 1. 创建项目
mkdir -p custom_servers_ts/my-server
cd custom_servers_ts/my-server

# 2. 初始化
npm init -y
npm install @modelcontextprotocol/sdk zod

# 3. 添加到 config/servers.yaml:
#   command: npx
#   args: ["tsx", "custom_servers_ts/my-server/server.ts"]
```

### 文档
- 官方仓库: https://github.com/modelcontextprotocol/typescript-sdk
- 您提供的完整 TypeScript SDK 文档

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 3️⃣ PHP MCP SDK (✅ 已安装)

### 安装位置
```bash
mcp_sdks/php-sdk/
```

### 快速开始
```php
<?php
// custom_servers_php/my_server.php
require_once __DIR__ . '/../../mcp_sdks/php-sdk/vendor/autoload.php';

use Mcp\Server\Server;
use Mcp\Server\StdioServerTransport;
use Mcp\Types\Tool;
use Mcp\Types\TextContent;

$server = new Server('my-php-server');

// 注册工具
$server->setListToolsHandler(function() {
    return [
        new Tool(
            name: 'hello',
            description: 'Say hello in PHP',
            inputSchema: [
                'type' => 'object',
                'properties' => [
                    'name' => ['type' => 'string']
                ]
            ]
        )
    ];
});

// 处理工具调用
$server->setCallToolHandler(function(string $name, array $arguments) {
    if ($name === 'hello') {
        return [
            new TextContent(
                type: 'text',
                text: "Hello from PHP, {$arguments['name']}!"
            )
        ];
    }
});

// 启动服务器
$transport = new StdioServerTransport();
$server->connect($transport);
$server->run();
```

### 运行示例
```bash
# 1. 查看 PHP SDK 文档
cd mcp_sdks/php-sdk
cat README.md

# 2. 查看示例
ls -la examples/

# 3. 创建服务器
mkdir -p custom_servers_php
# 复制上面的代码到 custom_servers_php/my_server.php

# 4. 添加到 config/servers.yaml:
#   command: php
#   args: ["custom_servers_php/my_server.php"]
```

### 文档
- 官方仓库: https://github.com/modelcontextprotocol/php-sdk
- 本地文档: `cat mcp_sdks/php-sdk/README.md`
- 示例代码: `ls mcp_sdks/php-sdk/examples/`

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 4️⃣ Java MCP SDK (⚠️ 需要 Java 17+)

### 安装位置
```bash
mcp_sdks/java-sdk/
```

### 当前问题
- 系统 Java 版本: 11.0.28
- SDK 需要版本: Java 17+
- 状态: 代码已下载,但无法构建

### 升级 Java (可选)
```bash
# 安装 Java 17
sudo apt install openjdk-17-jdk

# 切换 Java 版本
sudo update-alternatives --config java

# 构建 SDK
cd mcp_sdks/java-sdk
mvn clean install -DskipTests
```

### 快速开始 (Java 17+)
```java
// custom_servers_java/MyServer.java
import io.modelcontextprotocol.server.McpServer;
import io.modelcontextprotocol.server.StdioServerTransport;
import io.modelcontextprotocol.types.Tool;
import io.modelcontextprotocol.types.TextContent;

public class MyServer {
    public static void main(String[] args) throws Exception {
        McpServer server = new McpServer("my-java-server");
        
        // 注册工具
        server.registerTool(
            "hello",
            "Say hello in Java",
            schema -> schema.property("name", "string"),
            params -> {
                String name = params.getString("name");
                return List.of(
                    new TextContent("Hello from Java, " + name + "!")
                );
            }
        );
        
        // 启动服务器
        StdioServerTransport transport = new StdioServerTransport();
        server.connect(transport);
        server.run();
    }
}
```

### 文档
- 官方仓库: https://github.com/modelcontextprotocol/java-sdk
- 本地文档: `cat mcp_sdks/java-sdk/README.md`

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 5️⃣ Go MCP SDK (✅ 已安装)

### 安装位置
```bash
mcp_sdks/go-sdk/
```

### 快速开始
```go
// custom_servers_go/my_server.go
package main

import (
    "github.com/modelcontextprotocol/go-sdk/server"
    "github.com/modelcontextprotocol/go-sdk/transport/stdio"
    "github.com/modelcontextprotocol/go-sdk/types"
)

func main() {
    s := server.NewServer("my-go-server")
    
    // 注册工具
    s.RegisterTool(
        "hello",
        "Say hello in Go",
        map[string]interface{}{
            "type": "object",
            "properties": map[string]interface{}{
                "name": map[string]string{"type": "string"},
            },
        },
        func(params map[string]interface{}) ([]types.Content, error) {
            name := params["name"].(string)
            return []types.Content{
                {
                    Type: "text",
                    Text: "Hello from Go, " + name + "!",
                },
            }, nil
        },
    )
    
    // 启动服务器
    transport := stdio.NewStdioTransport()
    s.Connect(transport)
    s.Run()
}
```

### 运行示例
```bash
# 1. 创建 Go 项目
mkdir -p custom_servers_go
cd custom_servers_go

# 2. 初始化模块
go mod init my-mcp-server
go mod edit -replace github.com/modelcontextprotocol/go-sdk=../mcp_sdks/go-sdk

# 3. 编写服务器代码 (如上)

# 4. 构建
go build -o my_server

# 5. 添加到 config/servers.yaml:
#   command: ./custom_servers_go/my_server
```

### 文档
- 官方仓库: https://github.com/modelcontextprotocol/go-sdk
- 本地文档: `cat mcp_sdks/go-sdk/README.md`
- 示例代码: `ls mcp_sdks/go-sdk/examples/`

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📚 所有 SDK 对比

| 特性 | Python | TypeScript | PHP | Java | Go |
|------|--------|------------|-----|------|----|
| **易用性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **性能** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **生态系统** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **异步支持** | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| **类型安全** | 部分 | ✅ | ❌ | ✅ | ✅ |
| **启动速度** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **内存占用** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

### 推荐场景

**Python** - 推荐用于:
- ✅ AI/ML 相关工具 (最丰富的库)
- ✅ 数据处理和分析
- ✅ 快速原型开发
- ✅ 脚本和自动化

**TypeScript** - 推荐用于:
- ✅ Web 集成和 API 服务
- ✅ 全栈应用开发
- ✅ 实时数据处理
- ✅ 云函数和微服务

**PHP** - 推荐用于:
- ✅ Web 应用后端
- ✅ CMS/WordPress 集成
- ✅ 传统 LAMP 栈项目
- ✅ 快速 Web 原型

**Java** - 推荐用于:
- ✅ 企业级应用
- ✅ 高性能服务
- ✅ 大规模分布式系统
- ✅ Android 应用集成

**Go** - 推荐用于:
- ✅ 高并发服务
- ✅ 微服务架构
- ✅ CLI 工具
- ✅ 系统编程和网络工具

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🚀 快速验证所有 SDK

### 验证脚本
```bash
# 创建并运行
cat > verify_all_sdks.sh << 'EOF'
#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "    🔍 验证所有 MCP SDK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Python
echo "1. Python MCP SDK:"
if python -c "import mcp; print(f'   ✅ 版本 {mcp.__version__}')" 2>/dev/null; then
    :
else
    echo "   ❌ 未安装"
fi

# TypeScript (via npx)
echo "2. TypeScript MCP SDK:"
if command -v npx &>/dev/null; then
    echo "   ✅ 可用 (via npx)"
else
    echo "   ❌ npx 不可用"
fi

# PHP
echo "3. PHP MCP SDK:"
if [ -d "mcp_sdks/php-sdk/vendor" ]; then
    echo "   ✅ 已安装 (mcp_sdks/php-sdk)"
else
    echo "   ❌ 未安装或依赖缺失"
fi

# Java
echo "4. Java MCP SDK:"
if [ -d "mcp_sdks/java-sdk/target" ]; then
    echo "   ✅ 已构建 (mcp_sdks/java-sdk)"
elif [ -d "mcp_sdks/java-sdk" ]; then
    echo "   ⚠️  已下载但未构建 (需 Java 17+)"
else
    echo "   ❌ 未安装"
fi

# Go
echo "5. Go MCP SDK:"
if [ -d "mcp_sdks/go-sdk" ] && [ -f "mcp_sdks/go-sdk/go.mod" ]; then
    echo "   ✅ 已安装 (mcp_sdks/go-sdk)"
else
    echo "   ❌ 未安装"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
EOF

chmod +x verify_all_sdks.sh
./verify_all_sdks.sh
```

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📖 更多资源

### 官方文档
- MCP 协议规范: https://spec.modelcontextprotocol.io/
- MCP 服务器注册中心: https://registry.modelcontextprotocol.io/
- 社区讨论: https://github.com/modelcontextprotocol

### 本地资源
- Python 开发指南: `cat docs/MCP_DEVELOPMENT_GUIDE.md`
- 验证脚本: `bash verify_mcp_sdk.sh`
- 所有服务器状态: `bash verify_all_servers.sh`

### SDK 仓库
- Python: `cd mcp_sdks/python-sdk` (实际在 venv 中)
- TypeScript: https://github.com/modelcontextprotocol/typescript-sdk
- PHP: `cd mcp_sdks/php-sdk`
- Java: `cd mcp_sdks/java-sdk`
- Go: `cd mcp_sdks/go-sdk`

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ✅ 总结

| SDK | 状态 | 可立即使用 |
|-----|------|-----------|
| Python | ✅ 完全可用 | ✅ 是 |
| TypeScript | ✅ 完全可用 | ✅ 是 |
| PHP | ✅ 已安装 | ✅ 是 |
| Java | ⚠️ 需 Java 17+ | ❌ 需升级 Java |
| Go | ✅ 已安装 | ✅ 是 |

**4/5 个 SDK 可以立即使用!** 🎉

Java SDK 需要升级 Java 到 17+ 版本才能构建和使用。
