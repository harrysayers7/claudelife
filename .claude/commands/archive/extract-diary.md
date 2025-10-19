---
created: "2025-10-12 22:05"
description: |
  Extracts diary entries from Obsidian daily notes and consolidates them into a central diary file.

  This command:
    - Scans daily notes in /00 - Daily directory (and subdirectories)
    - Extracts content from ### Diary or ### diary sections
    - Appends to /04-resources/diary.md with wiki links to source notes
    - Tracks processed files to avoid re-scanning (incremental extraction)
    - Re-extracts if files were modified since last scan
    - Preserves markdown formatting while cleaning up presentation

  Outputs formatted diary entries with H3 headings linking back to source daily notes.
examples:
  - /extract-diary
---

# Extract Diary

This command scans your Obsidian daily notes, extracts diary entries, and consolidates them into a central diary file for easy review and reflection.

## Usage

```bash
/extract-diary
```

## What This Command Does

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

I will:
1. Load the tracking file to identify previously processed notes
2. Scan all markdown files in `/Users/harrysayers/Developer/claudelife/00 - Daily` (including subdirectories)
3. For each daily note:
   - Check if it's new or modified since last extraction
   - Extract content under `### Diary` or `### diary` heading
   - Skip files with no diary content (empty sections)
4. Append extracted diary to `/Users/harrysayers/Developer/claudelife/04-resources/diary.md`
5. Format each diary section with H3 wiki link to source note
6. Update tracking file with processed files and timestamps

## Tracking System

**Tracker Location**: `/Users/harrysayers/Developer/claudelife/.claude/commands/.extract-diary-tracker.json`

**Tracker Format**:
```json
{
  "last_scan": "2025-10-12T22:05:00Z",
  "processed_files": {
    "25-10-01 - Wed.md": {
      "extracted_at": "2025-10-12T22:05:00Z",
      "modified_at": "2025-10-01T15:20:00Z",
      "has_diary": true
    }
  }
}
```

## Process

### 1. Load or Create Tracker

```javascript
const trackerPath = '/Users/harrysayers/Developer/claudelife/.claude/commands/.extract-diary-tracker.json';

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

### 3. Extract Diary from Each Note

For each note in `notesToProcess`:

```javascript
const content = readFile(note);

// Find the diary section (handles both "### Diary" and "### diary")
const diaryMatch = content.match(/###\s*[Dd]iary\n([\s\S]*?)(?=\n###|\n---|$)/);

if (!diaryMatch || !diaryMatch[1].trim()) {
  continue; // Skip - no diary or empty section
}

// Extract and clean diary content
let diary = diaryMatch[1].trim();

// Clean up formatting while preserving content
diary = diary
  .replace(/\n{3,}/g, '\n\n')  // Max 2 consecutive newlines
  .trim();
```

### 4. Format Output with Wiki Links

```javascript
const noteName = path.basename(note, '.md');
const heading = `### [[${noteName}]]`;
const formattedDiary = `${heading}\n\n${diary}\n\n---\n\n`;
```

### 5. Append to diary.md

```javascript
const diaryFile = '/Users/harrysayers/Developer/claudelife/04-resources/diary.md';
appendToFile(diaryFile, formattedDiary);
```

### 6. Update Tracker

```javascript
tracker.processed_files[note] = {
  extracted_at: new Date().toISOString(),
  modified_at: getFileModifiedTime(note),
  has_diary: true
};

tracker.last_scan = new Date().toISOString();
writeFile(trackerPath, JSON.stringify(tracker, null, 2));
```

## Output Format

Diary entries are appended to `diary.md` in this format:

```markdown
### [[25-10-01 - Wed]]

Had a productive day working on MOKAI proposals. Met with potential clients and discussed Indigenous procurement advantages.

---

### [[25-10-04 Sat]]

Simulated a meeting
Went for a moring walk at narrawallee
Drove to Canberra to see friends for long weekend

---

### [[25-10-07 - Tue]]

Did get much done - got distracted, didnt go to the gym like i should have

---
```

## Examples

### Example 1: First Run

**Process**:
1. Create new tracker file
2. Scan all `.md` files in `/00 - Daily`
3. Extract diary from all notes with content
4. Append to `diary.md`
5. Record all processed files

**Output**:
```
Scanning daily notes for diary entries...
Found 15 daily notes
Processing 15 new files...

✓ Extracted diary from 25-10-04 Sat.md
✓ Extracted diary from 25-10-07 - Tue.md
✓ Skipped 25-10-01 - Wed.md (no diary)
✓ Extracted diary from 25-10-09 - Thu.md
...

Summary:
- 5 diary entries extracted
- 10 files skipped (no diary)
- diary.md updated
- Tracker created
```

### Example 2: Incremental Run

**Process**:
1. Load existing tracker
2. Only process new/modified files
3. Append new diary entries

**Output**:
```
Scanning daily notes for diary entries...
Found 16 daily notes
Previously processed: 15 files
Processing 1 new file...

✓ Extracted diary from 25-10-13 - Mon.md

Summary:
- 1 new diary entry extracted
- diary.md updated
```

## Evaluation Criteria

A successful extraction should:

1. **Correctly identify diary sections**: Find `### Diary` or `### diary` (case insensitive)
2. **Extract complete content**: Capture everything until next heading or end of file
3. **Preserve formatting**: Keep bullets, lists, bold, italic, links
4. **Clean presentation**: Remove excessive whitespace
5. **Create valid wiki links**: Format as `[[25-10-01 - Wed]]`
6. **Track accurately**: Record processed files with timestamps
7. **Handle incremental runs**: Only process new/modified files
8. **Skip empty sections**: Ignore empty diary sections
9. **Update tracker reliably**: Save after extraction
10. **Maintain diary.md integrity**: Append cleanly

## Edge Cases Handled

- **Empty diary sections**: Skip silently
- **Missing diary heading**: Skip file
- **Subdirectories**: Recursive scan
- **Non-standard filenames**: Handle any `.md` file
- **Diary at end of file**: Extract properly
- **Multiple diary sections**: Extract only first one
- **Modified files**: Re-extract if modified after last extraction

## Related Resources

- Diary file: `/Users/harrysayers/Developer/claudelife/04-resources/diary.md`
- Tracker: `/Users/harrysayers/Developer/claudelife/.claude/commands/.extract-diary-tracker.json`
- Daily notes: `/Users/harrysayers/Developer/claudelife/00 - Daily/`
- Similar commands: `/extract-insights`, `/extract-context`

## Maintenance Notes

### Tracker Management

**View tracker**:
```bash
cat /Users/harrysayers/Developer/claudelife/.claude/commands/.extract-diary-tracker.json | jq '.'
```

**Reset tracker** (force re-extraction):
```bash
rm /Users/harrysayers/Developer/claudelife/.claude/commands/.extract-diary-tracker.json
```

### diary.md Management

The diary file grows over time. Consider:
- Monthly archival (create separate files per month/year)
- Reflective review sessions
- Pattern analysis across diary entries
- Creating summaries or highlights

## Troubleshooting

**Issue**: Diary not being extracted
- **Check**: Does the note have `### Diary` or `### diary`?
- **Check**: Is there actual content (not just whitespace)?

**Issue**: Duplicate diary entries
- **Cause**: File was modified and re-extracted
- **Solution**: Expected behavior for modified files

**Issue**: Command runs slowly
- **Solution**: First run is slowest; subsequent runs are fast

---

**Ready to extract diary entries from your daily notes!**
