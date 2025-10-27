Read MOKAI daily notes, extract updates, and provide strategic status with dynamic task management.

**USES SERENA MCP FOR EFFICIENT PATTERN MATCHING**

## Process:

### 1. Read Tracker
- Read `/01-areas/business/mokai/.mokai-tracker.json`
- Get list of already processed files
- Get current phase and week

### 2. Scan Daily Notes (USE SERENA)
- Calculate today's date in YYYY-MM-DD format
- Use `mcp__serena__list_dir` on `/01-areas/business/mokai/diary/`
- **ALWAYS include today's diary note** (even if in processedFiles - allows same-day updates)
- Filter other files to only unprocessed (not in tracker's processedFiles array)
- For each file to process:
  - Use `mcp__serena__search_for_pattern` to extract sections:
    - Pattern: `(## 🏆 Wins|## 🚨 Blockers|## 💡 Learnings|## 📝 Context/Updates|## What I Did Today)`
    - Context lines: 5 after each match
  - Parse extracted content into structured data

### 2b. Scan MOKAI Task Files in Inbox (USE SERENA)
- Use `mcp__serena__find_file` with pattern `*.md` in `/00-inbox/tasks/`
- For each file found:
  - Use `mcp__serena__search_for_pattern` to check frontmatter:
    - Pattern: `(relation:.*mokai|relation:.*\[\[mokai\]\])`
    - Also verify: `type: Task` or `type: task` exists
  - For matching MOKAI tasks, extract:
    - **Filename** (without .md extension = task title)
    - **Done status**: `Done: true/false` (if false or missing = incomplete)
    - **Priority**: `priority: urgent|high|low` (or empty)
    - **Description**: Extract from `description:` field if present
  - Group incomplete tasks by priority:
    - 🔥 **Urgent**: `priority: urgent`
    - ⚠️ **High**: `priority: high`
    - 📌 **Normal**: `priority: low` or no priority field
  - Filter to only incomplete tasks (`Done: false` or no Done field)

### 3. Update Phase 1 Checklist Dynamically (USE SERENA)
- Read `/01-areas/business/mokai/status/phase-1-foundation.md`
- Use `mcp__serena__search_for_pattern` to find all unchecked tasks: `- \[ \]`
- For each "What I Did Today" item from diary:
  - Fuzzy match against unchecked tasks (keywords match, not exact)
  - Mark matching checklist items as [x] (completed)
- For incomplete tasks from past days:
  - Move them forward to current/next day
  - Add note: "(rolled from [date])"
- Calculate: What week are we in? (based on tracker)
- Highlight: What's the current week's focus?

### 4. Update Dashboard (with Deduplication)
- Read `/01-areas/business/mokai/mokai-dashboard.md`
- Update sections:
  - **This Week's Focus**: Set to current week from Phase 1 checklist
  - **Inbox Tasks**: Add section showing MOKAI tasks from /00-inbox/tasks/ grouped by priority
  - **Current Status**: Update blockers, learning progress
  - **Recent Wins**:
    - Read existing wins from dashboard
    - For each new win from diary:
      - Check if similar win already exists (fuzzy match on text, 80%+ similarity)
      - Only add if NOT a duplicate
    - Keep last 5-7 unique wins
  - **Blockers**:
    - Read existing blockers
    - Deduplicate new blockers against existing (fuzzy match)
    - Replace with updated list
  - **Last Updated**: Today's date
  - **Weekly Scorecard**: Add latest entries if Friday
- Write updated dashboard back

### 5. Check Memory for Context (USE SERENA)
- Try to read `mcp__serena__read_memory("mokai_progress_metrics")`
- If exists: Compare current week vs historical trends
- If not exists: Note to create during `/mokai-weekly`

### 6. Update Tracker
- Add processed diary files to tracker's processedFiles array
- **EXCEPT**: Do NOT add today's date to processedFiles (allow re-reading throughout the day)
- **Only mark as processed**: Files from previous days (once day is over, they're stable)
- Update lastProcessed timestamp
- Write tracker back

### 7. Strategic Status Report
Provide concise summary:
```
📍 MOKAI Status - [Date]

**Phase**: [Current Phase] - Week [X]
**This Week's Focus**: [Current week objective]

**Progress**:
- ✅ Completed: [X tasks from checklist]
- 🔄 In Progress: [Active tasks]
- ⏭️ Coming Up: [Next 2-3 tasks]

**Inbox Tasks** (from /00-inbox/tasks/):
🔥 **Urgent** ([X] tasks):
- [Task 1]
- [Task 2]

⚠️ **High Priority** ([X] tasks):
- [Task 1]
- [Task 2]

📌 **Normal** ([X] tasks):
- [Task 1]
- [Task 2]

**Recent Activity** (from diary):
- [Latest wins]
- [Current blockers]
- [Key learnings]

**⚡ What You Should Work On RIGHT NOW**:
[Prioritize: Urgent inbox tasks first, then current week focus tasks, then high priority inbox]

**Why This Matters**:
[Strategic context: how this connects to Phase 1 goal and urgent tasks]

**Pattern Alert** (if applicable):
[If memory shows recurring blocker/pattern, mention it]
```

### 8. Co-Founder Accountability
End with direct guidance:
- Be specific about next action (not vague)
- Reference Operations Guide sections if relevant
- Keep me focused on learning during Phase 1
- Remind me of the bigger picture if I seem scattered
- Call out patterns from memory if relevant

## Important Rules:
- USE SERENA for pattern matching (faster, more accurate)
- Always read diary notes FIRST before making recommendations
- **ALWAYS re-read today's diary note** (even if processed earlier - allows same-day updates)
- Mark diary files as processed ONLY if from previous days (not today)
- **Deduplicate wins and blockers** when updating dashboard (fuzzy match 80%+ similarity)
- **Scan inbox tasks** to surface urgent/high priority items
- **Prioritize urgent inbox tasks** over routine Phase 1 tasks when making recommendations
- Keep dashboard concise (don't let it bloat)
- Roll incomplete tasks forward automatically
- Be strategic, not just reactive
- Act like a co-founder who knows the plan and holds me accountable
- If urgent tasks exist in inbox, call them out prominently in status report
