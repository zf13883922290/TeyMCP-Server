slack-mcp-server
A MCP(Model Context Protocol) server for accessing Slack API. This server allows AI assistants to interact with the Slack API through a standardized interface.

Transport Support
This server supports both traditional and modern MCP transport methods:

Stdio Transport (default): Process-based communication for local integration
Streamable HTTP Transport: HTTP-based communication for web applications and remote clients
Features
Available tools:

slack_list_channels - List all conversations in the workspace (channels, DMs, group DMs)
slack_list_conversations - List conversations with flexible type filtering (public_channel, private_channel, mpim, im)
slack_post_message - Post a message to any Slack conversation as the authenticated user
slack_reply_to_thread - Reply to a message thread in any Slack conversation as the authenticated user
slack_get_channel_history - Get recent messages from any conversation you have access to
slack_get_thread_replies - Get all replies in a message thread from any conversation
slack_get_users - Retrieve basic profile information of all users in the workspace
slack_get_user_profile - Get a user's profile information
slack_get_user_profiles - Get multiple users' profile information in bulk (efficient for batch operations)
slack_search_messages - Search for messages in the workspace
Important Notes
User Authentication: All operations (reading and writing) use the user token, providing full access to conversations you can see.
DM Support: You can send and read DMs to/from any user without restrictions.
No Channel Membership Required: Since we use the user token, you can read messages from any channel you have access to.
Messages Appear From You: All posted messages and replies appear as coming from your user account.
Bot Token: Currently required by configuration but not actively used for any operations.
Quick Start
Installation
npm install -g markov-slack-mcp
Or use with npx (no installation required):

npx markov-slack-mcp
Configuration
You need to set the following environment variables:

SLACK_BOT_TOKEN: Slack Bot User OAuth Token
SLACK_USER_TOKEN: Slack User OAuth Token (required for some features like message search)
You can also create a .env file to set these environment variables:

SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_USER_TOKEN=xoxp-your-user-token
Usage
Start the MCP server
Stdio Transport (default):

npx markov-slack-mcp
Streamable HTTP Transport:

npx markov-slack-mcp -port 3000
You can also run the installed module with node:

# Stdio transport
slack-mcp-server

# HTTP transport  
slack-mcp-server -port 3000
Command Line Options:

-port <number>: Start with Streamable HTTP transport on specified port
-h, --help: Show help message
Client Configuration
For Claude Desktop (using Claude Code CLI):

claude mcp add slack -s local \
  -e SLACK_BOT_TOKEN=<your-bot-token> \
  -e SLACK_USER_TOKEN=<your-user-token> \
  -- npx -y markov-slack-mcp slack-mcp-server
For Manual MCP Configuration (Claude Desktop, etc.):

{
  "slack": {
    "command": "npx",
    "args": [
      "-y",
      "markov-slack-mcp",
      "slack-mcp-server"
    ],
    "env": {
      "SLACK_BOT_TOKEN": "<your-bot-token>",
      "SLACK_USER_TOKEN": "<your-user-token>"
    }
  }
}
For Streamable HTTP Transport (Web applications):

Start the server:

SLACK_BOT_TOKEN=<your-bot-token> SLACK_USER_TOKEN=<your-user-token> npx markov-slack-mcp -port 3000
Connect to: http://localhost:3000/mcp

See examples/README.md for detailed client examples.

Implementation Pattern
This server adopts the following implementation pattern:

Define request/response using Zod schemas

Request schema: Define input parameters
Response schema: Define responses limited to necessary fields
Implementation flow:

Validate request with Zod schema
Call Slack WebAPI
Parse response with Zod schema to limit to necessary fields
Return as JSON
For example, the slack_list_channels implementation parses the request with ListChannelsRequestSchema, calls slackClient.conversations.list, and returns the response parsed with ListChannelsResponseSchema.

Development
Available Scripts
npm run dev - Start the server in development mode with hot reloading
npm run build - Build the project for production
npm run start - Start the production server
npm run lint - Run linting checks (ESLint and Prettier)
npm run fix - Automatically fix linting issues
Contributing
Fork the repository
Create your feature branch
Run tests and linting: npm run lint
Commit your changes
Push to the branch
Create a Pull Request
Readme
Keywords
mcpslack
Package Sidebar
Install
npm i markov-slack-mcp


Repository
github.com/ubie-oss/slack-mcp-server

Homepage
github.com/ubie-oss/slack-mcp-server