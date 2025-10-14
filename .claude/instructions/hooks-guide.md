# Claude Code Hooks Guide

<!-- PACK_HASH: hooks-troubleshooting-guide -->
<!-- LAST_UPDATED: 2025-10-13 -->

**Load when**: Keywords detected - "hooks", "PostToolUse", "PreToolUse", "UserPromptSubmit", "hook not working", "hook configuration"

## Overview

Claude Code hooks are user-defined shell commands that execute at various points in Claude Code's lifecycle. Hooks provide deterministic control over Claude Code's behavior, ensuring certain actions always happen rather than relying on the LLM to choose to run them.

## Critical Hook Concepts

### How Hooks Receive Data

**🚨 MOST IMPORTANT**: Hooks receive data as **JSON on stdin**, NOT through environment variables or command arguments.

```bash
#!/bin/bash
# ✅ CORRECT: Read JSON from stdin
INPUT_JSON=$(cat)

# ❌ WRONG: Try to read from environment variables
FILE_PATH="${CLAUDE_TOOL_FILE_PATH:-$1}"  # These don't exist!
TOOL_NAME="${CLAUDE_TOOL_NAME:-}"         # These don't exist!
```

### Available Environment Variables

Only **one** environment variable is reliably available in hooks:

- `CLAUDE_PROJECT_DIR` - Absolute path to the project root directory

All other data comes from the JSON input on stdin.

## Hook JSON Input Structure

### PostToolUse Hook Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  }
}
```

### Key JSON Fields

- `tool_name` - Name of the tool that was executed (e.g., "Write", "Edit", "mcp__supabase__execute_sql")
- `tool_input` - Object containing the tool's input parameters
- `tool_response` - Object containing the tool's response/output
- `session_id` - Unique identifier for the current Claude Code session
- `hook_event_name` - The type of hook event (e.g., "PostToolUse", "PreToolUse")

## Hook Template

### Basic Hook Structure

```bash
#!/bin/bash
# Hook Description: What this hook does

# 1. Read JSON input from stdin
INPUT_JSON=$(cat)

# 2. Parse JSON using jq (recommended) or grep fallback
if command -v jq &> /dev/null; then
  TOOL_NAME=$(echo "$INPUT_JSON" | jq -r '.tool_name')
  FILE_PATH=$(echo "$INPUT_JSON" | jq -r '.tool_input.file_path // empty')
else
  # Fallback: grep-based parsing (less reliable)
  TOOL_NAME=$(echo "$INPUT_JSON" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
  FILE_PATH=$(echo "$INPUT_JSON" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)
fi

# 3. Debug logging (optional but recommended during development)
echo "[HOOK DEBUG] $(date)" >> /tmp/my-hook-debug.log
echo "Tool: $TOOL_NAME" >> /tmp/my-hook-debug.log
echo "File: $FILE_PATH" >> /tmp/my-hook-debug.log

# 4. Implement your hook logic
if [[ "$TOOL_NAME" == "Write" ]]; then
  if [[ "$FILE_PATH" == *".env"* ]]; then
    echo "⚠️  Warning: Modified .env file"
  fi
fi

# 5. Exit with appropriate code
exit 0  # Success
# exit 1  # Failure (for blocking hooks)
```

## Hook Types

### PostToolUse Hooks

Execute **after** a tool completes. Useful for:
- Monitoring file changes
- Triggering follow-up actions
- Logging tool usage
- Sending notifications

**Configuration in `.claude/settings.json`:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/post-write-hook.sh"
          }
        ]
      },
      {
        "matcher": "mcp__supabase__*",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/db-change-hook.sh"
          }
        ]
      }
    ]
  }
}
```

### PreToolUse Hooks

Execute **before** a tool runs. Can block tool execution. Useful for:
- Validation checks
- Permission verification
- Safety checks
- Audit logging

**Note**: PreToolUse hooks can return non-zero exit codes to block operations (though Claude Code's blocking behavior has limitations).

### UserPromptSubmit Hooks

Execute when the user submits a prompt. Useful for:
- Context injection
- Automatic memory updates
- Session tracking
- Prompt preprocessing

## Common Patterns

### Pattern 1: File Change Detection

```bash
#!/bin/bash
INPUT_JSON=$(cat)

if command -v jq &> /dev/null; then
  TOOL_NAME=$(echo "$INPUT_JSON" | jq -r '.tool_name')
  FILE_PATH=$(echo "$INPUT_JSON" | jq -r '.tool_input.file_path // empty')
fi

# Check for specific file patterns
if [[ "$FILE_PATH" == *"01-areas/business/mokai"* ]]; then
  echo "💾 Business documentation updated"
  echo "   Consider updating Serena's memory: /update-serena-memory"
fi

if [[ "$FILE_PATH" == *".mcp.json"* ]]; then
  echo "💾 MCP configuration changed"
  echo "   Restart Claude Code to load new configuration"
fi
```

### Pattern 2: Database Operation Monitoring

```bash
#!/bin/bash
INPUT_JSON=$(cat)

if command -v jq &> /dev/null; then
  TOOL_NAME=$(echo "$INPUT_JSON" | jq -r '.tool_name')
  SQL_QUERY=$(echo "$INPUT_JSON" | jq -r '.tool_input.query // empty')
fi

# Monitor specific database operations
if [[ "$TOOL_NAME" == "mcp__supabase__execute_sql" ]]; then
  if [[ "$SQL_QUERY" == *"DELETE"* ]] || [[ "$SQL_QUERY" == *"DROP"* ]]; then
    echo "⚠️  WARNING: Destructive database operation detected"
    echo "   Query: $SQL_QUERY"
  fi

  if [[ "$SQL_QUERY" == *"invoices"* ]] || [[ "$SQL_QUERY" == *"transactions"* ]]; then
    echo "💰 Financial data modified"
  fi
fi
```

### Pattern 3: Conditional Notifications

```bash
#!/bin/bash
INPUT_JSON=$(cat)

if command -v jq &> /dev/null; then
  TOOL_NAME=$(echo "$INPUT_JSON" | jq -r '.tool_name')
  FILE_PATH=$(echo "$INPUT_JSON" | jq -r '.tool_input.file_path // empty')
fi

SHOULD_NOTIFY=false

# Check multiple conditions
if [[ "$FILE_PATH" == *"CLAUDE.md"* ]]; then
  echo "📝 Project instructions updated"
  SHOULD_NOTIFY=true
fi

if [[ "$FILE_PATH" == *".claude/agents/"* ]]; then
  echo "🤖 Agent configuration changed"
  SHOULD_NOTIFY=true
fi

# Single notification at the end
if [[ "$SHOULD_NOTIFY" == true ]]; then
  echo ""
  echo "🔄 Recommendation: Update Serena's memory"
  echo "   Run: /update-serena-memory"
  echo ""
fi
```

## Debugging Hooks

### Debug Log Pattern

Always add debug logging during hook development:

```bash
#!/bin/bash
INPUT_JSON=$(cat)

# Debug: Log everything
DEBUG_LOG="/tmp/claude-hook-debug.log"
echo "[HOOK DEBUG START] $(date)" >> "$DEBUG_LOG"
echo "JSON Input: $INPUT_JSON" >> "$DEBUG_LOG"
echo "Environment:" >> "$DEBUG_LOG"
env | grep -i claude >> "$DEBUG_LOG"

# Parse values
if command -v jq &> /dev/null; then
  TOOL_NAME=$(echo "$INPUT_JSON" | jq -r '.tool_name')
  FILE_PATH=$(echo "$INPUT_JSON" | jq -r '.tool_input.file_path // empty')
fi

# Debug: Log parsed values
echo "Parsed values:" >> "$DEBUG_LOG"
echo "  TOOL_NAME: $TOOL_NAME" >> "$DEBUG_LOG"
echo "  FILE_PATH: $FILE_PATH" >> "$DEBUG_LOG"
echo "[HOOK DEBUG END]" >> "$DEBUG_LOG"

# Your hook logic here
```

### Check Debug Logs

```bash
# Watch logs in real-time
tail -f /tmp/claude-hook-debug.log

# View recent activity
tail -50 /tmp/claude-hook-debug.log

# Search for specific tool
grep "Edit" /tmp/claude-hook-debug.log
```

## Common Issues & Solutions

### Issue 1: Hook Not Executing

**Symptoms**: Hook never runs, no output appears

**Solutions**:
1. Check hook is executable: `chmod +x .claude/hooks/your-hook.sh`
2. Verify configuration in `.claude/settings.json`
3. Check hook matcher pattern matches the tool name
4. Add debug logging to confirm hook is being called

### Issue 2: Can't Parse JSON Input

**Symptoms**: Variables are empty, hook logic doesn't work

**Solutions**:
1. Ensure you're reading stdin: `INPUT_JSON=$(cat)`
2. Install `jq` for reliable parsing: `brew install jq`
3. Check debug logs to see actual JSON structure
4. Use grep fallback if jq unavailable

### Issue 3: Environment Variables Not Available

**Symptoms**: `$CLAUDE_TOOL_NAME`, `$FILE_PATH` are empty

**Solution**: These variables **don't exist**! All data comes from JSON on stdin. Only `CLAUDE_PROJECT_DIR` is available as an environment variable.

### Issue 4: Hook Doesn't Block Operations

**Symptoms**: PreToolUse hook returns non-zero exit code but operation proceeds

**Solution**: Claude Code hooks are "advisory" by design. They report violations but don't always prevent file operations. Use hooks for monitoring and alerting, not hard blocking.

## Best Practices

### 1. Always Read stdin First

```bash
#!/bin/bash
INPUT_JSON=$(cat)  # Do this FIRST, before anything else
```

### 2. Use jq for JSON Parsing

```bash
# Install jq
brew install jq

# Use jq in hooks
TOOL_NAME=$(echo "$INPUT_JSON" | jq -r '.tool_name')
```

### 3. Provide Fallback Parsing

```bash
if command -v jq &> /dev/null; then
  # Primary: jq parsing
  TOOL_NAME=$(echo "$INPUT_JSON" | jq -r '.tool_name')
else
  # Fallback: grep parsing
  TOOL_NAME=$(echo "$INPUT_JSON" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
fi
```

### 4. Add Debug Logging During Development

```bash
# Always log to /tmp during development
echo "[DEBUG] $(date): $TOOL_NAME on $FILE_PATH" >> /tmp/hook-debug.log
```

### 5. Make Hooks Fast

Hooks run synchronously and block Claude Code's response. Keep them fast:
- Avoid expensive operations
- Don't make external API calls
- Use async background processes for slow tasks

### 6. Handle Missing Fields Gracefully

```bash
# Use jq's // operator for defaults
FILE_PATH=$(echo "$INPUT_JSON" | jq -r '.tool_input.file_path // empty')

# Check before using
if [[ -n "$FILE_PATH" ]]; then
  # Safe to use FILE_PATH
fi
```

## Tool-Specific JSON Structures

### Write Tool

```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/absolute/path/to/file.txt",
    "content": "file contents here"
  },
  "tool_response": {
    "filePath": "/absolute/path/to/file.txt",
    "success": true
  }
}
```

### Edit Tool

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/absolute/path/to/file.txt",
    "old_string": "text to replace",
    "new_string": "replacement text"
  },
  "tool_response": {
    "filePath": "/absolute/path/to/file.txt",
    "success": true
  }
}
```

### Supabase MCP Tools

```json
{
  "tool_name": "mcp__supabase__execute_sql",
  "tool_input": {
    "project_id": "gshsshaodoyttdxippwx",
    "query": "SELECT * FROM invoices"
  },
  "tool_response": {
    "rows": [...],
    "count": 10
  }
}
```

## Example: Memory Sync Hook

This is the actual hook used in claudelife to remind about memory updates:

```bash
#!/bin/bash
# Post-Tool Execution Hook: Memory Sync Trigger
# Monitors Supabase, Obsidian MOKAI files, and MCP config changes

# Read JSON input from stdin
INPUT_JSON=$(cat)

# Debug logging
echo "[HOOK DEBUG START] $(date)" >> /tmp/claude-hook-debug.log
echo "JSON Input: $INPUT_JSON" >> /tmp/claude-hook-debug.log

SHOULD_UPDATE_MEMORY=false

# Parse JSON input using jq (or python as fallback)
if command -v jq &> /dev/null; then
  TOOL_NAME=$(echo "$INPUT_JSON" | jq -r '.tool_name')
  FILE_PATH=$(echo "$INPUT_JSON" | jq -r '.tool_input.file_path // empty')
  SQL_QUERY=$(echo "$INPUT_JSON" | jq -r '.tool_input.query // empty')
else
  # Fallback: Simple grep-based parsing
  TOOL_NAME=$(echo "$INPUT_JSON" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
  FILE_PATH=$(echo "$INPUT_JSON" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)
  SQL_QUERY=$(echo "$INPUT_JSON" | grep -o '"query":"[^"]*"' | cut -d'"' -f4)
fi

# Debug: Log parsed values
echo "Parsed values:" >> /tmp/claude-hook-debug.log
echo "  TOOL_NAME: $TOOL_NAME" >> /tmp/claude-hook-debug.log
echo "  FILE_PATH: $FILE_PATH" >> /tmp/claude-hook-debug.log
echo "  SQL_QUERY: $SQL_QUERY" >> /tmp/claude-hook-debug.log

# 1. Supabase database changes
if [[ "$TOOL_NAME" == "mcp__supabase__execute_sql" ]]; then
  if [[ "$SQL_QUERY" == *"invoices"* ]] || [[ "$SQL_QUERY" == *"entities"* ]] || [[ "$SQL_QUERY" == *"contacts"* ]]; then
    echo "💾 Supabase: Financial data updated"
    SHOULD_UPDATE_MEMORY=true
  fi
fi

# 2. Obsidian file changes in MOKAI business areas
if [[ "$FILE_PATH" == *"01-areas/business/mokai"* ]] || \
   [[ "$FILE_PATH" == *".claude/instructions/"* ]] || \
   [[ "$FILE_PATH" == *".claude/agents/"* ]] || \
   [[ "$FILE_PATH" == *".claude/commands/"* ]]; then
  echo "💾 Obsidian: MOKAI documentation updated"
  SHOULD_UPDATE_MEMORY=true
fi

# 3. MCP server configuration changes
if [[ "$FILE_PATH" == *".mcp.json"* ]]; then
  echo "💾 MCP: Server configuration changed"
  SHOULD_UPDATE_MEMORY=true
fi

# Unified reminder
if [[ "$SHOULD_UPDATE_MEMORY" == true ]]; then
  echo ""
  echo "🔄 Recommendation: Update Serena's memory to reflect changes"
  echo "   Run: /update-serena-memory"
  echo ""
fi
```

## Testing Hooks

### Test Hook Execution

```bash
# Create a test file to trigger Write hook
echo "test" >> test-file.md

# Watch debug logs
tail -f /tmp/claude-hook-debug.log

# Clean up
rm test-file.md
```

### Verify Hook Configuration

```bash
# Check settings.json syntax
jq . .claude/settings.json

# Verify hook file exists and is executable
ls -la .claude/hooks/

# Test hook script directly (simulate stdin)
echo '{"tool_name":"Write","tool_input":{"file_path":"test.md"}}' | .claude/hooks/your-hook.sh
```

## Related Documentation

- [Claude Code Hooks Official Docs](https://docs.claude.com/en/docs/claude-code/hooks)
- [Technical Pack](./.claude/instructions/technical-pack.md)
- [Memory System](./.claude/instructions/memory-system.md)

## Key Takeaways

1. **Always read stdin first**: `INPUT_JSON=$(cat)`
2. **Use jq for JSON parsing**: More reliable than grep
3. **Only CLAUDE_PROJECT_DIR is available** as environment variable
4. **All other data comes from JSON** on stdin
5. **Add debug logging** during development
6. **Keep hooks fast** - they block Claude Code responses
7. **Handle missing fields gracefully** with jq's `// empty` operator
8. **Check the tool_name** to filter which hooks execute

---

**Last Updated**: 2025-10-13
**Author**: Claude Code + Harry Sayers
**Purpose**: Prevent future hook troubleshooting issues by documenting correct patterns
