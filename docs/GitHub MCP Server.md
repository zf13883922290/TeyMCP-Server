GitHub MCP Server
The GitHub MCP Server connects AI tools directly to GitHub's platform. This gives AI agents, assistants, and chatbots the ability to read repositories and code files, manage issues and PRs, analyze code, and automate workflows. All through natural language interactions.

Use Cases
Repository Management: Browse and query code, search files, analyze commits, and understand project structure across any repository you have access to.
Issue & PR Automation: Create, update, and manage issues and pull requests. Let AI help triage bugs, review code changes, and maintain project boards.
CI/CD & Workflow Intelligence: Monitor GitHub Actions workflow runs, analyze build failures, manage releases, and get insights into your development pipeline.
Code Analysis: Examine security findings, review Dependabot alerts, understand code patterns, and get comprehensive insights into your codebase.
Team Collaboration: Access discussions, manage notifications, analyze team activity, and streamline processes for your team.
Built for developers who want to connect their AI tools to GitHub context and capabilities, from simple natural language queries to complex multi-step agent workflows.

Remote GitHub MCP Server
Install in VS Code Install in VS Code Insiders

The remote GitHub MCP Server is hosted by GitHub and provides the easiest method for getting up and running. If your MCP host does not support remote MCP servers, don't worry! You can use the local version of the GitHub MCP Server instead.

Prerequisites
A compatible MCP host with remote server support (VS Code 1.101+, Claude Desktop, Cursor, Windsurf, etc.)
Any applicable policies enabled
Install in VS Code
For quick installation, use one of the one-click install buttons above. Once you complete that flow, toggle Agent mode (located by the Copilot Chat text input) and the server will start. Make sure you're using VS Code 1.101 or later for remote MCP and OAuth support.

Alternatively, to manually configure VS Code, choose the appropriate JSON block from the examples below and add it to your host configuration:

Using OAuth	Using a GitHub PAT
VS Code (version 1.101 or greater)
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${input:github_mcp_pat}"
      }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "github_mcp_pat",
      "description": "GitHub Personal Access Token",
      "password": true
    }
  ]
}
Install in other MCP hosts
GitHub Copilot in other IDEs - Installation for JetBrains, Visual Studio, Eclipse, and Xcode with GitHub Copilot
Claude Applications - Installation guide for Claude Web, Claude Desktop and Claude Code CLI
Cursor - Installation guide for Cursor IDE
Windsurf - Installation guide for Windsurf IDE
Note: Each MCP host application needs to configure a GitHub App or OAuth App to support remote access via OAuth. Any host application that supports remote MCP servers should support the remote GitHub server with PAT authentication. Configuration details and support levels vary by host. Make sure to refer to the host application's documentation for more info.

Configuration
Toolset configuration
See Remote Server Documentation for full details on remote server configuration, toolsets, headers, and advanced usage. This file provides comprehensive instructions and examples for connecting, customizing, and installing the remote GitHub MCP Server in VS Code and other MCP hosts.

When no toolsets are specified, default toolsets are used.

Enterprise Cloud with data residency (ghe.com)
GitHub Enterprise Cloud can also make use of the remote server.

Example for https://octocorp.ghe.com:

{
    ...
    "proxima-github": {
      "type": "http",
      "url": "https://copilot-api.octocorp.ghe.com/mcp",
      "headers": {
        "Authorization": "Bearer ${input:github_mcp_pat}"
      }
    },
    ...
}
GitHub Enterprise Server does not support remote server hosting. Please refer to GitHub Enterprise Server and Enterprise Cloud with data residency (ghe.com) from the local server configuration.

Local GitHub MCP Server
Install with Docker in VS Code Install with Docker in VS Code Insiders

Prerequisites
To run the server in a container, you will need to have Docker installed.
Once Docker is installed, you will also need to ensure Docker is running. The image is public; if you get errors on pull, you may have an expired token and need to docker logout ghcr.io.
Lastly you will need to Create a GitHub Personal Access Token. The MCP server can use many of the GitHub APIs, so enable the permissions that you feel comfortable granting your AI tools (to learn more about access tokens, please check out the documentation).
Handling PATs Securely
GitHub Enterprise Server and Enterprise Cloud with data residency (ghe.com)
The flag --gh-host and the environment variable GITHUB_HOST can be used to set the hostname for GitHub Enterprise Server or GitHub Enterprise Cloud with data residency.

For GitHub Enterprise Server, prefix the hostname with the https:// URI scheme, as it otherwise defaults to http://, which GitHub Enterprise Server does not support.
For GitHub Enterprise Cloud with data residency, use https://YOURSUBDOMAIN.ghe.com as the hostname.
"github": {
    "command": "docker",
    "args": [
    "run",
    "-i",
    "--rm",
    "-e",
    "GITHUB_PERSONAL_ACCESS_TOKEN",
    "-e",
    "GITHUB_HOST",
    "ghcr.io/github/github-mcp-server"
    ],
    "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github_token}",
        "GITHUB_HOST": "https://<your GHES or ghe.com domain name>"
    }
}
Installation
Install in GitHub Copilot on VS Code
For quick installation, use one of the one-click install buttons above. Once you complete that flow, toggle Agent mode (located by the Copilot Chat text input) and the server will start.

More about using MCP server tools in VS Code's agent mode documentation.

Install in GitHub Copilot on other IDEs (JetBrains, Visual Studio, Eclipse, etc.)

Add the following JSON block to your IDE's MCP settings.

{
  "mcp": {
    "inputs": [
      {
        "type": "promptString",
        "id": "github_token",
        "description": "GitHub Personal Access Token",
        "password": true
      }
    ],
    "servers": {
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
          "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github_token}"
        }
      }
    }
  }
}
Optionally, you can add a similar example (i.e. without the mcp key) to a file called .vscode/mcp.json in your workspace. This will allow you to share the configuration with other host applications that accept the same format.

Example JSON block without the MCP key included
Install in Other MCP Hosts
For other MCP host applications, please refer to our installation guides:

GitHub Copilot in other IDEs - Installation for JetBrains, Visual Studio, Eclipse, and Xcode with GitHub Copilot
Claude Code & Claude Desktop - Installation guide for Claude Code and Claude Desktop
Cursor - Installation guide for Cursor IDE
Google Gemini CLI - Installation guide for Google Gemini CLI
Windsurf - Installation guide for Windsurf IDE
For a complete overview of all installation options, see our Installation Guides Index.

Note: Any host application that supports local MCP servers should be able to access the local GitHub MCP server. However, the specific configuration process, syntax and stability of the integration will vary by host application. While many may follow a similar format to the examples above, this is not guaranteed. Please refer to your host application's documentation for the correct MCP configuration syntax and setup process.

Build from source
If you don't have Docker, you can use go build to build the binary in the cmd/github-mcp-server directory, and use the github-mcp-server stdio command with the GITHUB_PERSONAL_ACCESS_TOKEN environment variable set to your token. To specify the output location of the build, use the -o flag. You should configure your server to use the built executable as its command. For example:

{
  "mcp": {
    "servers": {
      "github": {
        "command": "/path/to/github-mcp-server",
        "args": ["stdio"],
        "env": {
          "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
        }
      }
    }
  }
}
Tool Configuration
The GitHub MCP Server supports enabling or disabling specific groups of functionalities via the --toolsets flag. This allows you to control which GitHub API capabilities are available to your AI tools. Enabling only the toolsets that you need can help the LLM with tool choice and reduce the context size.

Toolsets are not limited to Tools. Relevant MCP Resources and Prompts are also included where applicable.

When no toolsets are specified, default toolsets are used.

Specifying Toolsets
To specify toolsets you want available to the LLM, you can pass an allow-list in two ways:

Using Command Line Argument:

github-mcp-server --toolsets repos,issues,pull_requests,actions,code_security
Using Environment Variable:

GITHUB_TOOLSETS="repos,issues,pull_requests,actions,code_security" ./github-mcp-server
The environment variable GITHUB_TOOLSETS takes precedence over the command line argument if both are provided.

Using Toolsets With Docker
When using Docker, you can pass the toolsets as environment variables:

docker run -i --rm \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=<your-token> \
  -e GITHUB_TOOLSETS="repos,issues,pull_requests,actions,code_security,experiments" \
  ghcr.io/github/github-mcp-server
Special toolsets
"all" toolset
The special toolset all can be provided to enable all available toolsets regardless of any other configuration:

./github-mcp-server --toolsets all
Or using the environment variable:

GITHUB_TOOLSETS="all" ./github-mcp-server
"default" toolset
The default toolset default is the configuration that gets passed to the server if no toolsets are specified.

The default configuration is:

context
repos
issues
pull_requests
users
To keep the default configuration and add additional toolsets:

GITHUB_TOOLSETS="default,stargazers" ./github-mcp-server
Available Toolsets
The following sets of tools are available:

Toolset	Description
context	Strongly recommended: Tools that provide context about the current user and GitHub context you are operating in
actions	GitHub Actions workflows and CI/CD operations
code_security	Code security related tools, such as GitHub Code Scanning
dependabot	Dependabot tools
discussions	GitHub Discussions related tools
experiments	Experimental features that are not considered stable yet
gists	GitHub Gist related tools
issues	GitHub Issues related tools
labels	GitHub Labels related tools
notifications	GitHub Notifications related tools
orgs	GitHub Organization related tools
projects	GitHub Projects related tools
pull_requests	GitHub Pull Request related tools
repos	GitHub Repository related tools
secret_protection	Secret protection related tools, such as GitHub Secret Scanning
security_advisories	Security advisories related tools
stargazers	GitHub Stargazers related tools
users	GitHub User related tools
Additional Toolsets in Remote Github MCP Server
Toolset	Description
copilot	Copilot related tools (e.g. Copilot Coding Agent)
copilot_spaces	Copilot Spaces related tools
github_support_docs_search	Search docs to answer GitHub product and support questions
Tools
Actions
Code Security
Context
Dependabot
Discussions
Gists
Issues
Labels
Notifications
Organizations
Projects
Pull Requests
Repositories
Secret Protection
Security Advisories
Stargazers
Users
Additional Tools in Remote Github MCP Server
Copilot
Copilot Spaces
GitHub Support Docs Search
Dynamic Tool Discovery
Note: This feature is currently in beta and may not be available in all environments. Please test it out and let us know if you encounter any issues.

Instead of starting with all tools enabled, you can turn on dynamic toolset discovery. Dynamic toolsets allow the MCP host to list and enable toolsets in response to a user prompt. This should help to avoid situations where the model gets confused by the sheer number of tools available.

Using Dynamic Tool Discovery
When using the binary, you can pass the --dynamic-toolsets flag.

./github-mcp-server --dynamic-toolsets
When using Docker, you can pass the toolsets as environment variables:

docker run -i --rm \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=<your-token> \
  -e GITHUB_DYNAMIC_TOOLSETS=1 \
  ghcr.io/github/github-mcp-server
Read-Only Mode
To run the server in read-only mode, you can use the --read-only flag. This will only offer read-only tools, preventing any modifications to repositories, issues, pull requests, etc.

./github-mcp-server --read-only
When using Docker, you can pass the read-only mode as an environment variable:

docker run -i --rm \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=<your-token> \
  -e GITHUB_READ_ONLY=1 \
  ghcr.io/github/github-mcp-server
i18n / Overriding Descriptions
The descriptions of the tools can be overridden by creating a github-mcp-server-config.json file in the same directory as the binary.

The file should contain a JSON object with the tool names as keys and the new descriptions as values. For example:

{
  "TOOL_ADD_ISSUE_COMMENT_DESCRIPTION": "an alternative description",
  "TOOL_CREATE_BRANCH_DESCRIPTION": "Create a new branch in a GitHub repository"
}
You can create an export of the current translations by running the binary with the --export-translations flag.

This flag will preserve any translations/overrides you have made, while adding any new translations that have been added to the binary since the last time you exported.

./github-mcp-server --export-translations
cat github-mcp-server-config.json
You can also use ENV vars to override the descriptions. The environment variable names are the same as the keys in the JSON file, prefixed with GITHUB_MCP_ and all uppercase.

For example, to override the TOOL_ADD_ISSUE_COMMENT_DESCRIPTION tool, you can set the following environment variable:

export GITHUB_MCP_TOOL_ADD_ISSUE_COMMENT_DESCRIPTION="an alternative description"
Library Usage
The exported Go API of this module should currently be considered unstable, and subject to breaking changes. In the future, we may offer stability; please file an issue if there is a use case where this would be valuable.

License
This project is licensed under the terms of the MIT open source license. Please refer to MIT for the