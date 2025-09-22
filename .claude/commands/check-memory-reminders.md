# Check Memory Capture Reminders

Check for git-generated reminders about capturing significant changes to memory.

## Steps:

1. **Check for reminder file**:
   - Look for `.memory-capture-needed` in project root
   - If found, display the contents

2. **If reminder exists**:
   - Show what changes triggered the reminder
   - Run `/remember` to capture the changes
   - Ask user if they want to delete the reminder file

3. **If no reminders**:
   - Confirm memory is up to date
   - Show last memory capture timestamp

**Usage**: `/check-memory-reminders` (run at start of Claude Code sessions)