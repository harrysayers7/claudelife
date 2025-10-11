#!/bin/bash
# Post-Tool Execution Hook: Memory Sync Trigger
# Monitors Supabase, Obsidian MOKAI files, and MCP config changes

SHOULD_UPDATE_MEMORY=false

# 1. Supabase database changes
if [[ "$TOOL_NAME" == "mcp__supabase__execute_sql" ]] && [[ "$EXIT_CODE" == "0" ]]; then
  if [[ "$TOOL_ARGS" == *"invoices"* ]] || [[ "$TOOL_ARGS" == *"entities"* ]] || [[ "$TOOL_ARGS" == *"contacts"* ]]; then
    echo "💾 Supabase: Financial data updated"
    SHOULD_UPDATE_MEMORY=true
  fi
fi

# 2. Obsidian file changes in MOKAI business areas
if [[ "$TOOL_NAME" == "Write" ]] || [[ "$TOOL_NAME" == "Edit" ]]; then
  if [[ "$TOOL_ARGS" == *"01-areas/business/mokai"* ]] || \
     [[ "$TOOL_ARGS" == *".claude/instructions/"* ]] || \
     [[ "$TOOL_ARGS" == *".claude/agents/"* ]] || \
     [[ "$TOOL_ARGS" == *".claude/commands/"* ]]; then
    echo "💾 Obsidian: MOKAI documentation updated"
    SHOULD_UPDATE_MEMORY=true
  fi
fi

# 3. MCP server configuration changes
if [[ "$TOOL_NAME" == "Write" ]] || [[ "$TOOL_NAME" == "Edit" ]]; then
  if [[ "$TOOL_ARGS" == *".mcp.json"* ]]; then
    echo "💾 MCP: Server configuration changed"
    SHOULD_UPDATE_MEMORY=true
  fi
fi

# Unified reminder
if [[ "$SHOULD_UPDATE_MEMORY" == true ]]; then
  echo ""
  echo "🔄 Recommendation: Update Serena's memory to reflect changes"
  echo "   Run: /update-serena-memory"
  echo ""
fi
