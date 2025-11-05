Playwright MCP
A Model Context Protocol (MCP) server that provides browser automation capabilities using Playwright. This server enables LLMs to interact with web pages through structured accessibility snapshots, bypassing the need for screenshots or visually-tuned models.

Key Features
Fast and lightweight. Uses Playwright's accessibility tree, not pixel-based input.
LLM-friendly. No vision models needed, operates purely on structured data.
Deterministic tool application. Avoids ambiguity common with screenshot-based approaches.
Requirements
Node.js 18 or newer
VS Code, Cursor, Windsurf, Claude Desktop, Goose or any other MCP client
Getting started
First, install the Playwright MCP server with your client.

Standard config works in most of the tools:

{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest"
      ]
    }
  }
}
Install in VS Code Install in VS Code Insiders

Amp
Claude Code
Claude Desktop
Codex
Cursor
Factory
Gemini CLI
Goose
Kiro
LM Studio
opencode
Qodo Gen
VS Code
Warp
Windsurf
Configuration
Playwright MCP server supports following arguments. They can be provided in the JSON configuration above, as a part of the "args" list:

> npx @playwright/mcp@latest --help
  --allowed-hosts <hosts...>            comma-separated list of hosts this
                                        server is allowed to serve from.
                                        Defaults to the host the server is bound
                                        to. Pass '*' to disable the host check.
  --allowed-origins <origins>           semicolon-separated list of origins to
                                        allow the browser to request. Default is
                                        to allow all.
  --blocked-origins <origins>           semicolon-separated list of origins to
                                        block the browser from requesting.
                                        Blocklist is evaluated before allowlist.
                                        If used without the allowlist, requests
                                        not matching the blocklist are still
                                        allowed.
  --block-service-workers               block service workers
  --browser <browser>                   browser or chrome channel to use,
                                        possible values: chrome, firefox,
                                        webkit, msedge.
  --caps <caps>                         comma-separated list of additional
                                        capabilities to enable, possible values:
                                        vision, pdf.
  --cdp-endpoint <endpoint>             CDP endpoint to connect to.
  --cdp-header <headers...>             CDP headers to send with the connect
                                        request, multiple can be specified.
  --config <path>                       path to the configuration file.
  --device <device>                     device to emulate, for example: "iPhone
                                        15"
  --executable-path <path>              path to the browser executable.
  --extension                           Connect to a running browser instance
                                        (Edge/Chrome only). Requires the
                                        "Playwright MCP Bridge" browser
                                        extension to be installed.
  --grant-permissions <permissions...>  List of permissions to grant to the
                                        browser context, for example
                                        "geolocation", "clipboard-read",
                                        "clipboard-write".
  --headless                            run browser in headless mode, headed by
                                        default
  --host <host>                         host to bind server to. Default is
                                        localhost. Use 0.0.0.0 to bind to all
                                        interfaces.
  --ignore-https-errors                 ignore https errors
  --init-script <path...>               path to JavaScript file to add as an
                                        initialization script. The script will
                                        be evaluated in every page before any of
                                        the page's scripts. Can be specified
                                        multiple times.
  --isolated                            keep the browser profile in memory, do
                                        not save it to disk.
  --image-responses <mode>              whether to send image responses to the
                                        client. Can be "allow" or "omit",
                                        Defaults to "allow".
  --no-sandbox                          disable the sandbox for all process
                                        types that are normally sandboxed.
  --output-dir <path>                   path to the directory for output files.
  --port <port>                         port to listen on for SSE transport.
  --proxy-bypass <bypass>               comma-separated domains to bypass proxy,
                                        for example
                                        ".com,chromium.org,.domain.com"
  --proxy-server <proxy>                specify proxy server, for example
                                        "http://myproxy:3128" or
                                        "socks5://myproxy:8080"
  --save-session                        Whether to save the Playwright MCP
                                        session into the output directory.
  --save-trace                          Whether to save the Playwright Trace of
                                        the session into the output directory.
  --save-video <size>                   Whether to save the video of the session
                                        into the output directory. For example
                                        "--save-video=800x600"
  --secrets <path>                      path to a file containing secrets in the
                                        dotenv format
  --shared-browser-context              reuse the same browser context between
                                        all connected HTTP clients.
  --storage-state <path>                path to the storage state file for
                                        isolated sessions.
  --test-id-attribute <attribute>       specify the attribute to use for test
                                        ids, defaults to "data-testid"
  --timeout-action <timeout>            specify action timeout in milliseconds,
                                        defaults to 5000ms
  --timeout-navigation <timeout>        specify navigation timeout in
                                        milliseconds, defaults to 60000ms
  --user-agent <ua string>              specify user agent string
  --user-data-dir <path>                path to the user data directory. If not
                                        specified, a temporary directory will be
                                        created.
  --viewport-size <size>                specify browser viewport size in pixels,
                                        for example "1280x720"
User profile
You can run Playwright MCP with persistent profile like a regular browser (default), in isolated contexts for testing sessions, or connect to your existing browser using the browser extension.

Persistent profile

All the logged in information will be stored in the persistent profile, you can delete it between sessions if you'd like to clear the offline state. Persistent profile is located at the following locations and you can override it with the --user-data-dir argument.

# Windows
%USERPROFILE%\AppData\Local\ms-playwright\mcp-{channel}-profile

# macOS
- ~/Library/Caches/ms-playwright/mcp-{channel}-profile

# Linux
- ~/.cache/ms-playwright/mcp-{channel}-profile
Isolated

In the isolated mode, each session is started in the isolated profile. Every time you ask MCP to close the browser, the session is closed and all the storage state for this session is lost. You can provide initial storage state to the browser via the config's contextOptions or via the --storage-state argument. Learn more about the storage state here.

{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--isolated",
        "--storage-state={path/to/storage.json}"
      ]
    }
  }
}
Browser Extension

The Playwright MCP Chrome Extension allows you to connect to existing browser tabs and leverage your logged-in sessions and browser state. See extension/README.md for installation and setup instructions.

Configuration file
The Playwright MCP server can be configured using a JSON configuration file. You can specify the configuration file using the --config command line option:

npx @playwright/mcp@latest --config path/to/config.json
Configuration file schema
Standalone MCP server
When running headed browser on system w/o display or from worker processes of the IDEs, run the MCP server from environment with the DISPLAY and pass the --port flag to enable HTTP transport.

npx @playwright/mcp@latest --port 8931
And then in MCP client config, set the url to the HTTP endpoint:

{
  "mcpServers": {
    "playwright": {
      "url": "http://localhost:8931/mcp"
    }
  }
}