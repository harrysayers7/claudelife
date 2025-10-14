---
Done: false
today: false
follow up: false
this week: false
back burner: false
type: Task
status:
relation:
description:
effort:
ai-assigned: true
priority:
---

use the .claude/commands/create-command slash command and create the following slash command
### /janitor


#### What it does

Clean up all files in claudelife project that have either one of the following properties:

---
done: true
archive: true

---
#### once identified
Move them to /99-archive

Also scan /99-archive for files older than 30 days and delete them

This command should use serena mcp for codebase navigation
