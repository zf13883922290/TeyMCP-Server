Microsoft 365 Agents Toolkit MCP Server
The Microsoft 365 Agents Toolkit MCP Server is a Model Context Protocol (MCP) server that provides a seamless connection between AI agents and developers for building apps and agents for Microsoft 365 and Microsoft 365 Copilot.

Overview
What can you do with it?
M365 Agents Toolkit MCP Server is designed to help you:

Build and deploy AI agents for Microsoft 365
Integrate with Microsoft 365 Copilot features
Access and manage app and agent templates
Troubleshoot common issues effectively
Currently Supported Tools
Schema Fetcher for:
App Manifest
Declarative Agent Manifest
API Plugin Manifest
Microsoft 365 and Microsoft 365 Copilot Knowledge Retriever
Apps and Agents Samples and Templates Code Snippets Retriever
Troubleshooting Retriever
Prerequisites
The Microsoft 365 Agents Toolkit MCP Server requires Node.js to install and run the server. If you don't have it installed, follow the instructions here.
Install either the stable or Insiders release of VS Code:
💫 Stable release
🔮 Insiders release
Install the GitHub Copilot and GitHub Copilot Chat extensions
Manual Install
For a step-by-step guide to install the Microsoft 365 Agents Toolkit MCP Server, follow these instructions:

Add .vscode/mcp.json:
{
    "servers": {
        "M365AgentsToolkit Server": {
            "command": "npx",
            "args": [
                "-y",
                "@microsoft/m365agentstoolkit-mcp@latest",
                "server",
                "start"
            ]
        }
    }
}
Install From Command Palette
Install with NPX in VS Code Install with NPX in VS Code Insiders
List The Tools
Open GitHub Copilot in VS Code and switch to Agent mode

Click refresh on the tools list.

For Visual Studio
Manual configuration required, please follow: Visual Studio MCP Official Guide

Feedback
We're building this in the open. Your feedback is much appreciated, and will help us shape the future of the Microsoft 365 Agents Toolkit MCP Server.

Open an issue in the public repository.
Send an email to tcsupport@microsoft.com to chat with the product team.
Code of Conduct
This project has adopted the Microsoft Open Source Code of Conduct. For more information see the Code of Conduct FAQ or contact opencode@microsoft.com with any additional questions or comments.

License
Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the MIT license.

Readme
Keywords
mcpmodel-context-protocolm365agentsm365agentstoolkit-mcp
Package Sidebar
Install
npm i @microsoft/m365agentstoolkit-mcp


Repository
github.com/OfficeDev/microsoft-365-agents-toolkit

Homepage
github.com/OfficeDev/microsoft-365-agents-toolkit#readme