---
date: "2025-10-15 13:35"
---

# Auto-Diary Capture Hook

Automatically logs MOKAI wins, learnings, and context to your daily diary when you complete tasks or make significant progress.

## What It Does

The auto-diary capture hook monitors your Claude Code activity and automatically adds entries to your MOKAI diary (`01-areas/business/mokai/diary/YYYY-MM-DD-mokai-daily.md`) based on:

### Automatic Captures

1. **Task Completions → 🏆 Wins**
   - When: `task-master set-status --status=done` for MOKAI tasks
   - Logged to: "## 🏆 Wins" section
   - Example: "Completed task 1.2.3"

2. **Research Updates → 💡 Learnings**
   - When: Editing files in `mokai/research/`, `mokai/learning/`, `mokai/guide/`
   - Logged to: "## 💡 Learnings" section
   - Example: "Updated learning material: Essential Eight Guide"

3. **Dashboard/Checklist Updates → 📝 Context/Updates**
   - When: Editing `dashboard.md` or `checklist.md` files
   - Logged to: "## 📝 Context/Updates" section
   - Example: "Updated Phase 1 Checklist"

4. **MOKAI Command Executions → 📝 Context/Updates**
   - When: Running `/mokai-*` slash commands
   - Logged to: "## 📝 Context/Updates" section
   - Example: "Executed /mokai-status command"

5. **Client/Tender Work → 🏆 Wins**
   - When: Editing tender, proposal, or client files
   - Logged to: "## 🏆 Wins" section
   - Example: "Worked on Client Proposal XYZ"

## How It Works

### Hook Trigger Points

The hook runs after these Claude Code tools execute:
- **Write**: Creating new files in MOKAI areas
- **Edit**: Modifying existing MOKAI files
- **Bash**: Running commands (task-master, /mokai-* commands)

### Diary Entry Logic

1. **Detects event type** from tool execution context
2. **Determines appropriate section** (Wins/Learnings/Context)
3. **Creates diary file** from template if doesn't exist for today
4. **Adds entry** to the relevant section (prevents duplicates)
5. **Shows notification** confirming capture

### Smart Features

- **Duplicate prevention**: Won't add the same entry twice
- **Auto-creates diary**: Uses `.diary-template.md` if today's diary doesn't exist
- **Non-blocking**: Always exits successfully, never interrupts your workflow
- **Debug logging**: Full debug log at `/tmp/claude-auto-diary-debug.log`

## Configuration

### Hook Registration

Located in `.claude/settings.json`:

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

### Hook Script

Location: `.claude/hooks/post-tool-auto-diary-capture.sh`
Permissions: Executable (`chmod +x`)

## Usage

### Activating the Hook

**IMPORTANT**: Restart Claude Code for the hook to take effect:

```bash
# Exit current Claude Code session
exit

# Start new session
claude
```

### Testing the Hook

After restarting, try any of these actions:

1. **Complete a MOKAI task**:
   ```bash
   task-master set-status --id=1.2 --status=done
   ```

2. **Edit a MOKAI file**:
   ```bash
   # Edit any file in 01-areas/business/mokai/
   ```

3. **Run a MOKAI command**:
   ```bash
   /mokai-status
   ```

You should see output like:
```
📔 Auto-Diary: Captured entry to 2025-10-15 diary
   View: cat 01-areas/business/mokai/diary/2025-10-15-mokai-daily.md
```

### Viewing Captured Entries

```bash
# View today's diary
cat 01-areas/business/mokai/diary/$(date +%Y-%m-%d)-mokai-daily.md

# Check hook debug log
tail -50 /tmp/claude-auto-diary-debug.log
```

## Examples

### Example 1: Task Completion

**Action**: Complete a MOKAI task
```bash
task-master set-status --id=1.2.3 --status=done
```

**Result**: Diary entry added
```markdown
## 🏆 Wins

- Completed task 1.2.3
```

**Hook Output**:
```
✅ Auto-captured: Task completion → Wins

📔 Auto-Diary: Captured entry to 2025-10-15 diary
   View: cat 01-areas/business/mokai/diary/2025-10-15-mokai-daily.md
```

### Example 2: Research Update

**Action**: Update MOKAI research document
```bash
# Edit 01-areas/business/mokai/research/essential-eight.md
```

**Result**: Diary entry added
```markdown
## 💡 Learnings

- Updated learning material: essential-eight
```

**Hook Output**:
```
📚 Auto-captured: Research update → Learnings

📔 Auto-Diary: Captured entry to 2025-10-15 diary
```

### Example 3: Dashboard Update

**Action**: Update Phase 1 checklist
```bash
# Edit 01-areas/business/mokai/dashboard.md
```

**Result**: Diary entry added
```markdown
## 📝 Context/Updates

- Updated dashboard
```

**Hook Output**:
```
📋 Auto-captured: Dashboard/checklist update → Context

📔 Auto-Diary: Captured entry to 2025-10-15 diary
```

## Troubleshooting

### Hook Not Firing

1. **Restart Claude Code**:
   ```bash
   exit
   claude
   ```

2. **Check hook is executable**:
   ```bash
   ls -la .claude/hooks/post-tool-auto-diary-capture.sh
   # Should show: -rwxr-xr-x
   ```

3. **Check settings.json syntax**:
   ```bash
   cat .claude/settings.json | jq . # Should parse without errors
   ```

4. **Check debug log**:
   ```bash
   tail -50 /tmp/claude-auto-diary-debug.log
   ```

### Entries Not Appearing

1. **Check diary file was created**:
   ```bash
   ls -la 01-areas/business/mokai/diary/$(date +%Y-%m-%d)*
   ```

2. **Check debug log for errors**:
   ```bash
   grep "ERROR\|error" /tmp/claude-auto-diary-debug.log
   ```

3. **Verify you're in claudelife directory**:
   ```bash
   pwd # Should be /Users/harrysayers/Developer/claudelife
   ```

### Duplicate Entries

The hook automatically prevents duplicates by checking if an entry already exists before adding it.

If you see duplicates, check the debug log to identify why the duplicate detection failed.

## Customization

### Adding New Capture Patterns

Edit `.claude/hooks/post-tool-auto-diary-capture.sh` to add new patterns:

```bash
# Example: Capture when updating specific files
if [[ "$FILE_PATH" == *"specific-file.md"* ]]; then
  CONTEXT="Updated specific file"
  if add_to_diary_section "🏆 Wins" "$CONTEXT"; then
    CAPTURED=true
    echo "🎯 Auto-captured: Specific file → Wins"
  fi
fi
```

### Changing Section Targets

Modify the section names in capture logic:

```bash
# Change from Context to Wins
add_to_diary_section "🏆 Wins" "$CONTEXT"  # Instead of Context/Updates
```

## Integration with Other Workflows

### With /mokai-status

The auto-diary hook complements `/mokai-status`:
- **Hook**: Captures entries throughout the day automatically
- **/mokai-status**: Aggregates and reviews all diary entries in the morning

### With /mokai-dump

For manual captures, still use `/mokai-dump`:
```bash
/mokai-dump "Had a breakthrough on Essential Eight compliance approach"
```

The hook handles automatic captures, `/mokai-dump` handles explicit manual captures.

### With task-master

Perfect integration with task-master workflow:
1. Work on task
2. Mark as done: `task-master set-status --id=X --status=done`
3. Hook automatically logs to diary
4. `/mokai-status` aggregates in morning review

## Benefits

✅ **Never forget to log wins** - Automatic capture when tasks complete
✅ **Reduced friction** - No manual diary updates during focused work
✅ **Better accuracy** - Captures in real-time vs. end-of-day recall
✅ **Consistent tracking** - Every significant action logged automatically
✅ **Complements /mokai-dump** - Auto captures routine, manual captures insights
✅ **Improves /mokai-status** - More complete diary data for morning review

## Related Files

- Hook script: `.claude/hooks/post-tool-auto-diary-capture.sh`
- Configuration: `.claude/settings.json`
- Diary template: `01-areas/business/mokai/diary/.diary-template.md`
- Debug log: `/tmp/claude-auto-diary-debug.log`
- Documentation: `.claude/hooks/README-auto-diary.md` (this file)
