JIRA MCP Server
A Model Context Protocol (MCP) server implementation that provides access to JIRA data with relationship tracking, optimized data payloads, and data cleaning for AI context windows.

Installation
npm install -g @answerai/jira-mcp
Usage
With Claude Desktop or Cline
{
  "mcpServers": {
    "jira": {
      "command": "answerai-jira-mcp",
      "env": {
        "JIRA_API_TOKEN": "your_api_token",
        "JIRA_BASE_URL": "your_jira_instance_url",
        "JIRA_USER_EMAIL": "your_email"
      }
    }
  }
}
For more detailed documentation, please visit the GitHub repository.

Readme
Keywords
mcpjiratypescriptnodemodel-context-protocolaiclaudeanthropicatlassian
Package Sidebar
Install
npm i @answerai/jira-mcp


Repository
github.com/the-answerai/jira-mcp

Homepage
github.com/the-answerai/jira-mcp#readme