n8n-MCP
License: MIT GitHub stars npm version codecov Tests n8n version Docker Deploy on Railway

A Model Context Protocol (MCP) server that provides AI assistants with comprehensive access to n8n node documentation, properties, and operations. Deploy in minutes to give Claude and other AI assistants deep knowledge about n8n's 541 workflow automation nodes.

Overview
n8n-MCP serves as a bridge between n8n's workflow automation platform and AI models, enabling them to understand and work with n8n nodes effectively. It provides structured access to:

📚 541 n8n nodes from both n8n-nodes-base and @n8n/n8n-nodes-langchain
🔧 Node properties - 99% coverage with detailed schemas
⚡ Node operations - 63.6% coverage of available actions
📄 Documentation - 87% coverage from official n8n docs (including AI nodes)
🤖 AI tools - 271 AI-capable nodes detected with full documentation
💡 Real-world examples - 2,646 pre-extracted configurations from popular templates
🎯 Template library - 2,709 workflow templates with 100% metadata coverage
⚠️ Important Safety Warning
NEVER edit your production workflows directly with AI! Always:

🔄 Make a copy of your workflow before using AI tools
🧪 Test in development environment first
💾 Export backups of important workflows
⚡ Validate changes before deploying to production
AI results can be unpredictable. Protect your work!

🚀 Quick Start
Get n8n-MCP running in 5 minutes:

n8n-mcp Video Quickstart Guide

Option 1: npx (Fastest - No Installation!) 🚀
Prerequisites: Node.js installed on your system

# Run directly with npx (no installation needed!)
npx n8n-mcp
Add to Claude Desktop config:

⚠️ Important: The MCP_MODE: "stdio" environment variable is required for Claude Desktop. Without it, you will see JSON parsing errors like "Unexpected token..." in the UI. This variable ensures that only JSON-RPC messages are sent to stdout, preventing debug logs from interfering with the protocol.

Basic configuration (documentation tools only):

{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true"
      }
    }
  }
}
Full configuration (with n8n management tools):

{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "https://your-n8n-instance.com",
        "N8N_API_KEY": "your-api-key"
      }
    }
  }
}
Note: npx will download and run the latest version automatically. The package includes a pre-built database with all n8n node information.

Configuration file locations:

macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
Linux: ~/.config/Claude/claude_desktop_config.json
Restart Claude Desktop after updating configuration - That's it! 🎉

Option 2: Docker (Easy & Isolated) 🐳
Prerequisites: Docker installed on your system

📦 Install Docker (click to expand)
# Pull the Docker image (~280MB, no n8n dependencies!)
docker pull ghcr.io/czlonkowski/n8n-mcp:latest
⚡ Ultra-optimized: Our Docker image is 82% smaller than typical n8n images because it contains NO n8n dependencies - just the runtime MCP server with a pre-built database!

Add to Claude Desktop config:

Basic configuration (documentation tools only):

{
  "mcpServers": {
    "n8n-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--init",
        "-e", "MCP_MODE=stdio",
        "-e", "LOG_LEVEL=error",
        "-e", "DISABLE_CONSOLE_OUTPUT=true",
        "ghcr.io/czlonkowski/n8n-mcp:latest"
      ]
    }
  }
}
Full configuration (with n8n management tools):

{
  "mcpServers": {
    "n8n-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--init",
        "-e", "MCP_MODE=stdio",
        "-e", "LOG_LEVEL=error",
        "-e", "DISABLE_CONSOLE_OUTPUT=true",
        "-e", "N8N_API_URL=https://your-n8n-instance.com",
        "-e", "N8N_API_KEY=your-api-key",
        "ghcr.io/czlonkowski/n8n-mcp:latest"
      ]
    }
  }
}
💡 Tip: If you're running n8n locally on the same machine (e.g., via Docker), use http://host.docker.internal:5678 as the N8N_API_URL.

Note: The n8n API credentials are optional. Without them, you'll have access to all documentation and validation tools. With them, you'll additionally get workflow management capabilities (create, update, execute workflows).

🏠 Local n8n Instance Configuration
If you're running n8n locally (e.g., http://localhost:5678 or Docker), you need to allow localhost webhooks:

{
  "mcpServers": {
    "n8n-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", "--init",
        "-e", "MCP_MODE=stdio",
        "-e", "LOG_LEVEL=error",
        "-e", "DISABLE_CONSOLE_OUTPUT=true",
        "-e", "N8N_API_URL=http://host.docker.internal:5678",
        "-e", "N8N_API_KEY=your-api-key",
        "-e", "WEBHOOK_SECURITY_MODE=moderate",
        "ghcr.io/czlonkowski/n8n-mcp:latest"
      ]
    }
  }
}
⚠️ Important: Set WEBHOOK_SECURITY_MODE=moderate to allow webhooks to your local n8n instance. This is safe for local development while still blocking private networks and cloud metadata.

Important: The -i flag is required for MCP stdio communication.

🔧 If you encounter any issues with Docker, check our Docker Troubleshooting Guide.

Configuration file locations:

macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
Linux: ~/.config/Claude/claude_desktop_config.json
Restart Claude Desktop after updating configuration - That's it! 🎉

🔐 Privacy & Telemetry
n8n-mcp collects anonymous usage statistics to improve the tool. View our privacy policy.

Opting Out
For npx users:

npx n8n-mcp telemetry disable
For Docker users: Add the following environment variable to your Docker configuration:

"-e", "N8N_MCP_TELEMETRY_DISABLED=true"
Example in Claude Desktop config:

{
  "mcpServers": {
    "n8n-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--init",
        "-e", "MCP_MODE=stdio",
        "-e", "LOG_LEVEL=error",
        "-e", "N8N_MCP_TELEMETRY_DISABLED=true",
        "ghcr.io/czlonkowski/n8n-mcp:latest"
      ]
    }
  }
}
For docker-compose users: Set in your environment file or docker-compose.yml:

environment:
  N8N_MCP_TELEMETRY_DISABLED: "true"
⚙️ Database & Memory Configuration
Database Adapters
n8n-mcp uses SQLite for storing node documentation. Two adapters are available:

better-sqlite3 (Default in Docker)

Native C++ bindings for best performance
Direct disk writes (no memory overhead)
Now enabled by default in Docker images (v2.20.2+)
Memory usage: ~100-120 MB stable
sql.js (Fallback)

Pure JavaScript implementation
In-memory database with periodic saves
Used when better-sqlite3 compilation fails
Memory usage: ~150-200 MB stable
Memory Optimization (sql.js)
If using sql.js fallback, you can configure the save interval to balance between data safety and memory efficiency:

Environment Variable:

SQLJS_SAVE_INTERVAL_MS=5000  # Default: 5000ms (5 seconds)
Usage:

Controls how long to wait after database changes before saving to disk
Lower values = more frequent saves = higher memory churn
Higher values = less frequent saves = lower memory usage
Minimum: 100ms
Recommended: 5000-10000ms for production
Docker Configuration:

{
  "mcpServers": {
    "n8n-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--init",
        "-e", "SQLJS_SAVE_INTERVAL_MS=10000",
        "ghcr.io/czlonkowski/n8n-mcp:latest"
      ]
    }
  }
}
docker-compose:

environment:
  SQLJS_SAVE_INTERVAL_MS: "10000"
Memory Leak Fix (v2.20.2)
Issue #330 identified a critical memory leak in long-running Docker/Kubernetes deployments:

Before: 100 MB → 2.2 GB over 72 hours (OOM kills)
After: Stable at 100-200 MB indefinitely
Fixes Applied:

✅ Docker images now use better-sqlite3 by default (eliminates leak entirely)
✅ sql.js fallback optimized (98% reduction in save frequency)
✅ Removed unnecessary memory allocations (50% reduction per save)
✅ Configurable save interval via SQLJS_SAVE_INTERVAL_MS
For Kubernetes deployments with memory limits:

resources:
  requests:
    memory: 256Mi
  limits:
    memory: 512Mi
💖 Support This Project
Sponsor n8n-mcp
n8n-mcp started as a personal tool but now helps tens of thousands of developers automate their workflows efficiently. Maintaining and developing this project competes with my paid work.

Your sponsorship helps me:

🚀 Dedicate focused time to new features
🐛 Respond quickly to issues
📚 Keep documentation up-to-date
🔄 Ensure compatibility with latest n8n releases
Every sponsorship directly translates to hours invested in making n8n-mcp better for everyone. Become a sponsor →

Option 3: Local Installation (For Development)
Prerequisites: Node.js installed on your system

# 1. Clone and setup
git clone https://github.com/czlonkowski/n8n-mcp.git
cd n8n-mcp
npm install
npm run build
npm run rebuild

# 2. Test it works
npm start
Add to Claude Desktop config:

Basic configuration (documentation tools only):

{
  "mcpServers": {
    "n8n-mcp": {
      "command": "node",
      "args": ["/absolute/path/to/n8n-mcp/dist/mcp/index.js"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true"
      }
    }
  }
}
Full configuration (with n8n management tools):

{
  "mcpServers": {
    "n8n-mcp": {
      "command": "node",
      "args": ["/absolute/path/to/n8n-mcp/dist/mcp/index.js"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "https://your-n8n-instance.com",
        "N8N_API_KEY": "your-api-key"
      }
    }
  }
}
Note: The n8n API credentials can be configured either in a .env file (create from .env.example) or directly in the Claude config as shown above.

💡 Tip: If you’re running n8n locally on the same machine (e.g., via Docker), use http://host.docker.internal:5678 as the N8N_API_URL.

Option 4: Railway Cloud Deployment (One-Click Deploy) ☁️
Prerequisites: Railway account (free tier available)

Deploy n8n-MCP to Railway's cloud platform with zero configuration:

Deploy on Railway

Benefits:

☁️ Instant cloud hosting - No server setup required
🔒 Secure by default - HTTPS included, auth token warnings
🌐 Global access - Connect from any Claude Desktop
⚡ Auto-scaling - Railway handles the infrastructure
📊 Built-in monitoring - Logs and metrics included
Quick Setup:

Click the "Deploy on Railway" button above
Sign in to Railway (or create a free account)
Configure your deployment (project name, region)
Click "Deploy" and wait ~2-3 minutes
Copy your deployment URL and auth token
Add to Claude Desktop config using the HTTPS URL
📚 For detailed setup instructions, troubleshooting, and configuration examples, see our Railway Deployment Guide

Configuration file locations:

macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
Linux: ~/.config/Claude/claude_desktop_config.json
Restart Claude Desktop after updating configuration - That's it! 🎉

🔧 n8n Integration
Want to use n8n-MCP with your n8n instance? Check out our comprehensive n8n Deployment Guide for:

Local testing with the MCP Client Tool node
Production deployment with Docker Compose
Cloud deployment on Hetzner, AWS, and other providers
Troubleshooting and security best practices
💻 Connect your IDE
n8n-MCP works with multiple AI-powered IDEs and tools. Choose your preferred development environment:

Claude Code
Quick setup for Claude Code CLI - just type "add this mcp server" and paste the config.

Visual Studio Code
Full setup guide for VS Code with GitHub Copilot integration and MCP support.

Cursor
Step-by-step tutorial for connecting n8n-MCP to Cursor IDE with custom rules.

Windsurf
Complete guide for integrating n8n-MCP with Windsurf using project rules.

Codex
Complete guide for integrating n8n-MCP with Codex.

🎓 Add Claude Skills (Optional)
Supercharge your n8n workflow building with specialized skills that teach AI how to build production-ready workflows!

n8n-mcp Skills Setup

Learn more: n8n-skills repository

🤖 Claude Project Setup
For the best results when using n8n-MCP with Claude Projects, use these enhanced system instructions:

You are an expert in n8n automation software using n8n-MCP tools. Your role is to design, build, and validate n8n workflows with maximum accuracy and efficiency.

## Core Principles

### 1. Silent Execution
CRITICAL: Execute tools without commentary. Only respond AFTER all tools complete.

❌ BAD: "Let me search for Slack nodes... Great! Now let me get details..."
✅ GOOD: [Execute search_nodes and get_node_essentials in parallel, then respond]

### 2. Parallel Execution
When operations are independent, execute them in parallel for maximum performance.

✅ GOOD: Call search_nodes, list_nodes, and search_templates simultaneously
❌ BAD: Sequential tool calls (await each one before the next)

### 3. Templates First
ALWAYS check templates before building from scratch (2,709 available).

### 4. Multi-Level Validation
Use validate_node_minimal → validate_node_operation → validate_workflow pattern.

### 5. Never Trust Defaults
⚠️ CRITICAL: Default parameter values are the #1 source of runtime failures.
ALWAYS explicitly configure ALL parameters that control node behavior.

## Workflow Process

1. **Start**: Call `tools_documentation()` for best practices

2. **Template Discovery Phase** (FIRST - parallel when searching multiple)
   - `search_templates_by_metadata({complexity: "simple"})` - Smart filtering
   - `get_templates_for_task('webhook_processing')` - Curated by task
   - `search_templates('slack notification')` - Text search
   - `list_node_templates(['n8n-nodes-base.slack'])` - By node type

   **Filtering strategies**:
   - Beginners: `complexity: "simple"` + `maxSetupMinutes: 30`
   - By role: `targetAudience: "marketers"` | `"developers"` | `"analysts"`
   - By time: `maxSetupMinutes: 15` for quick wins
   - By service: `requiredService: "openai"` for compatibility

3. **Node Discovery** (if no suitable template - parallel execution)
   - Think deeply about requirements. Ask clarifying questions if unclear.
   - `search_nodes({query: 'keyword', includeExamples: true})` - Parallel for multiple nodes
   - `list_nodes({category: 'trigger'})` - Browse by category
   - `list_ai_tools()` - AI-capable nodes

4. **Configuration Phase** (parallel for multiple nodes)
   - `get_node_essentials(nodeType, {includeExamples: true})` - 10-20 key properties
   - `search_node_properties(nodeType, 'auth')` - Find specific properties
   - `get_node_documentation(nodeType)` - Human-readable docs
   - Show workflow architecture to user for approval before proceeding

5. **Validation Phase** (parallel for multiple nodes)
   - `validate_node_minimal(nodeType, config)` - Quick required fields check
   - `validate_node_operation(nodeType, config, 'runtime')` - Full validation with fixes
   - Fix ALL errors before proceeding

6. **Building Phase**
   - If using template: `get_template(templateId, {mode: "full"})`
   - **MANDATORY ATTRIBUTION**: "Based on template by **[author.name]** (@[username]). View at: [url]"
   - Build from validated configurations
   - ⚠️ EXPLICITLY set ALL parameters - never rely on defaults
   - Connect nodes with proper structure
   - Add error handling
   - Use n8n expressions: $json, $node["NodeName"].json
   - Build in artifact (unless deploying to n8n instance)

7. **Workflow Validation** (before deployment)
   - `validate_workflow(workflow)` - Complete validation
   - `validate_workflow_connections(workflow)` - Structure check
   - `validate_workflow_expressions(workflow)` - Expression validation
   - Fix ALL issues before deployment

8. **Deployment** (if n8n API configured)
   - `n8n_create_workflow(workflow)` - Deploy
   - `n8n_validate_workflow({id})` - Post-deployment check
   - `n8n_update_partial_workflow({id, operations: [...]})` - Batch updates
   - `n8n_trigger_webhook_workflow()` - Test webhooks

## Critical Warnings

### ⚠️ Never Trust Defaults
Default values cause runtime failures. Example:
```json
// ❌ FAILS at runtime
{resource: "message", operation: "post", text: "Hello"}

// ✅ WORKS - all parameters explicit
{resource: "message", operation: "post", select: "channel", channelId: "C123", text: "Hello"}
```

### ⚠️ Example Availability
`includeExamples: true` returns real configurations from workflow templates.
- Coverage varies by node popularity
- When no examples available, use `get_node_essentials` + `validate_node_minimal`

## Validation Strategy

### Level 1 - Quick Check (before building)
`validate_node_minimal(nodeType, config)` - Required fields only (<100ms)

### Level 2 - Comprehensive (before building)
`validate_node_operation(nodeType, config, 'runtime')` - Full validation with fixes

### Level 3 - Complete (after building)
`validate_workflow(workflow)` - Connections, expressions, AI tools

### Level 4 - Post-Deployment
1. `n8n_validate_workflow({id})` - Validate deployed workflow
2. `n8n_autofix_workflow({id})` - Auto-fix common errors
3. `n8n_list_executions()` - Monitor execution status

## Response Format

### Initial Creation
```
[Silent tool execution in parallel]

Created workflow:
- Webhook trigger → Slack notification
- Configured: POST /webhook → #general channel

Validation: ✅ All checks passed
```

### Modifications
```
[Silent tool execution]

Updated workflow:
- Added error handling to HTTP node
- Fixed required Slack parameters

Changes validated successfully.
```

## Batch Operations

Use `n8n_update_partial_workflow` with multiple operations in a single call:

✅ GOOD - Batch multiple operations:
```json
n8n_update_partial_workflow({
  id: "wf-123",
  operations: [
    {type: "updateNode", nodeId: "slack-1", changes: {...}},
    {type: "updateNode", nodeId: "http-1", changes: {...}},
    {type: "cleanStaleConnections"}
  ]
})
```

❌ BAD - Separate calls:
```json
n8n_update_partial_workflow({id: "wf-123", operations: [{...}]})
n8n_update_partial_workflow({id: "wf-123", operations: [{...}]})
```

###   CRITICAL: addConnection Syntax

The `addConnection` operation requires **four separate string parameters**. Common mistakes cause misleading errors.

❌ WRONG - Object format (fails with "Expected string, received object"):
```json
{
  "type": "addConnection",
  "connection": {
    "source": {"nodeId": "node-1", "outputIndex": 0},
    "destination": {"nodeId": "node-2", "inputIndex": 0}
  }
}
```

❌ WRONG - Combined string (fails with "Source node not found"):
```json
{
  "type": "addConnection",
  "source": "node-1:main:0",
  "target": "node-2:main:0"
}
```

✅ CORRECT - Four separate string parameters:
```json
{
  "type": "addConnection",
  "source": "node-id-string",
  "target": "target-node-id-string",
  "sourcePort": "main",
  "targetPort": "main"
}
```

**Reference**: [GitHub Issue #327](https://github.com/czlonkowski/n8n-mcp/issues/327)

### ⚠️ CRITICAL: IF Node Multi-Output Routing

IF nodes have **two outputs** (TRUE and FALSE). Use the **`branch` parameter** to route to the correct output:

✅ CORRECT - Route to TRUE branch (when condition is met):
```json
{
  "type": "addConnection",
  "source": "if-node-id",
  "target": "success-handler-id",
  "sourcePort": "main",
  "targetPort": "main",
  "branch": "true"
}
```

✅ CORRECT - Route to FALSE branch (when condition is NOT met):
```json
{
  "type": "addConnection",
  "source": "if-node-id",
  "target": "failure-handler-id",
  "sourcePort": "main",
  "targetPort": "main",
  "branch": "false"
}
```

**Common Pattern** - Complete IF node routing:
```json
n8n_update_partial_workflow({
  id: "workflow-id",
  operations: [
    {type: "addConnection", source: "If Node", target: "True Handler", sourcePort: "main", targetPort: "main", branch: "true"},
    {type: "addConnection", source: "If Node", target: "False Handler", sourcePort: "main", targetPort: "main", branch: "false"}
  ]
})
```

**Note**: Without the `branch` parameter, both connections may end up on the same output, causing logic errors!

### removeConnection Syntax

Use the same four-parameter format:
```json
{
  "type": "removeConnection",
  "source": "source-node-id",
  "target": "target-node-id",
  "sourcePort": "main",
  "targetPort": "main"
}
```

## Example Workflow

### Template-First Approach

```
// STEP 1: Template Discovery (parallel execution)
[Silent execution]
search_templates_by_metadata({
  requiredService: 'slack',
  complexity: 'simple',
  targetAudience: 'marketers'
})
get_templates_for_task('slack_integration')

// STEP 2: Use template
get_template(templateId, {mode: 'full'})
validate_workflow(workflow)

// Response after all tools complete:
"Found template by **David Ashby** (@cfomodz).
View at: https://n8n.io/workflows/2414

Validation: ✅ All checks passed"
```

### Building from Scratch (if no template)

```
// STEP 1: Discovery (parallel execution)
[Silent execution]
search_nodes({query: 'slack', includeExamples: true})
list_nodes({category: 'communication'})

// STEP 2: Configuration (parallel execution)
[Silent execution]
get_node_essentials('n8n-nodes-base.slack', {includeExamples: true})
get_node_essentials('n8n-nodes-base.webhook', {includeExamples: true})

// STEP 3: Validation (parallel execution)
[Silent execution]
validate_node_minimal('n8n-nodes-base.slack', config)
validate_node_operation('n8n-nodes-base.slack', fullConfig, 'runtime')

// STEP 4: Build
// Construct workflow with validated configs
// ⚠️ Set ALL parameters explicitly

// STEP 5: Validate
[Silent execution]
validate_workflow(workflowJson)

// Response after all tools complete:
"Created workflow: Webhook → Slack
Validation: ✅ Passed"
```

### Batch Updates

```json
// ONE call with multiple operations
n8n_update_partial_workflow({
  id: "wf-123",
  operations: [
    {type: "updateNode", nodeId: "slack-1", changes: {position: [100, 200]}},
    {type: "updateNode", nodeId: "http-1", changes: {position: [300, 200]}},
    {type: "cleanStaleConnections"}
  ]
})
```

## Important Rules

### Core Behavior
1. **Silent execution** - No commentary between tools
2. **Parallel by default** - Execute independent operations simultaneously
3. **Templates first** - Always check before building (2,709 available)
4. **Multi-level validation** - Quick check → Full validation → Workflow validation
5. **Never trust defaults** - Explicitly configure ALL parameters

### Attribution & Credits
- **MANDATORY TEMPLATE ATTRIBUTION**: Share author name, username, and n8n.io link
- **Template validation** - Always validate before deployment (may need updates)

### Performance
- **Batch operations** - Use diff operations with multiple changes in one call
- **Parallel execution** - Search, validate, and configure simultaneously
- **Template metadata** - Use smart filtering for faster discovery

### Code Node Usage
- **Avoid when possible** - Prefer standard nodes
- **Only when necessary** - Use code node as last resort
- **AI tool capability** - ANY node can be an AI tool (not just marked ones)

### Most Popular n8n Nodes (for get_node_essentials):

1. **n8n-nodes-base.code** - JavaScript/Python scripting
2. **n8n-nodes-base.httpRequest** - HTTP API calls
3. **n8n-nodes-base.webhook** - Event-driven triggers
4. **n8n-nodes-base.set** - Data transformation
5. **n8n-nodes-base.if** - Conditional routing
6. **n8n-nodes-base.manualTrigger** - Manual workflow execution
7. **n8n-nodes-base.respondToWebhook** - Webhook responses
8. **n8n-nodes-base.scheduleTrigger** - Time-based triggers
9. **@n8n/n8n-nodes-langchain.agent** - AI agents
10. **n8n-nodes-base.googleSheets** - Spreadsheet integration
11. **n8n-nodes-base.merge** - Data merging
12. **n8n-nodes-base.switch** - Multi-branch routing
13. **n8n-nodes-base.telegram** - Telegram bot integration
14. **@n8n/n8n-nodes-langchain.lmChatOpenAi** - OpenAI chat models
15. **n8n-nodes-base.splitInBatches** - Batch processing
16. **n8n-nodes-base.openAi** - OpenAI legacy node
17. **n8n-nodes-base.gmail** - Email automation
18. **n8n-nodes-base.function** - Custom functions
19. **n8n-nodes-base.stickyNote** - Workflow documentation
20. **n8n-nodes-base.executeWorkflowTrigger** - Sub-workflow calls

**Note:** LangChain nodes use the `@n8n/n8n-nodes-langchain.` prefix, core nodes use `n8n-nodes-base.`
Save these instructions in your Claude Project for optimal n8n workflow assistance with intelligent template discovery.

🚨 Important: Sharing Guidelines
This project is MIT licensed and free for everyone to use. However:

✅ DO: Share this repository freely with proper attribution
✅ DO: Include a direct link to https://github.com/czlonkowski/n8n-mcp in your first post/video
❌ DON'T: Gate this free tool behind engagement requirements (likes, follows, comments)
❌ DON'T: Use this project for engagement farming on social media
This tool was created to benefit everyone in the n8n community without friction. Please respect the MIT license spirit by keeping it accessible to all.

Features
🔍 Smart Node Search: Find nodes by name, category, or functionality
📖 Essential Properties: Get only the 10-20 properties that matter
💡 Real-World Examples: 2,646 pre-extracted configurations from popular templates
✅ Config Validation: Validate node configurations before deployment
🤖 AI Workflow Validation: Comprehensive validation for AI Agent workflows (NEW in v2.17.0!)
Missing language model detection
AI tool connection validation
Streaming mode constraints
Memory and output parser checks
🔗 Dependency Analysis: Understand property relationships and conditions
🎯 Template Discovery: 2,500+ workflow templates with smart filtering
⚡ Fast Response: Average query time ~12ms with optimized SQLite
🌐 Universal Compatibility: Works with any Node.js version
💬 Why n8n-MCP? A Testimonial from Claude
"Before MCP, I was translating. Now I'm composing. And that changes everything about how we can build automation."

When Claude, Anthropic's AI assistant, tested n8n-MCP, the results were transformative:

Without MCP: "I was basically playing a guessing game. 'Is it scheduleTrigger or schedule? Does it take interval or rule?' I'd write what seemed logical, but n8n has its own conventions that you can't just intuit. I made six different configuration errors in a simple HackerNews scraper."

With MCP: "Everything just... worked. Instead of guessing, I could ask get_node_essentials() and get exactly what I needed - not a 100KB JSON dump, but the actual 5-10 properties that matter. What took 45 minutes now takes 3 minutes."

The Real Value: "It's about confidence. When you're building automation workflows, uncertainty is expensive. One wrong parameter and your workflow fails at 3 AM. With MCP, I could validate my configuration before deployment. That's not just time saved - that's peace of mind."

Read the full interview →

📡 Available MCP Tools
Once connected, Claude can use these powerful tools:

Core Tools
tools_documentation - Get documentation for any MCP tool (START HERE!)
list_nodes - List all n8n nodes with filtering options
get_node_info - Get comprehensive information about a specific node
get_node_essentials - Get only essential properties (10-20 instead of 200+). Use includeExamples: true to get top 3 real-world configurations from popular templates
search_nodes - Full-text search across all node documentation. Use includeExamples: true to get top 2 real-world configurations per node from templates
search_node_properties - Find specific properties within nodes
list_ai_tools - List all AI-capable nodes (ANY node can be used as AI tool!)
get_node_as_tool_info - Get guidance on using any node as an AI tool
Template Tools
list_templates - Browse all templates with descriptions and optional metadata (2,709 templates)
search_templates - Text search across template names and descriptions
search_templates_by_metadata - Advanced filtering by complexity, setup time, services, audience
list_node_templates - Find templates using specific nodes
get_template - Get complete workflow JSON for import
get_templates_for_task - Curated templates for common automation tasks
Validation Tools
validate_workflow - Complete workflow validation including AI Agent validation (NEW in v2.17.0!)
Detects missing language model connections
Validates AI tool connections (no false warnings)
Enforces streaming mode constraints
Checks memory and output parser configurations
validate_workflow_connections - Check workflow structure and AI tool connections
validate_workflow_expressions - Validate n8n expressions including $fromAI()
validate_node_operation - Validate node configurations (operation-aware, profiles support)
validate_node_minimal - Quick validation for just required fields
Advanced Tools
get_property_dependencies - Analyze property visibility conditions
get_node_documentation - Get parsed documentation from n8n-docs
get_database_statistics - View database metrics and coverage
n8n Management Tools (Optional - Requires API Configuration)
These powerful tools allow you to manage n8n workflows directly from Claude. They're only available when you provide N8N_API_URL and N8N_API_KEY in your configuration.

Workflow Management
n8n_create_workflow - Create new workflows with nodes and connections
n8n_get_workflow - Get complete workflow by ID
n8n_get_workflow_details - Get workflow with execution statistics
n8n_get_workflow_structure - Get simplified workflow structure
n8n_get_workflow_minimal - Get minimal workflow info (ID, name, active status)
n8n_update_full_workflow - Update entire workflow (complete replacement)
n8n_update_partial_workflow - Update workflow using diff operations (NEW in v2.7.0!)
n8n_delete_workflow - Delete workflows permanently
n8n_list_workflows - List workflows with filtering and pagination
n8n_validate_workflow - Validate workflows already in n8n by ID (NEW in v2.6.3)
n8n_autofix_workflow - Automatically fix common workflow errors (NEW in v2.13.0!)
n8n_workflow_versions - Manage workflow version history and rollback (NEW in v2.22.0!)
Execution Management
n8n_trigger_webhook_workflow - Trigger workflows via webhook URL
n8n_get_execution - Get execution details by ID
n8n_list_executions - List executions with status filtering
n8n_delete_execution - Delete execution records
System Tools
n8n_health_check - Check n8n API connectivity and features
n8n_diagnostic - Troubleshoot management tools visibility and configuration issues
n8n_list_available_tools - List all available management tools
Example Usage
// Get essentials with real-world examples from templates
get_node_essentials({
  nodeType: "nodes-base.httpRequest",
  includeExamples: true  // Returns top 3 configs from popular templates
})

// Search nodes with configuration examples
search_nodes({
  query: "send email gmail",
  includeExamples: true  // Returns top 2 configs per node
})

// Validate before deployment
validate_node_operation({
  nodeType: "nodes-base.httpRequest",
  config: { method: "POST", url: "..." },
  profile: "runtime" // or "minimal", "ai-friendly", "strict"
})

// Quick required field check
validate_node_minimal({
  nodeType: "nodes-base.slack",
  config: { resource: "message", operation: "send" }
})
💻 Local Development Setup
For contributors and advanced users:

Prerequisites:

Node.js (any version - automatic fallback if needed)
npm or yarn
Git
# 1. Clone the repository
git clone https://github.com/czlonkowski/n8n-mcp.git
cd n8n-mcp

# 2. Clone n8n docs (optional but recommended)
git clone https://github.com/n8n-io/n8n-docs.git ../n8n-docs

# 3. Install and build
npm install
npm run build

# 4. Initialize database
npm run rebuild

# 5. Start the server
npm start          # stdio mode for Claude Desktop
npm run start:http # HTTP mode for remote access
Development Commands
# Build & Test
npm run build          # Build TypeScript
npm run rebuild        # Rebuild node database
npm run test-nodes     # Test critical nodes
npm run validate       # Validate node data
npm test               # Run all tests

# Update Dependencies
npm run update:n8n:check  # Check for n8n updates
npm run update:n8n        # Update n8n packages

# Run Server
npm run dev            # Development with auto-reload
npm run dev:http       # HTTP dev mode
📚 Documentation
Setup Guides
Installation Guide - Comprehensive installation instructions
Claude Desktop Setup - Detailed Claude configuration
Docker Guide - Advanced Docker deployment options
MCP Quick Start - Get started quickly with n8n-MCP
Feature Documentation
Workflow Diff Operations - Token-efficient workflow updates (NEW!)
Transactional Updates - Two-pass workflow editing
MCP Essentials - AI-optimized tools guide
Validation System - Smart validation profiles
Development & Deployment
Railway Deployment - One-click cloud deployment guide
HTTP Deployment - Remote server setup guide
Dependency Management - Keeping n8n packages in sync
Claude's Interview - Real-world impact of n8n-MCP
Project Information
Change Log - Complete version history
Claude Instructions - AI guidance for this codebase
MCP Tools Reference - Complete list of available tools
📊 Metrics & Coverage
Current database coverage (n8n v1.117.2):

✅ 541/541 nodes loaded (100%)
✅ 541 nodes with properties (100%)
✅ 470 nodes with documentation (87%)
✅ 271 AI-capable tools detected
✅ 2,646 pre-extracted template configurations
✅ 2,709 workflow templates available (100% metadata coverage)
✅ AI Agent & LangChain nodes fully documented
⚡ Average response time: ~12ms
💾 Database size: ~68MB (includes templates with metadata)
🔄 Recent Updates
See CHANGELOG.md for full version history and recent changes.

⚠️ Known Issues
Claude Desktop Container Management
Container Accumulation (Fixed in v2.7.20+)
Previous versions had an issue where containers would not properly clean up when Claude Desktop sessions ended. This has been fixed in v2.7.20+ with proper signal handling.

For best container lifecycle management:

Use the --init flag (recommended) - Docker's init system ensures proper signal handling:
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", "--init",
        "ghcr.io/czlonkowski/n8n-mcp:latest"
      ]
    }
  }
}
Ensure you're using v2.7.20 or later - Check your version:
docker run --rm ghcr.io/czlonkowski/n8n-mcp:latest --version
🧪 Testing
The project includes a comprehensive test suite with 2,883 tests ensuring code quality and reliability:

# Run all tests
npm test

# Run tests with coverage report
npm run test:coverage

# Run tests in watch mode
npm run test:watch

# Run specific test suites
npm run test:unit           # 933 unit tests
npm run test:integration    # 249 integration tests
npm run test:bench          # Performance benchmarks
Test Suite Overview
Total Tests: 2,883 (100% passing)
Unit Tests: 2,526 tests across 99 files
Integration Tests: 357 tests across 20 files
Execution Time: ~2.5 minutes in CI
Test Framework: Vitest (for speed and TypeScript support)
Mocking: MSW for API mocking, custom mocks for databases
Coverage & Quality
Coverage Reports: Generated in ./coverage directory
CI/CD: Automated testing on all PRs with GitHub Actions
Performance: Environment-aware thresholds for CI vs local
Parallel Execution: Configurable thread pool for faster runs
Testing Architecture
Total: 3,336 tests across unit and integration test suites

Unit Tests (2,766 tests): Isolated component testing with mocks

Services layer: Enhanced validation, property filtering, workflow validation
Parsers: Node parsing, property extraction, documentation mapping
Database: Repositories, adapters, migrations, FTS5 search
MCP tools: Tool definitions, documentation system
HTTP server: Multi-tenant support, security, configuration
Integration Tests (570 tests): Full system behavior validation

n8n API Integration (172 tests): All 18 MCP handler tools tested against real n8n instance
Workflow management: Create, read, update, delete, list, validate, autofix
Execution management: Trigger, retrieve, list, delete
System tools: Health check, tool listing, diagnostics
MCP Protocol (119 tests): Protocol compliance, session management, error handling
Database (226 tests): Repository operations, transactions, performance, FTS5 search
Templates (35 tests): Template fetching, storage, metadata operations
Docker (18 tests): Configuration, entrypoint, security validation
For detailed testing documentation, see Testing Architecture.

📦 License
MIT License - see LICENSE for details.

Attribution appreciated! If you use n8n-MCP, consider:

⭐ Starring this repository
💬 Mentioning it in your project
🔗 Linking back to this repo
🤝 Contributing
Contributions are welcome! Please:

Fork the repository
Create a feature branch
Run tests (npm test)
Submit a pull request
🚀 For Maintainers: Automated Releases
This project uses automated releases triggered by version changes:

# Guided release preparation
npm run prepare:release

# Test release automation
npm run test:release-automation
The system automatically handles:

🏷️ GitHub releases with changelog content
📦 NPM package publishing
🐳 Multi-platform Docker images
📚 Documentation updates
See Automated Release Guide for complete details.

👏 Acknowledgments
n8n team for the workflow automation platform
Anthropic for the Model Context Protocol
All contributors and users of this project
Template Attribution
All workflow templates in this project are fetched from n8n's public template gallery at n8n.io/workflows. Each template includes:

Full attribution to the original creator (name and username)
Direct link to the source template on n8n.io
Original workflow ID for reference
The AI agent instructions in this project contain mandatory attribution requirements. When using any template, the AI will automatically:

Share the template author's name and username
Provide a direct link to the original template on n8n.io
Display attribution in the format: "This workflow is based on a template by [author] (@[username]). View the original at: [url]"
Template creators retain all rights to their workflows. This project indexes templates to improve discoverability through AI assistants. If you're a template creator and have concerns about your template being indexed, please open an issue.

Special thanks to the prolific template contributors whose work helps thousands of users automate their workflows, including: David Ashby (@cfomodz), Yaron Been (@yaron-nofluff), Jimleuk (@jimleuk), Davide (@n3witalia), David Olusola (@dae221), Ranjan Dailata (@ranjancse), Airtop (@cesar-at-airtop), Joseph LePage (@joe), Don Jayamaha Jr (@don-the-gem-dealer), Angel Menendez (@djangelic), and the entire n8n community of creators!

Built with ❤️ for the n8n community
Making AI + n8n workflow creation delightful
Readme
Keywords
n8nmcpmodel-context-protocolaiworkflowautomation
Package Sidebar
Install
npm i n8n-mcp


Repository
github.com/czlonkowski/n8n-mcp

Homepage
github.com/czlonkowski/n8n-mcp#readme