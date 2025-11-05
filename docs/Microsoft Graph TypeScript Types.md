Microsoft Graph TypeScript Types
The Microsoft Graph TypeScript definitions enable editors to provide intellisense on Microsoft Graph objects including users, messages, and groups.

NOTE: The Microsoft Graph TypeScript Types Beta npm package and GitHub repo is now available. Imports from the microsoftgraph/msgraph-typescript-typings#beta branch will no longer be supported.

Installation
We recommend including the .d.ts file by downloading this package through npm.

# Install types and save in package.json as a development dependency
npm install @microsoft/microsoft-graph-types --save-dev
GIF showing intellisense and autocompletion for Microsoft Graph entities in Visual Studio Code 

Examples
The following examples assume that you have a valid access token. The following example uses isomorphic-fetch and Microsoft Graph JavaScript client library -

import { User } from "@microsoft/microsoft-graph-types-beta";

import { Client } from "@microsoft/microsoft-graph-client";

import 'isomorphic-fetch';

const client = Client.initWithMiddleware({
	defaultVersion: 'beta',
    ...
});

const response = await client.api("/me").get();
const user = response as User;
Example of creating an object
// Create the message object

// Note that all the properties must follow the interface definitions.
// For example, this will not compile if you try to type "xml" instead of "html" for contentType.

let mail:MicrosoftGraphBeta.Message = {
    subject: "Microsoft Graph TypeScript Sample",
    toRecipients: [{
        emailAddress: {
            address: "microsoftgraph@example.com"
        }
    }],
    body: {
        content: "<h1>Microsoft Graph TypeScript Sample</h1>Try modifying the sample",
        contentType: "html"
    }
}
Example of using v1 types and beta types together
  "devDependencies": {
    // import published v1.0 types with a version from NPM
    "@microsoft/microsoft-graph-types": "^0.4.0",
    // import beta types with a version from NPM
    "@microsoft/microsoft-graph-types-beta": "^0.1.0-preview"
  }
}
import * as MicrosoftGraph from "@microsoft/microsoft-graph-types"

import * as MicrosoftGraphBeta from "@microsoft/microsoft-graph-types-beta"

const v1User: MicrosoftGraph.User = {
	givenName: "V1 User"
}

const betaUser: MicrosoftGraphBeta.User = {
	givenName: "Beta User"
}
Supported editors
Any TypeScript project can consume these types when using at least TypeScript 2.0. We've tested including the types as a dependency in the following editors.

Visual Studio Code
WebStorm
Atom with the atom-typescript plugin
Questions and comments
We'd love to get your feedback about the TypeScript definitions project. You can send your questions and suggestions to us in the Issues section of this repository.

Contributing
Please see the contributing guidelines.

Additional resources
Microsoft Graph
Office Dev Center
Microsoft Graph JavaScript Client Library
Security Reporting
If you find a security issue with our libraries or services please report it to secure@microsoft.com with as much detail as possible. Your submission may be eligible for a bounty through the Microsoft Bounty program. Please do not post security issues to GitHub Issues or any other public site. We will contact you shortly upon receiving the information. We encourage you to get notifications of when security incidents occur by visiting this page and subscribing to Security Advisory Alerts.

License
Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT License (the "License");

We Value and Adhere to the Microsoft Open Source Code of Conduct
This project has adopted the Microsoft Open Source Code of Conduct. For more information see the Code of Conduct FAQ or contact opencode@microsoft.com with any additional questions or comments.

Readme
Keywords
none
Package Sidebar
Install
npm i @microsoft/microsoft-graph-types


Repository
github.com/microsoftgraph/msgraph-typescript-typings

Homepage
github.com/microsoftgraph/msgraph-typescript-typings#readme