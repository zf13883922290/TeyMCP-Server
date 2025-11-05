GitHub Remote MCP Integration Guide for MCP Host Authors
This guide outlines high-level considerations for MCP Host authors who want to allow installation of the Remote GitHub MCP server.

The goal is to explain the architecture at a high-level, define key requirements, and provide guidance to get you started, while pointing to official documentation for deeper implementation details.

Table of Contents
Understanding MCP Architecture
Connecting to the Remote GitHub MCP Server
Authentication and Authorization
OAuth Support on GitHub
Create an OAuth-enabled App Using the GitHub UI
Things to Consider
Initiating the OAuth Flow from your Client Application
Handling Organization Access Restrictions
Essential Security Considerations
Additional Resources
Understanding MCP Architecture
The Model Context Protocol (MCP) enables seamless communication between your application and various external tools through an architecture defined by the MCP Standard.

High-level Architecture
The diagram below illustrates how a single client application can connect to multiple MCP Servers, each providing access to a unique set of resources. Notice that some MCP Servers are running locally (side-by-side with the client application) while others are hosted remotely. GitHub's MCP offerings are available to run either locally or remotely.


Runtime Environment
Application: The user-facing application you are building. It instantiates one or more MCP clients and orchestrates tool calls.
MCP Client: A component within your client application that maintains a 1:1 connection with a single MCP server.
MCP Server: A service that provides access to a specific set of tools.
Local MCP Server: An MCP Server running locally, side-by-side with the Application.
Remote MCP Server: An MCP Server running remotely, accessed via the internet. Most Remote MCP Servers require authentication via OAuth.
For more detail, see the official MCP specification.

Note

GitHub offers both a Local MCP Server and a Remote MCP Server.

Connecting to the Remote GitHub MCP Server
Authentication and Authorization
GitHub MCP Servers require a valid access token in the Authorization header. This is true for both the Local GitHub MCP Server and the Remote GitHub MCP Server.

For the Remote GitHub MCP Server, the recommended way to obtain a valid access token is to ensure your client application supports OAuth 2.1. It should be noted, however, that you may also supply any valid access token. For example, you may supply a pre-generated Personal Access Token (PAT).

Important

The Remote GitHub MCP Server itself does not provide Authentication services. Your client application must obtain valid GitHub access tokens through one of the supported methods.

The expected flow for obtaining a valid access token via OAuth is depicted in the MCP Specification. For convenience, we've embedded a copy of the authorization flow below. Please study it carefully as the remainder of this document is written with this flow in mind.


Note

Dynamic Client Registration is NOT supported by Remote GitHub MCP Server at this time.

OAuth Support on GitHub
GitHub offers two solutions for obtaining access tokens via OAuth: GitHub Apps and OAuth Apps. These solutions are typically created, administered, and maintained by GitHub Organization administrators. Collaborate with a GitHub Organization administrator to configure either a GitHub App or an OAuth App to allow your client application to utilize GitHub OAuth support. Furthermore, be aware that it may be necessary for users of your client application to register your GitHub App or OAuth App within their own GitHub Organization in order to generate authorization tokens capable of accessing Organization's GitHub resources.

Tip

Before proceeding, check whether your organization already supports one of these solutions. Administrators of your GitHub Organization can help you determine what GitHub Apps or OAuth Apps are already registered. If there's an existing GitHub App or OAuth App that fits your use case, consider reusing it for Remote MCP Authorization. That said, be sure to take heed of the following warning.

Warning

Both GitHub Apps and OAuth Apps require the client application to pass a "client secret" in order to initiate the OAuth flow. If your client application is designed to run in an uncontrolled environment (i.e. customer-provided hardware), end users will be able to discover your "client secret" and potentially exploit it for other purposes. In such cases, our recommendation is to register a new GitHub App (or OAuth App) exclusively dedicated to servicing OAuth requests from your client application.

Create an OAuth-enabled App Using the GitHub UI
Detailed instructions for creating a GitHub App can be found at "Creating GitHub Apps". (RECOMMENDED)
Detailed instructions for creating an OAuth App can be found "Creating an OAuth App".

For guidance on which type of app to choose, see "Differences Between GitHub Apps and OAuth Apps".

Things to Consider:
Tokens provided by GitHub Apps are generally more secure because they:
include an expiration
include support for fine-grained permissions
GitHub Apps must be installed on a GitHub Organization before they can be used.
In general, installation must be approved by someone in the Organization with administrator permissions. For more details, see this explanation.
By contrast, OAuth Apps don't require installation and, typically, can be used immediately.
Members of an Organization may use the GitHub UI to request that a GitHub App be installed organization-wide.
While not strictly necessary, if you expect that a wide range of users will use your MCP Server, consider publishing its corresponding GitHub App or OAuth App on the GitHub App Marketplace to ensure that it's discoverable by your audience.
Initiating the OAuth Flow from your Client Application
For GitHub Apps, details on initiating the OAuth flow from a client application are described in detail here.

For OAuth Apps, details on initiating the OAuth flow from a client application are described in detail here.

Important

For endpoint discovery, be sure to honor the WWW-Authenticate information provided by the Remote GitHub MCP Server rather than relying on hard-coded endpoints like https://github.com/login/oauth/authorize.

Handling Organization Access Restrictions
Organizations may block GitHub Apps and OAuth Apps until explicitly approved. Within your client application code, you can provide actionable next steps for a smooth user experience in the event that OAuth-related calls fail due to your GitHub App or OAuth App being unavailable (i.e. not registered within the user's organization).

Detect the specific error.
Notify the user clearly.
Depending on their GitHub organization privileges:
Org Members: Prompt them to request approval from a GitHub organization admin, within the organization where access has not been approved.
Org Admins: Link them to the corresponding GitHub organization’s App approval settings at https://github.com/organizations/[ORG_NAME]/settings/oauth_application_policy
Essential Security Considerations
Token Storage: Use secure platform APIs (e.g. keytar for Node.js).
Input Validation: Sanitize all tool arguments.
HTTPS Only: Never send requests over plaintext HTTP. Always use HTTPS in production.
PKCE: We strongly recommend implementing PKCE for all OAuth flows to prevent code interception, to prepare for upcoming PKCE support.
Additional Resources
MCP Official Spec
MCP SDKs
GitHub Docs on Creating GitHub Apps
GitHub Docs on Using GitHub Apps
GitHub Docs on Creating OAuth Apps
GitHub Docs on Installing OAuth Apps into a Personal Account and Organization
Managing OAuth Apps at the Organization Level
Managing Programmatic Access at the GitHub Organization Level
Building Copilot Extensions
Managing App/Extension Visibility (including GitHub Marketplace information)
Example Implementation in VS Code Repository