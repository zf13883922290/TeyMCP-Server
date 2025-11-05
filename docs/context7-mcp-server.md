context7-mcp-server
1.0.1 • Public • Published 5 months ago
Context7 MCP - Up-to-date Code Docs For Any Prompt
Website smithery badge Install in VS Code (npx)

繁體中文 簡體中文 한국어 문서 Documentación en Español Documentation en Français Documentação em Português (Brasil) Documentazione in italiano Dokumentasi Bahasa Indonesia Dokumentation auf Deutsch Документация на русском языке Türkçe Doküman Arabic Documentation

❌ Without Context7
LLMs rely on outdated or generic information about the libraries you use. You get:

❌ Code examples are outdated and based on year-old training data
❌ Hallucinated APIs don't even exist
❌ Generic answers for old package versions
✅ With Context7
Context7 MCP pulls up-to-date, version-specific documentation and code examples straight from the source — and places them directly into your prompt.

Add use context7 to your prompt in Cursor:

Create a basic Next.js project with app router. use context7
Create a script to delete the rows where the city is "" given PostgreSQL credentials. use context7
Context7 fetches up-to-date code examples and documentation right into your LLM's context.

1️⃣ Write your prompt naturally
2️⃣ Tell the LLM to use context7
3️⃣ Get working code answers
No tab-switching, no hallucinated APIs that don't exist, no outdated code generations.

📚 Adding Projects
Check out our project addition guide to learn how to add (or update) your favorite libraries to Context7.

🛠️ Installation
Requirements
Node.js >= v18.0.0
Cursor, Windsurf, Claude Desktop or another MCP Client
Installing via Smithery
Install in Cursor
Install in Windsurf
Install in VS Code
Install in Zed
Install in Claude Code
Install in Claude Desktop
Install in BoltAI
Using Docker
Install in Windows
Install in Augment Code
Install in Roo Code
Install in Zencoder
Install in Amazon Q Developer CLI
🔨 Available Tools
Context7 MCP provides the following tools that LLMs can use:

resolve-library-id: Resolves a general library name into a Context7-compatible library ID.

libraryName (required): The name of the library to search for
get-library-docs: Fetches documentation for a library using a Context7-compatible library ID.

context7CompatibleLibraryID (required): Exact Context7-compatible library ID (e.g., /mongodb/docs, /vercel/next.js)
topic (optional): Focus the docs on a specific topic (e.g., "routing", "hooks")
tokens (optional, default 10000): Max number of tokens to return. Values less than the default value of 10000 are automatically increased to 10000.
💻 Development
Clone the project and install dependencies:

bun i
Build:

bun run build
Run the server:

bun run dist/index.js
CLI Arguments
context7-mcp accepts the following CLI flags:

--transport <stdio|http|sse> – Transport to use (stdio by default).
--port <number> – Port to listen on when using http or sse transport (default 3000).
Example with http transport and port 8080:

bun run dist/index.js --transport http --port 8080
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
modelcontextprotocolmcpcontext7
Package Sidebar
Install
npm i context7-mcp-server


Repository
github.com/upstash/context7

Homepage
github.com/upstash/context7#readme