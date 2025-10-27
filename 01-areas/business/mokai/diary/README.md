---
tags: [mokai, diary, daily-ops]
relation:
  - "[[mokai]]"
  - "[[mokai]]"
date: "2025-10-14"
---
# MOKAI Diary System

## How It Works

Write naturally in daily notes → Slash commands extract & update everything → Stay accountable & strategic

---

## Daily Workflow

### Morning (30 seconds)
```bash
/mokai-status
```
- Reads all unprocessed diary notes
- Updates dashboard & checklist automatically
- Tells you: "Work on X today"

### During the Day (as you go)
Just write in today's diary note (`YYYY-MM-DD.md`):
- What you did
- What you learned
- Wins (big or small)
- Blockers
- Context/updates

**Or use quick win logging**:
```bash
/mokai-wins
```
- Asks "What did you accomplish?"
- Adds to today's diary automatically
- Gives you next priority

### Friday Afternoon (10 minutes)
```bash
/mokai-weekly
```
- Reviews entire week's diary notes
- Updates Phase 1 checklist (marks completed, rolls forward incomplete)
- Plans next week's focus
- Strategic pep talk

---

## File Structure

```
/01-areas/business/mokai/
├── mokai-dashboard.md          # Mission control (auto-updated)
├── .mokai-tracker.json         # Tracks processed notes
├── status/
│   ├── phase-1-foundation.md   # Next 30 days (auto-updated)
│   └── phase-2-3-future.md     # Reference only
└── diary/
    ├── .diary-template.md      # Template for Obsidian
    ├── 2025-10-14.md          # Daily notes (you write these)
    ├── 2025-10-15.md
    └── ...
```

---

## What Gets Updated Automatically

When you run `/mokai-status`:
- ✅ Marks completed tasks in Phase 1 checklist
- 📝 Updates dashboard with latest wins/blockers
- 🗓️ Rolls forward incomplete tasks
- 📊 Tracks which diary files have been processed

When you run `/mokai-weekly`:
- ✅ Reviews entire week's progress
- 📈 Updates Phase 1 checklist for next week
- 🎯 Sets next week's focus on dashboard
- 📝 Creates weekly scorecard entry

---

## Obsidian Setup (Optional)

### Daily Note Template
1. In Obsidian settings → Core plugins → Daily notes
2. Set template location: `01-areas/business/mokai/diary/.diary-template.md`
3. Set note location: `01-areas/business/mokai/diary`
4. Set date format: `YYYY-MM-DD`

Now clicking "Open today's daily note" creates properly formatted diary entries.

### Quick Command
- Add hotkey for "Open today's daily note" (e.g., `Cmd+Shift+D`)
- Write throughout the day naturally
- `/mokai-status` in morning pulls it all together

---

## The Magic

You never manually update:
- Dashboard
- Phase 1 checklist
- Tracker file
- Weekly scorecards

You just **write naturally in diary notes**, and the system stays current.

Zero friction. Maximum accountability.
