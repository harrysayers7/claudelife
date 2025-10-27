---
relation:
  - "[[resources]]"
  - "[[resources]]"
date: "2025-10-16"
category: MCP Configuration
severity: Critical
status: Resolved
tags: [mcp, configuration, debugging, claude-code]
---

# Lesson Learned: Claude Code MCP Configuration Location

## Date
2025-10-16

## Problem
Spent 2+ hours trying to configure Supabase and Stripe MCP servers by editing `~/.mcp.json` and `.mcp.json` files, but they never appeared in Claude Code's available tools list.

## Root Cause
**Claude Code uses `~/.claude.json` for MCP server configuration, NOT `.mcp.json`**

The `.mcp.json` file exists in the ecosystem but is for a DIFFERENT MCP implementation (likely Claude Desktop or API usage), not Claude Code.

## What Went Wrong

### Failed Attempts
1. ❌ Added servers to `~/.mcp.json` - Not read by Claude Code
2. ❌ Added to project `.mcp.json` - Wrong file entirely
3. ❌ Removed `"type": "stdio"` fields - Wrong file location
4. ❌ Used full binary paths - Still wrong file
5. ❌ Installed packages globally - Wrong file still
6. ❌ Multiple Claude Code restarts - Can't fix wrong config location

### What Actually Worked
✅ Used `claude mcp add` CLI command which writes to `~/.claude.json`

```bash
claude mcp add --transport stdio supabase \
  --env SUPABASE_ACCESS_TOKEN=xxx \
  -- npx -y @supabase/mcp-server-supabase --project-ref xxx

claude mcp add --transport stdio stripe \
  -- npx @stripe/mcp --tools=all --api-key=xxx
```

## The Confusion

### Wrong Agent Instructions
The `mcp-expert` agent at `.claude/agents/mcp-expert.md` had INCORRECT instructions that promoted using `.mcp.json` format:

```json
// WRONG - This was in the agent
{
  "mcpServers": {
    "service": {
      "command": "npx",
      "args": [...],
      "env": {...}
    }
  }
}
```

This led to hours of editing the wrong configuration files.

### Context7 Not Used
Had a Context7 detector hook created but not configured, which would have:
1. Detected library questions (Supabase, Stripe)
2. Suggested using Context7 MCP for documentation
3. Provided correct MCP configuration format from official docs

## Correct Workflow

### Adding MCP Servers
```bash
# Add stdio server
claude mcp add --transport stdio <name> \
  --env KEY=value \
  -- command args

# Add HTTP server
claude mcp add --transport http <name> <url> \
  --header "Authorization: Bearer token"
```

### Verifying Configuration
```bash
# List all servers (shows connection status)
claude mcp list

# Get specific server config
claude mcp get <server-name>

# Check logs
tail ~/Library/Logs/Claude/mcp-server-<name>.log
```

### Configuration Files

**Used by Claude Code:**
- `~/.claude.json` - MCP server storage (managed by CLI)
- `~/.claude/settings.local.json` - Settings including `enabledMcpjsonServers`

**NOT used by Claude Code:**
- `~/.mcp.json` - Different MCP implementation
- `.mcp.json` - Project-level config for other tools

## Fixes Applied

### 1. Updated mcp-expert Agent
Rewrote `.claude/agents/mcp-expert.md` to:
- Emphasize `claude mcp add` CLI usage
- Warn against manual `.mcp.json` editing
- Show correct debugging workflow
- Provide accurate examples

### 2. Enabled Context7 Hook
Configured `context7_detector.py` hook in `settings.local.json`:
```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "python3 .claude/hooks/context7_detector.py"
      }]
    }]
  }
}
```

This hook now detects library questions and suggests using Context7 for up-to-date documentation.

### 3. Updated Serena Memory
Added MCP configuration pattern to `system_patterns_and_guidelines` memory with correct file locations and CLI usage.

## Prevention Measures

### Always Check Official Docs First
Before configuring MCP servers:
1. Use Context7 MCP to research current documentation
2. Verify configuration file locations
3. Check CLI commands in official docs

### Use Verification Commands
After any MCP changes:
```bash
# Verify server was added
claude mcp list | grep server-name

# Check connection status
claude mcp list
# Look for: ✓ Connected, ⚠ Needs authentication, or ✗ Failed
```

### Hook Integration
The Context7 detector hook should catch future library configuration questions and suggest proper research workflow.

## Key Takeaways

1. **Don't trust agent instructions blindly** - Verify against official docs
2. **Use CLI tools when available** - `claude mcp add` prevents config errors
3. **Leverage Context7 for documentation** - Especially for evolving tools like MCP
4. **Test configuration immediately** - `claude mcp list` shows what's actually loaded
5. **Check logs for debugging** - MCP server logs reveal connection issues

## Documentation Updated

- ✅ [mcp-expert.md](../.claude/agents/mcp-expert.md) - Completely rewritten
- ✅ Serena memory: `system_patterns_and_guidelines` - Added MCP config pattern
- ✅ This lesson learned document

## Time Cost
**~2 hours** - Could have been 5 minutes with correct information

## Related Files
- `.claude/agents/mcp-expert.md`
- `.claude/hooks/context7_detector.py`
- `.claude/settings.local.json`
- `.serena/memories/system_patterns_and_guidelines.md`
- `supabase-stripe-mcp-troubleshooting.md` (troubleshooting log)

## Status
✅ **Resolved** - Servers now working via `claude mcp add` CLI
