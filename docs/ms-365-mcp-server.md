ms-365-mcp-server
npm version build status license

Microsoft 365 MCP Server

A Model Context Protocol (MCP) server for interacting with Microsoft 365 and Microsoft Office services through the Graph API.

Prerequisites
Node.js >= 20 (recommended)
Node.js 14+ may work with dependency warnings
Features
Authentication via Microsoft Authentication Library (MSAL)
Comprehensive Microsoft 365 service integration
Read-only mode support for safe operations
Tool filtering for granular access control
Supported Services & Tools
Personal Account Tools (Available by default)
Email (Outlook)
list-mail-messages, list-mail-folders, list-mail-folder-messages, get-mail-message, send-mail, delete-mail-message, create-draft-email, move-mail-message

Calendar
list-calendars, list-calendar-events, get-calendar-event, get-calendar-view, create-calendar-event, update-calendar-event, delete-calendar-event

OneDrive Files
list-drives, get-drive-root-item, list-folder-files, download-onedrive-file-content, upload-file-content, upload-new-file, delete-onedrive-file

Excel Operations
list-excel-worksheets, get-excel-range, create-excel-chart, format-excel-range, sort-excel-range

OneNote
list-onenote-notebooks, list-onenote-notebook-sections, list-onenote-section-pages, get-onenote-page-content, create-onenote-page

To Do Tasks
list-todo-task-lists, list-todo-tasks, get-todo-task, create-todo-task, update-todo-task, delete-todo-task

Planner
list-planner-tasks, get-planner-plan, list-plan-tasks, get-planner-task, create-planner-task

Contacts
list-outlook-contacts, get-outlook-contact, create-outlook-contact, update-outlook-contact, delete-outlook-contact

User Profile
get-current-user

Search
search-query

Organization Account Tools (Requires --org-mode flag)
Teams & Chats
list-chats, get-chat, list-chat-messages, get-chat-message, send-chat-message, list-chat-message-replies, reply-to-chat-message, list-joined-teams, get-team, list-team-channels, get-team-channel, list-channel-messages, get-channel-message, send-channel-message, list-team-members

SharePoint Sites
search-sharepoint-sites, get-sharepoint-site, get-sharepoint-site-by-path, list-sharepoint-site-drives, get-sharepoint-site-drive-by-id, list-sharepoint-site-items, get-sharepoint-site-item, list-sharepoint-site-lists, get-sharepoint-site-list, list-sharepoint-site-list-items, get-sharepoint-site-list-item, get-sharepoint-sites-delta

Shared Mailboxes
list-shared-mailbox-messages, list-shared-mailbox-folder-messages, get-shared-mailbox-message, send-shared-mailbox-mail

User Management
list-users

Organization/Work Mode
To access work/school features (Teams, SharePoint, etc.), enable organization mode using any of these flags:

{
  "mcpServers": {
    "ms365": {
      "command": "npx",
      "args": ["-y", "@softeria/ms-365-mcp-server", "--org-mode"]
    }
  }
}
Organization mode must be enabled from the start to access work account features. Without this flag, only personal account features (email, calendar, OneDrive, etc.) are available.

Shared Mailbox Access
To access shared mailboxes, you need:

Organization mode: Shared mailbox tools require --org-mode flag (work/school accounts only)
Delegated permissions: Mail.Read.Shared or Mail.Send.Shared scopes
Exchange permissions: The signed-in user must have been granted access to the shared mailbox
Usage: Use the shared mailbox's email address as the user-id parameter in the shared mailbox tools
Finding shared mailboxes: Use the list-users tool to discover available users and shared mailboxes in your organization.

Example: list-shared-mailbox-messages with user-id set to shared-mailbox@company.com

Quick Start Example
Test login in Claude Desktop:

Login example

Examples
Image

Integration
Claude Desktop
To add this MCP server to Claude Desktop:

Edit the config file under Settings > Developer:

{
  "mcpServers": {
    "ms365": {
      "command": "npx",
      "args": ["-y", "@softeria/ms-365-mcp-server"]
    }
  }
}
Claude Code CLI
claude mcp add ms365 -- npx -y @softeria/ms-365-mcp-server
For other interfaces that support MCPs, please refer to their respective documentation for the correct integration method.

Local Development
For local development or testing:

# From the project directory
claude mcp add ms -- npx tsx src/index.ts --org-mode
Or configure Claude Desktop manually:

{
  "mcpServers": {
    "ms365": {
      "command": "node",
      "args": ["/absolute/path/to/ms-365-mcp-server/dist/index.js", "--org-mode"]
    }
  }
}
Note: Run npm run build after code changes to update the dist/ folder.

Authentication
⚠️ You must authenticate before using tools.

The server supports three authentication methods:

1. Device Code Flow (Default)
For interactive authentication via device code:

MCP client login:
Call the login tool (auto-checks existing token)
If needed, get URL+code, visit in browser
Use verify-login tool to confirm
CLI login:
npx @softeria/ms-365-mcp-server --login
Follow the URL and code prompt in the terminal.
Tokens are cached securely in your OS credential store (fallback to file).

2. OAuth Authorization Code Flow (HTTP mode only)
When running with --http, the server requires OAuth authentication:

npx @softeria/ms-365-mcp-server --http 3000
This mode:

Advertises OAuth capabilities to MCP clients
Provides OAuth endpoints at /auth/* (authorize, token, metadata)
Requires Authorization: Bearer <token> for all MCP requests
Validates tokens with Microsoft Graph API
Disables login/logout tools by default (use --enable-auth-tools to enable them)
MCP clients will automatically handle the OAuth flow when they see the advertised capabilities.

Setting up Azure AD for OAuth Testing
To use OAuth mode with custom Azure credentials (recommended for production), you'll need to set up an Azure AD app registration:

Create Azure AD App Registration:
Go to Azure Portal
Navigate to Azure Active Directory → App registrations → New registration
Set name: "MS365 MCP Server"
Configure Redirect URIs: Add these redirect URIs for testing with MCP Inspector (npm run inspector):
http://localhost:6274/oauth/callback
http://localhost:6274/oauth/callback/debug
http://localhost:3000/callback (optional, for server callback)
Get Credentials:
Copy the Application (client) ID from Overview page
Go to Certificates & secrets → New client secret → Copy the secret value
Configure Environment Variables: Create a .env file in your project root:
MS365_MCP_CLIENT_ID=your-azure-ad-app-client-id-here
MS365_MCP_CLIENT_SECRET=your-azure-ad-app-client-secret-here
MS365_MCP_TENANT_ID=common
With these configured, the server will use your custom Azure app instead of the built-in one.

3. Bring Your Own Token (BYOT)
If you are running ms-365-mcp-server as part of a larger system that manages Microsoft OAuth tokens externally, you can provide an access token directly to this MCP server:

MS365_MCP_OAUTH_TOKEN=your_oauth_token npx @softeria/ms-365-mcp-server
This method:

Bypasses the interactive authentication flows
Use your pre-existing OAuth token for Microsoft Graph API requests
Does not handle token refresh (token lifecycle management is your responsibility)
Note: HTTP mode requires authentication. For unauthenticated testing, use stdio mode with device code flow.

Authentication Tools: In HTTP mode, login/logout tools are disabled by default since OAuth handles authentication. Use --enable-auth-tools if you need them available.

CLI Options
The following options can be used when running ms-365-mcp-server directly from the command line:

--login           Login using device code flow
--logout          Log out and clear saved credentials
--verify-login    Verify login without starting the server
--org-mode        Enable organization/work mode from start (includes Teams, SharePoint, etc.)
--work-mode       Alias for --org-mode
--force-work-scopes Backwards compatibility alias for --org-mode (deprecated)
Server Options
When running as an MCP server, the following options can be used:

-v                Enable verbose logging
--read-only       Start server in read-only mode, disabling write operations
--http [port]     Use Streamable HTTP transport instead of stdio (optionally specify port, default: 3000)
                  Starts Express.js server with MCP endpoint at /mcp
--enable-auth-tools Enable login/logout tools when using HTTP mode (disabled by default in HTTP mode)
--enabled-tools <pattern> Filter tools using regex pattern (e.g., "excel|contact" to enable Excel and Contact tools)
Environment variables:

READ_ONLY=true|1: Alternative to --read-only flag
ENABLED_TOOLS: Filter tools using a regex pattern (alternative to --enabled-tools flag)
MS365_MCP_ORG_MODE=true|1: Enable organization/work mode (alternative to --org-mode flag)
MS365_MCP_FORCE_WORK_SCOPES=true|1: Backwards compatibility for MS365_MCP_ORG_MODE
LOG_LEVEL: Set logging level (default: 'info')
SILENT=true|1: Disable console output
MS365_MCP_CLIENT_ID: Custom Azure app client ID (defaults to built-in app)
MS365_MCP_TENANT_ID: Custom tenant ID (defaults to 'common' for multi-tenant)
MS365_MCP_OAUTH_TOKEN: Pre-existing OAuth token for Microsoft Graph API (BYOT method)
Contributing
We welcome contributions! Before submitting a pull request, please ensure your changes meet our quality standards.

Run the verification script to check all code quality requirements:

npm run verify
For Developers
After cloning the repository, you may need to generate the client code from the Microsoft Graph OpenAPI specification:

npm run generate
Support
If you're having problems or need help:

Create an issue
Start a discussion
Email: eirikb@eirikb.no
Discord: https://discord.gg/WvGVNScrAZ or @eirikb
License
MIT © 2025 Softeria

Readme
Keywords
microsoft365mcpserver
Package Sidebar
Install
npm i @softeria/ms-365-mcp-server


Repository
github.com/softeria/ms-365-mcp-server

Homepage
github.com/softeria/ms-365-mcp-server#readme