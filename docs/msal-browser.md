msal-browser
TypeScript icon, indicating that this package has built-in type declarations
4.26.0 • Public • Published 7 days ago
Microsoft Authentication Library for JavaScript (MSAL.js) for Browser-Based Single-Page Applications
npm version npm version codecov

Getting Started	AAD Docs	Library Reference
About
FAQ
Changelog
Roadmap
Prerequisites
Installation
Usage
Migrating from Previous MSAL Versions
MSAL Basics
Advanced Topics
Samples
Build and Test
Authorization Code vs Implicit
Framework Wrappers
Security Reporting
License
Code of Conduct
About
The MSAL library for JavaScript enables client-side JavaScript applications to authenticate users using Azure AD work and school accounts (AAD), Microsoft personal accounts (MSA) and social identity providers like Facebook, Google, LinkedIn, Microsoft accounts, etc. through Azure AD B2C service. It also enables your app to get tokens to access Microsoft Cloud services such as Microsoft Graph.

The @azure/msal-browser package described by the code in this folder uses the @azure/msal-common package as a dependency to enable authentication in JavaScript Single-Page Applications without backend servers. This version of the library uses the OAuth 2.0 Authorization Code Flow with PKCE. To read more about this protocol, as well as the differences between implicit flow and authorization code flow, see the section below.

This is an improvement upon the previous @azure/msal library which will utilize the authorization code flow in the browser. Most features available in the old library will be available in this one, but there are nuances to the authentication flow in both. The @azure/msal-browser package does NOT support the implicit flow.

FAQ
See here.

Roadmap
See here.

Prerequisites
@azure/msal-browser is meant to be used in Single-Page Application scenarios.

Before using @azure/msal-browser you will need to register a Single Page Application in Azure AD to get a valid clientId for configuration, and to register the routes that your app will accept redirect traffic on.

Installation
Via NPM
npm install @azure/msal-browser
Usage
Migrating from Previous MSAL Versions
Migrating from MSAL v1.x to MSAL v2.x
Migrating from MSAL v2.x to MSAL v3.x
MSAL Basics
Initialization
Logging in a User
Acquiring and Using an Access Token
Managing Token Lifetimes
Managing Accounts
Logging Out a User
Advanced Topics
Configuration Options
Request and Response Details
Cache Storage
Performance Enhancements
Instance Aware Flow
Samples
The msal-browser-samples folder contains sample applications for our libraries.

More instructions to run the samples can be found in the README.md file of the VanillaJSTestApp2.0 folder.

More advanced samples backed with a tutorial can be found in the Azure Samples space on GitHub:

JavaScript SPA calling Express.js web API
JavaScript SPA calling Microsoft Graph via Express.js web API using on-behalf-of flow
Deployment tutorial for Azure App Service and Azure Storage
We also provide samples for addin/plugin scenarios:

Office Addin-in using MSAL.js
Teams Tab using MSAL.js
Chromium Extension using MSAL.js
Build and Test
See the contributing.md file for more information.

Building the package
To build the @azure/msal-browser library, you can do the following:

// Change to the msal-browser package directory
cd lib/msal-browser/
// To run build only for browser package
npm run build
To build both the @azure/msal-browser library and @azure/msal-common libraries, you can do the following:

// Change to the msal-browser package directory
cd lib/msal-browser/
// To run build for both browser and common packages
npm run build:all
Running Tests
@azure/msal-browser uses jest to run unit tests.

// To run tests
npm test
// To run tests with code coverage
npm run test:coverage
Implicit Flow vs Authorization Code Flow with PKCE
@azure/msal-browser implements the OAuth 2.0 Authorization Code Flow with PKCE for browser-based applications. This is a significant improvement over the Implicit Flow that was used in @azure/msal, msal or adal-angular.

Authorization Code Flow with PKCE
The Authorization Code Flow with Proof Key for Code Exchange (PKCE) is the current industry standard for securing OAuth 2.0 authorization in public clients, including single-page applications (SPAs). Key benefits include:

Enhanced Security: PKCE provides protection against authorization code interception attacks
No Tokens in URLs: Tokens are never exposed in the browser's URL or history
Refresh Token Support: Enables long-lived sessions through refresh tokens
OIDC Compliance: Fully compliant with OpenID Connect standards
Implicit Flow (Deprecated)
The Implicit Flow was the previous standard for SPAs but has been deprecated due to security concerns:

Tokens in URLs: Access tokens are returned in URL fragments, making them visible in browser history and server logs
No Refresh Tokens: Implicit flow cannot securely deliver refresh tokens to public clients
Increased Attack Surface: Tokens are more susceptible to token leakage attacks
Migration Considerations
@azure/msal-browser only supports Authorization Code Flow with PKCE - Implicit Flow is not supported
If you're migrating from @azure/msal, msal or adal-angular, see our migration guide
Your Azure AD app registration needs to be configured for the Authorization Code Flow
Existing applications using Implicit Flow should migrate to Authorization Code Flow for improved security
For more technical details about these flows, refer to the Microsoft identity platform documentation.

Framework Wrappers
If you are using a framework such as Angular or React you may be interested in using one of our wrapper libraries:

Angular: @azure/msal-angular v2
React: @azure/msal-react
Security Reporting
If you find a security issue with our libraries or services please report it to secure@microsoft.com with as much detail as possible. Your submission may be eligible for a bounty through the Microsoft Bounty program. Please do not post security issues to GitHub Issues or any other public site. We will contact you shortly upon receiving the information. We encourage you to get notifications of when security incidents occur by visiting this page and subscribing to Security Advisory Alerts.

License
Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT License.

We Value and Adhere to the Microsoft Open Source Code of Conduct
This project has adopted the Microsoft Open Source Code of Conduct. For more information see the Code of Conduct FAQ or contact opencode@microsoft.com with any additional questions or comments.

Readme
Keywords
implicitauthorization codePKCEjsAADmsaloauth
Package Sidebar
Install
npm i @azure/msal-browser


Repository
github.com/AzureAD/microsoft-authentication-library-for-js

Homepage
github.com/AzureAD/microsoft-authentication-library-for-js#readme