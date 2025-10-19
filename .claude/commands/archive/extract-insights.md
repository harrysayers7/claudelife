---
created: "2025-10-12 21:30"
description: |
  Extracts insights from Obsidian daily notes and consolidates them into a central insights file.

  This command:
    - Scans daily notes in /00 - Daily directory (and subdirectories)
    - Extracts content from ### 💡 Insights sections
    - Appends to /01-areas/p-dev/insights.md with wiki links to source notes
    - Tracks processed files to avoid re-scanning (incremental extraction)
    - Re-extracts if files were modified since last scan
    - Preserves markdown formatting while cleaning up presentation

  Outputs formatted insights with H3 headings linking back to source daily notes.
examples:
  - /extract-insights
---

# Extract Insights

This command scans your Obsidian daily notes, extracts insights, and consolidates them into a central insights file for easy review and knowledge management.

## Usage

```bash
/extract-insights
```

## What This Command Does

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

I will:
1. Load the tracking file to identify previously processed notes
2. Scan all markdown files in `/Users/harrysayers/Developer/claudelife/00 - Daily` (including subdirectories)
3. For each daily note:
   - Check if it's new or modified since last extraction
   - Extract content under `### 💡 Insights` heading
   - Skip files with no insights content (empty sections)
4. Append extracted insights to `/Users/harrysayers/Developer/claudelife/01-areas/p-dev/insights.md`
5. Format each insight section with H3 wiki link to source note
6. Update tracking file with processed files and timestamps

## Tracking System

The command uses **Option B: Separate tracking file** for cleanliness.

**Tracker Location**: `/Users/harrysayers/Developer/claudelife/.claude/commands/.extract-insights-tracker.json`

**Tracker Format**:
```json
{
  "last_scan": "2025-10-12T21:30:00Z",
  "processed_files": {
    "25-10-01 - Wed.md": {
      "extracted_at": "2025-10-12T21:30:00Z",
      "modified_at": "2025-10-01T15:20:00Z"
    },
    "25-10-02 - Thu.md": {
      "extracted_at": "2025-10-12T21:30:00Z",
      "modified_at": "2025-10-02T18:45:00Z"
    }
  }
}
```

## Process

### 1. Load or Create Tracker

```javascript
// Check if tracker exists
const trackerPath = '/Users/harrysayers/Developer/claudelife/.claude/commands/.extract-insights-tracker.json';

let tracker = {
  last_scan: null,
  processed_files: {}
};

// Load existing tracker if it exists
if (file exists) {
  tracker = JSON.parse(read file);
}
```

### 2. Scan Daily Notes Directory

```javascript
// Find all markdown files in 00 - Daily (recursive)
const dailyNotesPath = '/Users/harrysayers/Developer/claudelife/00 - Daily';
const allNotes = glob('**/*.md', { cwd: dailyNotesPath });

// Filter to only new or modified files
const notesToProcess = allNotes.filter(note => {
  const noteModifiedTime = getFileModifiedTime(note);
  const lastExtracted = tracker.processed_files[note]?.extracted_at;
  const lastModified = tracker.processed_files[note]?.modified_at;

  // Include if: never processed OR file modified since last extraction
  return !lastExtracted || noteModifiedTime > lastModified;
});
```

### 3. Extract Insights from Each Note

For each note in `notesToProcess`:

```javascript
// Read the daily note
const content = readFile(note);

// Find the ### 💡 Insights section
const insightsMatch = content.match(/### 💡 Insights\n([\s\S]*?)(?=\n###|\n---|$)/);

if (!insightsMatch || !insightsMatch[1].trim()) {
  // Skip - no insights or empty section
  continue;
}

// Extract and clean insights content
let insights = insightsMatch[1].trim();

// Clean up formatting while preserving content:
// - Remove excessive blank lines (more than 2 consecutive)
// - Preserve bullet points, numbered lists, paragraphs
// - Preserve markdown formatting (bold, italic, links, code)
// - Remove leading/trailing whitespace

insights = insights
  .replace(/\n{3,}/g, '\n\n')  // Max 2 consecutive newlines
  .trim();
```

### 4. Format Output with Wiki Links

```javascript
// Extract date from filename (e.g., "25-10-01 - Wed.md" → "25-10-01 - Wed")
const noteName = path.basename(note, '.md');

// Create H3 heading with wiki link
const heading = `### [[${noteName}]]`;

// Combine heading + insights
const formattedInsight = `${heading}\n\n${insights}\n\n---\n\n`;
```

### 5. Append to insights.md

```javascript
// Append to insights file (file already exists per requirements)
const insightsFile = '/Users/harrysayers/Developer/claudelife/01-areas/p-dev/insights.md';

appendToFile(insightsFile, formattedInsight);
```

### 6. Update Tracker

```javascript
// Record this file as processed
tracker.processed_files[note] = {
  extracted_at: new Date().toISOString(),
  modified_at: getFileModifiedTime(note)
};

// Update last scan time
tracker.last_scan = new Date().toISOString();

// Save tracker
writeFile(trackerPath, JSON.stringify(tracker, null, 2));
```

## Output Format

Insights are appended to `insights.md` in this format:

```markdown
### [[25-10-01 - Wed]]

- Learned that Serena MCP is faster for codebase search
- MOKAI Indigenous procurement threshold is $80k-$200k for MSA
- Need to update contractor agreements

---

### [[25-10-02 - Thu]]

Discovered that FastAPI MCP servers need restart after .mcp.json changes.

The key insight: MCP servers cache their configuration independently of the codebase, so code changes don't automatically reflect until restart.

---

### [[25-10-03 - Fri]]

- Supabase project ID must be verified before operations
- Always use project `gshsshaodoyttdxippwx` for SAYERS DATA
- Row-level security policies enforce entity isolation

---
```

## Examples

### Example 1: First Run (No Tracker Exists)

**Scenario**: First time running the command, no tracker file exists.

**Process**:
1. Create new tracker file
2. Scan all `.md` files in `/00 - Daily`
3. Extract insights from all notes that have content under `### 💡 Insights`
4. Append all extracted insights to `insights.md`
5. Record all processed files in tracker with timestamps

**Output**:
```
Scanning daily notes...
Found 45 daily notes
Processing 45 new files...

✓ Extracted insights from 25-09-15 - Mon.md
✓ Extracted insights from 25-09-16 - Tue.md
✓ Skipped 25-09-17 - Wed.md (no insights)
✓ Extracted insights from 25-09-18 - Thu.md
...

Summary:
- 32 insights extracted
- 13 files skipped (no insights)
- insights.md updated
- Tracker created at .claude/commands/.extract-insights-tracker.json
```

### Example 2: Incremental Run (Tracker Exists)

**Scenario**: Running command after a few days, some new notes created.

**Process**:
1. Load existing tracker
2. Identify files created/modified since last scan
3. Extract insights only from new/modified files
4. Append to `insights.md`
5. Update tracker with new files

**Output**:
```
Scanning daily notes...
Found 48 daily notes
Previously processed: 45 files
Processing 3 new/modified files...

✓ Extracted insights from 25-10-11 - Sat.md
✓ Extracted insights from 25-10-12 - Sun.md
✓ Skipped 25-10-13 - Mon.md (no insights)

Summary:
- 2 new insights extracted
- 1 file skipped (no insights)
- insights.md updated
- Tracker updated
```

### Example 3: Re-extraction (Modified File)

**Scenario**: You edited a daily note to add more insights after it was already processed.

**Process**:
1. Load tracker
2. Detect that `25-10-05 - Sun.md` was modified after last extraction
3. Re-extract insights from that file
4. Append updated insights to `insights.md` (will create duplicate section)
5. Update tracker timestamp

**Output**:
```
Scanning daily notes...
Found 48 daily notes
Previously processed: 48 files
Processing 1 modified file...

✓ Re-extracted insights from 25-10-05 - Sun.md (file was modified)

Summary:
- 1 insight re-extracted
- insights.md updated
- Tracker updated

Note: 25-10-05 - Sun.md appears twice in insights.md (original + updated).
Consider manually consolidating if needed.
```

## Evaluation Criteria

A successful extraction should:

1. **Correctly identify insights sections**: Find `### 💡 Insights` heading (including emoji)
2. **Extract complete content**: Capture everything until next heading or end of file
3. **Preserve formatting**: Keep bullets, lists, bold, italic, links, code blocks
4. **Clean presentation**: Remove excessive whitespace while maintaining readability
5. **Create valid wiki links**: Format as `[[25-10-01 - Wed]]` for Obsidian linking
6. **Track accurately**: Record processed files with correct timestamps
7. **Handle incremental runs**: Only process new/modified files on subsequent runs
8. **Skip empty sections**: Ignore notes with empty or whitespace-only insights
9. **Update tracker reliably**: Save tracker after successful extraction
10. **Maintain insights.md integrity**: Append cleanly without corrupting existing content

## Edge Cases Handled

- **Empty insights sections**: Silently skip, don't append empty H3 headings
- **Missing insights heading**: Skip file, no error
- **Subdirectories**: Recursively scan all subdirectories in `/00 - Daily`
- **Non-standard filenames**: Handle any `.md` file regardless of naming pattern
- **Insights at end of file**: Extract even if no heading follows (use end of file as boundary)
- **Multiple insights sections**: Only extract from first `### 💡 Insights` found
- **Modified files**: Re-extract if file modified after last extraction timestamp

## Related Resources

- Daily notes template: `/Users/harrysayers/Developer/claudelife/98-templates/`
- Insights file: `/Users/harrysayers/Developer/claudelife/01-areas/p-dev/insights.md`
- Tracker file: `/Users/harrysayers/Developer/claudelife/.claude/commands/.extract-insights-tracker.json`
- PARA method structure: `/Users/harrysayers/Developer/claudelife/CLAUDE.md`

## Maintenance Notes

### Tracker Management

**View tracker status**:
```bash
cat /Users/harrysayers/Developer/claudelife/.claude/commands/.extract-insights-tracker.json | jq '.'
```

**Reset tracker** (force re-extraction of all files):
```bash
rm /Users/harrysayers/Developer/claudelife/.claude/commands/.extract-insights-tracker.json
```

**View last scan time**:
```bash
cat /Users/harrysayers/Developer/claudelife/.claude/commands/.extract-insights-tracker.json | jq '.last_scan'
```

### insights.md Management

The insights file grows over time. Consider:
- Periodic review and archival of old insights
- Tagging insights by theme or project
- Creating derivative documents (monthly summaries, thematic collections)
- Using Obsidian's graph view to explore insight relationships

### Performance Considerations

- **First run**: May take 30-60 seconds for large daily note collections
- **Incremental runs**: Typically under 5 seconds
- **Re-extractions**: Minimal performance impact unless many files modified
- **Subdirectories**: Recursive scanning adds minimal overhead

## Troubleshooting

**Issue**: Insights not being extracted

- **Check**: Does the note have `### 💡 Insights` (with emoji)?
- **Check**: Is there content after the heading (not just whitespace)?
- **Solution**: Ensure heading matches exactly, including emoji

**Issue**: Duplicate insights in insights.md

- **Cause**: File was modified and re-extracted
- **Solution**: This is expected behavior for modified files. Manually consolidate if desired.

**Issue**: Tracker shows files that don't exist

- **Cause**: Daily notes were deleted or renamed
- **Solution**: Tracker is harmless; it simply records history. Delete tracker to clean up.

**Issue**: Command runs slowly

- **Check**: How many daily notes exist?
- **Solution**: First run is slowest; subsequent runs are fast (incremental)

---

**Ready to extract insights from your daily notes!**
