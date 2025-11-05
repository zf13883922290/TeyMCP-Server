Remote GitHub MCP Server 🚀
Install in VS Code Install in VS Code Insiders

Easily connect to the GitHub MCP Server using the hosted version – no local setup or runtime required.

URL: https://api.githubcopilot.com/mcp/

About
The remote GitHub MCP server is built using this repository as a library, and binding it into GitHub server infrastructure with an internal repository. You can open issues and propose changes in this repository, and we regularly update the remote server to include the latest version of this code.

The remote server has additional tools that are not available in the local MCP server, such as the create_pull_request_with_copilot tool for invoking Copilot coding agent.

Remote MCP Toolsets
Below is a table of available toolsets for the remote GitHub MCP Server. Each toolset is provided as a distinct URL so you can mix and match to create the perfect combination of tools for your use-case. Add /readonly to the end of any URL to restrict the tools in the toolset to only those that enable read access. We also provide the option to use headers instead.

Name	Description	API URL	1-Click Install (VS Code)	Read-only Link	1-Click Read-only Install (VS Code)
all	All available GitHub MCP tools	https://api.githubcopilot.com/mcp/	Install	read-only	Install read-only
Actions	GitHub Actions workflows and CI/CD operations	https://api.githubcopilot.com/mcp/x/actions	Install	read-only	Install read-only
Code Security	Code security related tools, such as GitHub Code Scanning	https://api.githubcopilot.com/mcp/x/code_security	Install	read-only	Install read-only
Dependabot	Dependabot tools	https://api.githubcopilot.com/mcp/x/dependabot	Install	read-only	Install read-only
Discussions	GitHub Discussions related tools	https://api.githubcopilot.com/mcp/x/discussions	Install	read-only	Install read-only
Experiments	Experimental features that are not considered stable yet	https://api.githubcopilot.com/mcp/x/experiments	Install	read-only	Install read-only
Gists	GitHub Gist related tools	https://api.githubcopilot.com/mcp/x/gists	Install	read-only	Install read-only
Issues	GitHub Issues related tools	https://api.githubcopilot.com/mcp/x/issues	Install	read-only	Install read-only
Labels	GitHub Labels related tools	https://api.githubcopilot.com/mcp/x/labels	Install	read-only	Install read-only
Notifications	GitHub Notifications related tools	https://api.githubcopilot.com/mcp/x/notifications	Install	read-only	Install read-only
Organizations	GitHub Organization related tools	https://api.githubcopilot.com/mcp/x/orgs	Install	read-only	Install read-only
Projects	GitHub Projects related tools	https://api.githubcopilot.com/mcp/x/projects	Install	read-only	Install read-only
Pull Requests	GitHub Pull Request related tools	https://api.githubcopilot.com/mcp/x/pull_requests	Install	read-only	Install read-only
Repositories	GitHub Repository related tools	https://api.githubcopilot.com/mcp/x/repos	Install	read-only	Install read-only
Secret Protection	Secret protection related tools, such as GitHub Secret Scanning	https://api.githubcopilot.com/mcp/x/secret_protection	Install	read-only	Install read-only
Security Advisories	Security advisories related tools	https://api.githubcopilot.com/mcp/x/security_advisories	Install	read-only	Install read-only
Stargazers	GitHub Stargazers related tools	https://api.githubcopilot.com/mcp/x/stargazers	Install	read-only	Install read-only
Users	GitHub User related tools	https://api.githubcopilot.com/mcp/x/users	Install	read-only	Install read-only
Additional Remote Server Toolsets
These toolsets are only available in the remote GitHub MCP Server and are not included in the local MCP server.

Name	Description	API URL	1-Click Install (VS Code)	Read-only Link	1-Click Read-only Install (VS Code)
Copilot	Copilot related tools	https://api.githubcopilot.com/mcp/x/copilot	Install	read-only	Install read-only
Copilot Spaces	Copilot Spaces tools	https://api.githubcopilot.com/mcp/x/copilot_spaces	Install	read-only	Install read-only
GitHub support docs search	Retrieve documentation to answer GitHub product and support questions. Topics include: GitHub Actions Workflows, Authentication, ...	https://api.githubcopilot.com/mcp/x/github_support_docs_search	Install	read-only	Install read-only
Optional Headers
The Remote GitHub MCP server has optional headers equivalent to the Local server env vars:

X-MCP-Toolsets: Comma-separated list of toolsets to enable. E.g. "repos,issues".
Equivalent to GITHUB_TOOLSETS env var for Local server.
If the list is empty, default toolsets will be used. If a bad toolset is provided, the server will fail to start and emit a 400 bad request status. Whitespace is ignored.
X-MCP-Readonly: Enables only "read" tools.
Equivalent to GITHUB_READ_ONLY env var for Local server.
If this header is empty, "false", "f", "no", "n", "0", or "off" (ignoring whitespace and case), it will be interpreted as false. All other values are interpreted as true.
Example:

{
    "type": "http",
    "url": "https://api.githubcopilot.com/mcp/",
    "headers": {
        "X-MCP-Toolsets": "repos,issues",
        "X-MCP-Readonly": "true"
    }
}
URL Path Parameters
The Remote GitHub MCP server supports the following URL path patterns:

/ - Default toolset (see "default" toolset)
/readonly - Default toolset in read-only mode
/x/all - All available toolsets
/x/all/readonly - All available toolsets in read-only mode
/x/{toolset} - Single specific toolset
/x/{toolset}/readonly - Single specific toolset in read-only mode
Note: {toolset} can only be a single toolset, not a comma-separated list. To combine multiple toolsets, use the X-MCP-Toolsets header instead.

Example:

{
    "type": "http",
    "url": "https://api.githubcopilot.com/mcp/x/issues/readonly"
}
