# Setup File Protection Hook

Sets up file protection for critical documentation and configuration files.

## What it protects:

### 🔴 CRITICAL (Requires confirmation):
- `/CLAUDE.md` - Main Claude Code instructions
- `/.taskmaster/CLAUDE.md` - Task Master integration guide
- `/package.json` - Project dependencies
- `/trigger.config.*` - Trigger.dev configuration
- `/.mcp.json` - MCP server configuration
- `/context-manager-analysis.md` - System analysis

### 🟡 IMPORTANT (Warning only):
- `/README.md` - Project documentation
- `/context/*/*.md` - Context documentation
- `/.claude/instructions/*.md` - Domain packs
- `/memory/conversation-context.md` - Session memory

## Installation:

Copy the hook file to your Claude Code settings:
```bash
cp .claude/hooks/protect-critical-docs.json ~/.claude/hooks/
```

Or install system-wide protection:
```bash
# Add to ~/.claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == */CLAUDE.md ]] || [[ \"$CLAUDE_TOOL_FILE_PATH\" == */.taskmaster/CLAUDE.md ]] || [[ \"$CLAUDE_TOOL_FILE_PATH\" == */package.json ]] || [[ \"$CLAUDE_TOOL_FILE_PATH\" == */.mcp.json ]]; then echo '⚠️  CRITICAL FILE: '$CLAUDE_TOOL_FILE_PATH >&2; echo 'This file controls core system behavior. Continue? (y/N)' >&2; read -r response; [[ ! \"$response\" =~ ^[Yy]$ ]] && exit 1; fi"
          }
        ]
      }
    ]
  }
}
```

## Usage:
- Hook runs automatically before any file edit
- Shows warning with file importance level
- Asks for confirmation on critical files
- Allows cancellation to prevent accidental changes

This protects your system configuration while still allowing intentional edits when needed.
