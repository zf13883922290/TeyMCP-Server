nx-mcp
0.9.0 • Public • Published 13 hours ago
Nx MCP Server
npm version

A Model Context Protocol server implementation for Nx.

Overview
The Nx MCP server gives LLMs deep access to your monorepo’s structure: project relationships, file mappings, runnable tasks, ownership info, tech stacks, Nx generators, and even Nx documentation. With this context, LLMs can generate code tailored to your stack, understand the impact of a change, and apply modifications across connected files with precision. This is possible because Nx already understands the higher-level architecture of your workspace, and monorepos bring all relevant projects into one place.

Read more in our blog post and in our docs.

Installation and Usage
There are two ways to use this MCP server:

a) Run it via the nx-mcp package
Simply invoke the MCP server via npx or your package manager's equivalent.

Here's an example of a mcp.json configuration:

{
  "servers": {
    "nx-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["nx-mcp@latest"]
    }
  }
}
Claude Code
VSCode
Warp
Refer to your AI tool's documentation for how to register an MCP server. For example, Cursor or Claude Desktop support MCP.

If you want to host the server instead of communicating via stdio, you can use the --sse and --port flags. Keep in mind that the Nx MCP server only supports a single concurrent connection right now, so connecting multiple clients at the same time might break in some cases.

Run nx-mcp --help to see what options are available.

b) Use the Nx Console extension
If you're using Cursor you can directly install the Nx Console extension which automatically manages the MCP server for you.

More info:

Install Nx Console
Configure Cursor to use the nx-mcp
Available Tools
The Nx MCP server provides a comprehensive set of tools for interacting with your Nx workspace.

nx_docs: Returns documentation sections relevant to user queries about Nx
nx_available_plugins: Lists available Nx plugins from the core team and local workspace plugins
nx_workspace_path: Returns the path to the Nx workspace root
nx_workspace: Returns readable representation of project graph and nx.json configuration
nx_project_details: Returns complete project configuration in JSON format for a given project
nx_generators: Returns list of generators relevant to user queries
nx_generator_schema: Returns detailed JSON schema for a specific Nx generator
nx_current_running_tasks_details: Lists currently running Nx TUI processes and task statuses
nx_current_running_task_output: Returns terminal output for specific running tasks
nx_run_generator: Opens generate UI with prefilled options (requires running IDE instance)
nx_visualize_graph: Visualizes the Nx graph (requires running IDE instance)
Nx Cloud Analytics Tools (only available w/ Nx Cloud enabled)
These tools provide analytics and insights into your Nx Cloud CI/CD data, helping you track performance trends and team productivity:

nx_cloud_analytics_pipeline_executions_search: Analyzes historical pipeline execution data to identify trends and patterns
nx_cloud_analytics_pipeline_execution_details: Analyzes detailed data for a specific pipeline execution to investigate performance
nx_cloud_analytics_runs_search: Analyzes historical run data to track performance trends and productivity patterns
nx_cloud_analytics_run_details: Analyzes detailed data for a specific run to investigate command execution performance
nx_cloud_analytics_tasks_search: Analyzes aggregated task performance statistics including success rates and cache hit rates
nx_cloud_analytics_task_executions_search: Analyzes individual task execution data to investigate performance trends
When no workspace path is specified, only the nx_docs and nx_available_plugins tools will be available.

Available Resources
When connected to an Nx Cloud-enabled workspace, the Nx MCP server automatically exposes recent CI Pipeline Executions (CIPEs) as MCP resources. Resources appear in your AI tool's resource picker, allowing the LLM to access detailed information about CI runs including failed tasks, terminal output, and affected files.

Contributing & Development
Contributions are welcome! Please see the Nx Console contribution guide for more details.

The basic steps are:

Clone the Nx Console repository and follow installation steps
Build the nx-mcp using nx run nx-mcp:build (or nx run nx-mcp:build:debug for debugging with source maps)
Use the MCP Inspector to test out your changes
License
MIT

Readme
Keywords
nxmonorepoaimcpmodelcontextprotocol
Provenance
Built and signed on
GitHub Actions
View build summary
Source Commit

github.com/nrwl/nx-console@2d01ffd
Build File

.github/workflows/publish-nx-mcp.yml
Public Ledger

Transparency log entry
Share feedback
Package Sidebar
Install
npm i nx-mcp


Repository
github.com/nrwl/nx-console

Homepage
nx.dev