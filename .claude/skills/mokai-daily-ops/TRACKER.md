# MOKAI Tracker System

**Location**: `/01-areas/business/mokai/.mokai-tracker.json`

## Structure

```json
{
  "processedFiles": [
    "2025-10-15-mokai-daily.md",
    "2025-10-16-mokai-daily.md"
  ],
  "currentWeek": 3,
  "currentWeekStart": "2025-10-14",
  "currentPhase": "Phase 1: Foundation",
  "lastProcessed": "2025-10-17T08:30:00Z"
}
```

## Fields

- **processedFiles**: Array of diary filenames already scanned
  - Only includes previous days (NOT today)
  - Prevents duplicate processing
  - Today's file is ALWAYS re-read (same-day updates)

- **currentWeek**: Week number in current phase (from Phase 1 checklist)
  - Updated by `/mokai-weekly` command
  - Used to determine "This Week's Focus"

- **currentWeekStart**: ISO date of week start (Monday)
  - Updated by `/mokai-weekly`
  - Helps calculate week boundaries

- **currentPhase**: "Phase 1: Foundation" | "Phase 2: Growth" | etc.
  - Updated when advancing phases
  - Determines which checklist to use

- **lastProcessed**: ISO timestamp of last tracker update
  - Updated every time daily-ops runs
  - Used for debugging/auditing

## Processing Rules

### Adding to processedFiles
```javascript
// Pseudo-code
const today = getTodayDate(); // "2025-10-17"

diaryFiles.forEach(file => {
  const fileDate = extractDate(file); // "2025-10-15"

  if (fileDate < today) {
    // Previous day - mark as processed
    tracker.processedFiles.push(file);
  } else if (fileDate === today) {
    // Today - DO NOT mark as processed
    // (allows re-reading throughout day)
  }
});
```

### Week Increment
Only during `/mokai-weekly`:
```javascript
tracker.currentWeek += 1;
tracker.currentWeekStart = getNextMondayDate();
```

## Usage in Daily Ops

1. **Read tracker** → Get processedFiles list
2. **List diary directory** → Get all diary files
3. **Filter files**:
   - Include: Files NOT in processedFiles
   - Always include: Today's date
4. **Process filtered files** → Extract content
5. **Update tracker**:
   - Add previous days to processedFiles
   - Do NOT add today
   - Update lastProcessed timestamp
