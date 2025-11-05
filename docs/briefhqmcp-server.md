briefhq/mcp-server
Brief MCP server and CLI – connect Cursor/Claude MCP to your Brief organization.

Quick Start (recommended)
One-liner setup: Run this command to configure Brief MCP and install into your tools:

npx -y @briefhq/mcp-server@latest init
This guided setup will:

Save your API key securely using your system keychain
Automatically detect and configure supported tools (Cursor, Claude Desktop, etc.)
Add Brief MCP to your development environment
You can also run non‑interactively with flags like --app, --scope, --yes, and --write.

Prerequisites
Ensure you have Node.js installed (>= 18.18). For automated installs, use version managers:

nvm install 20 or brew install node
Download from nodejs.org if needed
Windows: use nvm-windows or the official Node.js installer
To check if Node.js is installed: node --version

Configuration
Generate an API key in the Brief web app (Organization → MCP Integration)
Configure the server with your API credentials:
npx -y @briefhq/mcp-server@latest configure --api-url https://app.briefhq.ai --api-key <your_api_key>
Replace <your_api_key> with the API key you generated in step 1.

Use with Cursor
Automatic Setup (recommended): Visit your Brief organization’s MCP Integration page and click “Add Brief MCP server to Cursor.”

Manual setup: In Cursor, go to Settings → Cursor Settings → Tools & Integrations, click “+ New MCP Server,” and add:

{
  "mcpServers": {
    "brief": {
      "command": "npx",
      "args": ["-y", "@briefhq/mcp-server@latest", "serve"]
    }
  }
}
Restart Cursor, then invoke Brief tools from the MCP panel.

Use with Claude Code
Choose the appropriate scope based on your needs:

Local Scope (Project-specific):

claude mcp add brief --scope local -- npx -y @briefhq/mcp-server@latest serve
Project Scope (Team-shared):

claude mcp add brief --scope project -- npx -y @briefhq/mcp-server@latest serve
User Scope (Global for you):

claude mcp add brief --scope user -- npx -y @briefhq/mcp-server@latest serve
Verify installation: claude mcp list

Use with Claude Desktop
Download the Claude Desktop Extension (.DXT file) from your Brief organization's MCP Integration page
Open Claude Desktop → Settings → Extensions
Drag and drop the .DXT file to install
Configure with your organization name and API key
Restart Claude Desktop
Commands
npx @briefhq/mcp-server@latest init – One‑liner setup (credentials + install targets)
npx @briefhq/mcp-server@latest configure – Save API base and key securely
npx @briefhq/mcp-server@latest update-guidelines – Update .brief/brief-guidelines.md to the latest version
npx @briefhq/mcp-server@latest test – Verify connectivity to Brief
npx @briefhq/mcp-server@latest serve – Start the MCP server
npx @briefhq/mcp-server@latest --help – Show all available commands
Notes
No global installation required – uses npx to always get the latest version
Auto-updates: .brief/brief-guidelines.md automatically updates to the latest version when the MCP server starts (silent by default, set BRIEF_VERBOSE=1 to see update messages)
API keys are scoped to your organization; you can revoke/rotate any time
Never paste server-only secrets into MCP; only use Brief API keys
Requires Node.js >= 18.18
Readme
Keywords
mcpmodel-context-protocolcursorclaudebriefcli
Package Sidebar
Install
npm i @briefhq/mcp-server


Repository
github.com/Mocksi/brief

Homepage
app.briefhq.ai