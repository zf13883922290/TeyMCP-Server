Magic UI MCP Server

Installation

Copy Page



Previous

Next

How to install dependencies and structure your app.



Note: We have the exact same installation process as shadcn/ui.



Create project

Run the init command to create a new Next.js project or to setup an existing one:



pnpm

npm

yarn

bun

pnpm dlx shadcn@latest init

Copy

Add components

You can now start adding components to your project.



pnpm

npm

yarn

bun

pnpm dlx shadcn@latest add @magicui/globe

Copy

Import component

The command above will add the Globe component to your project. You can then import it like this:



Copy

import { Globe } from "@/components/ui/globe"

&nbsp;

export default function Home() {

&nbsp; return <Globe />

}
Copy Page

Previous
Next
Learn how to use the Model Context Protocol with Magic UI.

Magic UI now has an official MCP server 🎉.

MCP is an open protocol that standardizes how applications provide context to LLMs.

This is useful for Magic UI because you can now give your AI-assisted IDE direct access to all Magic UI components so that it can generate code with minimal errors.

CLI
Manual
Installation
Cursor
Windsurf
Claude
Cline
Roo-Cline
pnpm
npm
yarn
bun
pnpm dlx @magicuidesign/cli@latest install cursor
Copy
Restart your IDE
Usage
You can now ask your IDE to use any Magic UI component. Here are some examples:

"Add a blur fade text animation"
"Add a grid background"
"Add a vertical marquee of logos"

