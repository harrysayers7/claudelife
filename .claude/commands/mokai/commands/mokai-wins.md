Quick win logging - adds to today's diary note automatically.

## Process:

### 1. Ask for Win
Ask: "What did you accomplish?"

### 2. Find/Create Today's Diary Note
- Get today's date in format: YYYY-MM-DD
- Check if `/01-areas/business/mokai/diary/[today].md` exists
- If NOT exists: Create it from template (see below)
- If exists: Read it

### 3. Add Win to Diary
- Find the "## 🏆 Wins" section
- Add new win as bullet point: `- [win description]`
- Write diary note back

### 4. Quick Celebration + Next Priority
Response format:
```
🎉 Nice! Added to today's diary:
✅ [win description]

Keep the momentum going. Next priority: [based on current week's focus from Phase 1 checklist]
```

## Diary Note Template (if creating new):
```markdown
---
date: [YYYY-MM-DD]
day: [Day of week]
---
# MOKAI Daily Note - [Month Day, Year]

## What I Did Today
-

## 💡 Learnings
-

## 🏆 Wins
- [The new win]

## 🚨 Blockers
-

## 📝 Context/Updates
-

## 🎯 Tomorrow's Focus
-
```

## Important Rules:
- Never overwrite existing diary content
- Add to sections, don't replace
- Keep it fast (<30 seconds total)
- Always give next priority hint
