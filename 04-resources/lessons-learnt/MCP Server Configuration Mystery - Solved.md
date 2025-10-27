---
tags: [resources, reference]
relation:
  - "[[resources]]"
  - "[[resources]]"
date: "2025-10-13 15:15"
date created: Mon, 10 13th 25, 3:33:34 pm
date modified: Thu, 10 16th 25, 8:33:18 pm
---

# MCP Server Configuration Mystery - Solved

### The Problem

You were seeing only 4 MCP servers (archon, linear-server, notionApi, trigger) when running Claude Code from the terminal, despite having configured 15+ servers in various `.mcp.json` files. Nothing we tried - editing configs, restarting processes, clearing caches - made the other servers appear.

### The Confusion

Claude Code has **THREE completely separate MCP configuration systems** that don't talk to each other:

1. **Terminal CLI**: Uses `~/.claude.json` - managed ONLY via `claude mcp add/remove` commands
2. **Cursor Extension**: Uses `.cursor/mcp.json` - edited manually as JSON
3. **Claude Desktop App**: Uses `~/Library/Application Support/Claude/claude_desktop_config.json`

We kept editing the wrong files. When you ran `claude` in the terminal, it ignored ALL `.mcp.json` files and `claude_desktop_config.json` - it only read from `~/.claude.json` which had just 2 servers configured.

The other 2 servers you saw (archon, gen-pdf-mcp) were from Anthropic's remote marketplace registry, not local configs.

### What We Fixed

Added all your MCP servers to the terminal CLI registry using:

```bash
claude mcp add <name> <command> [args...] -e KEY=value
```

Now the terminal shows: gpt-researcher, supabase, github, memory, gmail, context7, graphiti, notion, obsidian, trigger, linear-server, serena, gen-pdf-mcp.

### Key Lesson

**Different Claude Code environments = different MCP configs**. Always use the right tool for each environment:
- Terminal: `claude mcp add`
- Cursor: Edit `.cursor/mcp.json`
- Desktop: Edit `claude_desktop_config.json`

The files aren't interchangeable - they're completely isolated systems.
