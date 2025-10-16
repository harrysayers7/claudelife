---
created: "2025-10-15 09:30"
description: |
  Intelligently rename markdown files and automatically update all references across the claudelife vault.
  Handles both Obsidian wikilinks [[filename]] and markdown links [text](path/file.md).
  Provides preview of changes before applying, supports custom search scope, and ensures consistency.
examples:
  - "/rename-file old-name.md new-name.md"
  - "/rename-file 'tasks/Old Task.md' 'tasks/New Task.md' --scope=00-inbox"
  - "/rename-file meeting-notes.md client-meeting-2025-10-15.md --preview"
---

# Rename File with Reference Updates

This command helps you safely rename markdown files in the claudelife vault while automatically updating all references to that file across your entire knowledge base.

## Usage

```bash
/rename-file [old-path] [new-path] [--scope=directory] [--preview]
```

## Interactive Process

When you run this command, I will:

1. **Confirm the file exists** and validate the old path
2. **Ask you to specify the new filename/path**
3. **Determine search scope** (entire vault or specific directories)
4. **Scan for all references** using both:
   - Obsidian wikilinks: `[[filename]]`
   - Markdown links: `[text](path/to/file.md)`
   - Relative and absolute path references
5. **Preview all changes** before applying them
6. **Ask for confirmation** before making any modifications
7. **Execute the rename** and update all references
8. **Verify completion** and report results

## Input Requirements

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

Before running this command, prepare:

1. **Current file path**: Exact path to the file you want to rename
   - Example: `00-inbox/tasks/old-task-name.md`
   - Example: `meeting-notes.md`

2. **New file path**: Desired new name/path
   - Example: `00-inbox/tasks/new-task-name.md`
   - Example: `client-meeting-2025-10-15.md`

3. **Search scope** (optional): Directory to search for references
   - Example: `00-inbox` (search only inbox)
   - Example: `01-areas/business` (search business area only)
   - Default: entire vault

## Process

I'll help you rename the file safely by:

1. **Fast Reference Scan (using script)**
   - Run `./scripts/rename-file.sh` for 10-20x faster scanning
   - Single-pass search for all reference patterns
   - Get JSON output with complete file list in 1-2 seconds

2. **Validate Input**
   - Script validates that source file exists
   - Script checks destination doesn't already exist
   - Script warns if destination directory needs creation

3. **Preview Changes**
   - Display files found by script with references
   - Show total reference count
   - Highlight potential issues before proceeding

4. **Execute Updates**
   - Update all references using `Edit` tool
   - Handle both wikilinks and markdown links
   - Preserve file structure and formatting

5. **Rename File**
   - Create destination directory if needed
   - Move file to new location using `Bash(mv)`

6. **Verify & Report**
   - Confirm file was renamed successfully
   - Report number of references updated
   - List any issues encountered

## Technical Implementation Guide

### Step 1: Fast Script-Based Scan (RECOMMENDED)

**Performance**: 10-20x faster than sequential Serena searches

```bash
# Run the companion script
./scripts/rename-file.sh "old-path.md" "new-path.md" "scope"

# Example output (JSON to stdout):
{
  "success": true,
  "old_path": "00-inbox/meeting-notes.md",
  "new_path": "01-areas/client-meeting.md",
  "old_name": "meeting-notes",
  "new_name": "client-meeting",
  "reference_count": 5,
  "files": [
    "00-inbox/tasks.md",
    "01-areas/business/log.md",
    "97-tags/mokai.md"
  ],
  "patterns_searched": [
    "[[meeting-notes]]",
    "[[meeting-notes.md]]",
    "[text](*/meeting-notes.md)"
  ]
}
```

**Script features**:
- Single ripgrep pass for all patterns (wikilinks + markdown links)
- Colored human-readable summary to stderr
- Structured JSON output to stdout for parsing
- Validates inputs and checks for conflicts

### Step 2: Parse Script Output

```javascript
// Execute script and parse JSON
const result = await Bash({
  command: `./scripts/rename-file.sh "${oldPath}" "${newPath}" "${scope}"`,
  description: "Scan for file references using fast script"
});

const scanData = JSON.parse(result);

// scanData contains:
// - old_path, new_path
// - old_name, new_name (without .md extension)
// - reference_count
// - files[] (array of files with references)
// - patterns_searched[] (what patterns were used)
```

### Step 3: Fallback to Serena (if script unavailable)

If the script doesn't exist or fails, fall back to Serena:

```javascript
// Fallback: Use Serena search_for_pattern
mcp__serena__search_for_pattern({
  substring_pattern: "\\[\\[meeting-notes\\]\\]",
  paths_include_glob: "**/*.md",
  output_mode: "files_with_matches"
});
```

### Step 4: Update References in Each File

```javascript
// For each file found by the script
for (const filePath of scanData.files) {
  // Read the file to find exact reference patterns
  const content = await Read({ file_path: filePath });

  // Update wikilinks: [[old-name]] or [[old-name.md]]
  if (content.includes(`[[${scanData.old_name}]]`)) {
    await Edit({
      file_path: filePath,
      old_string: `[[${scanData.old_name}]]`,
      new_string: `[[${scanData.new_name}]]`
    });
  }

  if (content.includes(`[[${scanData.old_basename}]]`)) {
    await Edit({
      file_path: filePath,
      old_string: `[[${scanData.old_basename}]]`,
      new_string: `[[${scanData.new_basename}]]`
    });
  }

  // Update markdown links: [text](path/old-file.md)
  // Note: Need to parse and update relative paths based on file locations
  if (content.includes(`](`) && content.includes(scanData.old_basename)) {
    // Use regex to find and replace markdown links
    // Calculate correct relative path based on both file locations
  }
}
```

### Step 5: Rename File

```javascript
// Create destination directory if needed
const destDir = path.dirname(scanData.new_path);
if (destDir !== path.dirname(scanData.old_path)) {
  await Bash({
    command: `mkdir -p "${destDir}"`,
    description: `Create destination directory: ${destDir}`
  });
}

// Move the file
await Bash({
  command: `mv "${scanData.old_path}" "${scanData.new_path}"`,
  description: `Rename ${scanData.old_basename} to ${scanData.new_basename}`
});
```

## Output Format

I'll provide:

1. **Pre-rename Summary**
   ```
   📝 File Rename Preview
   ─────────────────────────────────────────
   Source: 00-inbox/tasks/meeting-notes.md
   Destination: 00-inbox/tasks/client-meeting-2025-10-15.md
   Search Scope: Entire vault

   References Found: 12 occurrences in 8 files

   Files to Update:
   ✓ 00-inbox/related-task.md (2 references)
   ✓ 01-areas/business/notes.md (1 reference)
   ✓ 97-tags/mokai.md (1 reference)
   ... (5 more files)

   Proceed with rename? (y/n)
   ```

2. **Reference Details Table**
   | File | Line | Before | After |
   |------|------|--------|-------|
   | related-task.md | 12 | `[[meeting-notes]]` | `[[client-meeting-2025-10-15]]` |
   | notes.md | 45 | `[Notes](../../meeting-notes.md)` | `[Notes](../../client-meeting-2025-10-15.md)` |

3. **Post-rename Confirmation**
   ```
   ✅ File Renamed Successfully
   ─────────────────────────────────────────
   ✓ File renamed
   ✓ 12 references updated in 8 files
   ✓ No broken links detected

   Summary:
   - Wikilinks updated: 10
   - Markdown links updated: 2
   - Files modified: 8

   New location: 00-inbox/tasks/client-meeting-2025-10-15.md
   ```

## Examples

### Example 1: Simple Rename in Same Directory

**User request**: "Rename `meeting-notes.md` to `client-meeting-2025-10-15.md`"

**Process**:
1. Search for `[[meeting-notes]]` across vault
2. Find 5 references in 3 files
3. Preview changes:
   - `00-inbox/tasks.md`: `[[meeting-notes]]` → `[[client-meeting-2025-10-15]]`
   - `01-areas/business/log.md`: `[[meeting-notes]]` → `[[client-meeting-2025-10-15]]`
4. Confirm with user
5. Execute rename and updates
6. Report success

### Example 2: Moving File to Different Directory

**User request**: "Move `00-inbox/task.md` to `01-areas/business/mokai/task.md`"

**Process**:
1. Search for all references to `task.md`
2. Identify 8 markdown links with relative paths
3. Preview changes showing updated relative paths:
   - `00-inbox/notes.md`: `[Task](task.md)` → `[Task](../01-areas/business/mokai/task.md)`
   - `01-areas/business/index.md`: `[Task](../../00-inbox/task.md)` → `[Task](mokai/task.md)`
4. Confirm with user
5. Execute move and path updates
6. Report success

### Example 3: Scoped Search

**User request**: "Rename `project-plan.md` to `mokai-q4-plan.md`, only search in business area"

**Process**:
1. Search only in `01-areas/business/**` directory
2. Find 3 references in business notes
3. Skip searching entire vault (faster)
4. Preview and confirm
5. Execute rename
6. Report success

## Evaluation Criteria

A successful rename operation should:

1. **File renamed correctly** - Source file moved to destination without data loss
2. **All references updated** - No broken wikilinks or markdown links remain
3. **Path accuracy maintained** - Relative paths correctly recalculated for moved files
4. **Formatting preserved** - No changes to file content beyond reference updates
5. **User confirmation obtained** - Preview shown and approved before execution
6. **Clear reporting** - User informed of all changes made
7. **Error handling** - Graceful handling of edge cases (duplicate names, missing files)

## Edge Cases & Recommendations

### Multiple Files Reference the Renamed File
**Handling**: Update all references automatically after user confirmation

### File Referenced with Different Path Styles
**Recommendation**:
- Normalize to consistent style (prefer Obsidian wikilinks `[[filename]]` for vault-internal links)
- Preserve markdown links for external references
- Ask user preference if mixed styles found

### Broken Links After Renaming
**Prevention**:
- Search for all pattern variations before renaming
- Verify no references will break
- Warn user if potential issues detected

### File with Same Name Exists
**Handling**:
- Detect conflict before attempting rename
- Ask user to choose different name or confirm overwrite
- Never silently overwrite existing files

### Moving to Different Directory
**Path Handling**:
- Recalculate all relative paths based on new location
- Update `[text](path)` style links with correct relative paths
- Maintain `[[wikilink]]` style (path-independent in Obsidian)

## Related Resources

- Serena search tools: `mcp__serena__search_for_pattern`
- File operations: `Edit`, `Bash(mv)`
- Similar patterns: `.claude/commands/complete-task.md` (checkbox updates)

---

**Pro tip**: For bulk renames, run this command multiple times or request a custom batch rename command.
