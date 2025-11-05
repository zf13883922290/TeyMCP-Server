slack-mcp
1.0.2 • Public • Published a month ago
Slack MCP Server
Integrate the Slack Web API into agentic workflows via MCP. Inspired by the structure of the Productboard MCP server. See the reference README for layout and usage style: tg-productboard-mcp README.

Tools
search_messages
get_message_thread
Setup
Access Token
Create a Slack app and obtain a User OAuth Token (starts with xoxp-). Ensure the authorized user is a member of the channels you want to search.

Required environment variables (can be set in your shell or a .env file):

SLACK_AUTH_USER_TOKEN (starts with xoxp-)
SLACK_SEARCH_CHANNELS (comma-separated channel names without '#' with no leading or trailing spaces)
Example .env:

SLACK_AUTH_USER_TOKEN=xoxp-...
SLACK_SEARCH_CHANNELS=general,random
Slack Scopes
Grant the following user token scopes to your Slack app (choose public and/or private based on your needs):

search:read
channels:history (public) and/or groups:history (private) (read messages and other content in a user’s public channels)
channels:read / groups:read (view basic information about public channels in a workspace)
channels:history (read messages and other content in a user’s public channels)
links:read (view URLs in messages)
search:read (search a workspace’s content)
search:read.private (search a workspace's content in private channels)
search:read.public (search a workspace's content in public channels)
search:read.users (search a workspace's users)
users.profile:read (view a user’s profile information)
Usage with Claude Desktop
To use this with Claude Desktop, add the following to your claude_desktop_config.json:

{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": [
        "-y",
        "@tomgutt/slack-mcp"
      ],
      "env": {
        "SLACK_AUTH_USER_TOKEN": "xoxp-...",
        "SLACK_SEARCH_CHANNELS": "general,random"
      }
    }
  }
}
NPX
If published, you can run it directly via NPX (example shown in the Claude configuration above).

Run locally
Build:

npm run build
Use the mcp inspector:

npm run inspector
Test a tool without inspector
./run-test.sh
Tool Inputs
search_messages: { query: string, messageCount?: number, includeThreads?: boolean, threadCount?: number, sortMessages?: "mostRelevant" | "latest" | "oldest" }
get_message_thread: { channelId: string, ts: string, threadCount?: number }
All tools restrict results to SLACK_SEARCH_CHANNELS. sortMessages is only used for search_messages.

Changes to original
Implements Slack message search with optional thread inclusion and paging
Adds lightweight response shaping to reduce token usage
Provides a channel allow-list via SLACK_SEARCH_CHANNELS
License
This MCP server is licensed under the MIT License. See LICENSE for details.

Readme
Keywords
mcpagentautonomousaislack
Package Sidebar
Install
npm i slack-mcp


Repository
github.com/tomgutt/slack-mcp

Homepage
github.com/tomgutt/slack-mcp#readme