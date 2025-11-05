wordbricks/fetch-mcp
TypeScript icon, indicating that this package has built-in type declarations
1.3.0 • Public • Published 4 months ago
@wordbricks/fetch-mcp
A Model Context Protocol (MCP) server for fetching data from the web. This server provides AI models with the ability to fetch and process web content.

Features
Fetch web pages and APIs
Multiple transport modes (stdio, HTTP)
Easy integration with MCP-compatible AI tools
Command-line interface for standalone usage
Usage
Basic Usage
Start the MCP server with default stdio transport:

bunx @wordbricks/fetch-mcp@latest
HTTP Mode
Start the server in HTTP mode:

bunx @wordbricks/fetch-mcp@latest --transport=http --port=3000
Command Line Options
Usage: npx @wordbricks/fetch-mcp [options]

Options:
  --transport=<type>  Transport type: stdio, http (default: stdio)
  --port=<number>     Port for HTTP transport (default: 11891)
  --help, -h          Show this help message

Examples:
  npx @wordbricks/fetch-mcp
  npx @wordbricks/fetch-mcp --transport=stdio
  npx @wordbricks/fetch-mcp --transport=http --port=3000
Integration with AI Tools
This MCP server can be integrated with various AI tools that support the Model Context Protocol. Configure your AI tool to connect to this server using the appropriate transport method.

Claude Desktop Integration
Add to your Claude Desktop configuration:

{
  "mcpServers": {
    "fetch": {
      "command": "bunx",
      "args": ["@wordbricks/fetch-mcp@latest"]
    }
  }
}
Development
Prerequisites
Bun v1.2.15 or later
Setup
bun install
Development Mode
bun run dev
Build
bun run build
Testing
bun test
Publishing to npm
Automated Releases (Recommended)
This project uses GitHub Actions for automated releases. When you push a version change to the main branch, it will automatically:

Build and test the package
Publish to npm
Create a GitHub release
To trigger an automated release:

Update the version in package.json:

# For a patch release
npm version patch

# For a minor release
npm version minor

# For a major release
npm version major
Push to main:

git push origin main --follow-tags
Prerequisites for automated releases:

Set the NPM_TOKEN secret in your GitHub repository settings
The token should have publish permissions for the @wordbricks scope
Manual Publishing
Ensure you're logged into npm:

npm login
Update the version in package.json

Build and publish:

bun run build
npm publish --access public
The prepublishOnly script will automatically build the package before publishing.

Note: The --access public flag is required for scoped packages (packages starting with @) to make them publicly accessible. This is also configured in package.json under publishConfig.

License
MIT

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Readme
Keywords
mcpmodel-context-protocolfetchweb-scrapingai-tools
Package Sidebar
Install
npm i @wordbricks/fetch-mcp


Repository
github.com/wordbricks/fetch-mcp

Homepage
github.com/wordbricks/fetch-mcp#readme