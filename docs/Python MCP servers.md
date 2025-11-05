Python MCP servers

Copy page

Deploy Python MCP servers on Smithery

​
Overview
Deploy Python MCP servers using FastMCP with automatic containerization and infrastructure managed by Smithery.
​
Prerequisites
Python MCP server using FastMCP that exports a server creation function
Python 3.12+ installed locally
A Python package manager: uv (recommended), poetry, or pip
​
FastMCP Compatibility
When using FastMCP, ensure you have compatible versions:
mcp>=1.6.0 OR fastmcp>=2.0.0
New to MCP servers? See the Getting Started guide to learn how to build Python MCP servers from scratch using FastMCP.
​
Project Structure
Your Python project should look like this:

Copy

Ask AI
my-mcp-server/
  smithery.yaml          # Smithery configuration
  pyproject.toml         # Python dependencies and configuration
  src/
    my_server/
      __init__.py
      server.py          # Your MCP server code with decorated function
​
Setup
​
1. Configure smithery.yaml
Create a smithery.yaml file in your repository root (usually where the pyproject.toml is):

Copy

Ask AI
runtime: "python"
That’s it! This minimal configuration is intentional - Smithery handles containerization, and deployment automatically for Python projects.
​
2. Configure pyproject.toml
Your pyproject.toml must include the Smithery server configuration:

Copy

Ask AI
[build-system]
requires = ["uv_build>=0.8.15,<0.9.0"]
build-backend = "uv_build"

[project]
name = "my_server"
version = "0.1.0"
description = "My MCP server"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "mcp>=1.15.0",
    "smithery>=0.4.2",
]

[project.scripts]
dev = "smithery.cli.dev:main"
playground = "smithery.cli.playground:main"

# Points to your server function
[tool.smithery] 
server = "my_server.server:create_server"
​
3. Ensure Proper Server Structure
Your Python MCP server must have a function decorated with @smithery.server() that returns a FastMCP server object.

Copy

Ask AI
# src/weather_server/server.py
from mcp.server.fastmcp import Context, FastMCP
from smithery.decorators import smithery
from pydantic import BaseModel, Field

class ConfigSchema(BaseModel):
    unit: str = Field("celsius", description="Temperature unit (celsius or fahrenheit)")

@smithery.server(config_schema=ConfigSchema) 
def create_server(): 
    """Create and return a FastMCP server instance with session config."""
    
    server = FastMCP(name="Weather Server")

    @server.tool()
    def get_weather(city: str, ctx: Context) -> str: 
        """Get weather for a city."""
        # Access session-specific config through context
        session_config = ctx.session_config 
        
        # Use the configured temperature unit
        unit = session_config.unit
        formatted_temp = f"22°C" if unit == "celsius" else "72°F"

        return f"Weather in {city}: {formatted_temp}"

    return server
Accessing Session Configuration
Session-specific configuration is accessed through the Context parameter in your tools:

Copy

Ask AI
@server.tool()
def my_tool(arg: str, ctx: Context) -> str:
    # Access user's session config
    config = ctx.session_config
    
    # Use config values to customize behavior
    if config.api_key:
        # Make authenticated API calls
        pass
Each user session gets its own configuration instance, enabling per-user customization of your server’s behavior.
No config needed? Just omit the config_schema parameter: @smithery.server()
Key Requirements:
Function must be decorated with @smithery.server()
Function must return a FastMCP server instance
The function path must be specified in [tool.smithery] section of pyproject.toml
​
Local Development
After installing dependencies (uv sync or poetry install), test your server locally using the Smithery CLI:

Copy

Ask AI
# Start development server with interactive playground
uv run playground
# or
poetry run playground

# Or just run the server
uv run dev
# or  
poetry run dev
This opens the Smithery interactive playground where you can:
Test your MCP server tools in real-time
See tool responses and debug issues
Experiment with different inputs
​
Deploy
Push your code (including smithery.yaml) to GitHub
Connect your GitHub to Smithery (or claim your server if already listed)
Navigate to the Deployments tab on your server page
Click Deploy to build and host your server