Slack MCP Server
A Model Context Protocol (MCP) server for Slack integration that provides tools for interacting with Slack workspaces.

Features
Channel Management: List channels and get channel information
Messaging: Post messages and reply to threads
Reactions: Add emoji reactions to messages
History: Retrieve channel message history and thread replies
User Management: Get user lists and profile information
Installation
npm install -g @serverkit-project/slack-mcp-server
Usage
Environment Variables
Before using the server, you need to set up the following environment variables:

export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export SLACK_TEAM_ID="your-team-id"
export SLACK_CHANNEL_IDS="channel1,channel2,channel3"  # Optional: predefined channels
Running the Server
slack-mcp-server
The server runs on stdio and communicates using the Model Context Protocol.

Available Tools
slack_list_channels - List public channels in the workspace
slack_post_message - Post a new message to a channel
slack_reply_to_thread - Reply to a specific message thread
slack_add_reaction - Add emoji reactions to messages
slack_get_channel_history - Get recent messages from a channel
slack_get_thread_replies - Get all replies in a message thread
slack_get_users - Get list of workspace users
slack_get_user_profile - Get detailed user profile information
Setup Instructions
1. Create a Slack App
Go to Slack API
Click "Create New App" → "From scratch"
Choose your workspace and app name
2. Configure Bot Permissions
Add the following OAuth scopes to your bot:

channels:read - View basic information about public channels
chat:write - Send messages as the app
reactions:write - Add and edit emoji reactions
users:read - View people in the workspace
users:read.email - View email addresses of people in the workspace
3. Install App to Workspace
Install the app to your workspace
Copy the "Bot User OAuth Token" (starts with xoxb-)
Get your Team ID from your workspace settings
Development
# Clone the repository
git clone https://github.com/Serverkit-Project/slack-mcp-server.git
cd slack-mcp-server

# Install dependencies
npm install

# Build the project
npm run build

# Run in development mode
npm run dev
License
MIT

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Readme
Keywords
slackmcpmodel-context-protocolaichatintegration
Package Sidebar
Install
npm i slack-mcp-server-kit


Repository
github.com/Serverkit-Project/slack-mcp-server

Homepage
github.com/Serverkit-Project/slack-mcp-server