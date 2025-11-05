Microsoft Graph JavaScript Client Library
npm version badge Known Vulnerabilities Licence code style: prettier Downloads

The Microsoft Graph JavaScript client library is a lightweight wrapper around the Microsoft Graph API that can be used server-side and in the browser.

Microsoft Graph JavaScript Client Library
Installation
Via npm
Via Script Tag
Getting started
1. Register your application
2. Create a Client Instance
3. Make requests to the graph
Documentation
HTTP Actions
Chained APIs to call Microsoft Graph
OData system query options - Query Parameters
Batch multiple requests into single HTTP request
Cancel a HTTP request
Configurations to your request
Query
Version
Headers
Options
MiddlewareOptions
ResponseType
Upload large files to OneDrive, Outlook, Print API
Page Iteration
Getting Raw Response
Creating an instance of TokenCredentialAuthenticationProvider
Samples and tutorials
Step-by-step training exercises on creating a basic application using the Microsoft Graph JavaScript SDK:
Build Angular single-page apps with Microsoft Graph
Build Node.js Express apps with Microsoft Graph
Build React Native apps with Microsoft Graph
Build React single-page apps with Microsoft Graph
Build JavaScript single-page apps with Microsoft Graph
Explore Microsoft Graph scenarios for JavaScript development
Samples using TokenCredentialAuthenticationProvider with the @azure/identity library:
TokenCredentialAuthenticationProvider Samples
Samples using LargeFileUploadTask and OneDriveLargeFileTask:
LargeFileUploadTask Samples
Samples to learn more about authentication using MSALlibraries:
Azure-Sample Vanilla JS SPA using MSAL Browser and Microsoft Graph JavaScript SDK
Azure-Sample Angular SPA using MSAL Angular and Microsoft Graph JavaScript SDK
Azure-Sample React SPA using MSAL React and Microsoft Graph JavaScript SDK
Questions and comments
Contributing
Additional resources
Third Party Notices
Security Reporting
License
We Value and Adhere to the Microsoft Open Source Code of Conduct
Looking for IntelliSense on models (Users, Groups, etc.)? Check out the Microsoft Graph Types v1.0 and beta!!

TypeScript demo

Node version requirement
Node.js 12 LTS or higher. The active Long Term Service (LTS) version of Node.js is used for on-going testing of existing and upcoming product features.

For Node.js 18 users, it is recommended to disable the experimental fetch feature by supplying the --no-experimental-fetch command-line flag while using the Microsoft Graph JavaScript client library.

Installation
Via npm
npm install @microsoft/microsoft-graph-client
import @microsoft/microsoft-graph-client into your module.

Also, you will need to import any fetch polyfill which suits your requirements. Following are some fetch polyfills -

isomorphic-fetch.
cross-fetch
whatwg-fetch
import "isomorphic-fetch"; // or import the fetch polyfill you installed
import { Client } from "@microsoft/microsoft-graph-client";
Via Script Tag
Include graph-js-sdk.js in your HTML page.

<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/@microsoft/microsoft-graph-client/lib/graph-js-sdk.js"></script>
In case your browser doesn't have support for Fetch [support] or Promise [support], you need to use polyfills like github/fetch for fetch and es6-promise for promise.

<!-- polyfilling promise -->
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/es6-promise/dist/es6-promise.auto.min.js"></script>

<!-- polyfilling fetch -->
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/whatwg-fetch/dist/fetch.umd.min.js"></script>

<!-- depending on your browser you might wanna include babel polyfill -->
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/@babel/polyfill@7.4.4/dist/polyfill.min.js"></script>
Getting started
1. Register your application
To call Microsoft Graph, your app must acquire an access token from the Microsoft identity platform. Learn more about this -

Authentication and authorization basics for Microsoft Graph
Register your app with the Microsoft identity platform
2. Create a Client Instance
The Microsoft Graph client is designed to make it simple to make calls to Microsoft Graph. You can use a single client instance for the lifetime of the application.

For information on how to create a client instance, see Creating Client Instance

3. Make requests to the graph
Once you have authentication setup and an instance of Client, you can begin to make calls to the service. All requests should start with client.api(path) and end with an action.

Example of getting user details:

try {
	let userDetails = await client.api("/me").get();
	console.log(userDetails);
} catch (error) {
	throw error;
}
Example of sending an email to the recipients:

// Construct email object
const mail = {
	subject: "Microsoft Graph JavaScript Sample",
	toRecipients: [
		{
			emailAddress: {
				address: "example@example.com",
			},
		},
	],
	body: {
		content: "<h1>MicrosoftGraph JavaScript Sample</h1>Check out https://github.com/microsoftgraph/msgraph-sdk-javascript",
		contentType: "html",
	},
};
try {
	let response = await client.api("/me/sendMail").post({ message: mail });
	console.log(response);
} catch (error) {
	throw error;
}
For more information, refer: Calling Pattern, Actions, Query Params, API Methods and more.

Samples and tutorials
Step-by-step training exercises that guide you through creating a basic application that accesses data via the Microsoft Graph:

Build Angular single-page apps with Microsoft Graph
Build Node.js Express apps with Microsoft Graph
Build React Native apps with Microsoft Graph
Build React single-page apps with Microsoft Graph
Build JavaScript single-page apps with Microsoft Graph
Explore Microsoft Graph scenarios for JavaScript development
The Microsoft Graph JavaScript SDK provides a TokenCredentialAuthenticationProvider to authenticate using the @azure/identity auth library. Learn more:

Documentation for creating an instance of TokenCredentialAuthenticationProvider
TokenCredentialAuthenticationProvider Samples
The Microsoft Graph JavaScript SDK provides a LargeFileUploadTask to upload large files to OneDrive, Outlook and Print API:

LargeFileUploadTask documentation

Samples using LargeFileUploadTask and OneDriveLargeFileTask The following MSAL samples provide information on authentication using MSAL libraries and how to use the Microsoft Graph JavaScript SDK client with MSAL as a custom authentication provider to query the Graph API:

Azure-Sample Vanilla JS SPA using MSAL Browser and Microsoft Graph JavaScript SDK

Azure-Sample Angular SPA using MSAL Angular and Microsoft Graph JavaScript SDK

Azure-Sample React SPA using MSAL React and Microsoft Graph JavaScript SDK

Questions and comments
We'd love to get your feedback about the Microsoft Graph JavaScript client library. You can send your questions and suggestions to us in the Issues section of this repository.

Contributing
Please see the contributing guidelines.

Additional resources
Microsoft Graph website
The Microsoft Graph TypeScript definitions enable editors to provide intellisense on Microsoft Graph objects including users, messages, and groups.
@microsoft/microsoft-graph-types or @types/microsoft-graph
@microsoft/microsoft-graph-types-beta
Microsoft Graph Toolkit: UI Components and Authentication Providers for Microsoft Graph
Office Dev Center
Tips and Tricks
Microsoft Graph SDK n.call is not a function by Lee Ford
Example of using the Graph JS library with ESM and importmaps
Third Party Notices
See Third Party Notices for information on the packages that are included in the package.json

Security Reporting
If you find a security issue with our libraries or services please report it to secure@microsoft.com with as much detail as possible. Your submission may be eligible for a bounty through the Microsoft Bounty program. Please do not post security issues to GitHub Issues or any other public site. We will contact you shortly upon receiving the information. We encourage you to get notifications of when security incidents occur by visiting this page and subscribing to Security Advisory Alerts.

License
Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT License (the "License");

We Value and Adhere to the Microsoft Open Source Code of Conduct
This project has adopted the Microsoft Open Source Code of Conduct. For more information see the Code of Conduct FAQ or contact opencode@microsoft.com with any additional questions or comments.

Readme
Keywords
MicrosoftGraphSDKJavaScriptClient
Package Sidebar
Install
npm i @microsoft/microsoft-graph-client


Repository
github.com/microsoftgraph/msgraph-sdk-javascript

Homepage
github.com/microsoftgraph/msgraph-sdk-javascript#readme