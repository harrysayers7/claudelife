---
date: "{{date}} {{time}}"
relation:
  - "[[97-tags/claude-code|claude-code]]"
  - "[[97-tags/AI-Research]]"
  - "[[mcp]]"
tags:
description:
date created: Fri, 10 3rd 25, 11:07:07 am
date modified: Fri, 10 3rd 25, 11:11:04 am
---
Use Claude Code as an MCP server
You can use Claude Code itself as an MCP server that other applications can connect to:
#start CLaude as a stdio MCP server claude mcp serve
You can use this in Claude Desktop by adding this configuration to claude_desktop_config.json:
"mcpServers":
"claude-code": f "command": "claude" "args": ["mcp", "serve"], "env":
Tips:
The server provides access to Claude's tools like View, Edit, LS. etc.
In Claude Desktop, try asking Claude to read files in a directory, make edits, and more.
Note that this MCP server is simply exposing Claude Code's tools to your MCP client, so your own client is responsible for implementing user confirmation for individual tool calls.
