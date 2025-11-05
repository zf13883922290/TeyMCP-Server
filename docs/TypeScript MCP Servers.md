TypeScript MCP Servers

Copy page

Deploy and publish TypeScript MCP servers on Smithery using Smithery CLI

​
Overview
Deploy TypeScript MCP servers using the official MCP SDK with two deployment options:
Remote deployment: Automatic containerization and infrastructure managed by Smithery
Local servers (Beta): Distribute your server as MCP bundle allowing users to run it locally and one-click install it
​
Prerequisites
TypeScript MCP server using the official MCP SDK that exports the MCP server object at entry point
Node.js 18+ and npm installed locally
Smithery CLI installed as a dev dependency (npm i -D @smithery/cli)
New to MCP servers? See the Getting Started guide to learn how to build TypeScript MCP servers from scratch using the official SDK.
​
Project Structure
Your TypeScript project should look like this:

Copy

Ask AI
my-mcp-server/
  smithery.yaml          # Smithery configuration
  package.json           # Node.js dependencies and scripts
  tsconfig.json          # TypeScript configuration
  src/
    index.ts             # Your MCP server code with exported createServer function
​
Setup
​
1. Configure smithery.yaml
Create a smithery.yaml file in your repository root (usually where the package.json is):
​
Remote Deployment (Default)

Copy

Ask AI
runtime: "typescript"
​
Local Server (Beta)

Copy

Ask AI
runtime: "typescript"
target: "local"
Local servers are in beta - When you set target: "local", your server runs locally on user’s machine but is accessible through Smithery’s registry for easy discovery and connection by MCP clients.
​
2. Configure package.json
Your package.json must include the module field pointing to your server entry point:

Copy

Ask AI
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "module": "src/index.ts",  // Points to your server entry point
  "scripts": {
    "build": "npx smithery build",
    "dev": "npx smithery dev"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.17.3",
    "zod": "^3.25.46"
  },
  "devDependencies": {
    "@smithery/cli": "^1.4.6"
  }
}
Install the CLI locally with:

Copy

Ask AI
npm i -D @smithery/cli
The Smithery CLI externalizes your SDKs during bundling so your runtime uses the versions you install. If you see a warning about missing SDKs, add them to your dependencies (most servers need @modelcontextprotocol/sdk and @smithery/sdk).
​
3. Ensure Proper Server Structure
Your TypeScript MCP server must export a default createServer function that returns the MCP server object. If you built your server following the Getting Started guide, it should already have this structure.

Copy

Ask AI
// src/index.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

// Required: Export default createServer function
export default function createServer({ config }) {
  // config contains user-provided settings (see configSchema below)
  const server = new McpServer({
    name: "Your Server Name",
    version: "1.0.0",
  });

  // Register your tools here...
  
  return server.server; // Must return the MCP server object
}
Optional Configuration Schema: If your server needs user configuration (API keys, settings, etc.), export a configSchema:

Copy

Ask AI
// Optional: If your server doesn't need configuration, omit this
export const configSchema = z.object({
  apiKey: z.string().describe("Your API key"),
  timeout: z.number().default(5000).describe("Request timeout in milliseconds"),
});
Where it goes: Export configSchema from the same file as your createServer function (typically src/index.ts).
What it does: Automatically generates session configuration forms for users connecting to your server.
​
OAuth
OAuth is designed only for remote servers and is in beta. OAuth is not available for local servers (target: "local").
If your entry module exports oauth, Smithery CLI auto-mounts the required OAuth endpoints for you during remote deployment.
​
Export an OAuth provider

Copy

Ask AI
// src/index.ts
import type { AuthInfo } from "@modelcontextprotocol/sdk/server/auth/types.js"
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import type { OAuthProvider } from "@smithery/sdk"
import { MyProvider } from "./provider.js"

export default function createServer({ auth }: { auth: AuthInfo }) {
  const server = new McpServer({ name: "My MCP", version: "1.0.0" })
  // register tools...
  return server.server
}

export const oauth: OAuthProvider = new MyProvider() 
The CLI detects oauth and injects the auth routes automatically.
​
Local Development
Test your server locally using the Smithery CLI:

Copy

Ask AI
# Start development server with interactive playground
npm run dev
This opens the Smithery interactive playground where you can:
Test your MCP server tools in real-time
See tool responses and debug issues
Validate your configuration schema
Experiment with different inputs
​
Advanced Build Configuration
For advanced use cases, you can customize the build process using a smithery.config.js file. This is useful for:
Marking packages as external (to avoid bundling issues)
Configuring minification, targets, and other build options
Adding custom esbuild plugins
​
Configuration File
Create smithery.config.js in your project root:

Copy

Ask AI
export default {
  esbuild: {
    // Mark problematic packages as external
    external: ["playwright-core", "puppeteer-core"],

    // Enable minification for production
    minify: true,

    // Set Node.js target version
    target: "node18",
  },
};
​
Common Use Cases
External Dependencies: If you encounter bundling issues with packages like Playwright or native modules:

Copy

Ask AI
export default {
  esbuild: {
    external: ["playwright-core", "sharp", "@grpc/grpc-js"],
  },
};
Configuration applies to both build and dev commands.
​
Deploy
Push your code (including smithery.yaml) to GitHub
Connect your GitHub to Smithery (or claim your server if already listed)
Navigate to the Deployments tab on your server page
Click Deploy to build and host your server