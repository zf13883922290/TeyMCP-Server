tavily-mcp
0.2.10 • Public • Published 2 months ago
Tavily Crawl Beta
GitHub Repo stars npm smithery badge

MCP demo

The Tavily MCP server provides:

search, extract, map, crawl tools
Real-time web search capabilities through the tavily-search tool
Intelligent data extraction from web pages via the tavily-extract tool
Powerful web mapping tool that creates a structured map of website
Web crawler that systematically explores websites
📚 Helpful Resources
Tutorial on combining Tavily MCP with Neo4j MCP server
Tutorial on integrating Tavily MCP with Cline in VS Code
Remote MCP Server
Connect directly to Tavily's remote MCP server instead of running it locally. This provides a seamless experience without requiring local installation or configuration.

Simply use the remote MCP server URL with your Tavily API key:

https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key> 
Get your Tavily API key from tavily.com.

Connect to Cursor
Install MCP Server

Click the ⬆️ Add to Cursor ⬆️ button, this will do most of the work for you but you will still need to edit the configuration to add your API-KEY. You can get a Tavily API key here.

once you click the button you should be redirect to Cursor ...

Step 1
Click the install button



Step 2
You should see the MCP is now installed, if the blue slide is not already turned on, manually turn it on. You also need to edit the configuration to include your own Tavily API key. 

Step 3
You will then be redirected to your mcp.json file where you have to add your-api-key.

{
  "mcpServers": {
    "tavily-remote-mcp": {
      "command": "npx -y mcp-remote https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>",
      "env": {}
    }
  }
}
Connect to Claude Desktop
Claude desktop now supports adding integrations which is currently in beta. An integration in this case is the Tavily Remote MCP, below I will explain how to add the MCP as an integration in Claude desktop.

Step 1
open claude desktop, click the button with the two sliders and then navigate to add integrations. 

Step 2
click Add integrations 

Step 3
Name the integration and insert the Tavily remote MCP url with your API key. You can get a Tavily API key here. Click Add to confirm. 

Step 4
Retrun to the chat screen and you will see the Tavily Remote MCP is now connected to Claude desktop. 

OpenAI
Allow models to use remote MCP servers to perform tasks.

You first need to export your OPENAI_API_KEY
You must also add your Tavily API-key to <your-api-key>, you can get a Tavily API key here
from openai import OpenAI

client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1",
    tools=[
        {
            "type": "mcp",
            "server_label": "tavily",
            "server_url": "https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>",
            "require_approval": "never",
        },
    ],
    input="Do you have access to the tavily mcp server?",
)

print(resp.output_text)
Clients that don't support remote MCPs
mcp-remote is a lightweight bridge that lets MCP clients that can only talk to local (stdio) servers securely connect to remote MCP servers over HTTP + SSE with OAuth-based auth, so you can host and update your server in the cloud while existing clients keep working. It serves as an experimental stop-gap until popular MCP clients natively support remote, authorized servers.

{
    "tavily-remote": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>"
      ]
    }
}
Local MCP
Prerequisites 🔧
Before you begin, ensure you have:

Tavily API key
If you don't have a Tavily API key, you can sign up for a free account here
Claude Desktop or Cursor
Node.js (v20 or higher)
You can verify your Node.js installation by running:
node --version
Git installed (only needed if using Git installation method)
On macOS: brew install git
On Linux:
Debian/Ubuntu: sudo apt install git
RedHat/CentOS: sudo yum install git
On Windows: Download Git for Windows
Tavily MCP server installation ⚡
Running with NPX
npx -y tavily-mcp@latest 
Installing via Smithery
To install Tavily MCP Server for Claude Desktop automatically via Smithery:

npx -y @smithery/cli install @tavily-ai/tavily-mcp --client claude
Although you can launch a server on its own, it's not particularly helpful in isolation. Instead, you should integrate it into an MCP client. Below is an example of how to configure the Claude Desktop app to work with the tavily-mcp server.

Configuring MCP Clients ⚙️
This repository will explain how to configure VS Code, Cursor and Claude Desktop to work with the tavily-mcp server.

Configuring VS Code 💻
For one-click installation, click one of the install buttons below:

Install with NPX in VS Code Install with NPX in VS Code Insiders

Manual Installation
First check if there are install buttons at the top of this section that match your needs. If you prefer manual installation, follow these steps:

Add the following JSON block to your User Settings (JSON) file in VS Code. You can do this by pressing Ctrl + Shift + P (or Cmd + Shift + P on macOS) and typing Preferences: Open User Settings (JSON).

{
  "mcp": {
    "inputs": [
      {
        "type": "promptString",
        "id": "tavily_api_key",
        "description": "Tavily API Key",
        "password": true
      }
    ],
    "servers": {
      "tavily": {
        "command": "npx",
        "args": ["-y", "tavily-mcp@latest"],
        "env": {
          "TAVILY_API_KEY": "${input:tavily_api_key}"
        }
      }
    }
  }
}
Optionally, you can add it to a file called .vscode/mcp.json in your workspace:

{
  "inputs": [
    {
      "type": "promptString",
      "id": "tavily_api_key",
      "description": "Tavily API Key",
      "password": true
    }
  ],
  "servers": {
    "tavily": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@latest"],
      "env": {
        "TAVILY_API_KEY": "${input:tavily_api_key}"
      }
    }
  }
}
Configuring Cline 🤖
The easiest way to set up the Tavily MCP server in Cline is through the marketplace with a single click:

Open Cline in VS Code
Click on the Cline icon in the sidebar
Navigate to the "MCP Servers" tab ( 4 squares )
Search "Tavily" and click "install"
When prompted, enter your Tavily API key
Alternatively, you can manually set up the Tavily MCP server in Cline:

Open the Cline MCP settings file:

For macOS:
# Using Visual Studio Code
code ~/Library/Application\ Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json

# Or using TextEdit
open -e ~/Library/Application\ Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
For Windows:
code %APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
Add the Tavily server configuration to the file:

Replace your-api-key-here with your actual Tavily API key.

{
  "mcpServers": {
    "tavily-mcp": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@latest"],
      "env": {
        "TAVILY_API_KEY": "your-api-key-here"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
Save the file and restart Cline if it's already running.

When using Cline, you'll now have access to the Tavily MCP tools. You can ask Cline to use the tavily-search and tavily-extract tools directly in your conversations.

Configuring the Claude Desktop app 🖥️
For macOS:
# Create the config file if it doesn't exist
touch "$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Opens the config file in TextEdit 
open -e "$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Alternative method using Visual Studio Code (requires VS Code to be installed)
code "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
For Windows:
code %APPDATA%\Claude\claude_desktop_config.json
Add the Tavily server configuration:
Replace your-api-key-here with your actual Tavily API key.

{
  "mcpServers": {
    "tavily-mcp": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@latest"],
      "env": {
        "TAVILY_API_KEY": "your-api-key-here"
      }
    }
  }
}
2. Git Installation
Clone the repository:
git clone https://github.com/tavily-ai/tavily-mcp.git
cd tavily-mcp
Install dependencies:
npm install
Build the project:
npm run build
Configuring the Claude Desktop app ⚙️
Follow the configuration steps outlined in the Configuring the Claude Desktop app section above, using the below JSON configuration.

Replace your-api-key-here with your actual Tavily API key and /path/to/tavily-mcp with the actual path where you cloned the repository on your system.

{
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": ["/path/to/tavily-mcp/build/index.js"],
      "env": {
        "TAVILY_API_KEY": "your-api-key-here"
      }
    }
  }
}
Acknowledgments ✨
Model Context Protocol for the MCP specification
Anthropic for Claude Desktop
Readme
Keywords
tavily-mcptavilymcpcrawlmodel-context-protocolwebsearchclaudeclaude-desktopsearch-apiweb-searchai-searchanthropicreal-time-searchsearch-toolstavily-apitavily-searchtavily-extractweb-extractiondata-extractionsearch-integration
Package Sidebar
Install
npm i tavily-mcp