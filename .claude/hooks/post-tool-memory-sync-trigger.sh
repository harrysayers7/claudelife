#!/bin/bash
# Post-Tool Execution Hook: Memory Sync Trigger
# Monitors Supabase, Obsidian MOKAI files, and MCP config changes

# Read JSON input from stdin
INPUT_JSON=$(cat)

# Debug: Log the JSON input
echo "[HOOK DEBUG START] $(date)" >> /tmp/claude-hook-debug.log
echo "JSON Input: $INPUT_JSON" >> /tmp/claude-hook-debug.log
echo "All environment variables:" >> /tmp/claude-hook-debug.log
env | grep -i claude >> /tmp/claude-hook-debug.log
echo "[HOOK DEBUG END]" >> /tmp/claude-hook-debug.log

SHOULD_UPDATE_MEMORY=false

# Parse JSON input using jq (or python as fallback)
if command -v jq &> /dev/null; then
  TOOL_NAME=$(echo "$INPUT_JSON" | jq -r '.tool_name')
  FILE_PATH=$(echo "$INPUT_JSON" | jq -r '.tool_input.file_path // empty')
else
  # Fallback: Simple grep-based parsing (less reliable)
  TOOL_NAME=$(echo "$INPUT_JSON" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
  FILE_PATH=$(echo "$INPUT_JSON" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)
fi

# Extract query from tool_input if it's a Supabase operation
if command -v jq &> /dev/null; then
  SQL_QUERY=$(echo "$INPUT_JSON" | jq -r '.tool_input.query // empty')
else
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
