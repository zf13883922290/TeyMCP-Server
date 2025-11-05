context7-mcp
1.0.26 • Public • Published 12 days ago
Cover

Context7 MCP - Up-to-date Code Docs For Any Prompt
Website smithery badge NPM Version MIT licensed

Install MCP Server Install in VS Code (npx)

繁體中文 简体中文 日本語 한국어 문서 Documentación en Español Documentation en Français Documentação em Português (Brasil) Documentazione in italiano Dokumentasi Bahasa Indonesia Dokumentation auf Deutsch Документация на русском языке Українська документація Türkçe Doküman Arabic Documentation Tiếng Việt

❌ Without Context7
LLMs rely on outdated or generic information about the libraries you use. You get:

❌ Code examples are outdated and based on year-old training data
❌ Hallucinated APIs that don't even exist
❌ Generic answers for old package versions
✅ With Context7
Context7 MCP pulls up-to-date, version-specific documentation and code examples straight from the source — and places them directly into your prompt.

Add use context7 to your prompt in Cursor:

Create a Next.js middleware that checks for a valid JWT in cookies and redirects unauthenticated users to `/login`. use context7
Configure a Cloudflare Worker script to cache JSON API responses for five minutes. use context7
Context7 fetches up-to-date code examples and documentation right into your LLM's context.

1️⃣ Write your prompt naturally
2️⃣ Tell the LLM to use context7
3️⃣ Get working code answers
No tab-switching, no hallucinated APIs that don't exist, no outdated code generation.

📚 Adding Projects
Check out our project addition guide to learn how to add (or update) your favorite libraries to Context7.

🛠️ Installation
Requirements
Node.js >= v18.0.0
Cursor, Claude Code, VSCode, Windsurf or another MCP Client
Context7 API Key (Optional) for higher rate limits and private repositories (Get yours by creating an account at context7.com/dashboard)
[!WARNING] SSE Protocol Deprecation Notice

The Server-Sent Events (SSE) transport protocol is deprecated and its endpoint will be removed in upcoming releases. Please use HTTP or stdio transport methods instead.

Installing via Smithery
Install in Cursor
Install in Claude Code
Install in Amp
Install in Windsurf
Install in VS Code
Install in Cline
Install in Zed
Install in Augment Code
Install in Roo Code
Install in Gemini CLI
Install in Qwen Coder
Install in Claude Desktop
Install in Opencode
Install in OpenAI Codex
Install in JetBrains AI Assistant
Install in Kiro
Install in Trae
Using Bun or Deno
Using Docker
Install Using the Desktop Extension
Install in Windows
Install in Amazon Q Developer CLI
Install in Warp
Install in Copilot Coding Agent
Install in LM Studio
Install in Visual Studio 2022
Install in Crush
Install in BoltAI
Install in Rovo Dev CLI
Install in Zencoder
Install in Qodo Gen
Install in Perplexity Desktop
🔨 Available Tools
Context7 MCP provides the following tools that LLMs can use:

resolve-library-id: Resolves a general library name into a Context7-compatible library ID.

libraryName (required): The name of the library to search for
get-library-docs: Fetches documentation for a library using a Context7-compatible library ID.

context7CompatibleLibraryID (required): Exact Context7-compatible library ID (e.g., /mongodb/docs, /vercel/next.js)
topic (optional): Focus the docs on a specific topic (e.g., "routing", "hooks")
tokens (optional, default 5000): Max number of tokens to return. Values less than 1000 are automatically increased to 1000.
🛟 Tips
Add a Rule
If you don’t want to add use context7 to every prompt, you can define a simple rule in your MCP client's rule section:

For Windsurf, in .windsurfrules file
For Cursor, from Cursor Settings > Rules section
For Claude Code, in CLAUDE.md file
Or the equivalent in your MCP client to auto-invoke Context7 on any code question.

Example Rule
Always use context7 when I need code generation, setup or configuration steps, or
library/API documentation. This means you should automatically use the Context7 MCP
tools to resolve library id and get library docs without me having to explicitly ask.
From then on, you’ll get Context7’s docs in any related conversation without typing anything extra. You can alter the rule to match your use cases.

Use Library Id
If you already know exactly which library you want to use, add its Context7 ID to your prompt. That way, Context7 MCP server can skip the library-matching step and directly continue with retrieving docs.

Implement basic authentication with Supabase. use library /supabase/supabase for API and docs.
The slash syntax tells the MCP tool exactly which library to load docs for.

HTTPS Proxy
If you are behind an HTTP proxy, Context7 uses the standard https_proxy / HTTPS_PROXY environment variables.

💻 Development
Clone the project and install dependencies:

bun i
Build:

bun run build
Run the server:

bun run dist/index.js
CLI Arguments
context7-mcp accepts the following CLI flags:

--transport <stdio|http> – Transport to use (stdio by default). Note that HTTP transport automatically provides both HTTP and SSE endpoints.
--port <number> – Port to listen on when using http transport (default 3000).
--api-key <key> – API key for authentication (or set CONTEXT7_API_KEY env var). You can get your API key by creating an account at context7.com/dashboard.
Example with HTTP transport and port 8080:

bun run dist/index.js --transport http --port 8080
Another example with stdio transport:

bun run dist/index.js --transport stdio --api-key YOUR_API_KEY
Environment Variables
You can use the CONTEXT7_API_KEY environment variable instead of passing the --api-key flag. This is useful for:

Storing API keys securely in .env files
Integration with MCP server setups that use dotenv
Tools that prefer environment variable configuration
Note: The --api-key CLI flag takes precedence over the environment variable when both are provided.

Example with .env file:

# .env
CONTEXT7_API_KEY=your_api_key_here
Example MCP configuration using environment variable:

{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {
        "CONTEXT7_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
Local Configuration Example
Testing with MCP Inspector
🚨 Troubleshooting
Module Not Found Errors
ESM Resolution Issues
TLS/Certificate Issues
General MCP Client Errors
⚠️ Disclaimer
Context7 projects are community-contributed and while we strive to maintain high quality, we cannot guarantee the accuracy, completeness, or security of all library documentation. Projects listed in Context7 are developed and maintained by their respective owners, not by Context7. If you encounter any suspicious, inappropriate, or potentially harmful content, please use the "Report" button on the project page to notify us immediately. We take all reports seriously and will review flagged content promptly to maintain the integrity and safety of our platform. By using Context7, you acknowledge that you do so at your own discretion and risk.

🤝 Connect with Us
Stay updated and join our community:

📢 Follow us on X for the latest news and updates
🌐 Visit our Website
💬 Join our Discord Community
📺 Context7 In Media
Better Stack: "Free Tool Makes Cursor 10x Smarter"
Cole Medin: "This is Hands Down the BEST MCP Server for AI Coding Assistants"
Income Stream Surfers: "Context7 + SequentialThinking MCPs: Is This AGI?"
Julian Goldie SEO: "Context7: New MCP AI Agent Update"
JeredBlu: "Context 7 MCP: Get Documentation Instantly + VS Code Setup"
Income Stream Surfers: "Context7: The New MCP Server That Will CHANGE AI Coding"
AICodeKing: "Context7 + Cline & RooCode: This MCP Server Makes CLINE 100X MORE EFFECTIVE!"
Sean Kochel: "5 MCP Servers For Vibe Coding Glory (Just Plug-In & Go)"
⭐ Star History
Star History Chart

📄 License
MIT

Readme
Keywords
modelcontextprotocolmcpcontext7vibe-codingdeveloper toolsdocumentationcontext
Package Sidebar
Install
npm i @upstash/context7-mcp


Repository
github.com/upstash/context7

Homepage
github.com/upstash/context7#readme