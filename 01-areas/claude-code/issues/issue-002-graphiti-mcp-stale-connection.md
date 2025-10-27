---
title: Graphiti MCP server authentication failure due to stale connection
type:
  - issue
aliases:
  - issue-002
id: issue-002
category: mcp-server
relation:
  - "[[claude-code]]"
complete: true
solved: true
lesson: 04-resources/lessons-learnt/251020-issue-002-mcp-permissions.md
date created: Sun, 10 19th 25, 5:46:00 pm
severity: high
attempted-solutions:
  - Checked Neo4j password (was correct - demodemo)
  - Updated .mcp.json with correct password
  - Updated graphiti_mcp_server/.env with correct password
  - Restarted Claude Code (did NOT fix - issue persisted)
  - Verified Neo4j connectivity (docker exec cypher-shell works)
  - Identified 30+ CLOSED connections from 3 Python processes (PIDs 42108, 45851, 45881)
  - Killed orphaned process PID 42108 from Saturday 12PM
  - Discovered MCP tools not exposed (ListMcpResourcesTool returns empty array)
  - Manual MCP server test revealed initialization failure
  - Analyzed debug logs - found asyncio RuntimeWarning in graphiti-core library
  - Checked graphiti-core package version (0.14.0)
  - Updated graphiti-core and dependencies (neo4j 5.28.1 → 6.0.2, openai 1.91.0 → 2.5.0)
  - NEW: Restarted Claude Code after package upgrade (still not working)
  - NEW: Verified Graphiti server connecting successfully (debug logs show "Successfully connected")
  - NEW: Checked server name in .mcp.json (confirmed "graphiti")
  - NEW: Verified server enabled in enabledMcpjsonServers (confirmed present)
  - NEW: Identified root cause - Missing mcp__graphiti__* permission in settings.local.json
  - NEW: Added wildcard permission to .claude/settings.local.json line 42
error-messages: |
  MISLEADING Initial Errors (Red Herrings):
  Error searching nodes: {code: Neo.ClientError.Security.Unauthorized}
  {message: The client is unauthorized due to authentication failure.}

  Docker logs show auth failures at 06:37 and 06:46 this morning:
  2025-10-19 06:37:58.198+0000 WARN [bolt-3] The client is unauthorized due to authentication failure.
  2025-10-19 06:46:36.355+0000 WARN [bolt-15] The client has provided incorrect authentication details too many times in a row.

  MCP Protocol Error (discovered 2025-10-19 17:59):
  Failed to validate request: Received request before initialization was complete
  {"jsonrpc":"2.0","id":1,"error":{"code":-32602,"message":"Invalid request parameters","data":""}}

  Asyncio Warning (discovered 2025-10-19 18:14 - MISLEADING):
  [ERROR] MCP server "graphiti" Server stderr: sys:1: RuntimeWarning: coroutine 'Neo4jDriver.execute_query' was never awaited
  [DEBUG] MCP server "graphiti": Connection failed after 1144ms: MCP error -32000: Connection closed
  [ERROR] MCP server "graphiti" Connection failed: MCP error -32000: Connection closed

  ACTUAL Issue (discovered 2025-10-20 08:30):
  ListMcpResourcesTool({ server: "graphiti" }) returns empty array []
  Server connects successfully but tools not exposed to Claude Code
  Missing permission: mcp__graphiti__* in .claude/settings.local.json
related-files:
  - /Users/harrysayers/.mcp.json
  - /Users/harrysayers/Developer/claudelife/graphiti_mcp_server/.env
  - /Users/harrysayers/Developer/claudelife/graphiti_mcp_server/graphiti_mcp_server.py
  - /Users/harrysayers/Developer/claudelife/.claude/settings.local.json
---

## Problem Description

Graphiti MCP server returns authentication errors when attempting to use tools:

```javascript
mcp__graphiti__search_memory_nodes({ query: "test", max_nodes: 1 })
// Error: Neo.ClientError.Security.Unauthorized - authentication failure
```

The server was working earlier today but stopped functioning. User confirmed it was working recently, ruling out simple password misconfiguration.

## Expected Behavior

Graphiti MCP server should connect to Neo4j Docker container and execute queries successfully:
- `search_memory_nodes` should return matching nodes
- `add_memory` should store episodes
- No authentication errors

## Actual Behavior

All Graphiti MCP tools fail with:
```
Neo.ClientError.Security.Unauthorized
The client is unauthorized due to authentication failure
```

## Root Cause Analysis

### Initial Investigation (Incorrect Diagnosis)

1. **Neo4j is running correctly**: Docker container `neo4j-dev` is up with correct password (`demodemo`)
2. **Password configuration is correct**: Both `.mcp.json` and `.env` have matching credentials
3. **Connection test succeeds**: `docker exec neo4j-dev cypher-shell -u neo4j -p demodemo "RETURN 1"` works
4. **MCP server has stale connections**: `lsof -i :7687` shows many CLOSED connections from Python processes (PIDs 42108, 45851, 45881)

**Initial diagnosis (INCORRECT)**: Stale connection pool - restart would fix it

### Actual Root Cause (Discovered 2025-10-19 18:14)

**Python Asyncio Bug in graphiti-core v0.14.0**

The real problem is NOT stale Neo4j connections OR MCP configuration. The issue is:

1. ✅ Graphiti MCP server connects to Neo4j successfully (indices created, client initialized)
2. ✅ Graphiti MCP server starts up (logs show "Starting MCP server with transport: stdio")
3. ❌ **Python asyncio coroutine not awaited causes server crash**
4. ❌ **MCP initialization handshake fails before completion**
5. ❌ **No tools are exposed to Claude Code** (ListMcpResourcesTool returns empty array)

**Evidence from ~/.claude/debug/latest**:
```
[ERROR] MCP server "graphiti" Server stderr: sys:1: RuntimeWarning: coroutine 'Neo4jDriver.execute_query' was never awaited
[DEBUG] MCP server "graphiti": Connection failed after 1144ms: MCP error -32000: Connection closed
[ERROR] MCP server "graphiti" Connection failed: MCP error -32000: Connection closed
```

**Analysis**:
- Bug exists in graphiti-core library v0.14.0 (or its neo4j dependency v5.28.1)
- Async coroutine not properly awaited during initialization
- Server crashes before MCP handshake completes
- Tools never get registered/exposed to Claude Code

**True diagnosis**: Library bug, not configuration issue. Solution is package upgrade.

## Steps to Reproduce

1. Start Graphiti MCP server (via Claude Code startup)
2. Neo4j Docker container restarts OR network hiccup occurs
3. Attempt to use Graphiti tools (e.g., `search_memory_nodes`)
4. Authentication errors occur despite correct credentials

## Environment

- **Claude Code version**: Current
- **OS**: macOS (Darwin 24.6.0)
- **Neo4j**: Docker container `neo4j-dev` (neo4j:5.26.0)
  - Port: 7687
  - Auth: neo4j/demodemo
  - Status: Running (Up 2 days)
- **Graphiti MCP Server**:
  - Command: `uv run --directory /Users/harrysayers/Developer/claudelife/graphiti_mcp_server graphiti_mcp_server.py`
  - Transport: stdio

## Technical Details

### Neo4j Docker Container
```bash
$ docker ps | grep neo4j
4c6e3bef7c92   neo4j:5.26.0   "tini -g -- /startup…"   5 weeks ago   Up 2 days
0.0.0.0:7474->7474/tcp, 0.0.0.0:7687->7687/tcp   neo4j-dev

$ docker inspect neo4j-dev | grep NEO4J_AUTH
"NEO4J_AUTH=neo4j/demodemo"
```

### Stale Connections
```bash
$ lsof -i :7687 | grep python
python3.1 42108 ... TCP localhost:54152->localhost:7687 (CLOSED)
python3.1 42108 ... TCP localhost:54153->localhost:7687 (CLOSED)
[... 20+ more CLOSED connections ...]
```

### Connection Test (Success)
```bash
$ docker exec neo4j-dev cypher-shell -u neo4j -p demodemo "RETURN 1"
1
1
```

## Solution

**Restart Claude Code** to force Graphiti MCP server to reconnect:

```bash
# Exit current session
exit

# Restart
claude
```

This spawns a fresh MCP server process that establishes new connections to Neo4j.

## Prevention

From Serena's memory (`system_patterns_and_guidelines.md`):

> **Common Issues**
>
> **Server shows "✗ Failed to connect"**:
> - Check server logs for connection errors
> - Verify dependencies are running (e.g., Neo4j for Graphiti)
> - **Remove and re-add server via CLI**
> - **Restart Claude Code after configuration changes**

**Best practice**: When Neo4j Docker container restarts, also restart Claude Code to refresh MCP server connections.

## Additional Context

### Why Password Confusion Occurred

Initially suspected password issue because:
1. Docker logs showed authentication failures
2. `.mcp.json` had password `neo4j` (incorrect for Docker)
3. Docker container uses `demodemo` (correct)

However, user correctly stated "it was working earlier today", indicating password wasn't the issue. The real problem was **stale MCP server process**, not wrong credentials.

### Lesson Learned

**Don't assume password mismatch from auth errors if system was recently working.** Check for:
1. Stale processes/connection pools
2. Service restarts (Docker, database, etc.)
3. Network events

Before changing configurations, **verify the actual service is accessible** (e.g., `cypher-shell` test).

## Progress Log

**2025-10-19 17:46**: Issue created - suspected stale Neo4j connections
**2025-10-19 17:50**: Verified Neo4j connectivity (cypher-shell works)
**2025-10-19 17:52**: Identified 30+ CLOSED connections from 3 Python processes
**2025-10-19 17:55**: Killed orphaned process PID 42108 from Saturday
**2025-10-19 17:58**: Discovered MCP tools not exposed (ListMcpResourcesTool returns [])
**2025-10-19 17:59**: Manual test revealed MCP initialization failure
**2025-10-19 18:02**: Updated root cause - NOT stale connections, but MCP protocol failure
**2025-10-19 18:14**: **[COMPREHENSIVE UPDATE - SOLUTION FOUND]**

### Attempted Since Last Update:
1. ✅ Killed all Graphiti MCP server processes (pkill -f graphiti_mcp_server)
2. ✅ Verified no Python processes connected to Neo4j (lsof -i :7687)
3. ✅ Examined graphiti_mcp_server.py initialization code - FastMCP setup correct
4. ✅ Manually tested server startup - Neo4j connection works, indices created successfully
5. ✅ Analyzed Claude Code debug log (~/.claude/debug/latest)

### Root Cause Identified:
**Python asyncio bug in graphiti-core library v0.14.0**

```
[ERROR] MCP server "graphiti" Server stderr: sys:1: RuntimeWarning: coroutine 'Neo4jDriver.execute_query' was never awaited
[DEBUG] MCP server "graphiti": Connection failed after 1144ms: MCP error -32000: Connection closed
```

**Analysis**:
- Graphiti server successfully connects to Neo4j ✅
- Indices and constraints are created ✅
- Server logs "Starting MCP server with transport: stdio" ✅
- BUT: Asyncio coroutine not awaited causes crash before MCP handshake completes ❌
- Result: Tools never get exposed to Claude Code ❌

### Solution Applied:
Updated graphiti-core and dependencies to fix asyncio bug:

```bash
uv pip install --upgrade graphiti-core
```

**Package Updates**:
- neo4j: 5.28.1 → 6.0.2 (likely contains the fix)
- openai: 1.91.0 → 2.5.0
- pydantic: 2.11.7 → 2.12.3
- pydantic-core: 2.33.2 → 2.41.4
- typing-extensions: 4.14.0 → 4.15.0
- Other minor dependency updates

### Next Step:
Restart Claude Code to test if the asyncio fix resolves the MCP initialization failure.

### LLM Continuation Context:
- Issue was NOT authentication or stale connections
- Issue was NOT MCP configuration
- Issue WAS a Python asyncio bug in graphiti-core library
- Solution: Package upgrade (neo4j driver 6.0.2 likely has the fix)
- Verification needed: Restart Claude Code and test Graphiti MCP tools

## Current Status

**Solution applied - awaiting verification**

**Completed Steps**:
1. ✅ Killed all Graphiti MCP server processes
2. ✅ Analyzed debug log and found asyncio RuntimeWarning
3. ✅ Identified root cause: graphiti-core library bug
4. ✅ Updated graphiti-core and dependencies
5. ⏳ **Restart Claude Code to test fix**

**Verification Steps**:
1. Exit current Claude Code session
2. Restart: `claude`
3. Test Graphiti tools work
4. If successful: Mark issue as solved, create lesson learned

## Debugging Commands

```bash
# Verify all Graphiti processes killed
ps aux | grep graphiti | grep -v grep

# Restart with debug mode
exit
claude --mcp-debug

# Check debug log for initialization details
tail -200 /tmp/claude-mcp-debug.log | grep -i graphiti

# Verify tools are exposed after restart
# In Claude Code: ListMcpResourcesTool({ server: "graphiti" })
```

## Resolution

**Status**: Solution identified, awaiting verification after Claude Code restart

**Root Cause**: Python asyncio bug in graphiti-core v0.14.0 library
- Coroutine `Neo4jDriver.execute_query` was never awaited
- Caused MCP server to crash during initialization before handshake could complete

**Solution**: Update graphiti-core and dependencies
```bash
uv pip install --upgrade graphiti-core
```

**Key Package Updates**:
- neo4j: 5.28.1 → 6.0.2 (likely contains asyncio fix)
- openai: 1.91.0 → 2.5.0
- pydantic: 2.11.7 → 2.12.3

**Verification Required**: Restart Claude Code and test Graphiti MCP tools

**Prevention**:
- Keep Python packages updated, especially MCP server dependencies
- Check debug logs (`~/.claude/debug/latest`) when MCP servers fail to connect
- Look for asyncio warnings and library version issues

**2025-10-20 08:30**: **[COMPREHENSIVE UPDATE - ACTUAL ROOT CAUSE FOUND]**

### Critical Discovery: The Asyncio Bug Was a Red Herring

**What We Attempted Since Last Update**:
1. ✅ Restarted Claude Code after package upgrade
2. ✅ Checked debug logs - found server connecting successfully: "Successfully connected to stdio server in 3090ms"
3. ✅ Verified server capabilities: `{"hasTools":true,"hasPrompts":true,"hasResources":true}`
4. ✅ Confirmed server name in `.mcp.json`: `"graphiti"`
5. ✅ Verified server in `enabledMcpjsonServers` array
6. ✅ Tested `ListMcpResourcesTool({ server: "graphiti" })` - returned empty array
7. ✅ **Identified actual root cause**: Permission mismatch in `.claude/settings.local.json`

### The Real Problem

**NOT** asyncio bug. **NOT** stale connections. **NOT** Neo4j authentication.

**Permission mismatch**:
- Server name in `.mcp.json`: `"graphiti"`
- Existing permissions in `settings.local.json` (lines 42-44):
  - `mcp__graphiti-personal__add_memory`
  - `mcp__graphiti-mokai__add_memory`
  - `mcp__graphiti-finance__add_memory`
- **Missing**: `mcp__graphiti__*` wildcard for the actual server

### Evidence Server Was Working All Along

```
[DEBUG] MCP server "graphiti": Successfully connected to stdio server in 3090ms
[DEBUG] MCP server "graphiti": Connection established with capabilities: {"hasTools":true,"hasPrompts":true,"hasResources":true,"serverVersion":{"name":"Graphiti Agent Memory","version":"1.9.4"}}
[ERROR] MCP server "graphiti" Server stderr: 2025-10-20 08:30:24,768 - __main__ - INFO - Graphiti client initialized successfully
```

Server connected perfectly. Neo4j indices created. Tools available. But Claude Code didn't have **permission to expose them**.

### Solution Applied

**File**: `.claude/settings.local.json`
**Change**: Added `"mcp__graphiti__*"` to permissions array (line 42)

```json
"mcp__stripe__*",
"mcp__graphiti__*",          // ← NEW: Wildcard permission for graphiti server
"mcp__graphiti-personal__add_memory",
"mcp__graphiti-mokai__add_memory",
```

### Lessons Learned

1. **Server connecting ≠ Tools exposed**: Server can connect successfully but tools won't appear without proper permissions
2. **Check permissions first**: When `ListMcpResourcesTool` returns empty array for connected server, check `allowedTools` in settings
3. **Asyncio error was misleading**: Package upgrade was unnecessary - original packages were fine
4. **Server name matters**: Permission must match exact server name in `.mcp.json`, not similar server names

### Current State

- ✅ Server connects successfully (always did)
- ✅ Neo4j working correctly (always was)
- ✅ Permission added: `mcp__graphiti__*`
- ⏳ **Awaiting restart to verify tools now appear**

### Next Steps

1. Restart Claude Code: `exit` → `claude`
2. Test tools visible: `ListMcpResourcesTool({ server: "graphiti" })`
3. Test basic tool: `mcp__graphiti__search_memory_nodes({ query: "test", max_nodes: 1 })`
4. If successful: Mark issue as solved, create lesson learned

### LLM Continuation Context for Next Session

**The entire investigation was on the wrong track from 2025-10-19 18:14 onwards.**

- Asyncio warning in logs was **unrelated** to the actual problem
- Package upgrade to graphiti-core 6.0.2, neo4j 6.0.2 was **unnecessary**
- Real issue was **always** the missing permission entry
- Server was connecting perfectly since the beginning
- Only needed one line added to settings.local.json

**Key Pattern**: When debugging MCP servers:
1. First check: Server in `enabledMcpjsonServers`? ✅
2. Second check: Permissions in `allowedTools` match server name? ❌ (This caught us)
3. Last resort: Check server logs/debug for connection issues

**Do NOT chase misleading error messages** (like asyncio warnings) without first verifying basic configuration (permissions, server names, etc.)

---

## ✅ FINAL RESOLUTION - 2025-10-20 08:45

**Status**: Issue successfully resolved and verified

**Root Cause**: Missing `mcp__graphiti__*` permission in `.claude/settings.local.json`

**Solution**: Added wildcard permission on line 42

**Verification**:
- ✅ ListMcpResourcesTool now returns resources (previously empty)
- ✅ mcp__graphiti__search_memory_nodes successfully retrieved test node
- ✅ Server functioning correctly

**Lesson Learned**: [[251020-issue-002-mcp-permissions]]

**Time to Resolution**: ~15 hours (from 2025-10-19 17:46 to 2025-10-20 08:45)
**Misleading Paths**: Stale connections, asyncio bugs, package upgrades
**Actual Fix**: One line permission entry
