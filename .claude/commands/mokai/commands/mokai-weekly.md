Weekly review and planning - extracts from diary notes, updates trackers, plans next week.

**USES SERENA MCP FOR EFFICIENT AGGREGATION & MEMORY STORAGE**

## Process:

### 1. Gather Week's Diary Notes (USE SERENA)
- Read `.mokai-tracker.json` to get current week start date
- Calculate week date range (Monday-Sunday)
- Use `mcp__serena__search_for_pattern` across week's files:
  - Pattern: `(## 🏆 Wins|## 🚨 Blockers|## 💡 Learnings|## What I Did Today)`
  - Path filter: Only diary files from this week's date range
  - Context lines: 5 after each match
- Aggregate results by category

### 1b. Scan Completed MOKAI Inbox Tasks This Week (USE SERENA)
- Use `mcp__serena__find_file` with pattern `*.md` in `/00-inbox/tasks/`
- For each file:
  - Check frontmatter for `relation:.*mokai` and `type: Task`
  - Check if `Done: true` and `date modified` is within this week's date range
- Count completed inbox tasks for weekly metrics
- Include notable completed tasks in weekly summary

### 2. Analyze Week's Progress (USE SERENA)
- Read `/01-areas/business/mokai/status/phase-1-foundation.md`
- Use `mcp__serena__search_for_pattern` to find unchecked tasks in current week section
- Cross-reference "What I Did Today" items with unchecked tasks (fuzzy match)
- Count: How many checklist items completed this week?
- Identify: What didn't get done? (these roll to next week)

### 3. Read Last Week's Memory (USE SERENA)
- Try `mcp__serena__read_memory("mokai_progress_metrics")`
- If exists: Compare this week vs last week
  - Task completion rate trend
  - Blocker persistence check
  - Learning velocity comparison

### 4. Interactive Reflection
Ask me:
```
📊 Let's review this week together.

Based on your diary notes, here's what I see:
- ✅ Phase 1 Checklist: [X tasks] completed ([Y]% of week's goals)
- ✅ Inbox Tasks: [X tasks] completed this week
- 🏆 Wins: [aggregated wins]
- 🚨 Blockers: [aggregated blockers]
- 💡 Learnings: [aggregated learnings]

**Week-over-Week** (if memory exists):
- Last week: [X]% completion | This week: [Y]% completion
- Trend: [Improving / Stable / Declining]

Quick questions:
1. What's the ONE thing you're most proud of this week?
2. What's the BIGGEST blocker I should know about?
3. On a scale 1-10, how do you feel about MOKAI progress?
```

### 5. Update Phase 1 Checklist
- Mark completed items as [x]
- Roll incomplete items to next week with note "(from Week X)"
- Identify next week's focus section
- Write updated checklist back

### 6. Update Dashboard
- Read `/01-areas/business/mokai/mokai-dashboard.md`
- Update:
  - "This Week's Focus": Set to next week's focus from Phase 1
  - "Weekly Scorecard": Add new week entry with aggregated data
  - "Recent Wins": Update with top wins from week
  - "Current Status/Blockers": Update with latest blockers
  - "Last Updated": Today's date
- Write dashboard back

### 7. Store Week's Insights in Memory (USE SERENA)
```javascript
mcp__serena__write_memory({
  memory_name: "mokai_progress_metrics",
  content: `
# MOKAI Progress Metrics - Updated [Date]

## Week [X] Summary ([Date Range])
- Phase 1 checklist tasks: [X]/[Y] ([Z]%)
- Inbox tasks completed: [X]
- Diary notes: [X]/7 days
- Wins: [X]
- Blockers: [X]
- Top learning theme: [Theme]

## Historical Trend
- Week 1: [X]% completion
- Week 2: [Y]% completion
- Week 3: [Z]% completion

## Persistent Blockers
- "[Blocker]" - Week [X], [Y], [Z] (still active)

## Learning Velocity
- Ops Guide sections: [X] completed, [Y] remaining
- Estimated completion: [Date]
`
})

mcp__serena__write_memory({
  memory_name: "mokai_weekly_insights",
  content: `
# Week [X] Insights ([Date Range])

## Key Patterns
[Notable patterns from this week's diary]

## Strategic Context
[Decision made, pivot considered, etc.]

## Next Week Focus
[From Phase 1 checklist]

## Notes for Future
[Anything to remember for next review]
`
})
```

### 8. Update Tracker
- Increment weekInPhase (1 → 2 → 3 → 4)
- Set currentWeekStart to next Monday's date
- Update lastProcessed timestamp
- Write tracker back

### 9. Strategic Pep Talk
Provide personalized guidance:
```
🎯 Week [X] Wrap-Up

**This Week's Reality Check**:
[Honest assessment: what went well, what didn't]

**Comparison to Last Week**:
[If memory exists, show trend: improving/stable/declining]

**Next Week's Mission** (Week [X+1]):
[Focus area from Phase 1 checklist]

**Why This Week Matters**:
[Strategic context: how it connects to Phase 1 goal]

**Pattern Alert**:
[If blocker mentioned multiple weeks, or other pattern from memory]

**One Thing to Remember**:
[Most important principle for next week]

**You've got this. Let's keep building MOKAI. 🚀**
```

## Important Rules:
- USE SERENA for all pattern matching and aggregation
- Read ALL diary notes from the week (not just latest)
- STORE insights in memory for trend analysis
- Be honest in assessment (celebrate wins, acknowledge blockers)
- Keep next week's focus realistic (3-5 tasks max)
- Roll incomplete tasks forward automatically
- Update tracker so next `/mokai-status` knows the current week
- Be encouraging but hold me accountable
- Reference memory trends to show progress over time
