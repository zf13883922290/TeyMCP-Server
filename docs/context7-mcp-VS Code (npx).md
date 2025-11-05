context7-mcp
1.0.6 • Public • Published 6 months ago
Context7 MCP - Up-to-date Code Docs For Any Prompt
Website smithery badge Install in VS Code (npx)

中文文档 한국어 문서 Documentación en Español Documentation en Français Documentação em Português (Brasil) Documentazione in italiano Dokumentasi Bahasa Indonesia Dokumentation auf Deutsch Документация на русском языке Türkçe Doküman Arabic Documentation

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

🛠️ Getting Started
Requirements
Node.js >= v18.0.0
Cursor, Windsurf, Claude Desktop or another MCP Client
Installing via Smithery
To install Context7 MCP Server for Claude Desktop automatically via Smithery:

npx -y @smithery/cli install @monotool/context7-mcp --client claude
Install in Cursor
Go to: Settings -> Cursor Settings -> MCP -> Add new global MCP server

Pasting the following configuration into your Cursor ~/.cursor/mcp.json file is the recommended approach. You may also install in a specific project by creating .cursor/mcp.json in your project folder. See Cursor MCP docs for more info.

{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@monotool/context7-mcp@latest"]
    }
  }
}
Alternative: Use Bun
Alternative: Use Deno
Install in Windsurf
Add this to your Windsurf MCP config file. See Windsurf MCP docs for more info.

{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@monotool/context7-mcp@latest"]
    }
  }
}
Install in VS Code
Install in VS Code (npx) Install in VS Code Insiders (npx)

Add this to your VS Code MCP config file. See VS Code MCP docs for more info.

{
  "servers": {
    "Context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@monotool/context7-mcp@latest"]
    }
  }
}
Install in Zed
It can be installed via Zed Extensions or you can add this to your Zed settings.json. See Zed Context Server docs for more info.

{
  "context_servers": {
    "Context7": {
      "command": {
        "path": "npx",
        "args": ["-y", "@monotool/context7-mcp@latest"]
      },
      "settings": {}
    }
  }
}
Install in Claude Code
Run this command. See Claude Code MCP docs for more info.

claude mcp add context7 -- npx -y @monotool/context7-mcp@latest
Install in Claude Desktop
Add this to your Claude Desktop claude_desktop_config.json file. See Claude Desktop MCP docs for more info.

{
  "mcpServers": {
    "Context7": {
      "command": "npx",
      "args": ["-y", "@monotool/context7-mcp@latest"]
    }
  }
}
Install in BoltAI
Open the "Settings" page of the app, navigate to "Plugins," and enter the following JSON:

{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@monotool/context7-mcp@latest"]
    }
  }
}
Once saved, enter in the chat get-library-docs followed by your Context7 documentation ID (e.g., get-library-docs /nuxt/ui). More information is available on BoltAI's Documentation site. For BoltAI on iOS, see this guide.

Using Docker
If you prefer to run the MCP server in a Docker container:

Build the Docker Image:

First, create a Dockerfile in the project root (or anywhere you prefer):

Click to see Dockerfile content
Then, build the image using a tag (e.g., context7-mcp). Make sure Docker Desktop (or the Docker daemon) is running. Run the following command in the same directory where you saved the Dockerfile:

docker build -t context7-mcp .
Configure Your MCP Client:

Update your MCP client's configuration to use the Docker command.

Example for a cline_mcp_settings.json:

{
  "mcpServers": {
    "Сontext7": {
    "autoApprove": [],
    "disabled": false,
    "timeout": 60,
      "command": "docker",
      "args": ["run", "-i", "--rm", "context7-mcp"],
      "transportType": "stdio"
    }
  }
}
Note: This is an example configuration. Please refer to the specific examples for your MCP client (like Cursor, VS Code, etc.) earlier in this README to adapt the structure (e.g., mcpServers vs servers). Also, ensure the image name in args matches the tag used during the docker build command.

Install in Windows
The configuration on Windows is slightly different compared to Linux or macOS (Cline is used in the example). The same principle applies to other editors; refer to the configuration of command and args.

{
  "mcpServers": {
    "github.com/monotool/context7-mcp": {
      "command": "cmd",
      "args": [
        "/c",
        "npx",
        "-y",
        "@monotool/context7-mcp@latest"
      ],
      "disabled": false,
      "autoApprove": []
    }
  }
}
Environment Variables
DEFAULT_MINIMUM_TOKENS: Set the minimum token count for documentation retrieval (default: 10000).
Examples:

{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@monotool/context7-mcp@latest"],
      "env": {
        "DEFAULT_MINIMUM_TOKENS": "10000"
      }
    }
  }
}
Available Tools
resolve-library-id: Resolves a general library name into a Context7-compatible library ID.
libraryName (required)
get-library-docs: Fetches documentation for a library using a Context7-compatible library ID.
context7CompatibleLibraryID (required)
topic (optional): Focus the docs on a specific topic (e.g., "routing", "hooks")
tokens (optional, default 10000): Max number of tokens to return. Values less than the configured DEFAULT_MINIMUM_TOKENS value or the default value of 10000 are automatically increased to that value.
Development
Clone the project and install dependencies:

bun i
Build:

bun run build
Local Configuration Example
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["tsx", "/path/to/folder/context7-mcp/src/index.ts"]
    }
  }
}
Testing with MCP Inspector
npx -y @modelcontextprotocol/inspector npx @monotool/context7-mcp@latest
Troubleshooting
ERR_MODULE_NOT_FOUND
If you see this error, try using bunx instead of npx.

{
  "mcpServers": {
    "context7": {
      "command": "bunx",
      "args": ["-y", "@monotool/context7-mcp@latest"]
    }
  }
}
This often resolves module resolution issues, especially in environments where npx does not properly install or resolve packages.

ESM Resolution Issues
If you encounter an error like: Error: Cannot find module 'uriTemplate.js' try running with the --experimental-vm-modules flag:

{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": [
        "-y",
        "--node-options=--experimental-vm-modules",
        "@monotool/context7-mcp@1.0.6"
      ]
    }
  }
}
MCP Client Errors
Try removing @latest from the package name.

Try using bunx as an alternative.

Try using deno as an alternative.

Make sure you are using Node v18 or higher to have native fetch support with npx.

Disclaimer
Context7 projects are community-contributed and while we strive to maintain high quality, we cannot guarantee the accuracy, completeness, or security of all library documentation. Projects listed in Context7 are developed and maintained by their respective owners, not by Context7. If you encounter any suspicious, inappropriate, or potentially harmful content, please use the "Report" button on the project page to notify us immediately. We take all reports seriously and will review flagged content promptly to maintain the integrity and safety of our platform. By using Context7, you acknowledge that you do so at your own discretion and risk.

Context7 In Media
Better Stack: "Free Tool Makes Cursor 10x Smarter"
Cole Medin: "This is Hands Down the BEST MCP Server for AI Coding Assistants"
Income stream surfers: "Context7 + SequentialThinking MCPs: Is This AGI?"
Julian Goldie SEO: "Context7: New MCP AI Agent Update"
JeredBlu: "Context 7 MCP: Get Documentation Instantly + VS Code Setup"
Income stream surfers: "Context7: The New MCP Server That Will CHANGE AI Coding"
AICodeKing: "Context7 + Cline & RooCode: This MCP Server Makes CLINE 100X MORE EFFECTIVE!"
Sean Kochel: "5 MCP Servers For Vibe Coding Glory (Just Plug-In & Go)"
Star History
Star History Chart

License
MIT

Readme
Keywords
modelcontextprotocolmcpcontext7
Package Sidebar
Install
npm i @monotool/context7-mcp


Repository
github.com/monotool/context7

Homepage
github.com/monotool/context7#readme