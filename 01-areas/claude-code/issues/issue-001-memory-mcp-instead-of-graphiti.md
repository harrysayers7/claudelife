---
title: Memory MCP enabled instead of Graphiti MCP
type:
  - issue
aliases:
  - issue-001
id: issue-001
category: mcp-server
relation:
complete: true
solved: true
lesson:
created: Sat, 10 18th 25, 11:50:00 am
severity: medium
attempted-solutions:
  - Tested both "memory" and "graphiti" MCP servers
  - Confirmed "memory" is generic JSON-based server
  - Confirmed "graphiti" is Neo4j knowledge graph server
error-messages: |
  No error messages - both servers work but wrong one is enabled
related-files:
  - ~/.claude/settings.local.json
  - ~/.mcp.json
date created: Sat, 10 18th 25, 11:58:40 am
date modified: Sat, 10 18th 25, 2:13:31 pm
---

## Problem Description

The generic "memory" MCP server (`@modelcontextprotocol/server-memory`) is currently enabled and being used instead of the custom "graphiti" MCP server (Neo4j-based knowledge graph).

When testing MCP functionality, tools like `mcp__memory__create_entities` work correctly, but they're storing data to a JSON file (`/Users/harrysayers/.cursor/memory.json`) instead of the Neo4j knowledge graph that the Graphiti server uses.

## Expected Behavior

The "graphiti" MCP server should be the primary memory/knowledge graph system, storing entities and relations in Neo4j database at `bolt://localhost:7687`.

## Actual Behavior

The "memory" MCP server is enabled and active, storing data to a flat JSON file instead of the knowledge graph.

**Current enabled servers in `~/.claude/settings.local.json`:**
```json
{
  "enabledMcpjsonServers": [
    "serena",
    "task-master-ai",
    "context7",
    "n8n",
    "graphiti",      // ✅ This is the one we want
    "gpt-researcher",
    "supabase",
    "github",
    "memory",        // ❌ This is the wrong one
    "stripe",
    "gmail",
    "claudelife-obsidian",
    "google-calendar",
    "shadcn-ui"
  ]
}
```

**MCP Server Configurations:**

**Graphiti (DESIRED):**
```json
{
  "command": "/opt/homebrew/bin/uv",
  "args": [
    "run",
    "--directory",
    "/Users/harrysayers/Developer/claudelife/graphiti_mcp_server",
    "graphiti_mcp_server.py",
    "--transport",
    "stdio"
  ],
  "env": {
    "NEO4J_URI": "bolt://localhost:7687",
    "NEO4J_USER": "neo4j",
    "NEO4J_PASSWORD": "neo4j",
    "OPENAI_API_KEY": "[REDACTED]",
    "MODEL_NAME": "gpt-4o-mini",
    "GRAPHITI_TELEMETRY_ENABLED": "false"
  }
}
```

**Memory (CURRENTLY ACTIVE):**
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-memory"
  ],
  "env": {
    "MEMORY_FILE_PATH": "/Users/harrysayers/.cursor/memory.json"
  }
}
```

## Steps to Reproduce

1. Test MCP with: `mcp__memory__create_entities({ entities: [...] })`
2. Check where data is stored
3. Observe it goes to JSON file instead of Neo4j

## Environment

- Claude Code version: Latest
- OS: macOS (Darwin)
- Relevant MCP servers: "memory" (unwanted), "graphiti" (desired)
- Neo4j running: Yes, at bolt://localhost:7687

## Additional Context

Both servers are **enabled** in `enabledMcpjsonServers` array, which means both are active simultaneously. This causes confusion about which memory system is being used.

The "graphiti" server is the custom-built knowledge graph system specifically for the claudelife ecosystem, while "memory" is a generic MCP server that was likely enabled for testing.

## Impact

- **Medium severity** because there's a workaround (can use graphiti directly if needed)
- Data may be going to wrong storage location
- Knowledge graph relationships not being captured
- Potential data inconsistency between JSON file and Neo4j

## Next Steps

User has chosen **NOT** to disable the "memory" MCP server at this time. Issue is being tracked for future reference and documentation purposes.

**If resolution is desired later:**
1. Remove "memory" from `enabledMcpjsonServers` array
2. Restart Claude Code
3. Verify `mcp__memory__*` tools are no longer available
4. Use graphiti-specific tools or refer to graphiti by name

## Resolution

[To be filled when issue is resolved]
