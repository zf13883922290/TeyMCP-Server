msal-node
TypeScript icon, indicating that this package has built-in type declarations
3.8.1 • Public • Published 7 days ago
Microsoft Authentication Library for Node (msal-node)
npm version npm version codecov

Getting Started	AAD Docs	Library Reference
About
FAQ
Changelog
Prerequisites
Installation
Node Version Support
Usage
Samples
Build Library
Security Reporting
License
Code of Conduct
About
MSAL Node enables applications to authenticate users using Azure AD work and school accounts (AAD), Microsoft personal accounts (MSA) and social identity providers like Facebook, Google, LinkedIn, Microsoft accounts, etc. through Azure AD B2C service. It also enables your app to get tokens to access Microsoft Cloud services such as Microsoft Graph.

OAuth2.0 grant types supported:
The current version supports the following ways of acquiring tokens:

Public Client:
Authorization Code Grant with PKCE
Device Code Grant
Refresh Token Grant
Silent Flow
Username and Password flow
Confidential Client:
Authorization Code Grant with a client credential
Refresh Token Grant
Silent Flow
Client Credential Grant
On-behalf-of flow
Username and Password flow
Note that the username and password flow is deprecated and support will be removed in a future release.

More details on different grant types supported by Microsoft authentication libraries in general can be found here.

Scenarios supported:
The scenarios supported with this library are:

Desktop app that calls web APIs
Web app that calls web APIs
Web APIs that call web APIs
Daemon apps
More details on scenarios and the authentication flows that map to each of them can be found here.

FAQ
See here.

Prerequisites
Before using @azure/msal-node you will need to register your app in the azure portal:

App registration
Installation
Via NPM:
npm install @azure/msal-node
Node Version Support
MSAL Node will follow the Long Term Support (LTS) schedule of the Node.js project. Our support plan is as follows.

Any major MSAL Node release:

Will support stable (even-numbered) Maintenance LTS, Active LTS, and Current versions of Node
Will drop support for any previously supported Node versions that have reached end of life
Will not support prerelease/preview/pending versions until they are stable
MSAL Node version	MSAL support status	Supported Node versions
3.x.x	Active development	16, 18, 20, 22, 24
2.x.x	Active development	16, 18, 20, 22
1.x.x	In maintenance	10, 12, 14, 16, 18
Note: There have been no functional changes in the MSAL Node v2 release.

Usage
MSAL basics
Understand difference in between Public Client and Confidential Clients
Initialize a Public Client Application
Initialize a Confidential Client Application
Configuration
Request
Response
Samples
There are multiple samples included in the repository that use MSAL Node to acquire tokens. These samples are currently used for manual testing, and are not meant to be a reference of best practices, therefore use judgement and do not blindly copy this code to any production applications.

AAD samples:

auth-code: Express app using OAuth2.0 authorization code flow.
auth-code-pkce: Express app using OAuth2.0 authorization code flow with PKCE.
device-code: Command line app using OAuth 2.0 device code flow.
refresh-token: Command line app using OAuth 2.0 refresh flow.
silent-flow: Express app using OAuth2.0 authorization code flow to acquire a token and store in the token cache, and silent flow to use tokens in the token cache.
client-credentials: Daemon app using OAuth 2.0 client credential grant to acquire a token.
on-behalf-of: Web application using OAuth 2.0 auth code flow to acquire a token for a web API. The web API validates the token, and calls Microsoft Graph on behalf of the user who authenticated in the web application.
username-password: Web application using OAuth 2.0 resource owner password credentials (ROPC) flow to acquire a token for a web API.
ElectronTestApp: Electron desktop application using OAuth 2.0 auth code with PKCE flow to acquire a token for a web API such as Microsoft Graph.
Hybrid Spa Sample: Sample demonstrating how to use enableSpaAuthorizationCode to perform SSO for applications that leverage server-side and client-side authentication using MSAL Browser and MSAL Node.
B2C samples:

b2c-user-flows: Express app using OAuth2.0 authorization code flow.
Others:

msal-node-extensions: Uses authorization code flow to acquire tokens and the msal-extensions library to write the MSAL in-memory token cache to disk.
Build and Test
// Install dependencies from root of repo
npm install

// Change to the msal-node package directory
cd lib/msal-node

// To run build for common package & node package
npm run build:all

// To run build only for node package
npm run build

// To run tests
npm run test
Local Development
Below is a list of commands you will probably find useful:

npm run build:modules:watch
Runs the project in development/watch mode. Your project will be rebuilt upon changes. TSDX has a special logger for you convenience. Error messages are pretty printed and formatted for compatibility VS Code's Problems tab. The library will be rebuilt if you make edits.

npm run build
Bundles the package to the dist folder. The package is optimized and bundled with Rollup into multiple formats (CommonJS, UMD, and ES Module).

npm run build:all
Builds both msal-common and msal-node

npm run lint
Runs eslint with Prettier

npm test, npm run test:coverage, npm run test:watch
Runs the test watcher (Jest) in an interactive mode. By default, runs tests related to files changed since the last commit. Generate code coverage by adding the flag --coverage. No additional setup needed. Jest can collect code coverage information from entire projects, including untested files.

Security Reporting
If you find a security issue with our libraries or services please report it to secure@microsoft.com with as much detail as possible. Your submission may be eligible for a bounty through the Microsoft Bounty program. Please do not post security issues to GitHub Issues or any other public site. We will contact you shortly upon receiving the information. We encourage you to get notifications of when security incidents occur by visiting this page and subscribing to Security Advisory Alerts.

License
Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT License.

We Value and Adhere to the Microsoft Open Source Code of Conduct
This project has adopted the Microsoft Open Source Code of Conduct. For more information see the Code of Conduct FAQ or contact opencode@microsoft.com with any additional questions or comments.

Readme
Keywords
jstsnodeAADmsaloauth
Package Sidebar
Install
npm i @azure/msal-node


Repository
github.com/AzureAD/microsoft-authentication-library-for-js

Homepage
github.com/AzureAD/microsoft-authentication-library-for-js#readme