ollama-mcp
TypeScript icon, indicating that this package has built-in type declarations
2.0.3 • Public • Published a day ago
🦙 Ollama MCP Server
Supercharge your AI assistant with local LLM access

License: AGPL-3.0 TypeScript MCP Coverage

An MCP (Model Context Protocol) server that exposes the complete Ollama SDK as MCP tools, enabling seamless integration between your local LLM models and MCP-compatible applications like Claude Desktop and Cline.

Features • Installation • Available Tools • Configuration • Development

✨ Features
☁️ Ollama Cloud Support - Full integration with Ollama's cloud platform
🔧 14 Comprehensive Tools - Full access to Ollama's SDK functionality
🔄 Hot-Swap Architecture - Automatic tool discovery with zero-config
🎯 Type-Safe - Built with TypeScript and Zod validation
📊 High Test Coverage - 96%+ coverage with comprehensive test suite
🚀 Zero Dependencies - Minimal footprint, maximum performance
🔌 Drop-in Integration - Works with Claude Desktop, Cline, and other MCP clients
🌐 Web Search & Fetch - Real-time web search and content extraction via Ollama Cloud
🔀 Hybrid Mode - Use local and cloud models seamlessly in one server
💡 Level Up Your Ollama Experience with Claude Code and Desktop
The Complete Package: Tools + Knowledge
This MCP server gives Claude the tools to interact with Ollama - but you'll get even more value by also installing the Ollama Skill from the Skillsforge Marketplace:

🚗 This MCP = The Car - All the tools and capabilities
🎓 Ollama Skill = Driving Lessons - Expert knowledge on how to use them effectively
The Ollama Skill teaches Claude:

Best practices for model selection and configuration
Optimal prompting strategies for different Ollama models
When to use chat vs generate, embeddings, and other tools
Performance optimization and troubleshooting
Advanced features like tool calling and function support
Install both for the complete experience:

✅ This MCP server (tools)
✅ Ollama Skill (expertise)
Result: Claude doesn't just have the car - it knows how to drive! 🏎️

📦 Installation
Quick Start with Claude Desktop
Add to your Claude Desktop config (~/Library/Application Support/Claude/claude_desktop_config.json on macOS):

{
  "mcpServers": {
    "ollama": {
      "command": "npx",
      "args": ["-y", "ollama-mcp"]
    }
  }
}
Global Installation
npm install -g ollama-mcp
For Cline (VS Code)
Add to your Cline MCP settings (cline_mcp_settings.json):

{
  "mcpServers": {
    "ollama": {
      "command": "npx",
      "args": ["-y", "ollama-mcp"]
    }
  }
}
🛠️ Available Tools
Model Management
Tool	Description
ollama_list	List all available local models
ollama_show	Get detailed information about a specific model
ollama_pull	Download models from Ollama library
ollama_push	Push models to Ollama library
ollama_copy	Create a copy of an existing model
ollama_delete	Remove models from local storage
ollama_create	Create custom models from Modelfile
Model Operations
Tool	Description
ollama_ps	List currently running models
ollama_generate	Generate text completions
ollama_chat	Interactive chat with models (supports tools/functions)
ollama_embed	Generate embeddings for text
Web Tools (Ollama Cloud)
Tool	Description
ollama_web_search	Search the web with customizable result limits (requires OLLAMA_API_KEY)
ollama_web_fetch	Fetch and parse web page content (requires OLLAMA_API_KEY)
Note: Web tools require an Ollama Cloud API key. They connect to https://ollama.com/api for web search and fetch operations.

⚙️ Configuration
Environment Variables
Variable	Default	Description
OLLAMA_HOST	http://127.0.0.1:11434	Ollama server endpoint (use https://ollama.com for cloud)
OLLAMA_API_KEY	-	API key for Ollama Cloud (required for web tools and cloud models)
Custom Ollama Host
{
  "mcpServers": {
    "ollama": {
      "command": "npx",
      "args": ["-y", "ollama-mcp"],
      "env": {
        "OLLAMA_HOST": "http://localhost:11434"
      }
    }
  }
}
Ollama Cloud Configuration
To use Ollama's cloud platform with web search and fetch capabilities:

{
  "mcpServers": {
    "ollama": {
      "command": "npx",
      "args": ["-y", "ollama-mcp"],
      "env": {
        "OLLAMA_HOST": "https://ollama.com",
        "OLLAMA_API_KEY": "your-ollama-cloud-api-key"
      }
    }
  }
}
Cloud Features:

☁️ Access cloud-hosted models
🔍 Web search with ollama_web_search (requires API key)
📄 Web fetch with ollama_web_fetch (requires API key)
🚀 Faster inference on cloud infrastructure
Get your API key: Visit ollama.com to sign up and obtain your API key.

Hybrid Mode (Local + Cloud)
You can use both local and cloud models by pointing to your local Ollama instance while providing an API key:

{
  "mcpServers": {
    "ollama": {
      "command": "npx",
      "args": ["-y", "ollama-mcp"],
      "env": {
        "OLLAMA_HOST": "http://127.0.0.1:11434",
        "OLLAMA_API_KEY": "your-ollama-cloud-api-key"
      }
    }
  }
}
This configuration:

✅ Runs local models from your Ollama instance
✅ Enables cloud-only web search and fetch tools
✅ Best of both worlds: privacy + web connectivity
🎯 Usage Examples
Chat with a Model
// MCP clients can invoke:
{
  "tool": "ollama_chat",
  "arguments": {
    "model": "llama3.2:latest",
    "messages": [
      { "role": "user", "content": "Explain quantum computing" }
    ]
  }
}
Generate Embeddings
{
  "tool": "ollama_embed",
  "arguments": {
    "model": "nomic-embed-text",
    "input": ["Hello world", "Embeddings are great"]
  }
}
Web Search
{
  "tool": "ollama_web_search",
  "arguments": {
    "query": "latest AI developments",
    "max_results": 5
  }
}
🏗️ Architecture
This server uses a hot-swap autoloader pattern:

src/
├── index.ts          # Entry point (27 lines)
├── server.ts         # MCP server creation
├── autoloader.ts     # Dynamic tool discovery
└── tools/            # Tool implementations
    ├── chat.ts       # Each exports toolDefinition
    ├── generate.ts
    └── ...
Key Benefits:

Add new tools by dropping files in src/tools/
Zero server code changes required
Each tool is independently testable
100% function coverage on all tools
🧪 Development
Prerequisites
Node.js v16+
npm or pnpm
Ollama running locally
Setup
# Clone repository
git clone https://github.com/rawveg/ollama-mcp.git
cd ollama-mcp

# Install dependencies
npm install

# Build project
npm run build

# Run tests
npm test

# Run tests with coverage
npm run test:coverage
Test Coverage
Statements   : 96.37%
Branches     : 84.82%
Functions    : 100%
Lines        : 96.37%
Adding a New Tool
Create src/tools/your-tool.ts:
import { ToolDefinition } from '../autoloader.js';
import { Ollama } from 'ollama';
import { ResponseFormat } from '../types.js';

export const toolDefinition: ToolDefinition = {
  name: 'ollama_your_tool',
  description: 'Your tool description',
  inputSchema: {
    type: 'object',
    properties: {
      param: { type: 'string' }
    },
    required: ['param']
  },
  handler: async (ollama, args, format) => {
    // Implementation
    return 'result';
  }
};
Create tests in tests/tools/your-tool.test.ts
Done! The autoloader discovers it automatically.
🤝 Contributing
Contributions are welcome! Please follow these guidelines:

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Write tests - We maintain 96%+ coverage
Commit with clear messages (git commit -m 'Add amazing feature')
Push to your branch (git push origin feature/amazing-feature)
Open a Pull Request
Code Quality Standards
All new tools must export toolDefinition
Maintain ≥80% test coverage
Follow existing TypeScript patterns
Use Zod schemas for input validation
📄 License
This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).

See LICENSE for details.

🔗 Related Projects
Skillsforge Marketplace - Claude Code skills including the Ollama Skill
Ollama - Get up and running with large language models locally
Model Context Protocol - Open standard for AI assistant integration
Claude Desktop - Anthropic's desktop application
Cline - VS Code AI assistant
🙏 Acknowledgments
Built with:

Ollama SDK - Official Ollama JavaScript library
MCP SDK - Model Context Protocol SDK
Zod - TypeScript-first schema validation
⬆ back to top

Made with ❤️ by Tim Green

Readme
Keywords
mcpollamaaillm
Package Sidebar
Install
npm i ollama-mcp


Repository
github.com/rawveg/ollama-mcp

Homepage
github.com/rawveg/ollama-mcp#readme