#!/bin/bash
# Post-Tool Execution Hook: Auto-Diary Capture
# Automatically logs MOKAI wins, learnings, and context to diary when tasks complete

# Read JSON input from stdin
INPUT_JSON=$(cat)

# Debug logging
DEBUG_LOG="/tmp/claude-auto-diary-debug.log"
echo "[AUTO-DIARY DEBUG START] $(date)" >> "$DEBUG_LOG"
echo "JSON Input: $INPUT_JSON" >> "$DEBUG_LOG"

# Parse JSON input
if command -v jq &> /dev/null; then
  TOOL_NAME=$(echo "$INPUT_JSON" | jq -r '.tool_name')
  TOOL_INPUT=$(echo "$INPUT_JSON" | jq -r '.tool_input')

  # For Bash tool, get the command
  BASH_COMMAND=$(echo "$INPUT_JSON" | jq -r '.tool_input.command // empty')

  # For task-master commands
  TASK_ID=$(echo "$BASH_COMMAND" | grep -oP 'task-master.*--id=\K[0-9.]+' || echo "")
  TASK_STATUS=$(echo "$BASH_COMMAND" | grep -oP 'task-master.*--status=\K\w+' || echo "")

  # For file edits (capture file path for context)
  FILE_PATH=$(echo "$INPUT_JSON" | jq -r '.tool_input.file_path // empty')
else
  # Fallback: Simple grep-based parsing
  TOOL_NAME=$(echo "$INPUT_JSON" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
  BASH_COMMAND=$(echo "$INPUT_JSON" | grep -o '"command":"[^"]*"' | sed 's/"command":"//;s/"$//')
  FILE_PATH=$(echo "$INPUT_JSON" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)
fi

echo "Parsed values:" >> "$DEBUG_LOG"
echo "  TOOL_NAME: $TOOL_NAME" >> "$DEBUG_LOG"
echo "  BASH_COMMAND: $BASH_COMMAND" >> "$DEBUG_LOG"
echo "  TASK_ID: $TASK_ID" >> "$DEBUG_LOG"
echo "  TASK_STATUS: $TASK_STATUS" >> "$DEBUG_LOG"
echo "  FILE_PATH: $FILE_PATH" >> "$DEBUG_LOG"

# Get today's date in YYYY-MM-DD format
TODAY=$(date +%Y-%m-%d)
DIARY_DIR="01-areas/business/mokai/diary"
DIARY_FILE="$DIARY_DIR/$TODAY-mokai-daily.md"

# Check if we're in the claudelife directory
if [[ ! -d "$DIARY_DIR" ]]; then
  echo "  Not in claudelife directory, skipping auto-diary" >> "$DEBUG_LOG"
  echo "[AUTO-DIARY DEBUG END]" >> "$DEBUG_LOG"
  exit 0
fi

# Function to add entry to diary section
add_to_diary_section() {
  local section="$1"
  local entry="$2"

  # Create diary from template if it doesn't exist
  if [[ ! -f "$DIARY_FILE" ]]; then
    if [[ -f "$DIARY_DIR/.diary-template.md" ]]; then
      cp "$DIARY_DIR/.diary-template.md" "$DIARY_FILE"
      # Update the date in frontmatter
      sed -i '' "s/journal-date: .*/journal-date: $TODAY/" "$DIARY_FILE"
    else
      echo "  Diary template not found" >> "$DEBUG_LOG"
      return 1
    fi
  fi

  # Find the section and add entry if not already present
  if grep -q "## $section" "$DIARY_FILE"; then
    # Check if entry already exists (avoid duplicates)
    if ! grep -qF "$entry" "$DIARY_FILE"; then
      # Use awk to add entry after the section header and its first bullet
      awk -v section="## $section" -v entry="- $entry" '
        /^## / { in_section = ($0 == section) }
        in_section && /^-/ && !added { print; print entry; added=1; next }
        { print }
      ' "$DIARY_FILE" > "$DIARY_FILE.tmp" && mv "$DIARY_FILE.tmp" "$DIARY_FILE"

      echo "  Added to section: $section" >> "$DEBUG_LOG"
      echo "  Entry: $entry" >> "$DEBUG_LOG"
      return 0
    else
      echo "  Entry already exists in $section" >> "$DEBUG_LOG"
      return 1
    fi
  else
    echo "  Section not found: $section" >> "$DEBUG_LOG"
    return 1
  fi
}

# Detect and capture different types of events
CAPTURED=false

# 1. Task Master task completion (MOKAI-related)
if [[ "$TOOL_NAME" == "Bash" ]] && [[ "$BASH_COMMAND" == *"task-master"* ]] && [[ "$TASK_STATUS" == "done" ]]; then
  # Check if task is MOKAI-related
  if [[ "$BASH_COMMAND" == *"mokai"* ]] || [[ "$BASH_COMMAND" == *"MOKAI"* ]]; then
    # Extract task description (this is simplified - could be enhanced with task file reading)
    TASK_DESCRIPTION="Completed task $TASK_ID"

    if add_to_diary_section "🏆 Wins" "$TASK_DESCRIPTION"; then
      CAPTURED=true
      echo "✅ Auto-captured: Task completion → Wins"
    fi
  fi
fi

# 2. MOKAI document updates (learnings/context)
if [[ "$FILE_PATH" == *"01-areas/business/mokai"* ]]; then
  # Determine if it's learning material or general context
  if [[ "$FILE_PATH" == *"research"* ]] || [[ "$FILE_PATH" == *"learning"* ]] || [[ "$FILE_PATH" == *"guide"* ]]; then
    CONTEXT="Updated learning material: $(basename "$FILE_PATH" .md)"
    if add_to_diary_section "💡 Learnings" "$CONTEXT"; then
      CAPTURED=true
      echo "📚 Auto-captured: Research update → Learnings"
    fi
  elif [[ "$FILE_PATH" == *"dashboard"* ]] || [[ "$FILE_PATH" == *"checklist"* ]]; then
    CONTEXT="Updated $(basename "$FILE_PATH" .md)"
    if add_to_diary_section "📝 Context/Updates" "$CONTEXT"; then
      CAPTURED=true
      echo "📋 Auto-captured: Dashboard/checklist update → Context"
    fi
  fi
fi

# 3. Slash command completions (MOKAI commands)
if [[ "$BASH_COMMAND" == *"/mokai-"* ]]; then
  COMMAND_NAME=$(echo "$BASH_COMMAND" | grep -oP '/mokai-\w+')
  CONTEXT="Executed $COMMAND_NAME command"

  if add_to_diary_section "📝 Context/Updates" "$CONTEXT"; then
    CAPTURED=true
    echo "⚡ Auto-captured: MOKAI command → Context"
  fi
fi

# 4. Client/tender work completion
if [[ "$FILE_PATH" == *"tender"* ]] || [[ "$FILE_PATH" == *"proposal"* ]] || [[ "$FILE_PATH" == *"client"* ]]; then
  CONTEXT="Worked on $(basename "$FILE_PATH" .md)"
  if add_to_diary_section "🏆 Wins" "$CONTEXT"; then
    CAPTURED=true
    echo "💼 Auto-captured: Client work → Wins"
  fi
fi

# Output notification if something was captured
if [[ "$CAPTURED" == true ]]; then
  echo ""
  echo "📔 Auto-Diary: Captured entry to $TODAY diary"
  echo "   View: cat $DIARY_FILE"
  echo ""
fi

echo "[AUTO-DIARY DEBUG END]" >> "$DEBUG_LOG"

# Always exit 0 (non-blocking)
exit 0
