---
created: "2025-10-11 18:45"
updated: "2025-10-11 18:45"
system_type: "automation"
status: "active"
---

# Memory Sync Hook

## Overview

**Purpose**: Automatically detects when critical MOKAI business data changes and reminds you to update Serena MCP's memory files, ensuring the agent-mokai always has current context.

**Type**: Claude Code post-tool execution hook

**Status**: active

## Location

**Primary Files**:
- [.claude/hooks/post-tool-memory-sync-trigger.sh](/.claude/hooks/post-tool-memory-sync-trigger.sh) - Hook script that monitors tool executions
- [.claude/settings.json:3](/.claude/settings.json#L3) - Hook configuration

## Architecture

### Components

1. **Post-Tool Execution Hook** (.claude/hooks/post-tool-memory-sync-trigger.sh)
   - Purpose: Monitors successful tool executions and detects data changes
   - Triggers: Runs after every tool execution in Claude Code
   - Detection: Pattern matching on tool names and arguments

2. **Hook Configuration** (.claude/settings.json)
   - Purpose: Registers the hook with Claude Code
   - Configuration: Specifies bash execution with script path

### Data Flow

```
Tool Execution (Supabase/Edit/Write)
  → Hook Script Runs
  → Pattern Matching (invoices/entities/contacts/mokai docs/.mcp.json)
  → Memory Update Reminder Displayed
  → User Runs /update-serena-memory
  → Serena Memory Files Updated
```

### Integration Points

- **Supabase MCP**: Detects SQL queries touching `invoices`, `entities`, `contacts` tables
- **File System Tools**: Monitors `Write`/`Edit` operations in MOKAI business areas
- **MCP Configuration**: Tracks changes to `.mcp.json`
- **Serena MCP**: Triggered update command refreshes `.serena/memories/`

## Monitored Data Sources

### 1. Supabase Database
**Tool**: `mcp__supabase__execute_sql`
**Triggers on**: Queries touching these tables:
- `invoices` - Financial records
- `entities` - Business entities (Harrison Robert Sayers, MOKAI, MOK HOUSE)
- `contacts` - Business contacts and vendors

### 2. Obsidian Files
**Tools**: `Write`, `Edit`
**Triggers on**: Changes to these directories:
- `01-areas/business/mokai/` - MOKAI business documentation
- `.claude/instructions/` - Domain pack instructions (business/technical/automation)
- `.claude/agents/` - Agent configurations (agent-mokai)
- `.claude/commands/` - Custom slash commands

### 3. MCP Configuration
**Tools**: `Write`, `Edit`
**Triggers on**: Changes to:
- `.mcp.json` - MCP server configurations

## Configuration

### Hook Script Environment Variables
None required - uses Claude Code's built-in variables:
- `$TOOL_NAME` - Name of the tool that executed
- `$EXIT_CODE` - Exit code (0 = success)
- `$TOOL_ARGS` - Arguments/parameters passed to the tool

### Setup Requirements

1. Ensure hook script is executable:
   ```bash
   chmod +x .claude/hooks/post-tool-memory-sync-trigger.sh
   ```

2. Hook configuration in `.claude/settings.json`:
   ```json
   {
     "hooks": {
       "postToolExecution": [
         {
           "name": "memory-sync-trigger",
           "command": "bash",
           "args": [".claude/hooks/post-tool-memory-sync-trigger.sh"]
         }
       ]
     }
   }
   ```

3. Restart Claude Code for hook to take effect

## Usage

### Automatic Triggering

The hook runs automatically after every tool execution. When it detects relevant changes, you'll see:

```
💾 Supabase: Financial data updated

🔄 Recommendation: Update Serena's memory to reflect changes
   Run: /update-serena-memory
```

Or:

```
💾 Obsidian: MOKAI documentation updated

🔄 Recommendation: Update Serena's memory to reflect changes
   Run: /update-serena-memory
```

Or:

```
💾 MCP: Server configuration changed

🔄 Recommendation: Update Serena's memory to reflect changes
   Run: /update-serena-memory
```

### Manual Memory Update

When you see the reminder:

```bash
/update-serena-memory
```

This command will:
1. Scan the codebase for structural changes
2. Update Serena's memory files in `.serena/memories/`
3. Ensure agent-mokai has current context

## Examples

### Example 1: Supabase Invoice Update

```javascript
// You create a new invoice
mcp__supabase__execute_sql({
  query: "INSERT INTO invoices (entity_id, amount, due_date) VALUES (...)"
})

// Hook detects:
// ✓ Tool name: "mcp__supabase__execute_sql"
// ✓ Exit code: 0 (success)
// ✓ Query contains: "invoices"

// Output displayed:
// 💾 Supabase: Financial data updated
// 🔄 Recommendation: Update Serena's memory to reflect changes
//    Run: /update-serena-memory
```

### Example 2: MOKAI Documentation Edit

```javascript
// You update MOKAI operations guide
Edit({
  file_path: "01-areas/business/mokai/docs/operations-guide.md",
  old_string: "...",
  new_string: "..."
})

// Hook detects:
// ✓ Tool name: "Edit"
// ✓ Exit code: 0
// ✓ File path contains: "01-areas/business/mokai"

// Output displayed:
// 💾 Obsidian: MOKAI documentation updated
// 🔄 Recommendation: Update Serena's memory to reflect changes
//    Run: /update-serena-memory
```

### Example 3: MCP Server Configuration Change

```javascript
// You add a new MCP server
Write({
  file_path: ".mcp.json",
  content: "{ ... new server config ... }"
})

// Hook detects:
// ✓ Tool name: "Write"
// ✓ Exit code: 0
// ✓ File path: ".mcp.json"

// Output displayed:
// 💾 MCP: Server configuration changed
// 🔄 Recommendation: Update Serena's memory to reflect changes
//    Run: /update-serena-memory
```

## Dependencies

### External Services
- None - pure bash script

### Claude Code Built-in Variables
- `$TOOL_NAME` - Provided by Claude Code hooks system
- `$EXIT_CODE` - Provided by Claude Code hooks system
- `$TOOL_ARGS` - Provided by Claude Code hooks system

### Internal Dependencies
- `/update-serena-memory` slash command - Updates Serena MCP memory files
- Serena MCP server - Provides memory management functionality

## Troubleshooting

### Common Issues

**Issue 1: Hook not running**
- Cause: Script not executable or Claude Code not restarted
- Solution:
  ```bash
  chmod +x .claude/hooks/post-tool-memory-sync-trigger.sh
  # Restart Claude Code
  ```

**Issue 2: Hook runs but no output**
- Cause: Pattern matching not detecting the change
- Solution: Check if tool name/arguments match patterns in script
- Debug: Add `echo "TOOL: $TOOL_NAME, ARGS: $TOOL_ARGS"` to script

**Issue 3: False positives**
- Cause: Pattern too broad (e.g., any Edit in .claude/)
- Solution: Narrow pattern matching in script (e.g., specific subdirectories)

### Debugging

```bash
# Test hook manually
export TOOL_NAME="mcp__supabase__execute_sql"
export EXIT_CODE="0"
export TOOL_ARGS='query: "UPDATE invoices SET ..."'
bash .claude/hooks/post-tool-memory-sync-trigger.sh

# Check hook configuration
cat .claude/settings.json | grep -A 10 "hooks"

# Verify script is executable
ls -l .claude/hooks/post-tool-memory-sync-trigger.sh
```

## Monitoring & Maintenance

- **Logs**: Hook output appears in Claude Code conversation
- **Monitoring**: Watch for reminder messages during normal workflow
- **Update Frequency**: Update script patterns as new data sources are added

## Related Systems

- [agent-mokai](/.claude/agents/agent-mokai.md) - Primary beneficiary of fresh memory
- [Serena MCP](07-context/systems/mcp-servers/serena.md) - Provides memory management
- [/update-serena-memory command](/.claude/commands/update-serena-memory.md) - Triggered by this hook

## Why This Exists

### Problem Solved
The agent-mokai relies on Serena MCP's memory files to understand:
- Project structure and file locations
- Available commands and workflows
- MOKAI business context and operations
- Database schemas and relationships

When business data changes (new invoices, updated docs, new MCP servers), Serena's memory becomes stale, leading to:
- Outdated context in agent responses
- Incorrect file path suggestions
- Missing command awareness
- Poor code assistance

### Solution Approach
Rather than manually remembering to update Serena's memory after every significant change, this hook:
1. **Monitors critical operations** - Watches for data mutations
2. **Detects relevant changes** - Pattern matches on business-critical areas
3. **Provides timely reminders** - Prompts memory update when needed
4. **Maintains context freshness** - Ensures agent always has current information

### Business Value
- **Accuracy**: Agent provides correct, up-to-date information
- **Efficiency**: No manual tracking of when to update memory
- **Reliability**: Consistent memory updates prevent stale context
- **Developer Experience**: Automatic reminders in natural workflow

## Future Enhancements

- **Auto-update mode**: Option to automatically run `/update-serena-memory` instead of just reminding
- **Batch updates**: Collect multiple changes and trigger single update
- **Change logging**: Track what changed for audit trail
- **Conditional updates**: Smart detection of when update is truly needed (e.g., skip trivial changes)
- **Integration with git hooks**: Trigger memory update on commits that touch critical areas
- **Notification preferences**: Configure reminder style (silent, notification, blocking)

## Change Log

- 2025-10-11: Initial implementation - Monitors Supabase, Obsidian MOKAI files, and MCP config
