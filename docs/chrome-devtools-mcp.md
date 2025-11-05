chrome-devtools-mcp
0.9.0 • Public • Published 14 days ago
Chrome DevTools MCP
npm chrome-devtools-mcp package

chrome-devtools-mcp lets your coding agent (such as Gemini, Claude, Cursor or Copilot) control and inspect a live Chrome browser. It acts as a Model-Context-Protocol (MCP) server, giving your AI coding assistant access to the full power of Chrome DevTools for reliable automation, in-depth debugging, and performance analysis.

Tool reference | Changelog | Contributing | Troubleshooting
Key features
Get performance insights: Uses Chrome DevTools to record traces and extract actionable performance insights.
Advanced browser debugging: Analyze network requests, take screenshots and check the browser console.
Reliable automation. Uses puppeteer to automate actions in Chrome and automatically wait for action results.
Disclaimers
chrome-devtools-mcp exposes content of the browser instance to the MCP clients allowing them to inspect, debug, and modify any data in the browser or DevTools. Avoid sharing sensitive or personal information that you don't want to share with MCP clients.

Requirements
Node.js v20.19 or a newer latest maintenance LTS version.
Chrome current stable version or newer.
npm.
Getting started
Add the following config to your MCP client:

{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
[!NOTE]
Using chrome-devtools-mcp@latest ensures that your MCP client will always use the latest version of the Chrome DevTools MCP server.

MCP Client configuration
Amp
Claude Code
Cline
Codex
Copilot CLI
Copilot / VS Code
Cursor
Gemini CLI
Gemini Code Assist
JetBrains AI Assistant & Junie
Kiro
Qoder
Visual Studio
Warp
Your first prompt
Enter the following prompt in your MCP Client to check if everything is working:

Check the performance of https://developers.chrome.com
Your MCP client should open the browser and record a performance trace.

[!NOTE]
The MCP server will start the browser automatically once the MCP client uses a tool that requires a running browser instance. Connecting to the Chrome DevTools MCP server on its own will not automatically start the browser.

Tools
If you run into any issues, checkout our troubleshooting guide.

Input automation (7 tools)
click
drag
fill
fill_form
handle_dialog
hover
upload_file
Navigation automation (7 tools)
close_page
list_pages
navigate_page
navigate_page_history
new_page
select_page
wait_for
Emulation (3 tools)
emulate_cpu
emulate_network
resize_page
Performance (3 tools)
performance_analyze_insight
performance_start_trace
performance_stop_trace
Network (2 tools)
get_network_request
list_network_requests
Debugging (5 tools)
evaluate_script
get_console_message
list_console_messages
take_screenshot
take_snapshot
Configuration
The Chrome DevTools MCP server supports the following configuration option:

--browserUrl, -u Connect to a running Chrome instance using port forwarding. For more details see: https://developer.chrome.com/docs/devtools/remote-debugging/local-server.

Type: string
--wsEndpoint, -w WebSocket endpoint to connect to a running Chrome instance (e.g., ws://127.0.0.1:9222/devtools/browser/). Alternative to --browserUrl.

Type: string
--wsHeaders Custom headers for WebSocket connection in JSON format (e.g., '{"Authorization":"Bearer token"}'). Only works with --wsEndpoint.

Type: string
--headless Whether to run in headless (no UI) mode.

Type: boolean
Default: false
--executablePath, -e Path to custom Chrome executable.

Type: string
--isolated If specified, creates a temporary user-data-dir that is automatically cleaned up after the browser is closed.

Type: boolean
Default: false
--channel Specify a different Chrome channel that should be used. The default is the stable channel version.

Type: string
Choices: stable, canary, beta, dev
--logFile Path to a file to write debug logs to. Set the env variable DEBUG to * to enable verbose logs. Useful for submitting bug reports.

Type: string
--viewport Initial viewport size for the Chrome instances started by the server. For example, 1280x720. In headless mode, max size is 3840x2160px.

Type: string
--proxyServer Proxy server configuration for Chrome passed as --proxy-server when launching the browser. See https://www.chromium.org/developers/design-documents/network-settings/ for details.

Type: string
--acceptInsecureCerts If enabled, ignores errors relative to self-signed and expired certificates. Use with caution.

Type: boolean
--chromeArg Additional arguments for Chrome. Only applies when Chrome is launched by chrome-devtools-mcp.

Type: array
--categoryEmulation Set to false to exlcude tools related to emulation.

Type: boolean
Default: true
--categoryPerformance Set to false to exlcude tools related to performance.

Type: boolean
Default: true
--categoryNetwork Set to false to exlcude tools related to network.

Type: boolean
Default: true
Pass them via the args property in the JSON configuration. For example:

{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--channel=canary",
        "--headless=true",
        "--isolated=true"
      ]
    }
  }
}
Connecting via WebSocket with custom headers
You can connect directly to a Chrome WebSocket endpoint and include custom headers (e.g., for authentication):

{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--wsEndpoint=ws://127.0.0.1:9222/devtools/browser/<id>",
        "--wsHeaders={\"Authorization\":\"Bearer YOUR_TOKEN\"}"
      ]
    }
  }
}
To get the WebSocket endpoint from a running Chrome instance, visit http://127.0.0.1:9222/json/version and look for the webSocketDebuggerUrl field.

You can also run npx chrome-devtools-mcp@latest --help to see all available configuration options.

Concepts
User data directory
chrome-devtools-mcp starts a Chrome's stable channel instance using the following user data directory:

Linux / macOS: $HOME/.cache/chrome-devtools-mcp/chrome-profile-$CHANNEL
Windows: %HOMEPATH%/.cache/chrome-devtools-mcp/chrome-profile-$CHANNEL
The user data directory is not cleared between runs and shared across all instances of chrome-devtools-mcp. Set the isolated option to true to use a temporary user data dir instead which will be cleared automatically after the browser is closed.

Connecting to a running Chrome instance
You can connect to a running Chrome instance by using the --browser-url option. This is useful if you want to use your existing Chrome profile or if you are running the MCP server in a sandboxed environment that does not allow starting a new Chrome instance.

Here is a step-by-step guide on how to connect to a running Chrome Stable instance:

Step 1: Configure the MCP client

Add the --browser-url option to your MCP client configuration. The value of this option should be the URL of the running Chrome instance. http://127.0.0.1:9222 is a common default.

{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--browser-url=http://127.0.0.1:9222"
      ]
    }
  }
}
Step 2: Start the Chrome browser

[!WARNING]
Enabling the remote debugging port opens up a debugging port on the running browser instance. Any application on your machine can connect to this port and control the browser. Make sure that you are not browsing any sensitive websites while the debugging port is open.

Start the Chrome browser with the remote debugging port enabled. Make sure to close any running Chrome instances before starting a new one with the debugging port enabled. The port number you choose must be the same as the one you specified in the --browser-url option in your MCP client configuration.

For security reasons, Chrome requires you to use a non-default user data directory when enabling the remote debugging port. You can specify a custom directory using the --user-data-dir flag. This ensures that your regular browsing profile and data are not exposed to the debugging session.

macOS

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile-stable
Linux

/usr/bin/google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile-stable
Windows

"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%TEMP%\chrome-profile-stable"
Step 3: Test your setup

After configuring the MCP client and starting the Chrome browser, you can test your setup by running a simple prompt in your MCP client:

Check the performance of https://developers.chrome.com
Your MCP client should connect to the running Chrome instance and receive a performance report.

If you hit VM-to-host port forwarding issues, see the “Remote debugging between virtual machine (VM) and host fails” section in docs/troubleshooting.md.

For more details on remote debugging, see the Chrome DevTools documentation.

Known limitations
Operating system sandboxes
Some MCP clients allow sandboxing the MCP server using macOS Seatbelt or Linux containers. If sandboxes are enabled, chrome-devtools-mcp is not able to start Chrome that requires permissions to create its own sandboxes. As a workaround, either disable sandboxing for chrome-devtools-mcp in your MCP client or use --browser-url to connect to a Chrome instance that you start manually outside of the MCP client sandbox.

Readme
Keywords
none
Provenance
Built and signed on
GitHub Actions
View build summary
Source Commit

github.com/ChromeDevTools/chrome-devtools-mcp@2553006
Build File

.github/workflows/publish-to-npm-on-tag.yml
Public Ledger

Transparency log entry
Share feedback
Package Sidebar
Install
npm i chrome-devtools-mcp


Repository
github.com/ChromeDevTools/chrome-devtools-mcp

Homepage
github.com/ChromeDevTools/chrome-devtools-mcp#readme