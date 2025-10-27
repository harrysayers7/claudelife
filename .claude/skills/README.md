# Claude Code Skills - MOKAI Integration

**Created**: 2025-10-21
**Status**: Phase 1 Implementation Complete

## What Are Skills?

Skills are self-contained workflow packages that Claude automatically discovers and executes when relevant, based on the description in `SKILL.md`.

**vs Slash Commands**:
- **Skills** = Auto-detected from conversation context
- **Commands** = User explicitly invokes with `/command`

## Current Skills

### daily-workflow/
**Auto-triggers when**: User mentions daily notes, diary extraction, end-of-day, or asks "what did I work on today"

**What it does**:
1. Scans daily notes for `### 🧠 Notes` sections
2. Extracts and classifies entries (Diary/Insight/Context/Idea)
3. Routes entries to 24 context areas based on AI confidence >80%
4. Transforms diary narratives to factual statements for context files
5. Detects smart memory opportunities (Serena + Graphiti)
6. Updates tracker system
7. Creates cross-links bidirectionally

**Files**:
- `SKILL.md` - Main workflow (loaded when triggered)
- `reference/templates.md` - Daily note template guide
- `reference/formatting-rules.md` - Transformation and routing rules
- `scripts/extract_content.py` - Deterministic extraction operations

**Same logic as**: `/extract-daily-content` command (but auto-detected)

### mokai-daily-ops/
**Auto-triggers when**: User mentions MOKAI tasks, status, priorities, or asks what to work on

**What it does**:
1. Scans diary notes (via Serena MCP)
2. Scans inbox tasks for MOKAI items
3. Updates tracker, checklist, dashboard
4. Provides strategic status report

**Files**:
- `SKILL.md` - Main workflow (loaded when triggered)
- `TRACKER.md` - Tracker system reference
- `DIARY.md` - Diary format guide

**Same logic as**: `/mokai-status` command (but auto-detected)

## Hybrid Architecture

### Skills (Automatic)
- ✅ `daily-workflow` - Daily note extraction and categorization
- ✅ `mokai-daily-ops` - Daily status updates
- 🔜 `mokai-diary` - Auto-categorize diary entries
- 🔜 `mokai-tracker` - Auto-update tracker from conversation

### Commands (Explicit)
- 🔵 `/mokai-master` - Load context
- 🔵 `/mokai-weekly` - Weekly review ritual
- 🔵 `/mokai-status` - Manual status (fallback)
- 🔵 `/mokai-wins` - Quick win logging
- 🔵 `/mokai-dump` - Bulk entry categorization

## How to Test

After restarting Claude Code:

**Daily Workflow Skill**:
1. Say: "What did I work on today?"
   → Should auto-trigger `daily-workflow` skill
2. Say: "Extract content from my daily note"
   → Should scan and classify entries
3. Say: "I'm done for today, extract my notes"
   → Should process today's entries

**MOKAI Daily Ops Skill**:
1. Say: "What should I work on for MOKAI?"
   → Should auto-trigger `mokai-daily-ops` skill
2. Share an achievement naturally: "I just finished the Supply Nation application"
   → Should auto-log to diary
3. Ask: "What's my MOKAI status?"
   → Should provide strategic status without `/mokai-status`

## Next Steps (Phase 2)

1. **mokai-diary skill** - Auto-categorize when user shares updates
2. **mokai-insight-capture skill** - Auto-detect learnings/blockers in conversation
3. **Gradually deprecate commands** if skills prove superior

## File Structure

```
.claude/skills/
├── daily-workflow/
│   ├── SKILL.md                        # Main workflow
│   ├── reference/
│   │   ├── templates.md                # Daily note template guide
│   │   └── formatting-rules.md         # Transformation rules
│   └── scripts/
│       └── extract_content.py          # Extraction script
└── mokai-daily-ops/
    ├── SKILL.md                        # Main workflow
    ├── TRACKER.md                      # System reference
    └── DIARY.md                        # Format guide

.claude/commands/mokai/
├── commands/
│   ├── mokai-status.md                 # Manual fallback
│   ├── mokai-weekly.md                 # Weekly ritual
│   ├── mokai-wins.md                   # Quick logging
│   └── mokai-dump.md                   # Bulk categorization
└── agents/
    └── mokai-master.md                 # Context loading
```

## Benefits

- **Less friction**: Natural conversation vs remembering commands
- **Automatic capture**: Context stored without explicit logging
- **Progressive disclosure**: References loaded only when needed
- **Token efficient**: SKILL.md loads first, references on-demand
- **Composable**: Multiple skills work together automatically

## Notes

- Skills must be enabled in Claude Code Settings > Capabilities after restart
- Skills share context window - keep SKILL.md concise
- Use forward slashes in file references: `reference/guide.md`
- Test descriptions carefully - too broad = over-triggering
