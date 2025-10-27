# MOKAI Diary Format

**Location**: `/01-areas/business/mokai/diary/YYYY-MM-DD-mokai-daily.md`

**Template**: `/98-templates/mokai-note.md`

## Standard Sections

Daily notes follow consistent structure for pattern matching:

```markdown
---
date: "YYYY-MM-DD HH:MM"
type: daily-note
tags: [mokai, business]
---

# MOKAI Daily - [Day], [Month] [Date]

## 🏆 Wins
- [Achievement 1]
- [Achievement 2]

## 🚨 Blockers
- [Blocker 1]
- [Blocker 2]

## 💡 Learnings
- [Learning 1]
- [Learning 2]

## 📝 Context/Updates
- [Update 1]
- [Update 2]

## What I Did Today
- [ ] Task 1
- [x] Task 2 (completed)
- [ ] Task 3
```

## Extraction Patterns

### Wins Pattern
```regex
## 🏆 Wins
(.*?)(?=##|$)
```
Captures all list items under Wins section.

### Blockers Pattern
```regex
## 🚨 Blockers
(.*?)(?=##|$)
```

### Learnings Pattern
```regex
## 💡 Learnings
(.*?)(?=##|$)
```

### Context Pattern
```regex
## 📝 Context/Updates
(.*?)(?=##|$)
```

### Tasks Pattern
```regex
## What I Did Today
(.*?)(?=##|$)
```

## Serena Search Example

```javascript
mcp__serena__search_for_pattern({
  substring_pattern: "(## 🏆 Wins|## 🚨 Blockers|## 💡 Learnings|## 📝 Context/Updates|## What I Did Today)",
  relative_path: "01-areas/business/mokai/diary/2025-10-17-mokai-daily.md",
  context_lines_after: 5
})
```

Returns sections with 5 lines of content after each heading.

## Task Checkbox Parsing

- `- [ ]` = Incomplete task
- `- [x]` or `- [X]` = Completed task

Extract task text and completion status:
```javascript
const task = {
  text: "Task description",
  completed: true/false
}
```

## Dashboard Deduplication

When adding wins/blockers to dashboard:
1. Read existing items from dashboard
2. For each new item:
   - Fuzzy match against existing (80%+ similarity)
   - Skip if duplicate found
   - Add if unique
3. Keep last 5-7 unique items

## Same-Day Re-reading

**Critical**: Today's diary note is ALWAYS re-read during daily-ops, even if already processed earlier. This allows:
- Updating status multiple times per day
- Adding wins/blockers throughout the day
- Keeping dashboard current

**Previous days**: Marked as processed once and never re-read (stable data).
