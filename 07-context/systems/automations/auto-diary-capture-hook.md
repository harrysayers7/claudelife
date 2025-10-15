---
created: "2025-10-15 13:40"
system_type: "automation"
status: "active"
---

# Auto-Diary Capture Hook

## Overview

**Purpose**: Automatically logs MOKAI wins, learnings, and context to daily diary entries when completing tasks or making significant progress, eliminating manual logging friction and ensuring comprehensive activity tracking.

**Type**: Claude Code PostToolUse Hook

**Status**: Active

**Business Value**:
- Reduces cognitive overhead of manual diary updates during focused work
- Ensures complete activity logging for `/mokai-status` strategic reviews
- Captures wins in real-time rather than relying on end-of-day recall
- Complements `/mokai-dump` by handling routine captures automatically

## Location

**Primary Files**:
- [.claude/hooks/post-tool-auto-diary-capture.sh:1-175](/.claude/hooks/post-tool-auto-diary-capture.sh) - Main hook script with capture logic
- [.claude/settings.json:3-40](/.claude/settings.json) - Hook registration configuration
- [.claude/hooks/README-auto-diary.md](/.claude/hooks/README-auto-diary.md) - User documentation

**Configuration**:
- `.claude/settings.json` - Registers hook for Write, Edit, and Bash tool executions

**Related Directories**:
- `01-areas/business/mokai/diary/` - Target directory for diary entries
- `01-areas/business/mokai/diary/.diary-template.md` - Template for new diary creation

**Debug Output**:
- `/tmp/claude-auto-diary-debug.log` - Full execution trace for troubleshooting

## Architecture

### Components

1. **Hook Script** ([.claude/hooks/post-tool-auto-diary-capture.sh](/.claude/hooks/post-tool-auto-diary-capture.sh))
   - Purpose: Receives PostToolUse events, analyzes context, routes entries to diary sections
   - Key functions: JSON parsing, pattern detection, diary file manipulation, duplicate prevention
   - Execution: Triggered after Write, Edit, and Bash tools complete

2. **Hook Registration** ([.claude/settings.json](/.claude/settings.json))
   - Purpose: Configures Claude Code to execute hook on tool completion
   - Matchers: `Write`, `Edit`, `Bash`
   - Integration: Runs alongside `post-tool-memory-sync-trigger.sh` hook

3. **Diary Template** ([01-areas/business/mokai/diary/.diary-template.md](01-areas/business/mokai/diary/.diary-template.md))
   - Purpose: Template for creating new daily diary entries
   - Sections: What I Did Today, Learnings, Wins, Blockers, Context/Updates, Tomorrow's Focus, Agent-Mokai Discussion

### Data Flow

```
Claude Code Tool Execution (Write/Edit/Bash)
    ↓
PostToolUse Hook Trigger
    ↓
Hook receives JSON payload:
  - tool_name
  - tool_input (command, file_path, etc.)
  - tool_output
    ↓
Pattern Detection & Analysis:
  - Task completion? → Extract task ID
  - MOKAI file edit? → Identify file type
  - Command execution? → Parse command name
    ↓
Section Routing Logic:
  - Task done → 🏆 Wins
  - Research/learning update → 💡 Learnings
  - Dashboard/checklist → 📝 Context/Updates
  - MOKAI command → 📝 Context/Updates
  - Client/tender work → 🏆 Wins
    ↓
Diary File Operations:
  1. Create from template if missing
  2. Find target section
  3. Check for duplicates
  4. Append entry
    ↓
User Notification: "📔 Auto-Diary: Captured entry"
```

### Integration Points

- **Claude Code Hook System**: Receives PostToolUse events via JSON stdin
- **MOKAI Diary Structure**: Writes to `01-areas/business/mokai/diary/YYYY-MM-DD-mokai-daily.md`
- **task-master**: Detects `task-master set-status --status=done` completions
- **MOKAI Slash Commands**: Logs executions of `/mokai-*` commands
- **File System**: Monitors edits in `01-areas/business/mokai/` directory

## Configuration

### Hook Registration (settings.json)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/post-tool-auto-diary-capture.sh"
          }
        ]
      },
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/post-tool-auto-diary-capture.sh"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/post-tool-auto-diary-capture.sh"
          }
        ]
      }
    ]
  }
}
```

### Environment Variables

None required - operates on file system paths within claudelife repository.

### Setup Requirements

1. **Ensure hook is executable**:
   ```bash
   chmod +x .claude/hooks/post-tool-auto-diary-capture.sh
   ```

2. **Verify diary template exists**:
   ```bash
   ls 01-areas/business/mokai/diary/.diary-template.md
   ```

3. **Restart Claude Code** to activate hook:
   ```bash
   exit
   claude
   ```

4. **Dependencies**: Requires `jq` for JSON parsing (falls back to grep if unavailable)

## Usage

### Automatic Triggering

The hook automatically captures entries based on these patterns:

| Trigger Pattern | Section | Entry Format | Example |
|----------------|---------|--------------|---------|
| `task-master set-status --status=done` (MOKAI) | 🏆 Wins | "Completed task {id}" | "Completed task 1.2.3" |
| Edit `*/research/*.md` or `*/learning/*.md` | 💡 Learnings | "Updated learning material: {filename}" | "Updated Essential Eight Guide" |
| Edit `*/dashboard.md` or `*/checklist.md` | 📝 Context/Updates | "Updated {filename}" | "Updated Phase 1 Checklist" |
| Run `/mokai-*` command | 📝 Context/Updates | "Executed {command}" | "Executed /mokai-status" |
| Edit `*/tender/*.md` or `*/proposal/*.md` | 🏆 Wins | "Worked on {filename}" | "Worked on Client Proposal" |

### Common Scenarios

**Scenario 1: Task Completion**
```bash
# Complete MOKAI-related task
task-master set-status --id=1.2.3 --status=done
```

**Hook Output**:
```
✅ Auto-captured: Task completion → Wins

📔 Auto-Diary: Captured entry to 2025-10-15 diary
   View: cat 01-areas/business/mokai/diary/2025-10-15-mokai-daily.md
```

**Scenario 2: Research Update**
```bash
# Edit a MOKAI research document
# (happens automatically when you edit the file)
```

**Hook Output**:
```
📚 Auto-captured: Research update → Learnings

📔 Auto-Diary: Captured entry to 2025-10-15 diary
```

**Scenario 3: Strategic Review Command**
```bash
/mokai-status
```

**Hook Output**:
```
⚡ Auto-captured: MOKAI command → Context

📔 Auto-Diary: Captured entry to 2025-10-15 diary
```

### Manual Verification

```bash
# View today's diary
cat 01-areas/business/mokai/diary/$(date +%Y-%m-%d)-mokai-daily.md

# Check hook debug log
tail -50 /tmp/claude-auto-diary-debug.log

# Verify hook is executable
ls -la .claude/hooks/post-tool-auto-diary-capture.sh
```

## Examples

### Example 1: MOKAI Task Completion Workflow

**Context**: Completed reading Indigenous Business section of Operations Guide

**Action**:
```bash
task-master set-status --id=1.2 --status=done
```

**Hook Processing**:
1. Detects Bash tool execution with `task-master` command
2. Extracts task ID: `1.2`
3. Confirms status is `done`
4. Identifies MOKAI context (file path or command includes "mokai")
5. Routes to Wins section

**Diary Entry Added**:
```markdown
## 🏆 Wins

- Completed task 1.2
```

**Benefit**: Win logged automatically without manual `/mokai-dump` call

### Example 2: Research Document Update

**Context**: Updated Essential Eight compliance guide with ASD requirements

**Action**: Edit `01-areas/business/mokai/research/essential-eight-guide.md`

**Hook Processing**:
1. Detects Edit tool execution
2. Identifies file path contains `mokai/research/`
3. Extracts filename: `essential-eight-guide`
4. Routes to Learnings section

**Diary Entry Added**:
```markdown
## 💡 Learnings

- Updated learning material: essential-eight-guide
```

**Benefit**: Research progress automatically documented for knowledge tracking

### Example 3: Morning Strategic Review

**Context**: Running daily MOKAI status check

**Action**:
```bash
/mokai-status
```

**Hook Processing**:
1. Detects Bash tool with `/mokai-status` command
2. Extracts command name
3. Routes to Context/Updates section

**Diary Entry Added**:
```markdown
## 📝 Context/Updates

- Executed /mokai-status command
```

**Benefit**: Command execution logged for workflow tracking

## Dependencies

### External Tools
- `jq`: JSON parsing (optional, falls back to grep)
- `awk`: Text manipulation for diary insertion
- `sed`: Frontmatter date updates

### Internal Dependencies
- **MOKAI Diary System**: Requires diary template and structure
- **Claude Code Hook System**: PostToolUse event framework
- **task-master**: Task completion detection relies on task-master CLI
- **MOKAI Slash Commands**: `/mokai-status`, `/mokai-weekly`, etc.

### File System Requirements
- Write access to `01-areas/business/mokai/diary/`
- Diary template at `01-areas/business/mokai/diary/.diary-template.md`

## Capture Logic

### Pattern Detection

```bash
# 1. Task completion (MOKAI-related)
if [[ "$TOOL_NAME" == "Bash" ]] &&
   [[ "$BASH_COMMAND" == *"task-master"* ]] &&
   [[ "$TASK_STATUS" == "done" ]] &&
   [[ "$BASH_COMMAND" == *"mokai"* ]]; then
  add_to_diary_section "🏆 Wins" "Completed task $TASK_ID"
fi

# 2. Research/learning updates
if [[ "$FILE_PATH" == *"research"* ]] ||
   [[ "$FILE_PATH" == *"learning"* ]] ||
   [[ "$FILE_PATH" == *"guide"* ]]; then
  add_to_diary_section "💡 Learnings" "Updated learning material: $FILENAME"
fi

# 3. Dashboard/checklist updates
if [[ "$FILE_PATH" == *"dashboard"* ]] ||
   [[ "$FILE_PATH" == *"checklist"* ]]; then
  add_to_diary_section "📝 Context/Updates" "Updated $FILENAME"
fi

# 4. MOKAI command executions
if [[ "$BASH_COMMAND" == *"/mokai-"* ]]; then
  add_to_diary_section "📝 Context/Updates" "Executed $COMMAND_NAME"
fi

# 5. Client/tender work
if [[ "$FILE_PATH" == *"tender"* ]] ||
   [[ "$FILE_PATH" == *"proposal"* ]] ||
   [[ "$FILE_PATH" == *"client"* ]]; then
  add_to_diary_section "🏆 Wins" "Worked on $FILENAME"
fi
```

### Duplicate Prevention

```bash
# Check if entry already exists before adding
if ! grep -qF "$entry" "$DIARY_FILE"; then
  # Add entry using awk for precise insertion
  awk -v section="## $section" -v entry="- $entry" '
    /^## / { in_section = ($0 == section) }
    in_section && /^-/ && !added { print; print entry; added=1; next }
    { print }
  ' "$DIARY_FILE" > "$DIARY_FILE.tmp" && mv "$DIARY_FILE.tmp" "$DIARY_FILE"
fi
```

## Troubleshooting

### Common Issues

**Issue 1: Hook not firing**
- **Cause**: Claude Code not restarted after hook configuration
- **Solution**:
  ```bash
  exit
  claude
  ```

**Issue 2: Entries not appearing in diary**
- **Cause**: Not in claudelife directory or diary directory missing
- **Solution**:
  ```bash
  # Verify you're in the right directory
  pwd  # Should be /Users/harrysayers/Developer/claudelife

  # Check diary directory exists
  ls -la 01-areas/business/mokai/diary/
  ```

**Issue 3: Duplicate entries appearing**
- **Cause**: Duplicate detection logic may fail if entry format differs
- **Solution**: Check debug log to see exact entry being added
  ```bash
  tail -50 /tmp/claude-auto-diary-debug.log
  ```

**Issue 4: Hook executable permission denied**
- **Cause**: Hook script not executable
- **Solution**:
  ```bash
  chmod +x .claude/hooks/post-tool-auto-diary-capture.sh
  ```

### Debugging

```bash
# View hook execution trace
tail -100 /tmp/claude-auto-diary-debug.log

# Check what was parsed from JSON
grep "Parsed values:" /tmp/claude-auto-diary-debug.log -A 5

# Verify hook registration
cat .claude/settings.json | jq '.hooks.PostToolUse'

# Test diary file creation
ls -la 01-areas/business/mokai/diary/$(date +%Y-%m-%d)*

# Manual test: trigger hook with fake JSON
echo '{"tool_name":"Bash","tool_input":{"command":"task-master set-status --id=1.2 --status=done mokai"}}' | .claude/hooks/post-tool-auto-diary-capture.sh
```

## Monitoring & Maintenance

- **Logs**: Debug log at `/tmp/claude-auto-diary-debug.log` (auto-created, append-only)
- **Monitoring**: Check diary entries after significant activities to verify captures
- **Update Frequency**: Hook logic may need updates as MOKAI workflow evolves
- **Performance**: Non-blocking, minimal overhead (<100ms per execution)

## Related Systems

- [MOKAI Status Command](../../../.claude/commands/mokai-status.md) - Daily strategic review that reads diary entries
- [MOKAI Weekly Review](../../../.claude/commands/mokai-weekly.md) - End-of-week aggregation using diary data
- [MOKAI Dump Command](../../../.claude/commands/mokai-dump.md) - Manual diary entry logging
- [Post-Tool Memory Sync Hook](../../../.claude/hooks/post-tool-memory-sync-trigger.sh) - Companion hook for Serena memory updates
- [Task Master Integration](../../../.taskmaster/) - Task completion detection source

## Integration with MOKAI Workflows

### With /mokai-status
- **Hook Role**: Populates diary throughout the day automatically
- **/mokai-status Role**: Aggregates and analyzes diary entries in morning review
- **Benefit**: More complete data for strategic analysis

### With /mokai-dump
- **Hook Role**: Handles routine activity captures (task completions, file updates)
- **/mokai-dump Role**: Handles explicit insights and reflections
- **Usage Pattern**: Let hook auto-capture, use `/mokai-dump` for important learnings/insights

### With task-master
- **Integration**: Detects `task-master set-status --status=done` commands
- **MOKAI Context**: Only logs MOKAI-related tasks (keyword detection)
- **Workflow**: Complete task → Hook logs to Wins → `/mokai-status` reviews next day

## Future Enhancements

- **AI Sentiment Analysis**: Use LLM to determine section routing based on content sentiment
- **Rich Entry Generation**: Extract more context from task descriptions (requires task-master API integration)
- **Multi-Project Support**: Extend to MOK HOUSE diary for music production sessions
- **Confidence Scoring**: Add metadata about capture confidence for manual review
- **Blocker Detection**: Automatically route errors/failures to Blockers section
- **Weekly Summary**: Aggregate hook captures for `/mokai-weekly` automation

## Change Log

- 2025-10-15: Initial implementation with 5 capture patterns (task completion, research, dashboard, commands, client work)
- 2025-10-15: Added comprehensive documentation and debugging support
