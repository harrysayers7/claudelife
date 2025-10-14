---
date: "2025-10-14"
system: MOKAI Business Tracking
type: strategic-accountability
status: active
date created: Tue, 10 14th 25, 5:05:13 pm
date modified: Tue, 10 14th 25, 5:06:13 pm
---

# MOKAI Business Tracking System

## Overview

The MOKAI tracking system is a natural, low-friction accountability system that helps track progress for MOKAI (Indigenous-owned cybersecurity consultancy startup) using Obsidian vault + Claude Code + Serena MCP integration.

**Core Philosophy**: Write naturally in daily notes → Automated extraction & updates → Strategic guidance

**Key Benefits**:
- Zero manual dashboard editing
- Dynamic checklist management (auto-marks completed tasks)
- Week-over-week progress trends
- Pattern detection across all diary notes
- Strategic accountability without overwhelming complexity

## System Architecture

```
Daily Writing (Natural Language)
    ↓
Diary Notes (01-areas/business/mokai/diary/YYYY-MM-DD.md)
    ↓
Slash Commands with Serena MCP
    ↓
    ├─→ Extract wins/blockers/learnings/tasks
    ├─→ Fuzzy match task completions
    ├─→ Update dashboard automatically
    ├─→ Update Phase 1 checklist dynamically
    ├─→ Store trends in Serena memory
    └─→ Provide strategic guidance
```

### Technology Stack

- **Obsidian**: Markdown-based knowledge management vault
- **Claude Code**: AI assistant with slash commands
- **Serena MCP**: Pattern matching, memory storage, codebase analysis
- **JSON Tracker**: Prevents re-reading processed diary notes

## File Structure

```
01-areas/business/mokai/
├── mokai-dashboard.md              # Mission control (auto-updated)
├── status/
│   ├── phase-1-foundation.md      # 30-day checklist (dynamic)
│   └── phase-2-3-future.md        # Future reference (60/90 days)
├── diary/
│   ├── README.md                  # System documentation
│   ├── 2025-10-14.md             # Daily notes (user writes here)
│   ├── 2025-10-15.md
│   └── .diary-template.md        # Obsidian template
├── .mokai-tracker.json            # Processing metadata
└── docs/
    └── research/
        └── 📘 - OPERATIONS GUIDE.md  # Business operations manual

00-inbox/tasks/                     # Task files (scanned by /mokai-status)
├── Supply Nation application.md   # MOKAI task (relation: mokai)
├── Sign Partnership Agreement.md  # MOKAI task (relation: mokai)
└── [other task files]             # Tasks with frontmatter metadata
```

## Slash Commands

### 1. /mokai-status (Daily Strategic Status)

**Purpose**: Daily command that reads unprocessed diary notes, **scans MOKAI task files in /00-inbox/tasks/**, updates everything automatically, and provides strategic guidance with **priority-based task recommendations**.

**Workflow**:
1. Read `.mokai-tracker.json` to get list of processed files
2. Calculate today's date (YYYY-MM-DD)
3. Use Serena to list all files in `diary/` directory
4. **ALWAYS include today's diary note** (even if already processed - allows same-day updates)
5. Filter other files to only unprocessed (not in tracker)
6. For each diary note to process:
   - Use Serena pattern matching to extract sections
   - Parse structured data (wins, blockers, learnings, tasks)
7. **Scan MOKAI inbox tasks**:
   - Use Serena to find all `.md` files in `/00-inbox/tasks/`
   - Check frontmatter for:
     - `type: Task` or `type: task`
     - `relation: mokai` or `relation: [[mokai]]`
     - `Done: false` (or missing = incomplete)
     - `priority: urgent|high|low` (or empty)
   - Group by priority: 🔥 Urgent, ⚠️ High, 📌 Normal
8. Read Phase 1 checklist for current week's tasks
9. Fuzzy match "What I Did Today" items against unchecked tasks
10. Mark matching checklist items as completed `[x]`
11. Update dashboard with **deduplication**:
    - Read existing wins/blockers from dashboard
    - Fuzzy match new items against existing (80%+ similarity)
    - Only add unique items
    - Update inbox tasks section
12. Update tracker: Mark files as processed **except today's date** (always re-read same day)
13. Try to read Serena memory for week-over-week comparison
14. Provide strategic status report with next priorities (**urgent inbox tasks prioritized**)

**Key Features**:
- **Same-Day Re-Reading**: Always re-reads today's diary note (even if processed earlier) to capture updates throughout the day
- **Intelligent Tracking**: Only marks previous days' notes as processed (stable content)
- **Deduplication**: Fuzzy matches new wins/blockers against existing (80%+ similarity) to prevent duplicates
- **Inbox Task Scanning**: Automatically surfaces MOKAI tasks from /00-inbox/tasks/
- **Priority-Based Recommendations**: Urgent inbox tasks take precedence over routine Phase 1 tasks
- **Fuzzy Task Matching**: "Finished reading Indigenous section" matches "[ ] Read Indigenous Business & Procurement section"
- **Dynamic Checklist Updates**: Automatically marks completed tasks
- **Memory Retrieval**: Shows week-over-week progress trends if available

**Example Output**:
```
📊 MOKAI STATUS UPDATE - Oct 14, 2025

**Current Phase**: Phase 1 - Foundation (Week 1 of 4)
**Days into Phase 1**: 1 day

## ✅ Recent Activity (from diary notes)
**What You Did**:
- Had ultra-think session with Claude about MOKAI tracking system
- Set up dashboard and slash commands
- Learned about the 3-phase plan

**Wins** 🏆:
- Created MOKAI dashboard system
- Clarified ownership split (51% Indigenous)
- Kelly's website almost done

**Blockers** 🚨:
- Waiting on Jack's family trust setup
- Haven't started Operations Guide reading yet

## 🎯 This Week's Goals (Week 1: Oct 14-20)
Focus: Operations Guide Mastery

**Uncompleted Tasks**:
- [ ] Read Indigenous Business & Procurement section (1 hour)
- [ ] Read Prime Contractor Management section (1 hour)
- [ ] Do daily flashcard review (15 min/day)
- [ ] Write summary: "How MOKAI makes money" in own words

## 📥 Inbox Tasks (from /00-inbox/tasks/)

🔥 **Urgent** (2 tasks):
- Supply Nation application
- Sign Partnership Agreement

⚠️ **High Priority** (0 tasks)

📌 **Normal** (1 task):
- Open Bank Account

## 💡 Strategic Guidance

**What to Work On Today**:
🔥 **URGENT FIRST**: Complete Supply Nation application and Sign Partnership Agreement before routine tasks. These are blockers for legal registration.

**Then**: Start reading the Indigenous Business & Procurement section of the Operations Guide (1 hour).

**Why It Matters**:
Understanding Indigenous procurement advantages (IPP/MSA/Exemption 16) is foundational to MOKAI's competitive positioning. You need to be able to explain this confidently to potential clients.

**Next Steps**:
1. Find the Operations Guide in docs/research/
2. Read Indigenous Business & Procurement section
3. Do 15-min flashcard review today
4. Log learnings in today's diary note

**Reality Check**:
You're waiting on Jack's trust setup for legal registration. Use this time wisely to master the business fundamentals. When the trust is done, you want to hit the ground running.
```

---

### 2. /mokai-wins (Quick Win Logging)

**Purpose**: Quickly log a win to today's diary note without opening the file manually.

**Usage**: `/mokai-wins [win description]`

**Workflow**:
1. Calculate today's date (YYYY-MM-DD format)
2. Check if today's diary note exists
3. If not, create from template with frontmatter
4. Find the "## 🏆 Wins" section
5. Add new win as bullet point
6. Write diary note back
7. Provide quick celebration + next priority

**Example**:
```bash
/mokai-wins Completed reading Indigenous Business section of Ops Guide
```

**Output**:
```
🎉 Nice! Added to today's diary:
✅ Completed reading Indigenous Business section of Ops Guide

Keep the momentum going. Next priority: Read Prime Contractor Management section (1 hour)
```

---

### 3. /mokai-weekly (Weekly Review)

**Purpose**: End-of-week review that aggregates all diary notes, analyzes progress, updates Phase 1 checklist for next week, and stores insights in Serena memory.

**Workflow**:
1. Read `.mokai-tracker.json` to get current week start date
2. Calculate week date range (Monday-Sunday)
3. Use Serena to search for patterns across week's diary files
4. Aggregate results by category (wins, blockers, learnings)
5. Read Phase 1 checklist to find unchecked tasks in current week
6. Cross-reference "What I Did Today" items with unchecked tasks
7. Count completion rate for the week
8. Try to read Serena memory for week-over-week comparison
9. **Interactive Reflection**: Ask user 3 quick questions
10. Update Phase 1 checklist:
    - Mark completed items as `[x]`
    - Roll incomplete items to next week with note "(from Week X)"
    - Identify next week's focus section
11. Update dashboard with new "This Week's Focus" and Weekly Scorecard
12. Store insights in Serena memory:
    - `mokai_progress_metrics` (completion rates, trends)
    - `mokai_weekly_insights` (patterns, strategic context)
13. Update tracker (increment week, set new week start date)
14. Provide strategic pep talk with trend analysis

**Interactive Questions**:
```
📊 Let's review this week together.

Based on your diary notes, here's what I see:
- ✅ Completed: 3 tasks (75% of week's goals)
- 🏆 Wins: Dashboard system created, ownership clarified, Kelly's website done
- 🚨 Blockers: Jack's trust, haven't started Ops Guide
- 💡 Learnings: Ops Guide is key, Essential Eight is easiest first sale

**Week-over-Week**:
- Last week: 60% completion | This week: 75% completion
- Trend: Improving

Quick questions:
1. What's the ONE thing you're most proud of this week?
2. What's the BIGGEST blocker I should know about?
3. On a scale 1-10, how do you feel about MOKAI progress?
```

**Memory Storage**:
```markdown
# MOKAI Progress Metrics - Updated Oct 14, 2025

## Week 1 Summary (Oct 14-20)
- Tasks completed: 3/4 (75%)
- Diary notes: 5/7 days
- Wins: 8
- Blockers: 2
- Top learning theme: Operations Guide fundamentals

## Historical Trend
- Week 1: 75% completion

## Persistent Blockers
- "Jack's trust setup" - Week 1 (still active)

## Learning Velocity
- Ops Guide sections: 1 completed, 4 remaining
- Estimated completion: Oct 18
```

---

### 4. /mokai-insights (Deep Pattern Analysis)

**Purpose**: Deep dive analysis across ALL MOKAI diary notes to identify recurring themes, persistent blockers, learning velocity, and strategic recommendations.

**Workflow**:
1. Use Serena to list all files in `diary/` directory
2. Use Serena to search for patterns across ALL diary files (not just unprocessed)
3. Aggregate all wins, blockers, learnings, tasks
4. **Frequency Analysis**:
   - Count keyword mentions across all diary notes
   - Top blockers mentioned (frequency + dates)
   - Top learning themes (categorize by topic)
   - Win patterns (learning, execution, relationships)
5. **Trend Analysis**:
   - Weekly task completion rate (from Serena memory if exists)
   - Blocker persistence (same blocker multiple weeks?)
   - Learning velocity (sections per week, topics covered)
6. **Pattern Detection**:
   - What types of wins are most common?
   - Which blockers keep appearing?
   - What learning themes dominate?
   - Task completion patterns (mornings? evenings?)
7. **Strategic Recommendations**:
   - Based on patterns, what should change?
   - What's working well to double down on?
   - What blockers need escalation/different approach?

**Example Output**:
```
🧠 MOKAI INSIGHTS - Deep Pattern Analysis

**Analysis Period**: Oct 14 - Oct 20, 2025 (7 days)
**Total Diary Notes**: 5 notes processed

## 📊 Frequency Analysis

**Top Blockers** (by mention frequency):
1. "Jack's trust setup" - Mentioned 5 times (Oct 14, 15, 16, 17, 18)
   → **PERSISTENT BLOCKER**: Appeared every day this week
2. "Haven't started Ops Guide" - Mentioned 2 times (Oct 14, 15)
   → Resolved by Oct 16

**Top Learning Themes**:
1. Indigenous Procurement (IPP/MSA/Exemption 16) - 8 mentions
2. Operations Guide fundamentals - 6 mentions
3. Essential Eight cybersecurity assessment - 4 mentions

**Win Patterns**:
- **Execution Wins** (40%): Dashboard created, flashcards set up
- **Learning Wins** (35%): Completed Ops Guide sections, understood IPP
- **Relationship Wins** (25%): Jack alignment, Kelly website progress

## 📈 Trend Analysis

**Task Completion Rate**:
- Week 1: 75% completion (3/4 tasks)
- Daily completion: Monday 0%, Tuesday 1 task, Wednesday 2 tasks

**Blocker Persistence**:
- "Jack's trust" - ESCALATING (5 consecutive days)
  → **Recommendation**: Set deadline with Jack or explore parallel path

**Learning Velocity**:
- Operations Guide: 1 section/week (on track for 4-week completion)
- Flashcards: Consistent daily practice (5/5 days)

## 🎯 Strategic Recommendations

**What's Working Well** (double down):
✅ Daily diary habit (5/7 days) - keep this consistency
✅ Flashcard system for retention - learning is sticking
✅ Jack partnership clarity - aligned on roles/ownership

**What Needs Attention**:
🚨 "Jack's trust" blocker - Day 5 with no progress
   → Action: Schedule call with Jack to get timeline/backup plan
🚨 Ops Guide reading pace - Need to accelerate to hit Week 1 goal
   → Action: Block 2 hours tomorrow for focused reading

**Emerging Patterns**:
💡 Most productive task completion: Tuesday-Thursday mornings
💡 Learning wins dominate early week, execution wins late week
💡 Confidence in Indigenous procurement growing (good sign)

## 🔮 Next Week Prediction

Based on current patterns:
- **Expected completion rate**: 70-80% (if Jack's trust unblocks)
- **Risk area**: Legal setup delays could cascade to Week 2 prep tasks
- **Opportunity**: Operations Guide mastery on track for Day 30 goal
```

---

## Daily Diary Note Structure

### Template (.diary-template.md)

```markdown
---
date: {{date:YYYY-MM-DD}}
day: {{date:dddd}}
---
# MOKAI Daily Note - {{date:MMM DD, YYYY}}

## What I Did Today
-

## 💡 Learnings
-

## 🏆 Wins
-

## 🚨 Blockers
-

## 📝 Context/Updates
-

## 🎯 Tomorrow's Focus
-
```

### Writing Guidelines

**Natural Language**: Write as you think, no rigid structure required
**Section Markers**: Use emoji headers for easy parsing (🏆 🚨 💡)
**Task Descriptions**: Be specific enough for fuzzy matching
  - ✅ "Finished reading Indigenous Business section"
  - ✅ "Completed first flashcard review session"
  - ❌ "Did some reading" (too vague)

---

## Inbox Task Files (/00-inbox/tasks/)

### Purpose
Task files in `/00-inbox/tasks/` with `relation: mokai` are automatically scanned by `/mokai-status` and `/mokai-weekly` to surface urgent and high-priority tasks alongside Phase 1 checklist items.

### Frontmatter Structure

**Required Fields**:
```yaml
---
type: Task              # Or "task" (case-insensitive)
relation:
  - "[[mokai]]"         # Or single line: relation: mokai
Done: false             # true when completed (or omit for incomplete)
---
```

**Optional Fields**:
```yaml
priority: urgent        # urgent, high, low (or omit for normal priority)
description: Brief task description
date created: Mon, 10 14th 25, 10:24:37 am
date modified: Tue, 10 14th 25, 3:20:09 pm
```

### Priority Grouping

- **🔥 Urgent** (`priority: urgent`): Critical blockers, take precedence over all other tasks
- **⚠️ High** (`priority: high`): Important but not blocking, prioritized after urgent
- **📌 Normal** (`priority: low` or no priority field): Standard tasks, handled after high priority

### Example Task Files

**Urgent Task** (`Supply Nation application.md`):
```markdown
---
type: Task
relation:
  - "[[mokai]]"
priority: urgent
Done: false
description: Complete Supply Nation certification application
---
```

**High Priority Task** (`Sign Partnership Agreement.md`):
```markdown
---
type: Task
relation:
  - "[[mokai]]"
priority: high
Done: false
---
```

**Completed Task** (`Marlon mokai trust.md`):
```markdown
---
type: Task
relation:
  - "[[mokai]]"
Done: true
date modified: Fri, 10 3rd 25, 1:28:54 pm
---
```

### How Commands Use Inbox Tasks

**`/mokai-status`**:
- Scans all `.md` files in `/00-inbox/tasks/`
- Filters to MOKAI tasks (`relation: mokai` + `type: Task`)
- Groups incomplete tasks by priority
- Displays in dashboard and status report
- **Prioritizes urgent tasks in recommendations**

**`/mokai-weekly`**:
- Counts completed MOKAI inbox tasks this week
- Includes completion count in weekly metrics
- Stores inbox task metrics in Serena memory

### Best Practices

1. **Set priority for time-sensitive tasks**: Use `priority: urgent` for blockers
2. **Mark tasks done promptly**: Change `Done: false` to `Done: true` when complete
3. **Use descriptive filenames**: Filename becomes task title in status report
4. **Add descriptions for clarity**: Optional `description:` field provides context
5. **Review inbox weekly**: Use `/mokai-weekly` to see completion patterns

---

## Tracker File (.mokai-tracker.json)

### Purpose
Prevents re-reading already processed diary notes for efficiency.

### Structure
```json
{
  "lastProcessed": "2025-10-14T00:00:00Z",
  "processedFiles": [
    "2025-10-14.md",
    "2025-10-15.md"
  ],
  "currentWeekStart": "2025-10-14",
  "phase": 1,
  "weekInPhase": 1
}
```

### Fields
- `lastProcessed`: ISO timestamp of last command run
- `processedFiles`: Array of diary filenames already extracted
- `currentWeekStart`: Monday date of current week (YYYY-MM-DD)
- `phase`: Current phase number (1, 2, or 3)
- `weekInPhase`: Week number within current phase (1-4)

---

## Serena MCP Integration

### Pattern Matching

**Extracting Diary Sections**:
```javascript
mcp__serena__search_for_pattern({
  substring_pattern: "(## 🏆 Wins|## 🚨 Blockers|## 💡 Learnings|## What I Did Today)",
  relative_path: "01-areas/business/mokai/diary",
  paths_include_glob: "*.md",
  context_lines_after: 5
})
```

**Finding Unchecked Tasks in Phase 1**:
```javascript
mcp__serena__search_for_pattern({
  substring_pattern: "- \\[ \\]",
  relative_path: "01-areas/business/mokai/status/phase-1-foundation.md",
  context_lines_after: 0
})
```

### Memory Storage

**Progress Metrics**:
```javascript
mcp__serena__write_memory({
  memory_name: "mokai_progress_metrics",
  content: `
# MOKAI Progress Metrics - Updated ${date}

## Week ${weekNum} Summary (${dateRange})
- Tasks completed: ${completed}/${total} (${percent}%)
- Diary notes: ${noteCount}/7 days
- Wins: ${winCount}
- Blockers: ${blockerCount}
- Top learning theme: ${theme}

## Historical Trend
${weeklyCompletionData}

## Persistent Blockers
${persistentBlockers}

## Learning Velocity
${learningVelocityData}
`
})
```

**Weekly Insights**:
```javascript
mcp__serena__write_memory({
  memory_name: "mokai_weekly_insights",
  content: `
# Week ${weekNum} Insights (${dateRange})

## Key Patterns
${patterns}

## Strategic Context
${decisions}

## Next Week Focus
${nextWeekFocus}

## Notes for Future
${futureNotes}
`
})
```

### Memory Retrieval

```javascript
// Try to read memory (may not exist on first run)
const metrics = await mcp__serena__read_memory({
  memory_file_name: "mokai_progress_metrics.md"
})

// Compare week-over-week if memory exists
if (metrics.content) {
  // Parse previous week data
  // Compare to current week
  // Show trend: Improving / Stable / Declining
}
```

---

## Phase 1: Foundation (30 Days)

### Goal
Master business fundamentals while waiting for legal setup (Jack's family trust).

### Timeline
Oct 14 - Nov 14, 2025

### Weekly Breakdown

**Week 1: Operations Guide Deep Dive** (Oct 14-20)
- Daily 1-hour reading sessions
- 15-min flashcard reviews
- End of week: Write "MOKAI Business Model in My Own Words"

**Week 2: Legal & Setup Prep** (Oct 21-27)
- Review Constitution, Shareholders Agreement, Board Resolution
- Prepare Supply Nation application
- Get 3 insurance quotes (PI, PL, Cyber)

**Week 3: Business Operations Prep** (Oct 28 - Nov 3)
- Research business bank accounts
- Understand Xero setup
- Shadow Jack on contractor management
- Deep dive Essential Eight service packaging

**Week 4: Activation Ready** (Nov 4-10)
- QA Kelly's website and capability statement
- Jack alignment meeting (first client strategy)
- Complete "Ready to Launch" checklist

### Success Criteria (End of Day 30)

Can you answer YES to all 4?
1. Do you feel confident explaining MOKAI to a potential client?
2. Can you articulate IPP advantages without stumbling?
3. Do you understand how money flows (pricing, margins, cash flow)?
4. Are you ready to hit the ground running the moment Jack's trust is done?

If YES to all 4 → Move to Phase 2 (Register & Activate)
If NO to any → Spend extra week on that area

---

## Dashboard (mokai-dashboard.md)

### Purpose
Single source of truth for MOKAI's current status - auto-updated by slash commands.

### Key Sections

**Header**:
- Last Updated (auto-updated by `/mokai-status`)
- Current Phase
- Primary Goal

**This Week's Focus**:
- Updated weekly by `/mokai-weekly`
- 3-5 actionable tasks for current week
- Daily time allocation

**Current Status (Reality Check)**:
- Legal & Structure: ABN/ACN status, ownership, Supply Nation, insurance
- Team Status: Harry/Jack/Kelly roles and capacity
- Sales Comfort: Confidence level, network, first service
- Learning Progress: Ops Guide status, knowledge areas
- Blockers: Current impediments (auto-updated from diary notes)

**Recent Wins**:
- Auto-updated from diary notes
- Shows last 5-7 wins

**Weekly Scorecard**:
- Week summary (wins, blockers, next week focus, learning notes)
- Auto-updated by `/mokai-weekly`

---

## Configuration & Setup

### Obsidian Configuration

**Daily Notes Plugin**:
- Enable "Daily notes" core plugin
- Template location: `01-areas/business/mokai/diary/.diary-template.md`
- New file location: `01-areas/business/mokai/diary`
- Date format: `YYYY-MM-DD`

**Templater Plugin** (optional but recommended):
- Install for advanced template features
- Use `{{date}}` placeholders in template

### Serena MCP Setup

Ensure Serena MCP is configured in `.mcp.json`:
```json
{
  "mcpServers": {
    "serena": {
      "command": "npx",
      "args": ["-y", "@serenaai/serena"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

### Slash Commands Setup

Commands already exist in `.claude/commands/`:
- `mokai-status.md`
- `mokai-wins.md`
- `mokai-weekly.md`
- `mokai-insights.md`

No additional setup required - commands are ready to use.

---

## Usage Workflows

### Daily Routine (5 minutes)

**Morning**:
```bash
/mokai-status
```
- See yesterday's progress automatically extracted
- Get today's strategic focus
- Know what to work on next

**Throughout the Day**:
- Write naturally in today's diary note (`YYYY-MM-DD.md`)
- Log wins, blockers, learnings as they happen
- No need to update dashboard manually

**Quick Win**:
```bash
/mokai-wins Completed first flashcard review session
```

---

### Weekly Routine (30 minutes)

**End of Week** (Friday or Sunday):
```bash
/mokai-weekly
```
- Review entire week's progress
- Answer 3 reflection questions
- See week-over-week trends
- Get next week's focus automatically

---

### Monthly Routine (60 minutes)

**End of Month**:
```bash
/mokai-insights
```
- Deep pattern analysis across all diary notes
- Identify recurring themes and blockers
- Strategic recommendations based on data
- Prepare for next phase if approaching Day 30

**Optional**: Create monthly summary in `diary/YYYY-MM-summary.md`

---

## Troubleshooting

### Command Not Extracting Data

**Symptom**: `/mokai-status` runs but says no new diary notes found

**Solutions**:
1. Check diary note filename format: Must be `YYYY-MM-DD.md` (e.g., `2025-10-14.md`)
2. Check diary note location: Must be in `01-areas/business/mokai/diary/`
3. Check tracker file: If corrupted, delete `.mokai-tracker.json` and re-run command
4. Verify emoji headers: Use exact emoji markers (🏆 🚨 💡)

---

### Tasks Not Being Marked Complete

**Symptom**: Did tasks but checklist not updating

**Solutions**:
1. Check "What I Did Today" description is specific enough:
   - ✅ "Finished reading Indigenous Business section"
   - ❌ "Did some reading"
2. Verify task exists in current week's Phase 1 checklist
3. Use keywords from the checklist task title in your diary note
4. Fuzzy matching requires 60%+ keyword overlap

---

### Same-Day Updates Not Appearing

**Symptom**: Added wins/learnings to today's diary note but `/mokai-status` doesn't show them

**Expected Behavior**: This SHOULD work - today's note is always re-read

**Solutions**:
1. Verify you're editing today's date file (YYYY-MM-DD format)
2. Check emoji headers are correct: `## 🏆 Wins`, `## 💡 Learnings`
3. Run `/mokai-status` again after saving changes
4. If still not working, check diary note location: `01-areas/business/mokai/diary/`

---

### Duplicate Wins/Blockers on Dashboard

**Symptom**: Same win appears multiple times after running `/mokai-status` multiple times in one day

**Expected Behavior**: This should NOT happen - deduplication prevents this

**Solutions**:
1. Check deduplication is working (fuzzy match 80%+ similarity)
2. If duplicates persist, manually edit dashboard to remove
3. Slightly rephrase wins if appearing as separate items (e.g., "Read Ops Guide section 1" vs "Finished Ops Guide section 1" may match)

---

### Tracker File Issues

**Symptom**: Command re-reads all old diary notes every time (slow)

**Solutions**:
1. Check `.mokai-tracker.json` exists in `01-areas/business/mokai/`
2. Verify JSON format is valid (no syntax errors)
3. If corrupted, delete and re-run `/mokai-status` (will recreate)
4. **Note**: Today's diary note is ALWAYS re-read (by design)

---

### Serena Memory Not Loading

**Symptom**: No week-over-week comparison in `/mokai-status`

**Expected on First Run**: Memory doesn't exist until first `/mokai-weekly` completes

**Solutions**:
1. Run `/mokai-weekly` at least once to create memory
2. Verify Serena MCP is configured correctly in `.mcp.json`
3. Check memory files exist: Use `mcp__serena__list_memories()`

---

### Dashboard Not Updating

**Symptom**: Dashboard shows old data after running commands

**Solutions**:
1. Re-run `/moaki-status` (it auto-updates dashboard)
2. Check file permissions on `mokai-dashboard.md`
3. Verify dashboard file path hasn't changed

---

## Best Practices

### Writing Effective Diary Notes

**Be Specific**:
- ✅ "Completed reading Indigenous Business & Procurement section of Ops Guide"
- ❌ "Read some stuff"

**Use Task-Related Keywords**:
- If checklist says "Read Indigenous Business & Procurement section"
- Your diary should mention: "Indigenous", "Procurement", or "Ops Guide section"

**Log Context**:
- Don't just say "Blocker: Jack"
- Say "Blocker: Still waiting on Jack's family trust setup, no timeline yet"

**Celebrate Wins**:
- Small wins matter (first flashcard session, alignment call)
- Big wins matter (launched website, closed first client)
- Log them all

---

### Running Commands Strategically

**Daily Morning**: `/mokai-status`
- Sets your focus for the day
- Keeps dashboard current
- Surfaces blockers that need attention

**Throughout the Day**:
- **Add to today's diary note** as you work (wins, learnings, blockers)
- **Run `/mokai-status` again** to update dashboard with new content
- **No duplicates**: Deduplication ensures same win doesn't appear twice
- **Quick wins**: Use `/mokai-wins` for fast logging without opening diary

**As-You-Go**: `/mokai-wins`
- Quick dopamine hit when completing tasks
- Keeps momentum going
- Ensures wins are logged immediately (not forgotten)

**End of Day** (optional): `/mokai-status`
- Final check to capture all day's activity
- Today's note is always re-read (safe to run multiple times)

**Weekly Review**: `/mokai-weekly`
- Friday afternoon or Sunday evening
- When you have 30 minutes to reflect
- Sets up next week for success

**Monthly Deep Dive**: `/mokai-insights`
- End of month or when feeling stuck
- When you want to see the big picture
- Before major decisions or phase transitions

---

### Maintaining System Health

**Keep Diary Notes Consistent**:
- Try to write 5-7 days per week
- Even if brief ("No MOKAI work today, focused on client project")
- Consistency enables better trend analysis

**Same-Day Updates Are Safe**:
- Today's diary note is ALWAYS re-read (even if processed earlier)
- Add wins/learnings throughout the day - run `/mokai-status` to update dashboard
- Deduplication prevents duplicate entries (fuzzy match 80%+ similarity)
- No need to worry about running the command multiple times per day

**Don't Edit Old Diary Notes**:
- Previous days' notes are marked as processed (not re-read for efficiency)
- If you must edit old notes, they won't be re-extracted automatically
- Today's note is the exception - always re-processed

**Review Blockers Weekly**:
- Persistent blockers (5+ days) need escalation
- `/mokai-insights` helps identify these patterns

**Trust the System**:
- Let commands handle dashboard/checklist updates
- Focus your energy on writing naturally in diary notes
- Don't manually edit `mokai-dashboard.md` (commands will overwrite)

---

## Future Enhancements

### Potential Additions

**Phase 2/3 Automation**:
- Auto-advance to next phase when Phase 1 checklist 100% complete
- Generate Phase 2 checklist based on Phase 1 learnings

**Blocker Escalation**:
- Automatically flag blockers mentioned 5+ consecutive days
- Suggest specific actions to unblock

**Learning Velocity Predictions**:
- ML model to predict completion dates based on current pace
- Adjust weekly goals dynamically based on velocity

**Integration with External Systems**:
- Pull in calendar events (Jack meetings, Supply Nation deadlines)
- Sync with task managers (Linear, Notion) for operational tasks
- Connect to financial tracking (when revenue starts flowing)

**Mobile-Friendly Quick Logging**:
- SMS/WhatsApp bot to log wins on the go
- Voice notes transcribed to diary notes

---

## System Philosophy

### Why This Works

**1. Natural Input, Structured Output**:
- Write freely in diary notes (low friction)
- Commands extract structure automatically (high value)

**2. Dynamic vs Static**:
- Traditional checklists become stale
- This system updates based on actual behavior
- Tasks roll forward automatically

**3. Memory-Enabled Trends**:
- See week-over-week progress
- Identify patterns early
- Make data-informed decisions

**4. Strategic Accountability**:
- Not just "what did I do" but "what should I do next"
- Commands provide context-aware guidance
- Keeps you aligned with Phase 1 goals

**5. Obsidian-Native**:
- Lives where you already work
- Markdown files = future-proof, portable
- No external apps or subscriptions

### Design Decisions

**Why Diary Notes Over Dashboard Editing**:
- Writing is faster than updating structured fields
- Natural language captures nuance
- Encourages daily reflection habit

**Why Fuzzy Matching Over Exact**:
- Real writing doesn't match checklists exactly
- Captures intent ("finished reading section" = task complete)
- Reduces friction

**Why Serena MCP**:
- Efficient pattern matching across files
- Memory storage for longitudinal analysis
- Built for codebase analysis (perfect for markdown vault)

**Why Separate Phase Files**:
- Day 1 with 90-day checklist = overwhelming
- 30-day chunks = achievable, focused
- Future phases adjust based on reality (not static plan)

---

## Conclusion

The MOKAI tracking system is designed for one thing: **Keep you accountable and strategic without overwhelming you**.

Write naturally → Commands extract → Stay on track → Build MOKAI successfully.

**Key Reminder**: This system works best when used daily. Even 2 minutes of writing per day keeps the system informed and keeps you focused.

Start with `/mokai-status` every morning and see where MOKAI is at. That's all you need to do.

---

## Quick Reference

**Daily Commands**:
- `/mokai-status` - Morning strategic status
- `/mokai-wins [description]` - Quick win logging

**Weekly Commands**:
- `/mokai-weekly` - End of week review

**Monthly Commands**:
- `/mokai-insights` - Deep pattern analysis

**Key Files**:
- Diary notes: `01-areas/business/mokai/diary/YYYY-MM-DD.md`
- Dashboard: `01-areas/business/mokai/mokai-dashboard.md`
- Phase 1 checklist: `01-areas/business/mokai/status/phase-1-foundation.md`
- Tracker: `01-areas/business/mokai/.mokai-tracker.json`

**Serena Memories**:
- `mokai_progress_metrics` - Weekly completion rates, trends
- `mokai_weekly_insights` - Strategic patterns, context

---

*System created: Oct 14, 2025*
*Last updated: Oct 14, 2025*
*Version: 1.0*
