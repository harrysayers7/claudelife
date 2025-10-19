---
date: "2025-10-20 08:45"
issue-id: issue-002
category: mcp-server
severity: high
---

# Lesson: MCP Server Connects But Tools Not Exposed - Missing Permissions

## Problem

Graphiti MCP server appeared to fail with authentication errors:
```
Error: Neo.ClientError.Security.Unauthorized
The client is unauthorized due to authentication failure
```

**Symptoms**:
- `ListMcpResourcesTool({ server: "graphiti" })` returned empty array `[]`
- All MCP tool calls failed with authentication errors
- Debug logs showed server connecting successfully
- Neo4j container running and accessible

## Root Cause

**Missing wildcard permission in `.claude/settings.local.json`**

**Server name in `.mcp.json`**: `"graphiti"`

**Existing permissions** (incorrect):
```json
"mcp__graphiti-personal__add_memory",
"mcp__graphiti-mokai__add_memory",
"mcp__graphiti-finance__add_memory"
```

**Missing permission**: `"mcp__graphiti__*"`

The server connected successfully, registered tools, and was fully functional. However, Claude Code couldn't expose the tools to the user because the exact server name permission was missing from `allowedTools`.

## Solution

Add wildcard permission to `.claude/settings.local.json`:

```json
{
  "allowedTools": [
    // ... other permissions
    "mcp__graphiti__*",  // ← Add this for the main server
    "mcp__graphiti-personal__add_memory",
    "mcp__graphiti-mokai__add_memory",
    "mcp__graphiti-finance__add_memory"
  ]
}
```

**Restart Claude Code**:
```bash
exit
claude
```

**Verify**:
```javascript
ListMcpResourcesTool({ server: "graphiti" })
// Should return: Array of resources/tools

mcp__graphiti__search_memory_nodes({ query: "test", max_nodes: 1 })
// Should work without errors
```

## Prevention

### For Users: MCP Server Permission Checklist

When adding a new MCP server, **always verify permissions**:

1. **Add server to `.mcp.json`** with configuration
2. **Add server to `enabledMcpjsonServers`** in `.claude/settings.local.json`
3. **Add wildcard permission** `mcp__{server-name}__*` to `allowedTools`
4. **Restart Claude Code**
5. **Verify with `ListMcpResourcesTool`**

### For Debugging: Check Permissions FIRST

**When `ListMcpResourcesTool` returns empty array for connected server**:

```bash
# Step 1: Verify server enabled
cat ~/.claude/settings.local.json | jq '.enabledMcpjsonServers'
# Should include your server name

# Step 2: Check permissions
cat ~/.claude/settings.local.json | jq '.allowedTools[] | select(contains("{server-name}"))'
# Should show: mcp__{server-name}__*

# Step 3: Verify exact server name match
cat .mcp.json | jq '.mcpServers | keys'
# Compare to permission entries
```

**Permission must match exact server name in `.mcp.json`**

### For System: Automated Permission Check

Consider adding to MCP setup documentation:

```markdown
## MCP Server Setup Checklist

- [ ] Add server config to `.mcp.json`
- [ ] Add to `enabledMcpjsonServers` in settings
- [ ] **Add `mcp__{server-name}__*` to `allowedTools`**
- [ ] Restart Claude Code
- [ ] Test with `ListMcpResourcesTool`
```

## What NOT to Do (Misleading Paths)

This issue took ~15 hours to resolve because we chased **red herrings**:

### ❌ Don't Chase Stale Connections
- **Thought**: CLOSED connections in `lsof` meant stale connection pool
- **Reality**: Normal TCP connection lifecycle
- **Wasted effort**: Killed processes, cleared connections

### ❌ Don't Chase Log Warnings Without Context
- **Thought**: Asyncio RuntimeWarning meant library bug
- **Reality**: Unrelated warning, server working fine
- **Wasted effort**: Upgraded packages unnecessarily

### ❌ Don't Assume Auth Errors Mean Bad Credentials
- **Thought**: "Authentication failure" meant wrong password
- **Reality**: Tools weren't exposed, so couldn't authenticate
- **Wasted effort**: Verified passwords, checked configs

### ✅ What We SHOULD Have Done

**Check permissions IMMEDIATELY when tools don't appear**:

```javascript
// If this returns empty:
ListMcpResourcesTool({ server: "graphiti" })

// Check this FIRST:
cat ~/.claude/settings.local.json | jq '.allowedTools[] | select(contains("graphiti"))'
```

**The fix was one line. The debugging took 15 hours because we didn't check permissions first.**

## Debugging Pattern for MCP Servers

**When MCP tools don't work, check in this order**:

1. ✅ **Server in `enabledMcpjsonServers`?**
   ```bash
   cat ~/.claude/settings.local.json | jq '.enabledMcpjsonServers'
   ```

2. ✅ **Wildcard permission exists?**
   ```bash
   cat ~/.claude/settings.local.json | jq '.allowedTools[] | select(contains("{server}"))'
   ```

3. ✅ **Server name matches exactly?**
   ```bash
   # Compare these:
   cat .mcp.json | jq '.mcpServers | keys'
   cat ~/.claude/settings.local.json | jq '.allowedTools[] | select(contains("mcp__"))'
   ```

4. ✅ **Restart applied?**
   ```bash
   exit
   claude
   ```

5. **ONLY THEN** check server logs/debug for connection issues

## Key Insights

### Permission System Design

- **MCP servers connect independently** of Claude Code permissions
- **Tools are exposed only if permissions allow**
- **Server connecting ≠ Tools available**

### Common Mistakes

| Symptom | Wrong Diagnosis | Actual Problem |
|---------|----------------|----------------|
| Empty ListMcpResourcesTool | Server not connecting | Missing permission |
| Auth errors | Wrong password | Tools not exposed |
| Asyncio warnings in logs | Library bug | Unrelated warning |

### Quick Check Command

```bash
# One-liner to verify MCP server permissions
jq -n --arg server "graphiti" '
  {
    enabled: (env.SETTINGS | fromjson | .enabledMcpjsonServers | contains([$server])),
    permissions: (env.SETTINGS | fromjson | .allowedTools | map(select(contains($server))))
  }
' --slurpfile SETTINGS ~/.claude/settings.local.json
```

## Related

- Issue: [[issue-002-graphiti-mcp-stale-connection]]
- Category: mcp-server
- Documentation: Add to MCP setup guide
- Memory update: `.serena/memories/system_patterns_and_guidelines.md`

## Time Investment

- **Total debugging time**: ~15 hours
- **Actual fix**: 1 line, 30 seconds
- **Lesson**: Check basic config before complex debugging

**Prevention value**: This lesson could save hours on future MCP issues by establishing the correct debugging order.
