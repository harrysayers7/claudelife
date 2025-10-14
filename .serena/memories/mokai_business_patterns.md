# MOKAI Business Patterns

Last Updated: 2025-10-14

This memory captures MOKAI-specific patterns, formats, and workflows for efficient context retrieval.

## File Locations

- **Base Directory**: `/Users/harrysayers/Developer/claudelife/01-areas/business/mokai/`
- **Dashboard**: `mokai-dashboard.md`
- **Diary Notes**: `diary/YYYY-MM-DD.md`
- **Phase 1 Checklist**: `status/phase-1-foundation.md`
- **Operations Guide**: `docs/research/📘 - OPERATIONS GUIDE.md`
- **Inbox Tasks**: `/Users/harrysayers/Developer/claudelife/00-inbox/tasks/*.md` (filtered by `relation: mokai`)

## Diary Note Structure

**Format**: `YYYY-MM-DD.md` (e.g., `2025-10-14.md`)

**Required Sections**:
```markdown
## 🏆 Wins
[Daily accomplishments and positive outcomes]

## 🚨 Blockers
[Issues preventing progress or requiring decisions]

## 💡 Learnings
[Insights gained about MOKAI business, operations, or client interactions]

## What I Did Today
[Activity log - natural writing style]
```

**Usage Pattern**:
- Harrison writes naturally throughout the day
- Sections updated incrementally as events occur
- `/mokai-status` extracts wins/blockers/learnings for dashboard
- Same-day re-reading enabled (updates processed multiple times per day)

## Dashboard Structure

**File**: `mokai-dashboard.md`

**Purpose**: Single source of truth for current MOKAI status

**Sections**:
1. **This Week's Focus** - Current priorities and strategic objectives
2. **Inbox Tasks** - Grouped by priority (🔥 Urgent, ⚠️ High, 📌 Normal)
3. **Recent Wins** - Last 5-7 accomplishments (deduplication enabled)
4. **Current Status/Blockers** - Active issues and roadblocks
5. **Weekly Scorecard** - Metrics and progress indicators

**Update Method**: Automatically updated by `/mokai-status` command
**Deduplication**: Fuzzy matching (80%+ similarity) prevents duplicate wins/blockers

## Phase 1 Checklist

**File**: `status/phase-1-foundation.md`

**Purpose**: 30-day actionable checklist for business foundation (Oct 14 - Nov 14, 2025)

**Focus**: Master business fundamentals while waiting for legal setup completion

**Features**:
- Checkbox-based tasks with priority indicators
- Dynamically updated by slash commands (auto-marks completed tasks)
- Fuzzy task matching detects completion from diary notes
- Incomplete tasks roll forward to next week in `/mokai-weekly`

**Completion Detection**:
- Fuzzy text matching against diary content (80%+ similarity)
- Automatically marked when task description appears in wins/activities

## Inbox Task Format

**Location**: `/00-inbox/tasks/*.md`

**Required Frontmatter**:
```yaml
---
type: Task              # or "task" (case-insensitive)
relation: mokai         # or "[[mokai]]" (wiki-link format)
Done: false             # true when completed (or omit for incomplete)
priority: urgent        # urgent, high, low (or omit for normal priority)
---
```

**Priority Grouping**:
- 🔥 **Urgent** (`priority: urgent`) - Critical blockers, take precedence over routine Phase 1 tasks
- ⚠️ **High** (`priority: high`) - Important but not blocking, prioritized after urgent
- 📌 **Normal** (`priority: low` or no priority field) - Standard tasks

**Scanning**: Automatically scanned by `/mokai-status` and displayed in dashboard by priority

## Slash Commands

### `/mokai-status` - Daily Strategic Status
**When**: Every morning (30 seconds runtime)
**Safe to run multiple times per day** - same-day updates captured

**What it does**:
1. Scans unprocessed diary notes + always re-reads today's note
2. Scans inbox tasks, groups by priority
3. Updates Phase 1 checklist (fuzzy task matching marks completed)
4. Updates dashboard with deduplication
5. Provides strategic guidance on what to work on RIGHT NOW

**Prioritization Logic**: Urgent inbox tasks → Phase 1 focus → High priority inbox → Normal tasks

### `/mokai-weekly` - End-of-Week Review
**When**: Fridays or Sundays (2-3 minutes runtime)

**What it does**:
1. Aggregates week's diary notes
2. Counts completed inbox tasks
3. Compares week-over-week trends (reads Serena memory)
4. Interactive reflection (asks 3 questions)
5. Updates checklist (marks completed, rolls forward incomplete)
6. Stores metrics in Serena memory for next comparison

### `/mokai-insights` - Deep Pattern Analysis
**When**: Monthly (5 minutes runtime)

**What it does**:
1. Scans ALL diary notes for patterns
2. Frequency analysis (top blockers, learning themes, win patterns)
3. Trend analysis (completion rate, blocker persistence)
4. Strategic recommendations based on data

## Tracking System Key Concepts

**Same-Day Re-Reading**: Today's diary note is always re-read (even if processed earlier) to capture updates throughout the day. Only previous days' notes are marked as "processed" (stable content).

**Deduplication**: Fuzzy matching (80%+ similarity) prevents duplicate wins/blockers when running `/mokai-status` multiple times same day.

**Fuzzy Task Matching**: Phase 1 checklist tasks are automatically marked complete when similar text (80%+ match) appears in diary wins or activities.

**Tracker File**: `.mokai-tracker.json` stores processedFiles array (dates of diary notes already scanned, excluding today).

## MOKAI Business Context

**What MOKAI is**: Indigenous-owned technology consultancy delivering cybersecurity services and secure technology solutions to government and enterprise. Acts as prime contractor with single point of accountability.

**Current Focus**: Phase 1 Foundation (Oct 14 - Nov 14, 2025)
- Master business fundamentals
- Build initial processes
- Establish operational foundations
- Prepare for growth while awaiting legal setup completion

**Key Differentiation**:
- Indigenous procurement eligibility (IPP, Exemption 16, Supply Nation)
- Single point of accountability for quality, compliance, risk
- Prime contractor model (Mokai brand, subcontract specialists)
- Hub-and-spoke delivery model

## Agent-MOKAI Role

**Primary Responsibilities**:
1. Read dashboard for current status, recent wins, blockers
2. Read today's diary note for daily activity context
3. Scan inbox tasks for urgent items
4. Understand slash command purposes (don't execute, but explain behavior)
5. Provide strategic guidance based on Phase 1 goals, diary activity, blockers

**Data Source Priority**:
1. Embedded Knowledge (85% of queries)
2. MOKAI Dashboard (current status)
3. Diary Notes (daily activity)
4. Inbox Tasks (urgent/high-priority items)
5. Operations Guide (selective reading via Serena search)

## Common Query Patterns

**"What's the status of MOKAI?"** → Read dashboard + today's diary
**"What are the current blockers?"** → Dashboard "Current Status/Blockers" section
**"What did I accomplish this week?"** → Read week's diary notes, extract wins
**"What should I work on next?"** → Check inbox urgent tasks → Phase 1 focus → High priority tasks
**"How do I format a diary note?"** → Use structure above (🏆 Wins, 🚨 Blockers, etc.)
**"What's Phase 1 about?"** → Read `status/phase-1-foundation.md` or reference embedded knowledge

## Related Documentation

- **Complete Tracking System**: `07-context/systems/business-tools/mokai-tracking-system.md`
- **Commands Reference**: `04-resources/guides/commands/claudelife-commands-guide.md`
- **Agent Instructions**: `.claude/agents/agent-mokai.md`
