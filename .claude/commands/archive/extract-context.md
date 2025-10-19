---
created: "2025-10-12 22:00"
description: |
  Extracts context from Obsidian daily notes and consolidates them into a central context file.

  This command:
    - Scans daily notes in /00 - Daily directory (and subdirectories)
    - Extracts content from ### Context or ### 🌍 Context sections
    - Appends to /04-resources/context.md with wiki links to source notes
    - Tracks processed files to avoid re-scanning (incremental extraction)
    - Re-extracts if files were modified since last scan
    - Preserves markdown formatting while cleaning up presentation

  Outputs formatted context with H3 headings linking back to source daily notes.
examples:
  - /extract-context
---

# Extract Context

This command scans your Obsidian daily notes, extracts context information, and consolidates them into a central context file for easy review and AI reference.

## Usage

```bash
/extract-context
```

## What This Command Does

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

I will:
1. Load the tracking file to identify previously processed notes
2. Scan all markdown files in `/Users/harrysayers/Developer/claudelife/00 - Daily` (including subdirectories)
3. For each daily note:
   - Check if it's new or modified since last extraction
   - Extract content under `### Context` or `### 🌍 Context` heading
   - Skip files with no context content (empty sections)
4. Append extracted context to `/Users/harrysayers/Developer/claudelife/04-resources/context.md`
5. Format each context section with H3 wiki link to source note
6. Update tracking file with processed files and timestamps

## Tracking System

**Tracker Location**: `/Users/harrysayers/Developer/claudelife/.claude/commands/.extract-context-tracker.json`

**Tracker Format**:
```json
{
  "last_scan": "2025-10-12T22:00:00Z",
  "processed_files": {
    "25-10-01 - Wed.md": {
      "extracted_at": "2025-10-12T22:00:00Z",
      "modified_at": "2025-10-01T15:20:00Z",
      "has_context": true
    }
  }
}
```

## Process

### 1. Load or Create Tracker

```javascript
const trackerPath = '/Users/harrysayers/Developer/claudelife/.claude/commands/.extract-context-tracker.json';

let tracker = {
  last_scan: null,
  processed_files: {}
};

if (file exists) {
  tracker = JSON.parse(read file);
}
```

### 2. Scan Daily Notes Directory

```javascript
const dailyNotesPath = '/Users/harrysayers/Developer/claudelife/00 - Daily';
const allNotes = glob('**/*.md', { cwd: dailyNotesPath });

const notesToProcess = allNotes.filter(note => {
  const noteModifiedTime = getFileModifiedTime(note);
  const lastExtracted = tracker.processed_files[note]?.extracted_at;
  const lastModified = tracker.processed_files[note]?.modified_at;

  return !lastExtracted || noteModifiedTime > lastModified;
});
```

### 3. Extract Context from Each Note

For each note in `notesToProcess`:

```javascript
const content = readFile(note);

// Find the context section (handles both "### Context" and "### 🌍 Context")
const contextMatch = content.match(/###\s*(?:🌍\s*)?Context\n([\s\S]*?)(?=\n###|\n---|$)/);

if (!contextMatch || !contextMatch[1].trim()) {
  continue; // Skip - no context or empty section
}

// Extract and clean context content
let context = contextMatch[1].trim();

// Clean up formatting while preserving content
context = context
  .replace(/\n{3,}/g, '\n\n')  // Max 2 consecutive newlines
  .trim();
```

### 4. Format Output with Wiki Links

```javascript
const noteName = path.basename(note, '.md');
const heading = `### [[${noteName}]]`;
const formattedContext = `${heading}\n\n${context}\n\n---\n\n`;
```

### 5. Append to context.md

```javascript
const contextFile = '/Users/harrysayers/Developer/claudelife/04-resources/context.md';
appendToFile(contextFile, formattedContext);
```

### 6. Update Tracker

```javascript
tracker.processed_files[note] = {
  extracted_at: new Date().toISOString(),
  modified_at: getFileModifiedTime(note),
  has_context: true
};

tracker.last_scan = new Date().toISOString();
writeFile(trackerPath, JSON.stringify(tracker, null, 2));
```

## Output Format

Context is appended to `context.md` in this format:

```markdown
### [[25-10-01 - Wed]]

I use a Samsung S25+ as my mobile device

---

### [[25-10-05 Sun]]

I am very loyal to my wife and am always there for her

---
```

## Examples

### Example 1: First Run

**Process**:
1. Create new tracker file
2. Scan all `.md` files in `/00 - Daily`
3. Extract context from all notes with content
4. Append to `context.md`
5. Record all processed files

**Output**:
```
Scanning daily notes for context...
Found 15 daily notes
Processing 15 new files...

✓ Extracted context from 25-10-01 - Wed.md
✓ Extracted context from 25-10-05 Sun.md
✓ Skipped 25-10-02 - Thu.md (no context)
✓ Extracted context from 25-10-09 - Thu.md
...

Summary:
- 8 contexts extracted
- 7 files skipped (no context)
- context.md updated
- Tracker created
```

### Example 2: Incremental Run

**Process**:
1. Load existing tracker
2. Only process new/modified files
3. Append new context

**Output**:
```
Scanning daily notes for context...
Found 16 daily notes
Previously processed: 15 files
Processing 1 new file...

✓ Extracted context from 25-10-13 - Mon.md

Summary:
- 1 new context extracted
- context.md updated
```

## Evaluation Criteria

A successful extraction should:

1. **Correctly identify context sections**: Find `### Context` or `### 🌍 Context` (with/without emoji)
2. **Extract complete content**: Capture everything until next heading or end of file
3. **Preserve formatting**: Keep bullets, lists, bold, italic, links
4. **Clean presentation**: Remove excessive whitespace
5. **Create valid wiki links**: Format as `[[25-10-01 - Wed]]`
6. **Track accurately**: Record processed files with timestamps
7. **Handle incremental runs**: Only process new/modified files
8. **Skip empty sections**: Ignore empty context sections
9. **Update tracker reliably**: Save after extraction
10. **Maintain context.md integrity**: Append cleanly

## Edge Cases Handled

- **Empty context sections**: Skip silently
- **Missing context heading**: Skip file
- **Subdirectories**: Recursive scan
- **Non-standard filenames**: Handle any `.md` file
- **Context at end of file**: Extract properly
- **Multiple context sections**: Extract only first one
- **Modified files**: Re-extract if modified after last extraction

## Related Resources

- Context file: `/Users/harrysayers/Developer/claudelife/04-resources/context.md`
- Tracker: `/Users/harrysayers/Developer/claudelife/.claude/commands/.extract-context-tracker.json`
- Daily notes: `/Users/harrysayers/Developer/claudelife/00 - Daily/`
- Similar command: `/extract-insights`

## Maintenance Notes

### Tracker Management

**View tracker**:
```bash
cat /Users/harrysayers/Developer/claudelife/.claude/commands/.extract-context-tracker.json | jq '.'
```

**Reset tracker**:
```bash
rm /Users/harrysayers/Developer/claudelife/.claude/commands/.extract-context-tracker.json
```

### context.md Management

The context file grows over time. Consider:
- Periodic review and organization by themes
- Creating derivative context documents for specific domains
- Using context for AI persona development
- Tagging context entries for easy filtering

## Troubleshooting

**Issue**: Context not being extracted
- **Check**: Does the note have `### Context` or `### 🌍 Context`?
- **Check**: Is there actual content (not just whitespace)?

**Issue**: Duplicate context entries
- **Cause**: File was modified and re-extracted
- **Solution**: Expected behavior for modified files

**Issue**: Command runs slowly
- **Solution**: First run is slowest; subsequent runs are fast

---

**Ready to extract context from your daily notes!**
