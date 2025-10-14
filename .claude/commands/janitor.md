---
created: "2025-10-15 04:12"
updated: "2025-10-15 04:18"
description: |
  Maintenance command that cleans up the claudelife vault by archiving completed/archived files and purging old archives.
  This command:
    - Uses scan-archive-candidates.sh script for instant scanning (<1 second)
    - Moves files with `done: true` or `archive: true` to /99-archive directory
    - Deletes files in /99-archive older than 30 days
    - Provides summary of archived and deleted files
performance: |
  30-60x faster than Serena MCP scanning - processes 100+ files in <1 second
examples:
  - /janitor
  - npm run scan-archive  # Preview files before running /janitor
---

# Phase 1: Scan for Archivable Files

**Performance**: Uses `scan-archive-candidates.sh` script for instant scanning (<1 second vs 30+ seconds).

Run the archive candidate scanner:
```bash
npm run scan-archive:json
```

This returns JSON with:
- `archive_candidates`: All files to move to `/99-archive`
- `done_files`: Files with `done: true` or `Done: true`
- `archive_marked`: Files with `archive: true`
- `old_archive_files`: Files in `/99-archive` older than 30 days with modification dates
- `summary`: Count of each category

Parse the JSON output to get the list of files to process.

**Preview before executing**: User can run `npm run scan-archive` to see human-readable output before running `/janitor`.

# Phase 2: Move Files to Archive

For each file identified:
1. Verify frontmatter contains `done: true` or `archive: true`
2. Create `/99-archive/` directory if it doesn't exist
3. Move file to `/99-archive/` preserving filename
4. If file already exists in archive, append timestamp to filename

Track moved files for summary report.

# Phase 3: Clean Old Archives

The `old_archive_files` array from Phase 1 JSON output already contains files older than 30 days.

For each file in `old_archive_files`:
1. Delete the file
2. Track deleted files with their modification dates for summary report

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

- **Performance optimized**: Uses `scan-archive-candidates.sh` script (30-60x faster than MCP scanning)
- Preserve file structure (no subdirectories in /99-archive)
- Handle filename conflicts gracefully (append timestamp if needed)
- Provide clear summary of actions taken
- User can preview with `npm run scan-archive` before executing

# Error Handling

- Skip files without proper frontmatter
- Handle permission errors gracefully
- Warn if /99-archive can't be created
- Continue processing even if individual file operations fail
