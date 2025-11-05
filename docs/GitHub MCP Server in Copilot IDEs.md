
Install GitHub MCP Server in Copilot IDEs
Quick setup guide for the GitHub MCP server in GitHub Copilot across different IDEs. For VS Code instructions, refer to the VS Code install guide in the README

Requirements:
GitHub Copilot License: Any Copilot plan (Free, Pro, Pro+, Business, Enterprise) for Copilot access
GitHub Account: Individual GitHub account (organization/enterprise membership optional) for GitHub MCP server access
MCP Servers in Copilot Policy: Organizations assigning Copilot seats must enable this policy for all MCP access in Copilot for VS Code and Copilot Coding Agent – all other Copilot IDEs will migrate to this policy in the coming months
Editor Preview Policy: Organizations assigning Copilot seats must enable this policy for OAuth access while the Remote GitHub MCP Server is in public preview
Note: All Copilot IDEs now support the remote GitHub MCP server. VS Code offers OAuth authentication, while Visual Studio, JetBrains IDEs, Xcode, and Eclipse currently use PAT authentication with OAuth support coming soon.

Visual Studio
Requires Visual Studio 2022 version 17.14.9 or later.

Remote Server (Recommended)
The remote GitHub MCP server is hosted by GitHub and provides automatic updates with no local setup required.

Configuration
Create an .mcp.json file in your solution or %USERPROFILE% directory.
Add this configuration:
{
  "servers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
Save the file. Wait for CodeLens to update to offer a way to authenticate to the new server, activate that and pick the GitHub account to authenticate with.
In the GitHub Copilot Chat window, switch to Agent mode.
Activate the tool picker in the Chat window and enable one or more tools from the "github" MCP server.
Local Server
For users who prefer to run the GitHub MCP server locally. Requires Docker installed and running.

Configuration
Create an .mcp.json file in your solution or %USERPROFILE% directory.
Add this configuration:
{
  "inputs": [
    {
      "id": "github_pat",
      "description": "GitHub personal access token",
      "type": "promptString",
      "password": true
    }
  ],
  "servers": {
    "github": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github_pat}"
      }
    }
  }
}
Save the file. Wait for CodeLens to update to offer a way to provide user inputs, activate that and paste in a PAT you generate from https://github.com/settings/tokens.
In the GitHub Copilot Chat window, switch to Agent mode.
Activate the tool picker in the Chat window and enable one or more tools from the "github" MCP server.
Documentation: Visual Studio MCP Guide

JetBrains IDEs
Agent mode and MCP support available in public preview across IntelliJ IDEA, PyCharm, WebStorm, and other JetBrains IDEs.

Remote Server (Recommended)
The remote GitHub MCP server is hosted by GitHub and provides automatic updates with no local setup required.

Note: OAuth authentication for the remote GitHub server is not yet supported in JetBrains IDEs. You must use a Personal Access Token (PAT).

Configuration Steps
Install/update the GitHub Copilot plugin
Click GitHub Copilot icon in the status bar → Edit Settings → Model Context Protocol → Configure
Add configuration:
{
  "servers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "requestInit": {
        "headers": {
          "Authorization": "Bearer YOUR_GITHUB_PAT"
        }
      }
    }
  }
}
Press Ctrl + S or Command + S to save, or close the mcp.json file. The configuration should take effect immediately and restart all the MCP servers defined. You can restart the IDE if needed.
Local Server
For users who prefer to run the GitHub MCP server locally. Requires Docker installed and running.

Configuration
{
  "servers": {
    "github": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", 
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_PAT"
      }
    }
  }
}
Documentation: JetBrains Copilot Guide

Xcode
Agent mode and MCP support now available in public preview for Xcode.

Remote Server (Recommended)
The remote GitHub MCP server is hosted by GitHub and provides automatic updates with no local setup required.

Note: OAuth authentication for the remote GitHub server is not yet supported in Xcode. You must use a Personal Access Token (PAT).

Configuration Steps
Install/update GitHub Copilot for Xcode
Open GitHub Copilot for Xcode app → Agent Mode → 🛠️ Tool Picker → Edit Config
Configure your MCP servers:
{
  "servers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "requestInit": {
        "headers": {
          "Authorization": "Bearer YOUR_GITHUB_PAT"
        }
      }
    }
  }
}
Local Server
For users who prefer to run the GitHub MCP server locally. Requires Docker installed and running.

Configuration
{
  "servers": {
    "github": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", 
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_PAT"
      }
    }
  }
}
Documentation: Xcode Copilot Guide

Eclipse
MCP support available with Eclipse 2024-03+ and latest version of the GitHub Copilot plugin.

Remote Server (Recommended)
The remote GitHub MCP server is hosted by GitHub and provides automatic updates with no local setup required.

Note: OAuth authentication for the remote GitHub server is not yet supported in Eclipse. You must use a Personal Access Token (PAT).

Configuration Steps
Install GitHub Copilot extension from Eclipse Marketplace
Click the GitHub Copilot icon → Edit Preferences → MCP (under GitHub Copilot)
Add GitHub MCP server configuration:
{
  "servers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "requestInit": {
        "headers": {
          "Authorization": "Bearer YOUR_GITHUB_PAT"
        }
      }
    }
  }
}
Click the "Apply and Close" button in the preference dialog and the configuration will take effect automatically.
Local Server
For users who prefer to run the GitHub MCP server locally. Requires Docker installed and running.

Configuration
{
  "servers": {
    "github": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", 
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_PAT"
      }
    }
  }
}
Documentation: Eclipse Copilot plugin

GitHub Personal Access Token
For PAT authentication, see our Personal Access Token documentation for setup instructions.

Usage
After setup:

Restart your IDE completely
Open Agent mode in Copilot Chat
Try: "List recent issues in this repository"
Copilot can now access GitHub data and perform repository operations
Troubleshooting
Connection issues: Verify GitHub PAT permissions and IDE version compatibility
Authentication errors: Check if your organization has enabled the MCP policy for Copilot
Tools not appearing: Restart IDE after configuration changes and check error logs
Local server issues: Ensure Docker is running for Docker-based setups