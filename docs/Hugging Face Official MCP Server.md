Hugging Face Official MCP Server
汽车

JSON

TypeScript

Python

VS Code
VS Code
使用其HTTP URL连接到此远程服务器：

https://server.smithery.ai/@shreyaskarnik/huggingface-mcp-server/mcp

一键将此服务器连接到 VS Code。


一键安装
请使用以下终端命令安装此服务器：

终端

Copy
npx -y @smithery/cli@latest install @shreyaskarnik/huggingface-mcp-server --client vscode --profile changi

Welcome to the official Hugging Face MCP Server 🤗. Connect your LLM to the Hugging Face Hub and thousands of Gradio AI Applications.


🤗 Hugging Face MCP Server 🤗
smithery badge

A Model Context Protocol (MCP) server that provides read-only access to the Hugging Face Hub APIs. This server allows LLMs like Claude to interact with Hugging Face's models, datasets, spaces, papers, and collections.

Components
Resources
The server exposes popular Hugging Face resources:

Custom hf:// URI scheme for accessing resources
Models with hf://model/{model_id} URIs
Datasets with hf://dataset/{dataset_id} URIs
Spaces with hf://space/{space_id} URIs
All resources have descriptive names and JSON content type
Prompts
The server provides two prompt templates:

compare-models: Generates a comparison between multiple Hugging Face models

Required model_ids argument (comma-separated model IDs)
Retrieves model details and formats them for comparison
summarize-paper: Summarizes a research paper from Hugging Face

Required arxiv_id argument for paper identification
Optional detail_level argument (brief/detailed) to control summary depth
Combines paper metadata with implementation details
Tools
The server implements several tool categories:

Model Tools

search-models: Search models with filters for query, author, tags, and limit
get-model-info: Get detailed information about a specific model
Dataset Tools

search-datasets: Search datasets with filters
get-dataset-info: Get detailed information about a specific dataset
Space Tools

search-spaces: Search Spaces with filters including SDK type
get-space-info: Get detailed information about a specific Space
Paper Tools

get-paper-info: Get information about a paper and its implementations
get-daily-papers: Get the list of curated daily papers
Collection Tools

search-collections: Search collections with various filters
get-collection-info: Get detailed information about a specific collection
Configuration
The server does not require configuration, but supports optional Hugging Face authentication:

Set HF_TOKEN environment variable with your Hugging Face API token for:
Higher API rate limits
Access to private repositories (if authorized)
Improved reliability for high-volume requests
Quickstart
Install
Installing via Smithery
To install huggingface-mcp-server for Claude Desktop automatically via Smithery:

npx -y @smithery/cli install @shreyaskarnik/huggingface-mcp-server --client claude
Claude Desktop
On MacOS: ~/Library/Application\ Support/Claude/claude_desktop_config.json On Windows: %APPDATA%/Claude/claude_desktop_config.json

Development/Unpublished Servers Configuration
Development
Building and Publishing
To prepare the package for distribution:

Sync dependencies and update lockfile:
uv sync
Build package distributions:
uv build
This will create source and wheel distributions in the dist/ directory.

Publish to PyPI:
uv publish
Note: You'll need to set PyPI credentials via environment variables or command flags:

Token: --token or UV_PUBLISH_TOKEN
Or username/password: --username/UV_PUBLISH_USERNAME and --password/UV_PUBLISH_PASSWORD
Debugging
Since MCP servers run over stdio, debugging can be challenging. For the best debugging experience, we strongly recommend using the MCP Inspector.

You can launch the MCP Inspector via npm with this command:

npx @modelcontextprotocol/inspector uv --directory /path/to/huggingface-mcp-server run huggingface_mcp_server.py
Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.

Example Prompts for Claude
When using this server with Claude, try these example prompts:

"Search for BERT models on Hugging Face with less than 100 million parameters"
"Find the most popular datasets for text classification on Hugging Face"
"What are today's featured AI research papers on Hugging Face?"
"Summarize the paper with arXiv ID 2307.09288 using the Hugging Face MCP server"
"Compare the Llama-3-8B and Mistral-7B models from Hugging Face"
"Show me the most popular Gradio spaces for image generation"
"Find collections created by TheBloke that include Mixtral models"
Troubleshooting
If you encounter issues with the server:

Check server logs in Claude Desktop:

macOS: ~/Library/Logs/Claude/mcp-server-huggingface.log
Windows: %APPDATA%\Claude\logs\mcp-server-huggingface.log
For API rate limiting errors, consider adding a Hugging Face API token

Make sure your machine has internet connectivity to reach the Hugging Face API

If a particular tool is failing, try accessing the same data through the Hugging Face website to verify it exists
Installing the MCP Server
Follow the instructions below to get started:

Install in Claude Desktop or claude.ai
Install in Claude Code
Install in Gemini CLI
Install in VSCode
Install in Cursor
Once installed, navigate to https://huggingface.co/settings/mcp to configure your Tools and Spaces.

Tip

Add ?no_image_content=true to the URL to remove ImageContent blocks from Gradio Servers.

hf_mcp_server_small

Quick Guide (Repository Packages)
This repo contains:

(/mcp) MCP Implementations of Hub API and Search endpoints for integration with MCP Servers.
(/app) An MCP Server and Web Application for deploying endpoints.
MCP Server
The following transports are supported:

STDIO
SSE (To be deprecated, but still commonly deployed).
StreamableHTTP
StreamableHTTP in Stateless JSON Mode (StreamableHTTPJson)
The Web Application and HTTP Transports start by default on Port 3000.

SSE and StreamableHTTP services are available at /sse and /mcp respectively. Although though not strictly enforced by the specification this is common convention.

Tip

The Web Application allows you to switch tools on and off. For STDIO, SSE and StreamableHTTP this will send a ToolListChangedNotification to the MCP Client. In StreamableHTTPJSON mode the tool will not be listed when the client next requests the tool lists.

Running Locally
You can run the MCP Server locally with either npx or docker.

npx @llmindset/hf-mcp-server       # Start in STDIO mode
npx @llmindset/hf-mcp-server-http  # Start in Streamable HTTP mode
npx @llmindset/hf-mcp-server-json  # Start in Streamable HTTP (JSON RPC) mode
To run with docker:

docker pull ghcr.io/evalstate/hf-mcp-server:latest
docker run --rm -p 3000:3000 ghcr.io/evalstate/hf-mcp-server:latest
image

All commands above start the Management Web interface on http://localhost:3000/. The Streamable HTTP server is accessible on http://localhost:3000/mcp. See [Environment Variables](#Environment Variables) for configuration options. Docker defaults to Streamable HTTP (JSON RPC) mode.

Developing OpenAI Apps SDK Components
To build and test the Apps SDK component, run

cd packages/app
npm run dev:widget
Then open http://localhost:5173/gradio-widget-dev.html. This will bring up a browser with HMR where you can send Structured Content to the components for testing.

skybridge-viewer

Development
This project uses pnpm for build and development. Corepack is used to ensure everyone uses the same pnpm version (10.12.3).

# Install dependencies
pnpm install

# Build all packages
pnpm build
Build Commands
pnpm run clean -> clean build artifacts

pnpm run build -> build packages

pnpm run start -> start the mcp server application

pnpm run buildrun -> clean, build and start

pnpm run dev -> concurrently watch mcp and start dev server with HMR

Docker Build
Build the image:

docker build -t hf-mcp-server .
Run with default settings (Streaming HTTP JSON Mode), Dashboard on Port 3000:

docker run --rm -p 3000:3000 -e DEFAULT_HF_TOKEN=hf_xxx hf-mcp-server
Run STDIO MCP Server:

docker run -i --rm -e TRANSPORT=stdio -p 3000:3000 -e DEFAULT_HF_TOKEN=hf_xxx hf-mcp-server
TRANSPORT can be stdio, sse, streamingHttp or streamingHttpJson (default).

Transport Endpoints
The different transport types use the following endpoints:

SSE: /sse (with message endpoint at /message)
Streamable HTTP: /mcp (regular or JSON mode)
STDIO: Uses stdin/stdout directly, no HTTP endpoint
Stateful Connection Management
The sse and streamingHttp transports are both stateful - they maintain a connection with the MCP Client through an SSE connection. When using these transports, the following configuration options take effect:

Environment Variable	Default	Description
MCP_CLIENT_HEARTBEAT_INTERVAL	30000ms	How often to check SSE connection health
MCP_CLIENT_CONNECTION_CHECK	90000ms	How often to check for stale sessions
MCP_CLIENT_CONNECTION_TIMEOUT	300000ms	Remove sessions inactive for this duration
MCP_PING_ENABLED	true	Enable ping keep-alive for sessions
MCP_PING_INTERVAL	30000ms	Interval between ping cycles
Environment Variables
The server respects the following environment variables:

TRANSPORT: The transport type to use (stdio, sse, streamableHttp, or streamableHttpJson)
DEFAULT_HF_TOKEN: ⚠️ Requests are serviced with the HF_TOKEN received in the Authorization: Bearer header. The DEFAULT_HF_TOKEN is used if no header was sent. Only set this in Development / Test environments or for local STDIO Deployments. ⚠️
If running with stdio transport, HF_TOKEN is used if DEFAULT_HF_TOKEN is not set.
HF_API_TIMEOUT: Timeout for Hugging Face API requests in milliseconds (default: 12500ms / 12.5 seconds)
USER_CONFIG_API: URL to use for User settings (defaults to Local front-end)
MCP_STRICT_COMPLIANCE: set to True for GET 405 rejects in JSON Mode (default serves a welcome page).
AUTHENTICATE_TOOL: whether to include an Authenticate tool to issue an OAuth challenge when called
SEARCH_ENABLES_FETCH: When set to true, automatically enables the hf_doc_fetch tool whenever hf_doc_search is enabled


拥抱脸
欢迎来到 Hugging Face MCP 服务器
将助手连接到中心和数千个 AI 应用

开始使用
1
使用此 URL 设置您的客户端：
https://huggingface.co/mcp?login

2
选择您的应用和工具
Go to MCP Settings


工具预设和 URL 选项
点击查看预设和自定义选项。
详细的客户端设置
选择您偏好的AI客户端并按照设置说明进行操作

Claude Desktop 和 Claude.ai
指示：
1. 点击下方打开 Claude Connectors
前往 Claude Connectors
2. 点击“浏览连接器”
3. 选择“拥抱的脸”，然后点击“添加”。

Visual Studio Code
一键安装：
添加到 VS Code
点击即可在 VS Code 中安装 MCP 服务器。
手动配置/使用 READ HF_TOKEN 而不是 OAuth：
添加到您的 VS Codesettings.json 文件中：
{
  "servers": {
    "huggingface": {
      "url": "https://huggingface.co/mcp",
      "headers": {
        "Authorization": "Bearer <HF_TOKEN>"
      }
    }
  }
}

请替换<HF_TOKEN>为您的 Hugging Face API 令牌。

光标
一键安装：
将 huggingface MCP 服务器添加到光标
点击安装 Cursor 中的 MCP 服务器。
手动配置/使用 READ HF_TOKEN 而不是 OAuth：
编辑 Cursormcp.json 配置文件，添加 Hugging Face MCP 服务器：
{
  "mcpServers": {
    "huggingface": {
      "url": "https://huggingface.co/mcp",
      "headers": {
        "Authorization": "Bearer <HF_TOKEN>"
      }
    }
  }
}

请替换<HF_TOKEN>为您的 Hugging Face API Token。

LM工作室
一键安装：
将 MCP Server huggingface 添加到 LM Studio
点击后，替换为您的 READ Hugging Face API 令牌。 <HF_TOKEN>

Gemini CLI

Gemini CLI 文档
指示：
在 Gemini CLI 中输入以下命令进行安装：
gemini mcp add -t http huggingface https://huggingface.co/mcp?login

然后启动 Gemini CLI 并按照说明完成身份验证。
使用 HuggingFace Gemini CLI 扩展：
HuggingFace Gemini CLI 扩展程序将 MCP 服务器与上下文文件和自定义命令捆绑在一起，教 Gemini 如何更好地使用所有工具。
请使用以下命令安装扩展程序：
gemini extensions install https://github.com/huggingface/hf-mcp-server

启动 Gemini CLI 并运行以进行身份​​验证。 /mcp auth huggingface

克劳德·科德

Claude 代码文档
指示：
在 Claude Code 中输入以下命令进行安装：
claude mcp add hf-mcp-server -t http https://huggingface.co/mcp?login

然后启动 Claude 并按照说明完成身份验证。
使用 READ HF_TOKEN 而不是 OAuth：
要使用 READ HF_TOKEN 而不是 OAuth，请使用以下命令：
claude mcp add hf-mcp-server \
  -t http https://huggingface.co/mcp \
  -H "Authorization: Bearer <HF_TOKEN>"

请替换<HF_TOKEN>为您的 Hugging Face API 令牌。

Codex CLI

Codex CLI 使用说明
指示：
Codex CLI 使用说明位于：https://github.com/openai/codex
请编辑您的内容~/.codex/config.toml并添加以下内容：
[mcp_servers.huggingface]
command = "npx"
args = ["-y", "mcp-remote@latest", "https://huggingface.co/mcp?login"]

什么是MCP？
模型上下文协议 (MCP) 是一种开放标准，它使 AI 助手能够安全地连接到外部数据源和工具。

Hugging Face MCP 服务器提供对 Hugging Face 庞大的模型、数据集、研究论文和尖端 AI 工具生态系统的无缝访问。该服务器是开源的，点击下方链接了解其他部署选项的详细信息，提出问题或建议贡献代码。

将您的 MCP 客户端连接到 Hugging Face Hub
我们推出了官方的 Hugging Face MCP（模型控制协议）服务器，实现了 Hub 与任何兼容 MCP 的 AI 助手（包括 VSCode、Cursor 和 Claude Desktop）之间的无缝集成。

使用精心挑选的内置工具集（例如空间和论文语义搜索、模型和数据集探索）配置您的设置，并通过连接到任何兼容 MCP 的 Gradio 应用来增强助手的功能，使其能够使用 Hugging Face 社区构建的 ML 应用。

访问huggingface.co/settings/mcp即可开始使用。

注意：此功能为实验性功能⚗️，并将持续改进。

MCP 服务器
连接您的 MCP 客户端，并配置 Hugging Face Hub MCP 服务器中可用的工具。
在 ZeroGPU Spaces（H200 硬件）上获得 25 分钟的每日计算使用时间，与通过 MCP 使用 Spaces 时兼容。

使用您的 AI 助手进行设置
分享反馈
点击“添加到 VSCode”按钮即可一键安装，或者将以下代码片段添加到您的.vscode/mcp.json 文件中。

添加到
VSCode
VSCode
MCP

复制
{
  "servers": {
    "hf-mcp-server": {
      "url": "https://huggingface.co/mcp?login"
    }
  }
}


MCP 服务器
连接您的 MCP 客户端，并配置 Hugging Face Hub MCP 服务器中可用的工具。
在 ZeroGPU Spaces（H200 硬件）上获得 25 分钟的每日计算使用时间，与通过 MCP 使用 Spaces 时兼容。

使用您的 AI 助手进行设置
分享反馈
HuggingFace Gemini CLI 扩展程序将 MCP 服务器与上下文文件和自定义命令捆绑在一起，使 Gemini 能够更好地使用所有工具。
启动 Gemini CLI 并输入 /mcp auth huggingface进行身份验证。

使用以下命令在 Gemini CLI 中安装扩展程序：

VSCode
MCP

复制

Run Inference on servers
Inference is the process of using a trained model to make predictions on new data. Because this process can be compute-intensive, running on a dedicated or external service can be an interesting option. The huggingface_hub library provides a unified interface to run inference across multiple services for models hosted on the Hugging Face Hub:

Inference Providers: a streamlined, unified access to hundreds of machine learning models, powered by our serverless inference partners. This new approach builds on our previous Serverless Inference API, offering more models, improved performance, and greater reliability thanks to world-class providers. Refer to the documentation for a list of supported providers.
Inference Endpoints: a product to easily deploy models to production. Inference is run by Hugging Face in a dedicated, fully managed infrastructure on a cloud provider of your choice.
Local endpoints: you can also run inference with local inference servers like llama.cpp, Ollama, vLLM, LiteLLM, or Text Generation Inference (TGI) by connecting the client to these local endpoints.
[!TIP][InferenceClient](/docs/huggingface_hub/main/en/package_reference/inference_client#huggingface_hub.InferenceClient) is a Python client making HTTP calls to our APIs. If you want to make the HTTP calls directly using your preferred tool (curl, postman,…), please refer to the Inference Providers documentation or to the Inference Endpoints documentation pages.

For web development, a JS client has been released. If you are interested in game development, you might have a look at our C# project.

Getting started
Let’s get started with a text-to-image task:

CopiedCopied
from huggingface_hub import InferenceClient

# Example with an external provider (e.g. replicate)
replicate_client = InferenceClient(
    provider="replicate",
    api_key="my_replicate_api_key",
)
replicate_image = replicate_client.text_to_image(
    "A flying car crossing a futuristic cityscape.",
    model="black-forest-labs/FLUX.1-schnell",
)
replicate_image.save("flying_car.png")
In the example above, we initialized an InferenceClient with a third-party provider, Replicate. When using a provider, you must specify the model you want to use. The model id must be the id of the model on the Hugging Face Hub, not the id of the model from the third-party provider. In our example, we generated an image from a text prompt. The returned value is a PIL.Image object that can be saved to a file. For more details, check out the text_to_image() documentation.

Let’s now see an example using the chat_completion() API. This task uses an LLM to generate a response from a list of messages:

CopiedCopied
from huggingface_hub import InferenceClient
messages = [
    {
        "role": "user",
        "content": "What is the capital of France?",
    }
]
client = InferenceClient(
    provider="together",
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    api_key="my_together_api_key",
)
client.chat_completion(messages, max_tokens=100)
ChatCompletionOutput(
    choices=[
        ChatCompletionOutputComplete(
            finish_reason="eos_token",
            index=0,
            message=ChatCompletionOutputMessage(
                role="assistant", content="The capital of France is Paris.", name=None, tool_calls=None
            ),
            logprobs=None,
        )
    ],
    created=1719907176,
    id="",
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    object="text_completion",
    system_fingerprint="2.0.4-sha-f426a33",
    usage=ChatCompletionOutputUsage(completion_tokens=8, prompt_tokens=17, total_tokens=25),
)
In the example above, we used a third-party provider (Together AI) and specified which model we want to use ("meta-llama/Meta-Llama-3-8B-Instruct"). We then gave a list of messages to complete (here, a single question) and passed an additional parameter to the API (max_token=100). The output is a ChatCompletionOutput object that follows the OpenAI specification. The generated content can be accessed with output.choices[0].message.content. For more details, check out the chat_completion() documentation.

The API is designed to be simple. Not all parameters and options are available or described for the end user. Check out this page if you are interested in learning more about all the parameters available for each task.

Using a specific provider
If you want to use a specific provider, you can specify it when initializing the client. The default value is “auto” which will select the first of the providers available for the model, sorted by the user’s order in https://hf.co/settings/inference-providers. Refer to the Supported providers and tasks section for a list of supported providers.

CopiedCopied
from huggingface_hub import InferenceClient
client = InferenceClient(provider="replicate", api_key="my_replicate_api_key")
Using a specific model
What if you want to use a specific model? You can specify it either as a parameter or directly at an instance level:

CopiedCopied
from huggingface_hub import InferenceClient
# Initialize client for a specific model
client = InferenceClient(provider="together", model="meta-llama/Llama-3.1-8B-Instruct")
client.text_to_image(...)
# Or use a generic client but pass your model as an argument
client = InferenceClient(provider="together")
client.text_to_image(..., model="meta-llama/Llama-3.1-8B-Instruct")
When using the “hf-inference” provider, each task comes with a recommended model from the 1M+ models available on the Hub. However, this recommendation can change over time, so it’s best to explicitly set a model once you’ve decided which one to use. For third-party providers, you must always specify a model that is compatible with that provider.

Visit the Models page on the Hub to explore models available through Inference Providers.

Using Inference Endpoints
The examples we saw above use inference providers. While these prove to be very useful for prototyping and testing things quickly. Once you’re ready to deploy your model to production, you’ll need to use a dedicated infrastructure. That’s where Inference Endpoints comes into play. It allows you to deploy any model and expose it as a private API. Once deployed, you’ll get a URL that you can connect to using exactly the same code as before, changing only the model parameter:

CopiedCopied
from huggingface_hub import InferenceClient
client = InferenceClient(model="https://uu149rez6gw9ehej.eu-west-1.aws.endpoints.huggingface.cloud/deepfloyd-if")
# or
client = InferenceClient()
client.text_to_image(..., model="https://uu149rez6gw9ehej.eu-west-1.aws.endpoints.huggingface.cloud/deepfloyd-if")
Note that you cannot specify both a URL and a provider - they are mutually exclusive. URLs are used to connect directly to deployed endpoints.

Using local endpoints
You can use InferenceClient to run chat completion with local inference servers (llama.cpp, vllm, litellm server, TGI, mlx, etc.) running on your own machine. The API should be OpenAI API-compatible.

CopiedCopied
from huggingface_hub import InferenceClient
client = InferenceClient(model="http://localhost:8080")

response = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ],
    max_tokens=100
)
print(response.choices[0].message.content)
Similarly to the OpenAI Python client, InferenceClient can be used to run Chat Completion inference with any OpenAI REST API-compatible endpoint.

Authentication
Authentication can be done in two ways:

Routed through Hugging Face : Use Hugging Face as a proxy to access third-party providers. The calls will be routed through Hugging Face’s infrastructure using our provider keys, and the usage will be billed directly to your Hugging Face account.

You can authenticate using a User Access Token. You can provide your Hugging Face token directly using the api_key parameter:

CopiedCopied
client = InferenceClient(
    provider="replicate",
    api_key="hf_****"  # Your HF token
)
If you don’t pass an api_key, the client will attempt to find and use a token stored locally on your machine. This typically happens if you’ve previously logged in. See the Authentication Guide for details on login.

CopiedCopied
client = InferenceClient(
    provider="replicate",
    token="hf_****"  # Your HF token
)
Direct access to provider: Use your own API key to interact directly with the provider’s service:

CopiedCopied
client = InferenceClient(
    provider="replicate",
    api_key="r8_****"  # Your Replicate API key
)
For more details, refer to the Inference Providers pricing documentation.

Supported providers and tasks
InferenceClient’s goal is to provide the easiest interface to run inference on Hugging Face models, on any provider. It has a simple API that supports the most common tasks. Here is a table showing which providers support which tasks:

Task	Black Forest Labs	Cerebras	Clarifai	Cohere	fal-ai	Featherless AI	Fireworks AI	Groq	HF Inference	Hyperbolic	Nebius AI Studio	Novita AI	Nscale	Public AI	Replicate	Sambanova	Scaleway	Together	Wavespeed	Zai
audio_classification()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
audio_to_audio()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
automatic_speech_recognition()	❌	❌	❌	❌	✅	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
chat_completion()	❌	✅	✅	✅	❌	✅	✅	✅	✅	✅	✅	✅	✅	✅	❌	✅	✅	✅	❌	✅
document_question_answering()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
feature_extraction()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	✅	❌	❌	❌	❌	✅	✅	❌	❌	❌
fill_mask()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
image_classification()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
image_segmentation()	❌	❌	❌	❌	✅	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
image_to_image()	❌	❌	❌	❌	✅	❌	❌	❌	✅	❌	❌	❌	❌	❌	✅	❌	❌	❌	✅	❌
image_to_video()	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌
image_to_text()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
object_detection()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
question_answering()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
sentence_similarity()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
summarization()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
table_question_answering()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
text_classification()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
text_generation()	❌	❌	❌	❌	❌	✅	❌	❌	✅	✅	✅	✅	❌	❌	❌	❌	❌	✅	❌	❌
text_to_image()	✅	❌	❌	❌	✅	❌	❌	❌	✅	✅	✅	❌	✅	❌	✅	❌	❌	✅	✅	❌
text_to_speech()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌
text_to_video()	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	✅	❌	❌	✅	❌	❌	❌	✅	❌
tabular_classification()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
tabular_regression()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
token_classification()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
translation()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
visual_question_answering()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
zero_shot_image_classification()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
zero_shot_classification()	❌	❌	❌	❌	❌	❌	❌	❌	✅	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌	❌
Check out the Tasks page to learn more about each task.

OpenAI compatibility
The chat_completion task follows OpenAI’s Python client syntax. What does it mean for you? It means that if you are used to play with OpenAI’s APIs you will be able to switch to huggingface_hub.InferenceClient to work with open-source models by updating just 2 line of code!

CopiedCopied
- from openai import OpenAI
+ from huggingface_hub import InferenceClient

- client = OpenAI(
+ client = InferenceClient(
    base_url=...,
    api_key=...,
)


output = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Count to 10"},
    ],
    stream=True,
    max_tokens=1024,
)

for chunk in output:
    print(chunk.choices[0].delta.content)
And that’s it! The only required changes are to replace from openai import OpenAI by from huggingface_hub import InferenceClient and client = OpenAI(...) by client = InferenceClient(...). You can choose any LLM model from the Hugging Face Hub by passing its model id as model parameter. Here is a list of supported models. For authentication, you should pass a valid User Access Token as api_key or authenticate using huggingface_hub (see the authentication guide).

All input parameters and output format are strictly the same. In particular, you can pass stream=True to receive tokens as they are generated. You can also use the AsyncInferenceClient to run inference using asyncio:

CopiedCopied
import asyncio
- from openai import AsyncOpenAI
+ from huggingface_hub import AsyncInferenceClient

- client = AsyncOpenAI()
+ client = AsyncInferenceClient()

async def main():
    stream = await client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=[{"role": "user", "content": "Say this is a test"}],
        stream=True,
    )
    async for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")

asyncio.run(main())
You might wonder why using InferenceClient instead of OpenAI’s client? There are a few reasons for that:

InferenceClient is configured for Hugging Face services. You don’t need to provide a base_url to run models with Inference Providers. You also don’t need to provide a token or api_key if your machine is already correctly logged in.
InferenceClient is tailored for both Text-Generation-Inference (TGI) and transformers frameworks, meaning you are assured it will always be on-par with the latest updates.
InferenceClient is integrated with our Inference Endpoints service, making it easier to launch an Inference Endpoint, check its status and run inference on it. Check out the Inference Endpoints guide for more details.
InferenceClient.chat.completions.create is simply an alias for InferenceClient.chat_completion. Check out the package reference of chat_completion() for more details. base_url and api_key parameters when instantiating the client are also aliases for model and token. These aliases have been defined to reduce friction when switching from OpenAI to InferenceClient.

Function Calling
Function calling allows LLMs to interact with external tools, such as defined functions or APIs. This enables users to easily build applications tailored to specific use cases and real-world tasks. InferenceClient implements the same tool calling interface as the OpenAI Chat Completions API. Here is a simple example of tool calling using Nebius as the inference provider:

CopiedCopied
from huggingface_hub import InferenceClient

tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current temperature for a given location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City and country e.g. Paris, France"
                        }
                    },
                    "required": ["location"],
                },
            }
        }
]

client = InferenceClient(provider="nebius")

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-72B-Instruct",
    messages=[
    {
        "role": "user",
        "content": "What's the weather like the next 3 days in London, UK?"
    }
    ],
    tools=tools,
    tool_choice="auto",
)

print(response.choices[0].message.tool_calls[0].function.arguments)
Please refer to the providers’ documentation to verify which models are supported by them for Function/Tool Calling.

Structured Outputs & JSON Mode
InferenceClient supports JSON mode for syntactically valid JSON responses and Structured Outputs for schema-enforced responses. JSON mode provides machine-readable data without strict structure, while Structured Outputs guarantee both valid JSON and adherence to a predefined schema for reliable downstream processing.

We follow the OpenAI API specs for both JSON mode and Structured Outputs. You can enable them via the response_format argument. Here is an example of Structured Outputs using Cerebras as the inference provider:

CopiedCopied
from huggingface_hub import InferenceClient

json_schema = {
    "name": "book",
    "schema": {
        "properties": {
            "name": {
                "title": "Name",
                "type": "string",
            },
            "authors": {
                "items": {"type": "string"},
                "title": "Authors",
                "type": "array",
            },
        },
        "required": ["name", "authors"],
        "title": "Book",
        "type": "object",
    },
    "strict": True,
}

client = InferenceClient(provider="cerebras")


completion = client.chat.completions.create(
    model="Qwen/Qwen3-32B",
    messages=[
        {"role": "system", "content": "Extract the books information."},
        {"role": "user", "content": "I recently read 'The Great Gatsby' by F. Scott Fitzgerald."},
    ],
    response_format={
        "type": "json_schema",
        "json_schema": json_schema,
    },
)

print(completion.choices[0].message)
Please refer to the providers’ documentation to verify which models are supported by them for Structured Outputs and JSON Mode.

Async client
An async version of the client is also provided, based on asyncio and httpx. All async API endpoints are available via AsyncInferenceClient. Its initialization and APIs are strictly the same as the sync-only version.

CopiedCopied
# Code must be run in an asyncio concurrent context.
# $ python -m asyncio
from huggingface_hub import AsyncInferenceClient
client = AsyncInferenceClient()

image = await client.text_to_image("An astronaut riding a horse on the moon.")
image.save("astronaut.png")

async for token in await client.text_generation("The Huggingface Hub is", stream=True):
    print(token, end="")
 a platform for sharing and discussing ML-related content.
For more information about the asyncio module, please refer to the official documentation.

MCP Client
The huggingface_hub library now includes an experimental MCPClient, designed to empower Large Language Models (LLMs) with the ability to interact with external Tools via the Model Context Protocol (MCP). This client extends an AsyncInferenceClient to seamlessly integrate Tool usage.

The MCPClient connects to MCP servers (either local stdio scripts or remote http/sse services) that expose tools. It feeds these tools to an LLM (via AsyncInferenceClient). If the LLM decides to use a tool, MCPClient manages the execution request to the MCP server and relays the Tool’s output back to the LLM, often streaming results in real-time.

In the following example, we use Qwen/Qwen2.5-72B-Instruct model via Nebius inference provider. We then add a remote MCP server, in this case, an SSE server which made the Flux image generation tool available to the LLM.

CopiedCopied
import os

from huggingface_hub import ChatCompletionInputMessage, ChatCompletionStreamOutput, MCPClient


async def main():
    async with MCPClient(
        provider="nebius",
        model="Qwen/Qwen2.5-72B-Instruct",
        api_key=os.environ["HF_TOKEN"],
    ) as client:
        await client.add_mcp_server(type="sse", url="https://evalstate-flux1-schnell.hf.space/gradio_api/mcp/sse")

        messages = [
            {
                "role": "user",
                "content": "Generate a picture of a cat on the moon",
            }
        ]

        async for chunk in client.process_single_turn_with_tools(messages):
            # Log messages
            if isinstance(chunk, ChatCompletionStreamOutput):
                delta = chunk.choices[0].delta
                if delta.content:
                    print(delta.content, end="")

            # Or tool calls
            elif isinstance(chunk, ChatCompletionInputMessage):
                print(
                    f"\nCalled tool '{chunk.name}'. Result: '{chunk.content if len(chunk.content) < 1000 else chunk.content[:1000] + '...'}'"
                )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
For even simpler development, we offer a higher-level Agent class. This ‘Tiny Agent’ simplifies creating conversational Agents by managing the chat loop and state, essentially acting as a wrapper around MCPClient. It’s designed to be a simple while loop built right on top of an MCPClient. You can run these Agents directly from the command line:

Copied
# install latest version of huggingface_hub with the mcp extra
pip install -U huggingface_hub[mcp]
# Run an agent that uses the Flux image generation tool
tiny-agents run julien-c/flux-schnell-generator
When launched, the Agent will load, list the Tools it has discovered from its connected MCP servers, and then it’s ready for your prompts!

Advanced tips
In the above section, we saw the main aspects of InferenceClient. Let’s dive into some more advanced tips.

Billing
As an HF user, you get monthly credits to run inference through various providers on the Hub. The amount of credits you get depends on your type of account (Free or PRO or Enterprise Hub). You get charged for every inference request, depending on the provider’s pricing table. By default, the requests are billed to your personal account. However, it is possible to set the billing so that requests are charged to an organization you are part of by simply passing bill_to="<your_org_name>" to InferenceClient. For this to work, your organization must be subscribed to Enterprise Hub. For more details about billing, check out this guide.

Copied
from huggingface_hub import InferenceClient
client = InferenceClient(provider="fal-ai", bill_to="openai")
image = client.text_to_image(
    "A majestic lion in a fantasy forest",
    model="black-forest-labs/FLUX.1-schnell",
)
image.save("lion.png")
Note that it is NOT possible to charge another user or an organization you are not part of. If you want to grant someone else some credits, you must create a joint organization with them.

Timeout
Inference calls can take a significant amount of time. By default, InferenceClient will wait “indefinitely” until the inference complete. If you want more control in your workflow, you can set the timeout parameter to a specific value in seconds. If the timeout delay expires, an InferenceTimeoutError is raised, which you can catch in your code:

Copied
from huggingface_hub import InferenceClient, InferenceTimeoutError
client = InferenceClient(timeout=30)
try:
    client.text_to_image(...)
except InferenceTimeoutError:
    print("Inference timed out after 30s.")
Binary inputs
Some tasks require binary inputs, for example, when dealing with images or audio files. In this case, InferenceClient tries to be as permissive as possible and accept different types:

raw bytes
a file-like object, opened as binary (with open("audio.flac", "rb") as f: ...)
a path (str or Path) pointing to a local file
a URL (str) pointing to a remote file (e.g. https://...). In this case, the file will be downloaded locally before being sent to the API.
CopiedCopied
from huggingface_hub import InferenceClient
client = InferenceClient()
client.image_classification("https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Cute_dog.jpg/320px-Cute_dog.jpg")
[{'score': 0.9779096841812134, 'label': 'Blenheim spaniel'}, ...]

Command Line Interface (CLI)
The huggingface_hub Python package comes with a built-in CLI called hf. This tool allows you to interact with the Hugging Face Hub directly from a terminal. For example, you can log in to your account, create a repository, upload and download files, etc. It also comes with handy features to configure your machine or manage your cache. In this guide, we will have a look at the main features of the CLI and how to use them.

This guide covers the most important features of the hf CLI. For a complete reference of all commands and options, see the CLI reference.

Getting started
First of all, let’s install the CLI:

Copied
 pip install -U "huggingface_hub"
The CLI ships with the core huggingface_hub package.

Alternatively, you can install the hf CLI with a single command:

On macOS and Linux:

Copied
>>> curl -LsSf https://hf.co/cli/install.sh | bash
On Windows:

Copied
>>> powershell -ExecutionPolicy ByPass -c "irm https://hf.co/cli/install.ps1 | iex"
Once installed, you can check that the CLI is correctly setup:

Copied
>>> hf --help
Usage: hf [OPTIONS] COMMAND [ARGS]...

  Hugging Face Hub CLI

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  auth                 Manage authentication (login, logout, etc.).
  cache                Manage local cache directory.
  download             Download files from the Hub.
  env                  Print information about the environment.
  jobs                 Run and manage Jobs on the Hub.
  repo                 Manage repos on the Hub.
  repo-files           Manage files in a repo on the Hub.
  upload               Upload a file or a folder to the Hub.
  upload-large-folder  Upload a large folder to the Hub.
  version              Print information about the hf version.
If the CLI is correctly installed, you should see a list of all the options available in the CLI. If you get an error message such as command not found: hf, please refer to the Installation guide.

The --help option is very convenient for getting more details about a command. You can use it anytime to list all available options and their details. For example, hf upload --help provides more information on how to upload files using the CLI.

Other installation methods
Using uv
You can install and run the hf CLI with uv.

Make sure uv is installed (adds uv and uvx to your PATH):

Copied
>>> curl -LsSf https://astral.sh/uv/install.sh | sh
Then install the CLI globally and use it anywhere:

Copied
>>> uv tool install "huggingface_hub"
>>> hf auth whoami
Alternatively, run the CLI ephemerally with uvx (no global install):

Copied
>>> uvx --from huggingface_hub hf auth whoami
Using Homebrew
You can also install the CLI using Homebrew:

Copied
>>> brew install huggingface-cli
Check out the Homebrew huggingface page here for more details.

hf auth login
In many cases, you must be logged in to a Hugging Face account to interact with the Hub (download private repos, upload files, create PRs, etc.). To do so, you need a User Access Token from your Settings page. The User Access Token is used to authenticate your identity to the Hub. Make sure to set a token with write access if you want to upload or modify content.

Once you have your token, run the following command in your terminal:

Copied
>>> hf auth login
This command will prompt you for a token. Copy-paste yours and press Enter. Then, you’ll be asked if the token should also be saved as a git credential. Press Enter again (default to yes) if you plan to use git locally. Finally, it will call the Hub to check that your token is valid and save it locally.

Copied
_|    _|  _|    _|    _|_|_|    _|_|_|  _|_|_|  _|      _|    _|_|_|      _|_|_|_|    _|_|      _|_|_|  _|_|_|_|
_|    _|  _|    _|  _|        _|          _|    _|_|    _|  _|            _|        _|    _|  _|        _|
_|_|_|_|  _|    _|  _|  _|_|  _|  _|_|    _|    _|  _|  _|  _|  _|_|      _|_|_|    _|_|_|_|  _|        _|_|_|
_|    _|  _|    _|  _|    _|  _|    _|    _|    _|    _|_|  _|    _|      _|        _|    _|  _|        _|
_|    _|    _|_|      _|_|_|    _|_|_|  _|_|_|  _|      _|    _|_|_|      _|        _|    _|    _|_|_|  _|_|_|_|

To log in, `huggingface_hub` requires a token generated from https://huggingface.co/settings/tokens .
Enter your token (input will not be visible):
Add token as git credential? (Y/n)
Token is valid (permission: write).
Your token has been saved in your configured git credential helpers (store).
Your token has been saved to /home/wauplin/.cache/huggingface/token
Login successful
Alternatively, if you want to log-in without being prompted, you can pass the token directly from the command line. To be more secure, we recommend passing your token as an environment variable to avoid pasting it in your command history.

Copied
# Or using an environment variable
>>> hf auth login --token $HF_TOKEN --add-to-git-credential
Token is valid (permission: write).
The token `token_name` has been saved to /home/wauplin/.cache/huggingface/stored_tokens
Your token has been saved in your configured git credential helpers (store).
Your token has been saved to /home/wauplin/.cache/huggingface/token
Login successful
The current active token is: `token_name`
For more details about authentication, check out this section.

hf auth whoami
If you want to know if you are logged in, you can use hf auth whoami. This command doesn’t have any options and simply prints your username and the organizations you are a part of on the Hub:

Copied
hf auth whoami
Wauplin
orgs:  huggingface,eu-test,OAuthTesters,hf-accelerate,HFSmolCluster
If you are not logged in, an error message will be printed.

hf auth logout
This command logs you out. In practice, it will delete all tokens stored on your machine. If you want to remove a specific token, you can specify the token name as an argument.

This command will not log you out if you are logged in using the HF_TOKEN environment variable (see reference). If that is the case, you must unset the environment variable in your machine configuration.

hf download
Use the hf download command to download files from the Hub directly. Internally, it uses the same hf_hub_download() and snapshot_download() helpers described in the Download guide and prints the returned path to the terminal. In the examples below, we will walk through the most common use cases. For a full list of available options, you can run:

Copied
hf download --help
Download a single file
To download a single file from a repo, simply provide the repo_id and filename as follows:

Copied
>>> hf download gpt2 config.json
downloading https://huggingface.co/gpt2/resolve/main/config.json to /home/wauplin/.cache/huggingface/hub/tmpwrq8dm5o
(…)ingface.co/gpt2/resolve/main/config.json: 100%|██████████████████████████████████| 665/665 [00:00<00:00, 2.49MB/s]
/home/wauplin/.cache/huggingface/hub/models--gpt2/snapshots/11c5a3d5811f50298f278a704980280950aedb10/config.json
The command will always print on the last line the path to the file on your local machine.

To download a file located in a subdirectory of the repo, you should provide the path of the file in the repo in posix format like this:

Copied
>>> hf download HiDream-ai/HiDream-I1-Full text_encoder/model.safetensors
Download an entire repository
In some cases, you just want to download all the files from a repository. This can be done by just specifying the repo id:

Copied
>>> hf download HuggingFaceH4/zephyr-7b-beta
Fetching 23 files:   0%|                                                | 0/23 [00:00<?, ?it/s]
...
...
/home/wauplin/.cache/huggingface/hub/models--HuggingFaceH4--zephyr-7b-beta/snapshots/3bac358730f8806e5c3dc7c7e19eb36e045bf720
Download multiple files
You can also download a subset of the files from a repository with a single command. This can be done in two ways. If you already have a precise list of the files you want to download, you can simply provide them sequentially:

Copied
>>> hf download gpt2 config.json model.safetensors
Fetching 2 files:   0%|                                                                        | 0/2 [00:00<?, ?it/s]
downloading https://huggingface.co/gpt2/resolve/11c5a3d5811f50298f278a704980280950aedb10/model.safetensors to /home/wauplin/.cache/huggingface/hub/tmpdachpl3o
(…)8f278a7049802950aedb10/model.safetensors: 100%|██████████████████████████████| 8.09k/8.09k [00:00<00:00, 40.5MB/s]
Fetching 2 files: 100%|████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00,  3.76it/s]
/home/wauplin/.cache/huggingface/hub/models--gpt2/snapshots/11c5a3d5811f50298f278a704980280950aedb10
The other approach is to provide patterns to filter which files you want to download using --include and --exclude. For example, if you want to download all safetensors files from stabilityai/stable-diffusion-xl-base-1.0, except the files in FP16 precision:

Copied
>>> hf download stabilityai/stable-diffusion-xl-base-1.0 --include "*.safetensors" --exclude "*.fp16.*"*
Fetching 8 files:   0%|                                                                         | 0/8 [00:00<?, ?it/s]
...
...
Fetching 8 files: 100%|█████████████████████████████████████████████████████████████████████████| 8/8 (...)
/home/wauplin/.cache/huggingface/hub/models--stabilityai--stable-diffusion-xl-base-1.0/snapshots/462165984030d82259a11f4367a4eed129e94a7b
Download a dataset or a Space
The examples above show how to download from a model repository. To download a dataset or a Space, use the --repo-type option:

Copied
# https://huggingface.co/datasets/HuggingFaceH4/ultrachat_200k
>>> hf download HuggingFaceH4/ultrachat_200k --repo-type dataset

# https://huggingface.co/spaces/HuggingFaceH4/zephyr-chat
>>> hf download HuggingFaceH4/zephyr-chat --repo-type space

...
Download a specific revision
The examples above show how to download from the latest commit on the main branch. To download from a specific revision (commit hash, branch name or tag), use the --revision option:

Copied
>>> hf download bigcode/the-stack --repo-type dataset --revision v1.1
...
Download to a local folder
The recommended (and default) way to download files from the Hub is to use the cache-system. However, in some cases you want to download files and move them to a specific folder. This is useful to get a workflow closer to what git commands offer. You can do that using the --local-dir option.

A .cache/huggingface/ folder is created at the root of your local directory containing metadata about the downloaded files. This prevents re-downloading files if they’re already up-to-date. If the metadata has changed, then the new file version is downloaded. This makes the local-dir optimized for pulling only the latest changes.

For more details on how downloading to a local file works, check out the download guide.

Copied
>>> hf download adept/fuyu-8b model-00001-of-00002.safetensors --local-dir fuyu
...
fuyu/model-00001-of-00002.safetensors
Dry-run mode
In some cases, you would like to check which files would be downloaded before actually downloading them. You can check this using the --dry-run parameter. It lists all files to download on the repo and checks whether they are already downloaded or not. This gives an idea of how many files have to be downloaded and their sizes.

Copied
>>> hf download openai-community/gpt2 --dry-run
[dry-run] Fetching 26 files: 100%|█████████████| 26/26 [00:04<00:00,  6.26it/s]
[dry-run] Will download 11 files (out of 26) totalling 5.6G.
File                              Bytes to download
--------------------------------- -----------------
.gitattributes                    -
64-8bits.tflite                   125.2M
64-fp16.tflite                    248.3M
64.tflite                         495.8M
README.md                         -
config.json                       -
flax_model.msgpack                497.8M
generation_config.json            -
merges.txt                        -
model.safetensors                 548.1M
onnx/config.json                  -
onnx/decoder_model.onnx           653.7M
onnx/decoder_model_merged.onnx    655.2M
onnx/decoder_with_past_model.onnx 653.7M
onnx/generation_config.json       -
onnx/merges.txt                   -
onnx/special_tokens_map.json      -
onnx/tokenizer.json               -
onnx/tokenizer_config.json        -
onnx/vocab.json                   -
pytorch_model.bin                 548.1M
rust_model.ot                     702.5M
tf_model.h5                       497.9M
tokenizer.json                    -
tokenizer_config.json             -
vocab.json                        -
For more details, check out the download guide.

Specify cache directory
If not using --local-dir, all files will be downloaded by default to the cache directory defined by the HF_HOME environment variable. You can specify a custom cache using --cache-dir:

Copied
>>> hf download adept/fuyu-8b --cache-dir ./path/to/cache
...
./path/to/cache/models--adept--fuyu-8b/snapshots/ddcacbcf5fdf9cc59ff01f6be6d6662624d9c745
Specify a token
To access private or gated repositories, you must use a token. By default, the token saved locally (using hf auth login) will be used. If you want to authenticate explicitly, use the --token option:

Copied
>>> hf download gpt2 config.json --token=hf_****
/home/wauplin/.cache/huggingface/hub/models--gpt2/snapshots/11c5a3d5811f50298f278a704980280950aedb10/config.json
Quiet mode
By default, the hf download command will be verbose. It will print details such as warning messages, information about the downloaded files, and progress bars. If you want to silence all of this, use the --quiet option. Only the last line (i.e. the path to the downloaded files) is printed. This can prove useful if you want to pass the output to another command in a script.

Copied
>>> hf download gpt2 --quiet
/home/wauplin/.cache/huggingface/hub/models--gpt2/snapshots/11c5a3d5811f50298f278a704980280950aedb10
Download timeout
On machines with slow connections, you might encounter timeout issues like this one:

Copied
`httpx.TimeoutException: (TimeoutException("HTTPSConnectionPool(host='cdn-lfs-us-1.huggingface.co', port=443): Read timed out. (read timeout=10)"), '(Request ID: a33d910c-84c6-4514-8362-c705e2039d38)')`
To mitigate this issue, you can set the HF_HUB_DOWNLOAD_TIMEOUT environment variable to a higher value (default is 10):

Copied
export HF_HUB_DOWNLOAD_TIMEOUT=30
For more details, check out the environment variables reference. And rerun your download command.

hf upload
Use the hf upload command to upload files to the Hub directly. Internally, it uses the same upload_file() and upload_folder() helpers described in the Upload guide. In the examples below, we will walk through the most common use cases. For a full list of available options, you can run:

Copied
>>> hf upload --help
Upload an entire folder
The default usage for this command is:

Copied
# Usage:  hf upload [repo_id] [local_path] [path_in_repo]
To upload the current directory at the root of the repo, use:

Copied
>>> hf upload my-cool-model . .
https://huggingface.co/Wauplin/my-cool-model/tree/main/
If the repo doesn’t exist yet, it will be created automatically.

You can also upload a specific folder:

Copied
>>> hf upload my-cool-model ./models .
https://huggingface.co/Wauplin/my-cool-model/tree/main/
Finally, you can upload a folder to a specific destination on the repo:

Copied
>>> hf upload my-cool-model ./path/to/curated/data /data/train
https://huggingface.co/Wauplin/my-cool-model/tree/main/data/train
Upload a single file
You can also upload a single file by setting local_path to point to a file on your machine. If that’s the case, path_in_repo is optional and will default to the name of your local file:

Copied
>>> hf upload Wauplin/my-cool-model ./models/model.safetensors
https://huggingface.co/Wauplin/my-cool-model/blob/main/model.safetensors
If you want to upload a single file to a specific directory, set path_in_repo accordingly:

Copied
>>> hf upload Wauplin/my-cool-model ./models/model.safetensors /vae/model.safetensors
https://huggingface.co/Wauplin/my-cool-model/blob/main/vae/model.safetensors
Upload multiple files
To upload multiple files from a folder at once without uploading the entire folder, use the --include and --exclude patterns. It can also be combined with the --delete option to delete files on the repo while uploading new ones. In the example below, we sync the local Space by deleting remote files and uploading all files except the ones in /logs:

Copied
# Sync local Space with Hub (upload new files except from logs/, delete removed files)
>>> hf upload Wauplin/space-example --repo-type=space --exclude="/logs/*" --delete="*" --commit-message="Sync local Space with Hub"
...
Upload to a dataset or Space
To upload to a dataset or a Space, use the --repo-type option:

Copied
>>> hf upload Wauplin/my-cool-dataset ./data /train --repo-type=dataset
...
Upload to an organization
To upload content to a repo owned by an organization instead of a personal repo, you must explicitly specify it in the repo_id:

Copied
>>> hf upload MyCoolOrganization/my-cool-model . .
https://huggingface.co/MyCoolOrganization/my-cool-model/tree/main/
Upload to a specific revision
By default, files are uploaded to the main branch. If you want to upload files to another branch or reference, use the --revision option:

Copied
# Upload files to a PR
>>> hf upload bigcode/the-stack . . --repo-type dataset --revision refs/pr/104
...
Note: if revision does not exist and --create-pr is not set, a branch will be created automatically from the main branch.

Upload and create a PR
If you don’t have the permission to push to a repo, you must open a PR and let the authors know about the changes you want to make. This can be done by setting the --create-pr option:

Copied
# Create a PR and upload the files to it
>>> hf upload bigcode/the-stack . . --repo-type dataset --revision refs/pr/104
https://huggingface.co/datasets/bigcode/the-stack/blob/refs%2Fpr%2F104/
Upload at regular intervals
In some cases, you might want to push regular updates to a repo. For example, this is useful if you’re training a model and you want to upload the logs folder every 10 minutes. You can do this using the --every option:

Copied
# Upload new logs every 10 minutes
hf upload training-model logs/ --every=10
Specify a commit message
Use the --commit-message and --commit-description to set a custom message and description for your commit instead of the default one

Copied
>>> hf upload Wauplin/my-cool-model ./models . --commit-message="Epoch 34/50" --commit-description="Val accuracy: 68%. Check tensorboard for more details."
...
https://huggingface.co/Wauplin/my-cool-model/tree/main
Specify a token
To upload files, you must use a token. By default, the token saved locally (using hf auth login) will be used. If you want to authenticate explicitly, use the --token option:

Copied
>>> hf upload Wauplin/my-cool-model ./models . --token=hf_****
...
https://huggingface.co/Wauplin/my-cool-model/tree/main
Quiet mode
By default, the hf upload command will be verbose. It will print details such as warning messages, information about the uploaded files, and progress bars. If you want to silence all of this, use the --quiet option. Only the last line (i.e. the URL to the uploaded files) is printed. This can prove useful if you want to pass the output to another command in a script.

Copied
>>> hf upload Wauplin/my-cool-model ./models . --quiet
https://huggingface.co/Wauplin/my-cool-model/tree/main
hf repo
hf repo lets you create, delete, move repositories and update their settings on the Hugging Face Hub. It also includes subcommands to manage branches and tags.

Create a repo
Copied
>>> hf repo create Wauplin/my-cool-model
Successfully created Wauplin/my-cool-model on the Hub.
Your repo is now available at https://huggingface.co/Wauplin/my-cool-model
Create a private dataset or a Space:

Copied
>>> hf repo create my-cool-dataset --repo-type dataset --private
>>> hf repo create my-gradio-space --repo-type space --space-sdk gradio
Use --exist-ok if the repo may already exist, and --resource-group-id to target an Enterprise resource group.

Delete a repo
Copied
>>> hf repo delete Wauplin/my-cool-model
Datasets and Spaces:

Copied
>>> hf repo delete my-cool-dataset --repo-type dataset
>>> hf repo delete my-gradio-space --repo-type space
Move a repo
Copied
>>> hf repo move old-namespace/my-model new-namespace/my-model
Update repo settings
Copied
>>> hf repo settings Wauplin/my-cool-model --gated auto
>>> hf repo settings Wauplin/my-cool-model --private true
>>> hf repo settings Wauplin/my-cool-model --private false
--gated: one of auto, manual, false
--private true|false: set repository privacy
Manage branches
Copied
>>> hf repo branch create Wauplin/my-cool-model dev
>>> hf repo branch create Wauplin/my-cool-model release-1 --revision refs/pr/104
>>> hf repo branch delete Wauplin/my-cool-model dev
All commands accept --repo-type (one of model, dataset, space) and --token if you need to authenticate explicitly. Use --help on any command to see all options.

hf repo-files
If you want to delete files from a Hugging Face repository, use the hf repo-files command.

Delete files
The hf repo-files delete <repo_id> sub-command allows you to delete files from a repository. Here are some usage examples.

Delete a folder :

Copied
>>> hf repo-files delete Wauplin/my-cool-model folder/
Files correctly deleted from repo. Commit: https://huggingface.co/Wauplin/my-cool-mo...
Delete multiple files:

Copied
>>> hf repo-files delete Wauplin/my-cool-model file.txt folder/pytorch_model.bin
Files correctly deleted from repo. Commit: https://huggingface.co/Wauplin/my-cool-mo...
Use Unix-style wildcards to delete sets of files:

Copied
>>> hf repo-files delete Wauplin/my-cool-model "*.txt" "folder/*.bin"
Files correctly deleted from repo. Commit: https://huggingface.co/Wauplin/my-cool-mo...
Specify a token
To delete files from a repo you must be authenticated and authorized. By default, the token saved locally (using hf auth login) will be used. If you want to authenticate explicitly, use the --token option:

Copied
>>> hf repo-files delete --token=hf_**** Wauplin/my-cool-model file.txt
hf cache ls
Use hf cache ls to inspect what is stored locally in your Hugging Face cache. By default it aggregates information by repository:

Copied
>>> hf cache ls
ID                          SIZE     LAST_ACCESSED LAST_MODIFIED REFS        
--------------------------- -------- ------------- ------------- ----------- 
dataset/nyu-mll/glue          157.4M 2 days ago    2 days ago    main script 
model/LiquidAI/LFM2-VL-1.6B     3.2G 4 days ago    4 days ago    main        
model/microsoft/UserLM-8b      32.1G 4 days ago    4 days ago    main  

Found 3 repo(s) for a total of 5 revision(s) and 35.5G on disk.
Add --revisions to drill down to specific snapshots, and chain filters to focus on what matters:

Copied
>>> hf cache ls --filter "size>30g" --revisions
ID                        REVISION                                 SIZE     LAST_MODIFIED REFS 
------------------------- ---------------------------------------- -------- ------------- ---- 
model/microsoft/UserLM-8b be8f2069189bdf443e554c24e488ff3ff6952691    32.1G 4 days ago    main 

Found 1 repo(s) for a total of 1 revision(s) and 32.1G on disk.
The command supports several output formats for scripting: --format json prints structured objects, --format csv writes comma-separated rows, and --quiet prints only IDs. Use --sort to order entries by accessed, modified, name, or size (append :asc or :desc to control order), and --limit to restrict results to the top N entries. Combine these with --cache-dir to target alternative cache locations. See the Manage your cache guide for advanced workflows.

Delete cache entries selected with hf cache ls --q by piping the IDs into hf cache rm:

Copied
>>> hf cache rm $(hf cache ls --filter "accessed>1y" -q) -y
About to delete 2 repo(s) totalling 5.31G.
  - model/meta-llama/Llama-3.2-1B-Instruct (entire repo)
  - model/hexgrad/Kokoro-82M (entire repo)
Delete repo: ~/.cache/huggingface/hub/models--meta-llama--Llama-3.2-1B-Instruct
Delete repo: ~/.cache/huggingface/hub/models--hexgrad--Kokoro-82M
Cache deletion done. Saved 5.31G.
Deleted 2 repo(s) and 2 revision(s); freed 5.31G.
hf cache rm
hf cache rm removes cached repositories or individual revisions. Pass one or more repo IDs (model/bert-base-uncased) or revision hashes:

Copied
>>> hf cache rm model/LiquidAI/LFM2-VL-1.6B
About to delete 1 repo(s) totalling 3.2G.
  - model/LiquidAI/LFM2-VL-1.6B (entire repo)
Proceed with deletion? [y/N]: y
Delete repo: ~/.cache/huggingface/hub/models--LiquidAI--LFM2-VL-1.6B
Cache deletion done. Saved 3.2G.
Deleted 1 repo(s) and 2 revision(s); freed 3.2G.
Mix repositories and specific revisions in the same call. Use --dry-run to preview the impact, or --yes to skip the confirmation prompt—handy in automated scripts:

Copied
>>> hf cache rm model/t5-small 8f3ad1c --dry-run
About to delete 1 repo(s) and 1 revision(s) totalling 1.1G.
  - model/t5-small:
      8f3ad1c [main] 1.1G
Dry run: no files were deleted.
When working outside the default cache location, pair the command with --cache-dir PATH.

hf cache prune
hf cache prune is a convenience shortcut that deletes every detached (unreferenced) revision in your cache. This keeps only revisions that are still reachable through a branch or tag:

Copied
>>> hf cache prune
About to delete 3 unreferenced revision(s) (2.4G total).
  - model/t5-small:
      1c610f6b [refs/pr/1] 820.1M
      d4ec9b72 [(detached)] 640.5M
  - dataset/google/fleurs:
      2b91c8dd [(detached)] 937.6M
Proceed? [y/N]: y
Deleted 3 unreferenced revision(s); freed 2.4G.
As with the other cache commands, --dry-run, --yes, and --cache-dir are available. Refer to the Manage your cache guide for more examples.

hf cache verify
Use hf cache verify to validate local files against their checksums on the Hub. You can verify either a cache snapshot or a regular local directory.

Examples:

Copied
# Verify main revision of a model in cache
>>> hf cache verify deepseek-ai/DeepSeek-OCR

# Verify a specific revision
>>> hf cache verify deepseek-ai/DeepSeek-OCR --revision refs/pr/5
>>> hf cache verify deepseek-ai/DeepSeek-OCR --revision ef93bf4a377c5d5ed9dca78e0bc4ea50b26fe6a4

# Verify a private repo
>>> hf cache verify me/private-model --token hf_***

# Verify a dataset
>>> hf cache verify karpathy/fineweb-edu-100b-shuffle --repo-type dataset

# Verify files in a local directory
>>> hf cache verify deepseek-ai/DeepSeek-OCR --local-dir /path/to/repo
By default, the command warns about missing or extra files. Use flags to turn these warnings into errors:

Copied
>>> hf cache verify deepseek-ai/DeepSeek-OCR --fail-on-missing-files --fail-on-extra-files
On success, you will see a summary:

Copied
✅ Verified 13 file(s) for 'deepseek-ai/DeepSeek-OCR' (model) in ~/.cache/huggingface/hub/models--meta-llama--Llama-3.2-1B-Instruct/snapshots/9213176726f574b556790deb65791e0c5aa438b6
  All checksums match.
If mismatches are detected, the command prints a detailed list and exits with a non-zero status.

hf repo tag create
The hf repo tag create command allows you to tag, untag, and list tags for repositories.

Tag a model
To tag a repo, you need to provide the repo_id and the tag name:

Copied
>>> hf repo tag create Wauplin/my-cool-model v1.0
You are about to create tag v1.0 on model Wauplin/my-cool-model
Tag v1.0 created on Wauplin/my-cool-model
Tag a model at a specific revision
If you want to tag a specific revision, you can use the --revision option. By default, the tag will be created on the main branch:

Copied
>>> hf repo tag create Wauplin/my-cool-model v1.0 --revision refs/pr/104
You are about to create tag v1.0 on model Wauplin/my-cool-model
Tag v1.0 created on Wauplin/my-cool-model
Tag a dataset or a Space
If you want to tag a dataset or Space, you must specify the --repo-type option:

Copied
>>> hf repo tag create bigcode/the-stack v1.0 --repo-type dataset
You are about to create tag v1.0 on dataset bigcode/the-stack
Tag v1.0 created on bigcode/the-stack
List tags
To list all tags for a repository, use the -l or --list option:

Copied
>>> hf repo tag create Wauplin/gradio-space-ci -l --repo-type space
Tags for space Wauplin/gradio-space-ci:
0.2.2
0.2.1
0.2.0
0.1.2
0.0.2
0.0.1
Delete a tag
To delete a tag, use the -d or --delete option:

Copied
>>> hf repo tag create -d Wauplin/my-cool-model v1.0
You are about to delete tag v1.0 on model Wauplin/my-cool-model
Proceed? [Y/n] y
Tag v1.0 deleted on Wauplin/my-cool-model
You can also pass -y to skip the confirmation step.

hf env
The hf env command prints details about your machine setup. This is useful when you open an issue on GitHub to help the maintainers investigate your problem.

Copied
>>> hf env

Copy-and-paste the text below in your GitHub issue.

- huggingface_hub version: 1.0.0.rc6
- Platform: Linux-6.8.0-85-generic-x86_64-with-glibc2.35
- Python version: 3.11.14
- Running in iPython ?: No
- Running in notebook ?: No
- Running in Google Colab ?: No
- Running in Google Colab Enterprise ?: No
- Token path ?: /home/wauplin/.cache/huggingface/token
- Has saved token ?: True
- Who am I ?: Wauplin
- Configured git credential helpers: store
- Installation method: unknown
- Torch: N/A
- httpx: 0.28.1
- hf_xet: 1.1.10
- gradio: 5.41.1
- tensorboard: N/A
- pydantic: 2.11.7
- ENDPOINT: https://huggingface.co
- HF_HUB_CACHE: /home/wauplin/.cache/huggingface/hub
- HF_ASSETS_CACHE: /home/wauplin/.cache/huggingface/assets
- HF_TOKEN_PATH: /home/wauplin/.cache/huggingface/token
- HF_STORED_TOKENS_PATH: /home/wauplin/.cache/huggingface/stored_tokens
- HF_HUB_OFFLINE: False
- HF_HUB_DISABLE_TELEMETRY: False
- HF_HUB_DISABLE_PROGRESS_BARS: None
- HF_HUB_DISABLE_SYMLINKS_WARNING: False
- HF_HUB_DISABLE_EXPERIMENTAL_WARNING: False
- HF_HUB_DISABLE_IMPLICIT_TOKEN: False
- HF_HUB_DISABLE_XET: False
- HF_HUB_ETAG_TIMEOUT: 10
- HF_HUB_DOWNLOAD_TIMEOUT: 10
hf jobs
Run compute jobs on Hugging Face infrastructure with a familiar Docker-like interface.

hf jobs is a command-line tool that lets you run anything on Hugging Face’s infrastructure (including GPUs and TPUs!) with simple commands. Think docker run, but for running code on A100s.

Copied
# Directly run Python code
>>> hf jobs run python:3.12 python -c 'print("Hello from the cloud!")'

# Use GPUs without any setup
>>> hf jobs run --flavor a10g-small pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel \
... python -c "import torch; print(torch.cuda.get_device_name())"

# Run in an organization account
>>> hf jobs run --namespace my-org-name python:3.12 python -c "print('Running in an org account')"

# Run from Hugging Face Spaces
>>> hf jobs run hf.co/spaces/lhoestq/duckdb duckdb -c "select 'hello world'"

# Run a Python script with `uv` (experimental)
>>> hf jobs uv run my_script.py
✨ Key Features
🐳 Docker-like CLI: Familiar commands (run, ps, logs, inspect) to run and manage jobs
🔥 Any Hardware: From CPUs to A100 GPUs and TPU pods - switch with a simple flag
📦 Run Anything: Use Docker images, HF Spaces, or your custom containers
🔐 Simple Auth: Just use your HF token
📊 Live Monitoring: Stream logs in real-time, just like running locally
💰 Pay-as-you-go: Only pay for the seconds you use
Hugging Face Jobs are available only to Pro users and Team or Enterprise organizations. Upgrade your plan to get started!

Quick Start
1. Run your first job
Copied
# Run a simple Python script
>>> hf jobs run python:3.12 python -c "print('Hello from HF compute!')"
This command runs the job and shows the logs. You can pass --detach to run the Job in the background and only print the Job ID.

2. Check job status
Copied
# List your running jobs
>>> hf jobs ps

# Inspect the status of a job
>>> hf jobs inspect <job_id>

# View logs from a job
>>> hf jobs logs <job_id>

# Cancel a job
>>> hf jobs cancel <job_id>
3. Run on GPU
You can also run jobs on GPUs or TPUs with the --flavor option. For example, to run a PyTorch job on an A10G GPU:

Copied
# Use an A10G GPU to check PyTorch CUDA
>>> hf jobs run --flavor a10g-small pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel \
... python -c "import torch; print(f"This code ran with the following GPU: {torch.cuda.get_device_name()}")"
Running this will show the following output!

Copied
This code ran with the following GPU: NVIDIA A10G
That’s it! You’re now running code on Hugging Face’s infrastructure.

Common Use Cases
Model Training: Fine-tune or train models on GPUs (T4, A10G, A100) without managing infrastructure
Synthetic Data Generation: Generate large-scale datasets using LLMs on powerful hardware
Data Processing: Process massive datasets with high-CPU configurations for parallel workloads
Batch Inference: Run offline inference on thousands of samples using optimized GPU setups
Experiments & Benchmarks: Run ML experiments on consistent hardware for reproducible results
Development & Debugging: Test GPU code without local CUDA setup
Pass Environment variables and Secrets
You can pass environment variables to your job using

Copied
# Pass environment variables
>>> hf jobs run -e FOO=foo -e BAR=bar python:3.12 python -c "import os; print(os.environ['FOO'], os.environ['BAR'])"
Copied
# Pass an environment from a local .env file
>>> hf jobs run --env-file .env python:3.12 python -c "import os; print(os.environ['FOO'], os.environ['BAR'])"
Copied
# Pass secrets - they will be encrypted server side
>>> hf jobs run -s MY_SECRET=psswrd python:3.12 python -c "import os; print(os.environ['MY_SECRET'])"
Copied
# Pass secrets from a local .env.secrets file - they will be encrypted server side
>>> hf jobs run --secrets-file .env.secrets python:3.12 python -c "import os; print(os.environ['MY_SECRET'])"
Use --secrets HF_TOKEN to pass your local Hugging Face token implicitly. With this syntax, the secret is retrieved from the environment variable. For HF_TOKEN, it may read the token file located in the Hugging Face home folder if the environment variable is unset.

Hardware
Available --flavor options:

CPU: cpu-basic, cpu-upgrade
GPU: t4-small, t4-medium, l4x1, l4x4, a10g-small, a10g-large, a10g-largex2, a10g-largex4,a100-large
TPU: v5e-1x1, v5e-2x2, v5e-2x4
(updated in 07/2025 from Hugging Face suggested_hardware docs)

UV Scripts (Experimental)
Run UV scripts (Python scripts with inline dependencies) on HF infrastructure:

Copied
# Run a UV script (creates temporary repo)
>>> hf jobs uv run my_script.py

# Run with persistent repo
>>> hf jobs uv run my_script.py --repo my-uv-scripts

# Run with GPU
>>> hf jobs uv run ml_training.py --flavor gpu-t4-small

# Pass arguments to script
>>> hf jobs uv run process.py input.csv output.parquet

# Add dependencies
>>> hf jobs uv run --with transformers --with torch train.py

# Run a script directly from a URL
>>> hf jobs uv run https://huggingface.co/datasets/username/scripts/resolve/main/example.py

# Run a command
>>> hf jobs uv run --with lighteval python -c "import lighteval"
UV scripts are Python scripts that include their dependencies directly in the file using a special comment syntax. This makes them perfect for self-contained tasks that don’t require complex project setups. Learn more about UV scripts in the UV documentation.

Scheduled Jobs
Schedule and manage jobs that will run on HF infrastructure.

The schedule should be one of @annually, @yearly, @monthly, @weekly, @daily, @hourly, or a CRON schedule expression (e.g., "0 9 * * 1" for 9 AM every Monday).

Copied
# Schedule a job that runs every hour
>>> hf jobs scheduled run @hourly python:3.12 python -c 'print("This runs every hour!")'

# Use the CRON syntax
>>> hf jobs scheduled run "*/5 * * * *" python:3.12 python -c 'print("This runs every 5 minutes!")'

# Schedule with GPU
>>> hf jobs scheduled run @hourly --flavor a10g-small pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel \
... python -c "import torch; print(f"This code ran with the following GPU: {torch.cuda.get_device_name()}")"

# Schedule a UV script
>>> hf jobs scheduled uv run @hourly my_script.py
Use the same parameters as hf jobs run to pass environment variables, secrets, timeout, etc.

Manage scheduled jobs using

Copied
# List your active scheduled jobs
>>> hf jobs scheduled ps

# Inspect the status of a job
>>> hf jobs scheduled inspect <scheduled_job_id>

# Suspend (pause) a scheduled job
>>> hf jobs scheduled suspend <scheduled_job_id>

# Resume a scheduled job
>>> hf jobs scheduled resume <scheduled_job_id>

# Delete a scheduled job
>>> hf jobs scheduled delete <scheduled_job_id>

MCP Client
The huggingface_hub library now includes an MCPClient, designed to empower Large Language Models (LLMs) with the ability to interact with external Tools via the Model Context Protocol (MCP). This client extends an AsyncInferenceClient to seamlessly integrate Tool usage.

The MCPClient connects to MCP servers (local stdio scripts or remote http/sse services) that expose tools. It feeds these tools to an LLM (via AsyncInferenceClient). If the LLM decides to use a tool, MCPClient manages the execution request to the MCP server and relays the Tool’s output back to the LLM, often streaming results in real-time.

We also provide a higher-level Agent class. This ‘Tiny Agent’ simplifies creating conversational Agents by managing the chat loop and state, acting as a wrapper around MCPClient.

MCP Client
class huggingface_hub.MCPClient
<
source
>
( model: typing.Optional[str] = Noneprovider: typing.Union[typing.Literal['black-forest-labs', 'cerebras', 'clarifai', 'cohere', 'fal-ai', 'featherless-ai', 'fireworks-ai', 'groq', 'hf-inference', 'hyperbolic', 'nebius', 'novita', 'nscale', 'openai', 'publicai', 'replicate', 'sambanova', 'scaleway', 'together', 'wavespeed', 'zai-org'], typing.Literal['auto'], NoneType] = Nonebase_url: typing.Optional[str] = Noneapi_key: typing.Optional[str] = None )

Parameters

model (str, optional) — The model to run inference with. Can be a model id hosted on the Hugging Face Hub, e.g. meta-llama/Meta-Llama-3-8B-Instruct or a URL to a deployed Inference Endpoint or other local or remote endpoint.
provider (str, optional) — Name of the provider to use for inference. Defaults to “auto” i.e. the first of the providers available for the model, sorted by the user’s order in https://hf.co/settings/inference-providers. If model is a URL or base_url is passed, then provider is not used.
base_url (str, optional) — The base URL to run inference. Defaults to None.
api_key (str, optional) — Token to use for authentication. Will default to the locally Hugging Face saved token if not provided. You can also use your own provider API key to interact directly with the provider’s service.
Client for connecting to one or more MCP servers and processing chat completions with tools.

This class is experimental and might be subject to breaking changes in the future without prior notice.

add_mcp_server
<
source
>
( type: typing.Literal['stdio', 'sse', 'http']**params: typing.Any )

Parameters

type (str) — Type of the server to connect to. Can be one of:
“stdio”: Standard input/output server (local)
“sse”: Server-sent events (SSE) server
“http”: StreamableHTTP server
**params (dict[str, Any]) — Server parameters that can be either:
For stdio servers:
command (str): The command to run the MCP server
args (list[str], optional): Arguments for the command
env (dict[str, str], optional): Environment variables for the command
cwd (Union[str, Path, None], optional): Working directory for the command
allowed_tools (list[str], optional): List of tool names to allow from this server
For SSE servers:
url (str): The URL of the SSE server
headers (dict[str, Any], optional): Headers for the SSE connection
timeout (float, optional): Connection timeout
sse_read_timeout (float, optional): SSE read timeout
allowed_tools (list[str], optional): List of tool names to allow from this server
For StreamableHTTP servers:
url (str): The URL of the StreamableHTTP server
headers (dict[str, Any], optional): Headers for the StreamableHTTP connection
timeout (timedelta, optional): Connection timeout
sse_read_timeout (timedelta, optional): SSE read timeout
terminate_on_close (bool, optional): Whether to terminate on close
allowed_tools (list[str], optional): List of tool names to allow from this server
Connect to an MCP server

cleanup
<
source
>
( )

Clean up resources

process_single_turn_with_tools
<
source
>
( messages: listexit_loop_tools: typing.Optional[list[huggingface_hub.inference._generated.types.chat_completion.ChatCompletionInputTool]] = Noneexit_if_first_chunk_no_tool: bool = False )

Parameters

messages (list[dict]) — List of message objects representing the conversation history
exit_loop_tools (list[ChatCompletionInputTool], optional) — List of tools that should exit the generator when called
exit_if_first_chunk_no_tool (bool, optional) — Exit if no tool is present in the first chunks. Default to False.
Process a query using self.model and available tools, yielding chunks and tool outputs.

Agent
class huggingface_hub.Agent
<
source
>
( model: Optional[str] = Noneservers: Iterable[ServerConfig]provider: Optional[PROVIDER_OR_POLICY_T] = Nonebase_url: Optional[str] = Noneapi_key: Optional[str] = Noneprompt: Optional[str] = None )

Parameters

model (str, optional) — The model to run inference with. Can be a model id hosted on the Hugging Face Hub, e.g. meta-llama/Meta-Llama-3-8B-Instruct or a URL to a deployed Inference Endpoint or other local or remote endpoint.
servers (Iterable[dict]) — MCP servers to connect to. Each server is a dictionary containing a type key and a config key. The type key can be "stdio" or "sse", and the config key is a dictionary of arguments for the server.
provider (str, optional) — Name of the provider to use for inference. Defaults to “auto” i.e. the first of the providers available for the model, sorted by the user’s order in https://hf.co/settings/inference-providers. If model is a URL or base_url is passed, then provider is not used.
base_url (str, optional) — The base URL to run inference. Defaults to None.
api_key (str, optional) — Token to use for authentication. Will default to the locally Hugging Face saved token if not provided. You can also use your own provider API key to interact directly with the provider’s service.
prompt (str, optional) — The system prompt to use for the agent. Defaults to the default system prompt in constants.py.
Implementation of a Simple Agent, which is a simple while loop built right on top of an MCPClient.

This class is experimental and might be subject to breaking changes in the future without prior notice.

run
<
source
>
( user_input: strabort_event: Optional[asyncio.Event] = None )

Parameters

user_input (str) — The user input to run the agent with.
abort_event (asyncio.Event, optional) — An event that can be used to abort the agent. If the event is set, the agent will stop running.
Run the agent with the given user input.

mcp-hfspace MCP Server 🤗
Tip

You can access and configure Hugging Face MCP services directly at https://hf.co/mcp, including Gradio spaces.

This project has been superceded by the official Hugging Face MCP Server and Gradio MCP Endpoints.

Alternatively you can run hf-mcp-server locally as a STDIO Server, or with robust support for SSE, Streaming HTTP and Streaming HTTP JSON Mode. This also runs a local UI for selecting tools and endpoints and supports ToolListChangedNotifications too.

hf.co/mcp
image

mcp-hfspace
Read the introduction here llmindset.co.uk/resources/mcp-hfspace/

Connect to Hugging Face Spaces with minimal setup needed - simply add your spaces and go!

By default, it connects to black-forest-labs/FLUX.1-schnell providing Image Generation capabilities to Claude Desktop.

Default Setup

Gradio MCP Support
Tip

Gradio 5.28 now has integrated MCP Support via SSE: https://huggingface.co/blog/gradio-mcp. Check out whether your target Space is MCP Enabled!

Installation
NPM Package is @llmindset/mcp-hfspace.

Install a recent version of NodeJS for your platform, then add the following to the mcpServers section of your claude_desktop_config.json file:

    "mcp-hfspace": {
      "command": "npx",
      "args": [
        "-y",
        "@llmindset/mcp-hfspace"
      ]
    }
Please make sure you are using Claude Desktop 0.78 or greater.

This will get you started with an Image Generator.

Basic setup
Supply a list of HuggingFace spaces in the arguments. mcp-hfspace will find the most appropriate endpoint and automatically configure it for usage. An example claude_desktop_config.json is supplied below.

By default the current working directory is used for file upload/download. On Windows this is a read/write folder at \users\<username>\AppData\Roaming\Claude\<version.number\, and on MacOS it is the is the read-only root: /.

It is recommended to override this and set a Working Directory for handling the upload and download of images and other file-based content. Specify either the --work-dir=/your_directory argument or MCP_HF_WORK_DIR environment variable.

An example configuration for using a modern image generator, vision model and text to speech, with a working directory set is below:

    "mcp-hfspace": {
      "command": "npx",
      "args": [
        "-y",
        "@llmindset/mcp-hfspace",
        "--work-dir=/Users/evalstate/mcp-store",
        "shuttleai/shuttle-jaguar",
        "styletts2/styletts2",
        "Qwen/QVQ-72B-preview"
      ]
    }
To use private spaces, supply your Hugging Face Token with either the --hf-token=hf_... argument or HF_TOKEN environment variable.

It's possible to run multiple server instances to use different working directories and tokens if needed.

File Handling and Claude Desktop Mode
By default, the Server operates in Claude Desktop Mode. In this mode, Images are returned in the tool responses, while other files are saved in the working folder, their file path is returned as a message. This will usually give the best experience if using Claude Desktop as the client.

URLs can also be supplied as inputs: the content gets passed to the Space.

There is an "Available Resources" prompt that gives Claude the available files and mime types from your working directory. This is currently the best way to manage files.

Example 1 - Image Generation (Download Image / Claude Vision)
We'll use Claude to compare images created by shuttleai/shuttle-3.1-aesthetic and FLUX.1-schnell. The images gets saved to the Work Directory, as well as included in Claude's context window - so Claude can use its vision capabilities.

Image Generation Comparison

Example 2 - Vision Model (Upload Image)
We'll use merve/paligemma2-vqav2 space link to query an image. In this case, we specify the filename which is available in the Working Directory: we don't want to upload the Image directly to Claude's context window. So, we can prompt Claude:

use paligemma to find out who is in "test_gemma.jpg" -> Text Output: david bowie Vision - File Upload

If you are uploading something to Claude's context use the Paperclip Attachment button, otherwise specify the filename for the Server to send directly.

We can also supply a URL. For example : use paligemma to detect humans in https://e3.365dm.com/24/12/1600x900/skynews-taylor-swift-eras-tour_6771083.jpg?20241209000914 -> One person is detected in the image - Taylor Swift on stage.

Example 3 - Text-to-Speech (Download Audio)
In Claude Desktop Mode, the audio file is saved in the WORK_DIR, and Claude is notified of the creation. If not in desktop mode, the file is returned as a base64 encoded resource to the Client (useful if it supports embedded Audio attachments).

Voice Production

Example 4 - Speech-to-Text (Upload Audio)
Here, we use hf-audio/whisper-large-v3-turbo to transcribe some audio, and make it available to Claude.

Audio Transcribe

Example 5 - Image-to-Image
In this example, we specify the filename for microsoft/OmniParser to use, and get returned an annotated Image and 2 separate pieces of text: descriptions and coordinates. The prompt used was use omniparser to analyse ./screenshot.png and use the analysis to produce an artifact that reproduces that screen. DawnC/Pawmatch is also good at this.

Omniparser and Artifact

Example 6 - Chat
In this example, Claude sets a number of reasoning puzzles for Qwen, and asks follow-up questions for clarification.

Qwen Reasoning Test

Specifying API Endpoint
If you need, you can specify a specific API Endpoint by adding it to the spacename. So rather than passing in Qwen/Qwen2.5-72B-Instruct you would use Qwen/Qwen2.5-72B-Instruct/model_chat.

Claude Desktop Mode
This can be disabled with the option --desktop-mode=false or the environment variable CLAUDE_DESKTOP_MODE=false. In this case, content as returned as an embedded Base64 encoded Resource.

Recommended Spaces
Some recommended spaces to try:

Image Generation
shuttleai/shuttle-3.1-aesthetic
black-forest-labs/FLUX.1-schnell
yanze/PuLID-FLUX
gokaygokay/Inspyrenet-Rembg (Background Removal)
diyism/Datou1111-shou_xin - Beautiful Pencil Drawings
Chat
Qwen/Qwen2.5-72B-Instruct
prithivMLmods/Mistral-7B-Instruct-v0.3
Text-to-speech / Audio Generation
fantaxy/Sound-AI-SFX
parler-tts/parler_tts
Speech-to-text
hf-audio/whisper-large-v3-turbo
(the openai models use unnamed parameters so will not work)
Text-to-music
haoheliu/audioldm2-text2audio-text2music
Vision Tasks
microsoft/OmniParser
merve/paligemma2-vqav2
merve/paligemma-doc
DawnC/PawMatchAI
DawnC/PawMatchAI/on_find_match_click - for interactive dog recommendations
Other Features
Prompts
Prompts for each Space are generated, and provide an opportunity to input. Bear in mind that often Spaces aren't configured with particularly helpful labels etc. Claude is actually very good at figuring this out, and the Tool description is quite rich (but not visible in Claude Desktop).

Resources
A list of files in the WORK_DIR is returned, and as a convenience returns the name as "Use the file..." text. If you want to add something to Claude's context, use the paperclip - otherwise specify the filename for the MCP Server. Claude does not support transmitting resources from within Context.

Private Spaces
Private Spaces are supported with a HuggingFace token. The Token is used to download and save generated content.

Using Claude Desktop
To use with Claude Desktop, add the server config:

On MacOS: ~/Library/Application Support/Claude/claude_desktop_config.json On Windows: %APPDATA%/Claude/claude_desktop_config.json

{
  "mcpServers": {
    "mcp-hfspace": {
      "command": "npx"
      "args": [
        "-y",
        "@llmindset/mcp-hfspace",
        "--work-dir=~/mcp-files/ or x:/temp/mcp-files/",
        "--HF_TOKEN=HF_{optional token}"
        "Qwen/Qwen2-72B-Instruct",
        "black-forest-labs/FLUX.1-schnell",
        "space/example/specific-endpint"
        (... and so on)
        ]
    }
  }
}
Known Issues and Limitations
mcp-hfspace
Endpoints with unnamed parameters are unsupported for the moment.
Full translation from some complex Python types to suitable MCP formats.
Claude Desktop
Claude Desktop 0.75 doesn't seem to respond to errors from the MCP Server, timing out instead. For persistent issues, use the MCP Inspector to get a better look at diagnosing what's going wrong. If something suddenly stops working, it's probably due to exhausting your HuggingFace ZeroGPU quota - try again after a short period, or set up your own Space for hosting.
Claude Desktop seems to use a hard timeout value of 60s, and doesn't appear to use Progress Notifications to manage UX or keep-alive. If you are using ZeroGPU spaces, large/heavy jobs may timeout. Check the WORK_DIR for results though; the MCP Server will still capture and save the result if it was produced.
Claude Desktops reporting of Server Status, logging etc. isn't great - use @modelcontextprotocol/inspector to help diagnose issues.
HuggingFace Spaces
If ZeroGPU quotas or queues are too long, try duplicating the space. If your job takes less than sixty seconds, you can usually change the function decorator @spaces.GPU(duration=20) in app.py to request less quota when running the job.
Passing HF_TOKEN will make ZeroGPU quotas apply to your (Pro) HF account
If you have a private space, and dedicated hardware your HF_TOKEN will give you direct access to that - no quota's apply. I recommend this if you are using for any kind of Production task.
