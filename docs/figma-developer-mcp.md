figma-developer-mcp
TypeScript icon, indicating that this package has built-in type declarations
0.6.4 • Public • Published a month ago
Framelink
Framelink Figma MCP Server
🌐 Available in: 한국어 (Korean) | 日本語 (Japanese) | 简体中文 (Simplified Chinese) | 繁體中文 (Traditional Chinese)

Give your coding agent access to your Figma data.
Implement designs in any framework in one-shot.
weekly downloads MIT License Discord
Twitter

Give Cursor and other AI-powered coding tools access to your Figma files with this Model Context Protocol server.

When Cursor has access to Figma design data, it's way better at one-shotting designs accurately than alternative approaches like pasting screenshots.

See quickstart instructions →
Demo
Watch a demo of building a UI in Cursor with Figma design data

Watch the video

How it works
Open your IDE's chat (e.g. agent mode in Cursor).
Paste a link to a Figma file, frame, or group.
Ask Cursor to do something with the Figma file—e.g. implement the design.
Cursor will fetch the relevant metadata from Figma and use it to write your code.
This MCP server is specifically designed for use with Cursor. Before responding with context from the Figma API, it simplifies and translates the response so only the most relevant layout and styling information is provided to the model.

Reducing the amount of context provided to the model helps make the AI more accurate and the responses more relevant.

Getting Started
Many code editors and other AI clients use a configuration file to manage MCP servers.

The figma-developer-mcp server can be configured by adding the following to your configuration file.

NOTE: You will need to create a Figma access token to use this server. Instructions on how to create a Figma API access token can be found here.

MacOS / Linux
{
  "mcpServers": {
    "Framelink Figma MCP": {
      "command": "npx",
      "args": ["-y", "figma-developer-mcp", "--figma-api-key=YOUR-KEY", "--stdio"]
    }
  }
}
Windows
{
  "mcpServers": {
    "Framelink Figma MCP": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "figma-developer-mcp", "--figma-api-key=YOUR-KEY", "--stdio"]
    }
  }
}
Or you can set FIGMA_API_KEY and PORT in the env field.

If you need more information on how to configure the Framelink Figma MCP server, see the Framelink docs.

Star History
Star History Chart

Learn More
The Framelink Figma MCP server is simple but powerful. Get the most out of it by learning more at the Framelink site.

Readme
Keywords
figmamcptypescript
Package Sidebar
Install
npm i figma-developer-mcp


Repository
github.com/GLips/Figma-Context-MCP

Homepage
www.framelink.ai