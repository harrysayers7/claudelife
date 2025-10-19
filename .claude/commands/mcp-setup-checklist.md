---
description: Interactive checklist for setting up a new MCP server in Claude Code
---

# MCP Server Setup Checklist

Walk through the complete setup process for adding a new MCP server to Claude Code.

## Usage

```bash
/mcp-setup-checklist {server-name}
```

## What This Command Does

This command provides an interactive checklist to ensure all steps are completed when adding a new MCP server:

1. **Server configuration** - Add to `.mcp.json`
2. **Enable server** - Add to `enabledMcpjsonServers`
3. **Grant permissions** - Add wildcard to `allowedTools`
4. **Restart Claude Code** - Apply changes
5. **Verify connection** - Test server works
6. **Test tools** - Confirm tools are accessible

## Interactive Process

When you run this command, I will:

1. **Ask for server details**:
   - Server name (e.g., "graphiti", "supabase")
   - Command path (e.g., "/opt/homebrew/bin/uv")
   - Arguments (e.g., ["run", "server.py"])
   - Environment variables needed
   - Scope (local/project/user)

2. **Generate configuration**:
   - Show `.mcp.json` entry to add
   - Show `settings.local.json` entries needed
   - Provide exact commands to run

3. **Guide through each step**:
   ```
   ✅ Step 1: Add server to .mcp.json
   ⏳ Step 2: Enable in settings
   ⏳ Step 3: Add permissions
   ⏳ Step 4: Restart Claude Code
   ⏳ Step 5: Verify connection
   ⏳ Step 6: Test tools
   ```

4. **Verify at each checkpoint**:
   - Run validation commands
   - Check configuration correctness
   - Confirm before proceeding

5. **Troubleshoot if needed**:
   - If step fails, provide debugging guidance
   - Link to relevant troubleshooting section
   - Suggest common fixes

## Example Walkthrough

```
User: /mcp-setup-checklist graphiti

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠️  MCP Server Setup Checklist
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Setting up: graphiti

Let me gather the required information...

**Server Details**:
- Name: graphiti
- Command: ?
- Arguments: ?
- Environment variables: ?

What is the command to run the server?
Example: /opt/homebrew/bin/uv or python3

[User: /opt/homebrew/bin/uv]

What arguments does it need? (comma-separated)
Example: run, --directory, /path/to/server, server.py

[User: run, --directory, /Users/harrysayers/Developer/claudelife/graphiti_mcp_server, graphiti_mcp_server.py]

What environment variables are required? (KEY=VALUE, comma-separated)
Example: NEO4J_URI=bolt://localhost:7687, NEO4J_PASSWORD=secret

[User: NEO4J_URI=bolt://localhost:7687, NEO4J_USER=neo4j, NEO4J_PASSWORD=demodemo, OPENAI_API_KEY=sk-proj-...]

Which scope should this server use?
- local (this machine only)
- project (shared with team)
- user (global for your user)

[User: local]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Generated Configuration

**1. Server Config (.mcp.json or via CLI)**:

Option A: Via CLI (Recommended)
```bash
claude mcp add graphiti \
  --command "/opt/homebrew/bin/uv" \
  --arg "run" \
  --arg "--directory" \
  --arg "/Users/harrysayers/Developer/claudelife/graphiti_mcp_server" \
  --arg "graphiti_mcp_server.py" \
  --env NEO4J_URI=bolt://localhost:7687 \
  --env NEO4J_USER=neo4j \
  --env NEO4J_PASSWORD=demodemo \
  --env OPENAI_API_KEY=sk-proj-... \
  --scope local
```

Option B: Manual .mcp.json entry
```json
{
  "mcpServers": {
    "graphiti": {
      "command": "/opt/homebrew/bin/uv",
      "args": ["run", "--directory", "/Users/harrysayers/Developer/claudelife/graphiti_mcp_server", "graphiti_mcp_server.py"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "demodemo",
        "OPENAI_API_KEY": "sk-proj-..."
      }
    }
  }
}
```

**2. Enable Server (~/.claude/settings.local.json)**:
Add to `enabledMcpjsonServers` array:
```json
"enabledMcpjsonServers": ["graphiti", ...existing servers]
```

**3. Grant Permissions (~/.claude/settings.local.json)**:
Add to `allowedTools` array:
```json
"allowedTools": ["mcp__graphiti__*", ...existing permissions]
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Would you like me to:
1. Run CLI command to add server (recommended)
2. Show manual steps for editing configs
3. Both (add via CLI and show configs)

[User: 1]

Running: claude mcp add graphiti...

✅ Server added successfully!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: ✅ Add server to .mcp.json
Step 2: ⏳ Enable in settings

I'll now update your settings.local.json to enable the server.

[Updates file]

✅ Added to enabledMcpjsonServers

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: ✅ Add server to .mcp.json
Step 2: ✅ Enable in settings
Step 3: ⏳ Add permissions

I'll add the wildcard permission mcp__graphiti__* to allowedTools.

[Updates file]

✅ Permission added

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: ✅ Add server to .mcp.json
Step 2: ✅ Enable in settings
Step 3: ✅ Add permissions
Step 4: ⏳ Restart Claude Code

Configuration is complete! You need to restart Claude Code for changes to take effect.

Please run:
```bash
exit
claude
```

After restarting, run `/mcp-setup-checklist graphiti --verify` to test the setup.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[After user restarts]

User: /mcp-setup-checklist graphiti --verify

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Verifying setup for: graphiti

Step 5: ⏳ Verify connection

Testing server connection...

[Runs: claude mcp list]

✅ Server connected successfully
   Status: ✓ Connected
   Transport: stdio

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 6: ⏳ Test tools

Checking if tools are accessible...

[Runs: ListMcpResourcesTool({ server: "graphiti" })]

✅ Tools accessible
   Found 8 tools:
   - search_memory_nodes
   - search_memory_facts
   - add_memory
   - delete_entity_edge
   - delete_episode
   - get_entity_edge
   - get_episodes
   - clear_graph

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 Setup Complete!

Step 1: ✅ Add server to .mcp.json
Step 2: ✅ Enable in settings
Step 3: ✅ Add permissions
Step 4: ✅ Restart Claude Code
Step 5: ✅ Verify connection
Step 6: ✅ Test tools

MCP server "graphiti" is ready to use!

Try running a test tool:
mcp__graphiti__search_memory_nodes({ query: "test", max_nodes: 1 })

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Verification Mode

```bash
/mcp-setup-checklist {server-name} --verify
```

Runs only verification steps (5-6) to check if server is working correctly after restart.

## Troubleshooting Integration

If any step fails, I'll provide targeted troubleshooting:

**Step 1-3 fail**: Configuration issue
- Link to MCP troubleshooting guide
- Show example configs
- Suggest checking syntax

**Step 5 fails**: Connection issue
- Check server logs
- Verify dependencies running
- Test command manually
- Link to "Server Failed to Connect" section

**Step 6 fails**: Permission issue
- Verify wildcard permission exists
- Check exact name match
- Link to "Tools Don't Appear" section

## Related Resources

- **Troubleshooting Guide**: `04-resources/guides/mcp-troubleshooting.md`
- **Serena Memory**: `.serena/memories/system_patterns_and_guidelines.md`
- **Lesson Learned**: `04-resources/lessons-learnt/251020-issue-002-mcp-permissions.md`

## Common Server Examples

### Graphiti (Python + Neo4j)
```bash
/mcp-setup-checklist graphiti
# Command: /opt/homebrew/bin/uv
# Args: run, --directory, /path/to/graphiti_mcp_server, graphiti_mcp_server.py
# Env: NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, OPENAI_API_KEY
```

### Serena (NPM package)
```bash
/mcp-setup-checklist serena
# Command: npx
# Args: -y, --package=serena-mcp, serena-mcp
# Env: (none)
```

### Supabase (NPM package)
```bash
/mcp-setup-checklist supabase
# Command: npx
# Args: -y, @modelcontextprotocol/server-supabase
# Env: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_PROJECT_ID
```

## Notes

- This command automates the manual setup process
- Prevents common mistakes (missing permissions, wrong scope)
- Validates each step before proceeding
- Provides troubleshooting if issues occur
- Can be re-run with `--verify` to check existing setup

## Starting the Setup Process

Provide the server name to begin:

```bash
/mcp-setup-checklist {server-name}           # New setup
/mcp-setup-checklist {server-name} --verify  # Verify existing
```

I'll guide you through each step interactively.
