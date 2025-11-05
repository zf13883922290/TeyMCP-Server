Webflow's MCP server
A Node.js server implementing Model Context Protocol (MCP) for Webflow using the Webflow JavaScript SDK. Enable AI agents to interact with Webflow APIs. Learn more about Webflow's Data API in the developer documentation.

npm shield Webflow

Prerequisites
Node.js
NPM
A Webflow Account
🚀 Remote installation
Get started by installing Webflow's remote MCP server. The remote server uses OAuth to authenticate with your Webflow sites, and a companion app that syncs your live canvas with your AI agent.

Requirements
Node.js 22.3.0 or higher
Note: The MCP server currently supports Node.js 22.3.0 or higher. If you run into version issues, see the Node.js compatibility guidance.

Cursor
Add MCP server to Cursor
Go to Settings → Cursor Settings → MCP & Integrations.
Under MCP Tools, click + New MCP Server.
Paste the following configuration into .cursor/mcp.json (or add the webflow part to your existing configuration):
{
  "mcpServers": {
    "webflow": {
      "url": "https://mcp.webflow.com/sse"
    }
  }
}
Tip: You can create a project-level mcp.json to avoid repeated auth prompts across multiple Cursor windows. See Cursor’s docs on configuration locations.

Save and close the file. Cursor will automatically open an OAuth login page where you can authorize Webflow sites to use with the MCP server.
Open the Webflow Designer
Open your site in the Webflow Designer, or ask your AI agent:
Give me a link to open <MY_SITE_NAME> in the Webflow Designer
Open the MCP Webflow App
In the Designer, open the Apps panel (press E).
Launch your published "Webflow MCP Bridge App".
Wait for the app to connect to the MCP server.
Write your first prompt
Try these in your AI chat:

Analyze my last 5 blog posts and suggest 3 new topic ideas with SEO keywords
Find older blog posts that mention similar topics and add internal links to my latest post
Create a hero section card on my home page with a CTA button and responsive design
Claude desktop
Add MCP server to Claude desktop
Enable developer mode: Help → Troubleshooting → Enable Developer Mode.
Open developer settings: File → Settings → Developer.
Click Get Started or edit the configuration to open claude_desktop_config.json and add:
{
  "mcpServers": {
    "webflow": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.webflow.com/sse"]
    }
  }
}
Save and restart Claude Desktop (Cmd/Ctrl + R). An OAuth login page will open to authorize sites.
Open the Webflow Designer
Open your site in the Webflow Designer, or ask your AI agent:
Give me a link to open <MY_SITE_NAME> in the Webflow Designer
Open the MCP Webflow App
In the Designer, open the Apps panel (press E).
Launch your published "Webflow MCP Bridge App".
Wait for the app to connect to the MCP server.
Write your first prompt
Analyze my last 5 blog posts and suggest 3 new topic ideas with SEO keywords
Find older blog posts that mention similar topics and add internal links to my latest post
Create a hero section card on my home page with a CTA button and responsive design
Reset your OAuth token
To reset your OAuth token, run the following command in your terminal.

rm -rf ~/.mcp-auth
Node.js compatibility
Please see the Node.js compatibility guidance on Webflow's developer docs.

Local Installation
You can also configure the MCP server to run locally. This requires:

Creating and registering your own MCP Bridge App in a Webflow workspace with Admin permissions
Configuring your AI client to start the local MCP server with a Webflow API token
1. Create and publish the MCP bridge app
Before connecting the local MCP server to your AI client, you must create and publish the Webflow MCP Bridge App in your workspace.

Steps
Register a Webflow App

Go to your Webflow Workspace and register a new app.
Follow the official guide: Register an App.
Get the MCP Bridge App code

Option A: Download the latest bundle.zip from the releases page.
Option B: Clone the repository and build it:
git clone https://github.com/virat21/webflow-mcp-bridge-app
cd webflow-mcp-bridge-app
Then build the project following the repository instructions.
Publish the Designer Extension

Go to Webflow Dashboard → Workspace settings → Apps & Integrations → Develop → Your App.
Click “Publish Extension Version”.
Upload your built bundle.zip file.
Open the App in Designer

Once published, open the MCP Bridge App from the Designer → Apps panel in a site within your workspace.
2. Configure your AI client
Cursor
Add to .cursor/mcp.json:

{
  "mcpServers": {
    "webflow": {
      "command": "npx",
      "args": ["-y", "webflow-mcp-server@latest"],
      "env": {
        "WEBFLOW_TOKEN": "<YOUR_WEBFLOW_TOKEN>"
      }
    }
  }
}
Claude desktop
Add to claude_desktop_config.json:

{
  "mcpServers": {
    "webflow": {
      "command": "npx",
      "args": ["-y", "webflow-mcp-server@latest"],
      "env": {
        "WEBFLOW_TOKEN": "<YOUR_WEBFLOW_TOKEN>"
      }
    }
  }
}
3. Use the MCP server with the Webflow Designer
Open your site in the Webflow Designer.
Open the Apps panel (press E) and launch your published “Webflow MCP Bridge App”.
Wait for the app to connect to the MCP server, then use tools from your AI client.
If the Bridge App prompts for a local connection URL, call the get_designer_app_connection_info tool from your AI client and paste the returned http://localhost:<port> URL.
Optional: Run locally via shell
WEBFLOW_TOKEN="<YOUR_WEBFLOW_TOKEN>" npx -y webflow-mcp-server@latest
# PowerShell
$env:WEBFLOW_TOKEN="<YOUR_WEBFLOW_TOKEN>"
npx -y webflow-mcp-server@latest
Reset your OAuth Token
To reset your OAuth token, run the following command in your terminal.

rm -rf ~/.mcp-auth
Node.js compatibility
Please see the Node.js compatibility guidance on Webflow's developer docs.

❓ Troubleshooting
If you are having issues starting the server in your MCP client e.g. Cursor or Claude Desktop, please try the following.

Make sure you have a valid Webflow API token
Go to Webflow's API Playground, log in and generate a token, then copy the token from the Request Generator
Replace YOUR_WEBFLOW_TOKEN in your MCP client configuration with the token you copied
Save and restart your MCP client
Make sure you have the Node and NPM installed
Node.js
NPM
Run the following commands to confirm you have Node and NPM installed:

node -v
npm -v
Clear your NPM cache
Sometimes clearing your NPM cache can resolve issues with npx.

npm cache clean --force
Fix NPM global package permissions
If npm -v doesn't work for you but sudo npm -v does, you may need to fix NPM global package permissions. See the official NPM docs for more information.

Note: if you are making changes to your shell configuration, you may need to restart your shell for changes to take effect.

🛠️ Available tools
See the ./tools directory for a list of available tools

🗣️ Prompts & resources
This implementation doesn't include prompts or resources from the MCP specification. However, this may change in the future when there is broader support across popular MCP clients.

📄 Webflow developer resources
Webflow API Documentation
Webflow JavaScript SDK
⚠️ Known limitations
Static page content updates
The pages_update_static_content endpoint currently only supports updates to localized static pages in secondary locales. Updates to static content in the default locale aren't supported and will result in errors.

About
Webflow logo
Webflow

By webflow
·
86

Enable AI agents to interact with Webflow APIs.

Resources
webflow / mcp-server
Contact support
Footer
© 2025 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Comm