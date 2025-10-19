---
date: "2025-10-20 08:50"
---

# MCP Server Troubleshooting Guide

Quick reference for diagnosing and fixing common MCP server issues in Claude Code.

## Quick Diagnostic Checklist

When MCP server isn't working, check in this order:

```bash
# 1. Is server enabled?
cat ~/.claude/settings.local.json | jq '.enabledMcpjsonServers'

# 2. Does permission exist?
cat ~/.claude/settings.local.json | jq '.allowedTools[] | select(contains("{server-name}"))'

# 3. Do names match exactly?
cat .mcp.json | jq '.mcpServers | keys'

# 4. Check connection status
claude mcp list

# 5. Only then check logs
tail -50 ~/Library/Logs/Claude/mcp-server-{name}.log
```

---

## Issue #1: Server Connects But Tools Don't Appear

**Symptom**:
```javascript
ListMcpResourcesTool({ server: "graphiti" })
// Returns: []
```

**Root Cause**: Missing wildcard permission in `.claude/settings.local.json`

### Diagnosis

```bash
# Check if permission exists
cat ~/.claude/settings.local.json | jq '.allowedTools[] | select(contains("graphiti"))'
```

**If missing or only shows specific permissions** (e.g., `mcp__graphiti-personal__*`), you need the base wildcard.

### Solution

Add to `.claude/settings.local.json`:
```json
{
  "allowedTools": [
    "mcp__graphiti__*",  // ← Add wildcard for base server
    "mcp__graphiti-personal__add_memory",  // Specific permissions OK too
    "mcp__graphiti-mokai__add_memory"
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
```

### Prevention

When adding new MCP server:
1. Add config to `.mcp.json`
2. Add to `enabledMcpjsonServers`
3. **Add `mcp__{server-name}__*` to `allowedTools`** ← Don't forget this!
4. Restart Claude Code
5. Test with `ListMcpResourcesTool`

### Related

- **Lesson Learned**: [[251020-issue-002-mcp-permissions]]
- **Issue**: [[issue-002-graphiti-mcp-stale-connection]]

---

## Issue #2: Server Shows "✗ Failed to Connect"

**Symptom**: `claude mcp list` shows server with ✗ mark

### Diagnosis

```bash
# 1. Check server logs
tail -50 ~/Library/Logs/Claude/mcp-server-{name}.log

# 2. Test server command manually
/path/to/server-command --transport stdio
```

### Common Causes

#### Dependencies Not Running
Example: Graphiti requires Neo4j

```bash
# Check if dependency is running
docker ps | grep neo4j

# Start dependency
docker start neo4j-dev
```

#### Environment Variables Missing

```bash
# Check server config
claude mcp get {server-name}

# Verify env vars are set
cat .mcp.json | jq '.mcpServers.{server-name}.env'
```

#### Command Path Incorrect

```bash
# Find correct path
which uv
which python3

# Update config with full path
claude mcp add {server} --command "/opt/homebrew/bin/uv" ...
```

### Solution

1. Fix underlying issue (start service, add env vars, fix path)
2. Restart Claude Code
3. Verify: `claude mcp list` shows ✓

---

## Issue #3: Server Exists in Multiple Scopes

**Symptom**: CLI commands fail with "server exists in multiple scopes"

### Diagnosis

```bash
# Check all config files
cat ~/.claude.json | jq '.mcpServers | keys'
cat ~/.mcp.json | jq '.mcpServers | keys'
cat .mcp.json | jq '.mcpServers | keys'
```

### Solution

Remove from specific scope:
```bash
claude mcp remove {server-name} -s local
# or
claude mcp remove {server-name} -s project
# or
claude mcp remove {server-name} -s user
```

Verify:
```bash
claude mcp list
# Server should appear only once
```

---

## Issue #4: Tools Return Authentication Errors

**Symptom**: Tool calls fail with auth/permission errors

### This Could Mean Two Things

#### 1. Missing Permissions (Most Common)
See **Issue #1** above - check if wildcard permission exists.

#### 2. Actual Authentication Failure
Server can't connect to backend service.

**Diagnosis**:
```bash
# Check if backend is accessible
# Example for Neo4j:
docker exec neo4j-dev cypher-shell -u neo4j -p {password} "RETURN 1"

# Check server logs for auth errors
tail -50 ~/Library/Logs/Claude/mcp-server-{name}.log | grep -i auth
```

**Solution**: Fix backend credentials in `.mcp.json` or server `.env` file

---

## Issue #5: Changes Not Taking Effect

**Symptom**: Modified config but server still uses old settings

### Cause

Claude Code caches MCP server configurations until restart.

### Solution

```bash
# Always restart after config changes
exit
claude
```

---

## Common Debugging Mistakes

### ❌ Don't Do This

1. **Chase log warnings without checking basic config**
   - Red herrings like asyncio warnings are common
   - Check permissions FIRST before debugging complex issues

2. **Assume auth errors mean bad credentials**
   - Often means tools aren't exposed due to missing permissions
   - Verify tools appear in `ListMcpResourcesTool` first

3. **Kill processes trying to fix "stale connections"**
   - CLOSED TCP connections are normal
   - Server manages its own connection pool

4. **Upgrade packages without verifying the actual problem**
   - Easy to waste time on unnecessary upgrades
   - Isolate the real issue first

### ✅ Do This Instead

1. **Follow diagnostic checklist in order** (see top of guide)
2. **Check permissions before anything else**
3. **Test server command manually** to verify it works standalone
4. **Read debug logs only after basic config verified**

---

## Quick Reference: MCP Setup Checklist

- [ ] Add server config to `.mcp.json`
  ```json
  {
    "mcpServers": {
      "server-name": {
        "command": "/path/to/command",
        "args": ["arg1", "arg2"],
        "env": {
          "KEY": "value"
        }
      }
    }
  }
  ```

- [ ] Add to `enabledMcpjsonServers` in `~/.claude/settings.local.json`
  ```json
  {
    "enabledMcpjsonServers": ["server-name"]
  }
  ```

- [ ] **Add wildcard permission** to `allowedTools`
  ```json
  {
    "allowedTools": ["mcp__server-name__*"]
  }
  ```

- [ ] Restart Claude Code
  ```bash
  exit
  claude
  ```

- [ ] Verify connection
  ```bash
  claude mcp list
  # Should show: ✓ Connected
  ```

- [ ] Test tools accessible
  ```javascript
  ListMcpResourcesTool({ server: "server-name" })
  // Should return: Array of resources
  ```

---

## Debug Command One-Liners

```bash
# Check all MCP server permissions
jq -r '.allowedTools[] | select(contains("mcp__"))' ~/.claude/settings.local.json

# Compare server names vs permissions
diff <(jq -r '.mcpServers | keys[]' .mcp.json | sed 's/^/mcp__/; s/$/__*/') \
     <(jq -r '.allowedTools[] | select(contains("mcp__"))' ~/.claude/settings.local.json)

# List enabled servers
jq -r '.enabledMcpjsonServers[]' ~/.claude/settings.local.json

# Quick health check
echo "=== Enabled Servers ===" && \
jq -r '.enabledMcpjsonServers[]' ~/.claude/settings.local.json && \
echo -e "\n=== Permissions ===" && \
jq -r '.allowedTools[] | select(contains("mcp__"))' ~/.claude/settings.local.json
```

---

## Related Resources

- **Serena Memory**: `.serena/memories/system_patterns_and_guidelines.md`
- **Lesson Learned**: `04-resources/lessons-learnt/251020-issue-002-mcp-permissions.md`
- **Issue Tracker**: `01-areas/claude-code/issues/`

---

**Last Updated**: 2025-10-20
**Lesson Source**: Issue #002 - 15 hours of debugging reduced to 1-line fix by following checklist
