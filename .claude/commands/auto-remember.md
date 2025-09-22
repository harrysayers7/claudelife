# Auto-Remember Daily Sync

Check for new or modified files and automatically capture important changes to memory.

## Steps:

1. **Scan for changes** since last memory update:
   - Check `git log --since="24 hours ago" --name-only --oneline`
   - Look for new files in context/, .mcp/, infrastructure changes
   - Compare against last timeline entry timestamp

2. **Identify significant changes**:
   - New context files (*.md in context/)
   - MCP server modifications (.mcp.json, *server.py)
   - Infrastructure additions (trigger.config.ts, package.json)
   - New business profiles or configurations

3. **Auto-capture to memory**:
   - Create entities for new significant files/tools
   - Update relationships between existing entities
   - Add timeline events for major changes
   - Skip trivial changes (documentation updates, minor tweaks)

4. **Summary report**:
   - List what was captured
   - Highlight any manual review needed
   - Note any conflicts or unclear changes

Run this command daily or when starting work sessions to keep memory current.

**Usage**: `/auto-remember` (no arguments needed)