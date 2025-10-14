---
created: "2025-10-15 04:12"
updated: "2025-10-15 04:12"
description: |
  Maintenance command that cleans up the claudelife vault by archiving completed/archived files and purging old archives.
  This command:
    - Scans entire project using Serena MCP for files with `done: true` or `archive: true` in frontmatter
    - Moves identified files to /99-archive directory
    - Scans /99-archive and deletes files older than 30 days
    - Provides summary of archived and deleted files
examples:
  - /janitor
---

# Phase 1: Scan for Archivable Files

Use Serena MCP to find all markdown files in the claudelife project with either:
- `done: true` in frontmatter
- `archive: true` in frontmatter

Search locations:
- `/00-inbox/`
- `/00-Bases/`
- `/01-areas/`
- `/02-projects/`
- `/04-resources/`
- `/07-context/`
- Any other directories except `/99-archive/`

Use `mcp__serena__search_for_pattern` with:
```
pattern: "^done: true|^archive: true"
context_lines_before: 5
context_lines_after: 0
output_mode: "files_with_matches"
```

# Phase 2: Move Files to Archive

For each file identified:
1. Verify frontmatter contains `done: true` or `archive: true`
2. Create `/99-archive/` directory if it doesn't exist
3. Move file to `/99-archive/` preserving filename
4. If file already exists in archive, append timestamp to filename

Track moved files for summary report.

# Phase 3: Clean Old Archives

Scan `/99-archive/` directory:
1. Get file creation/modification dates
2. Identify files older than 30 days from today
3. Delete identified files
4. Track deleted files for summary report

Use bash commands:
```bash
find /Users/harrysayers/Developer/claudelife/99-archive -type f -mtime +30 -name "*.md"
```

# Phase 4: Summary Report

Provide clean summary:
```
🧹 Janitor Cleanup Complete

📦 Archived Files (moved to /99-archive):
- [filename1.md]
- [filename2.md]
Total: X files

🗑️ Deleted Old Archives (>30 days):
- [old-file1.md] (created: YYYY-MM-DD)
- [old-file2.md] (created: YYYY-MM-DD)
Total: Y files

✨ Vault cleaned successfully!
```

# Execution Notes

- Use Serena MCP for codebase navigation and file discovery
- Preserve file structure (no subdirectories in /99-archive)
- Handle filename conflicts gracefully
- Verify frontmatter before moving files
- Provide clear summary of actions taken

# Error Handling

- Skip files without proper frontmatter
- Handle permission errors gracefully
- Warn if /99-archive can't be created
- Continue processing even if individual file operations fail
