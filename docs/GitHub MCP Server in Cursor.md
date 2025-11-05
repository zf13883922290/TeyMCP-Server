Install GitHub MCP Server in Cursor
Prerequisites
Cursor IDE installed (latest version)
GitHub Personal Access Token with appropriate scopes
For local installation: Docker installed and running
Remote Server Setup (Recommended)
Install MCP Server

Uses GitHub's hosted server at https://api.githubcopilot.com/mcp/. Requires Cursor v0.48.0+ for Streamable HTTP support. While Cursor supports OAuth for some MCP servers, the GitHub server currently requires a Personal Access Token.

Install steps
Click the install button above and follow the flow, or go directly to your global MCP configuration file at ~/.cursor/mcp.json and enter the code block below
In Tools & Integrations > MCP tools, click the pencil icon next to "github"
Replace YOUR_GITHUB_PAT with your actual GitHub Personal Access Token
Save the file
Restart Cursor
Streamable HTTP Configuration
{
  "mcpServers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_GITHUB_PAT"
      }
    }
  }
}
Local Server Setup
Install MCP Server

The local GitHub MCP server runs via Docker and requires Docker Desktop to be installed and running.

Install steps
Click the install button above and follow the flow, or go directly to your global MCP configuration file at ~/.cursor/mcp.json and enter the code block below
In Tools & Integrations > MCP tools, click the pencil icon next to "github"
Replace YOUR_GITHUB_PAT with your actual GitHub Personal Access Token
Save the file
Restart Cursor
Docker Configuration
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_PAT"
      }
    }
  }
}
Important: The npm package @modelcontextprotocol/server-github is no longer supported as of April 2025. Use the official Docker image ghcr.io/github/github-mcp-server instead.

Configuration Files
Global (all projects): ~/.cursor/mcp.json
Project-specific: .cursor/mcp.json in project root
Verify Installation
Restart Cursor completely
Check for green dot in Settings → Tools & Integrations → MCP Tools
In chat/composer, check "Available Tools"
Test with: "List my GitHub repositories"
Troubleshooting
Remote Server Issues
Streamable HTTP not working: Ensure you're using Cursor v0.48.0 or later
Authentication failures: Verify PAT has correct scopes
Connection errors: Check firewall/proxy settings
Local Server Issues
Docker errors: Ensure Docker Desktop is running
Image pull failures: Try docker logout ghcr.io then retry
Docker not found: Install Docker Desktop and ensure it's running
General Issues
MCP not loading: Restart Cursor completely after configuration
Invalid JSON: Validate that json format is correct
Tools not appearing: Check server shows green dot in MCP settings
Check logs: Look for MCP-related errors in Cursor logs
Important Notes
Docker image: ghcr.io/github/github-mcp-server (official and supported)
npm package: @modelcontextprotocol/server-github (deprecated as of April 2025 - no longer functional)
Cursor specifics: Supports both project and global configurations, uses mcpServers key