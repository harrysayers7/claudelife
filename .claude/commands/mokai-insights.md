Deep pattern analysis across all MOKAI diary notes using Serena MCP.

**POWERED BY SERENA MCP FOR INTELLIGENT PATTERN RECOGNITION**

## Process:

### 1. Gather All Diary Data (USE SERENA)
- Use `mcp__serena__list_dir` on `/01-areas/business/mokai/diary/`
- Get all diary note files (*.md, excluding README and templates)
- Use `mcp__serena__search_for_pattern` across all files:
  - Pattern: `(🏆 Wins|🚨 Blockers|💡 Learnings|What I Did Today)`
  - Context lines: 3 after each match
- Aggregate results by category

### 2. Read Historical Memory (USE SERENA)
Try to read existing memories:
- `mcp__serena__read_memory("mokai_weekly_insights")`
- `mcp__serena__read_memory("mokai_progress_metrics")`
- `mcp__serena__read_memory("mokai_blockers_history")`
- `mcp__serena__read_memory("mokai_decision_log")`

If memories don't exist yet, note to create them.

### 3. Pattern Analysis

**Frequency Analysis**:
- Count keyword mentions across all diary notes
- Top blockers mentioned (frequency + dates)
- Top learning themes (categorize by topic)
- Win patterns (what types of wins: learning, execution, relationships?)

**Trend Analysis**:
- Weekly task completion rate (if memory exists)
- Blocker persistence (same blocker mentioned multiple weeks?)
- Learning velocity (sections per week, topics covered)
- Diary note consistency (how many days active per week?)

**Sentiment Tracking**:
- Ratio of wins to blockers
- Growth areas mentioned repeatedly
- Confidence indicators in writing

### 4. Strategic Insights Report

```
🧠 MOKAI Insights Analysis
Generated: [Date] | Analyzing [X] diary notes from [date range]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📊 Pattern Recognition

**Recurring Themes** (keyword frequency):
1. "[keyword]" - mentioned [X] times across [Y] notes
2. "[keyword]" - mentioned [X] times across [Y] notes
3. ...

**Persistent Blockers** 🚨:
- "[Blocker]" - mentioned [X] times over [Y] weeks
  First: [date] | Most Recent: [date]
  → Status: [Still active / Resolved]

**Learning Journey** 💡:
- Primary focus: [Most common learning theme]
- Progress indicators: [Specific learnings showing growth]
- Knowledge gaps: [Areas not yet addressed]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📈 Progress Trends

**Task Completion**:
- Week 1: [X]% completion
- Week 2: [X]% completion
- Week 3: [X]% completion
→ Trend: [Improving / Stable / Declining]

**Activity Consistency**:
- Diary notes written: [X]/[Y] days ([Z]%)
- Most active day: [Day of week]
- Gaps: [Any week with <5 notes?]

**Wins Momentum**:
- Total wins recorded: [X]
- Avg wins per week: [Y]
- Biggest win categories: [Learning / Execution / Relationships]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎯 Strategic Recommendations

**Critical Path Items**:
1. [Most urgent action based on patterns]
   Why: [Blocker mentioned X times, blocking progress]

2. [Second priority]
   Why: [Learning gap affecting confidence]

**Leverage Points**:
- [What's working well that should continue]
- [Area showing strong progress to accelerate]

**Risk Mitigation**:
- [Long-standing blocker needs escalation]
- [Pattern suggesting potential issue]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 💬 Co-Founder Perspective

[Honest, direct assessment in Harry's context]

**What I'm Seeing**:
[Observation about overall trajectory]

**What Concerns Me**:
[Any red flags or persistent issues]

**What Excites Me**:
[Positive momentum or breakthroughs]

**My Recommendation**:
[Specific next action with strategic reasoning]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5. Update Memory (USE SERENA)
Store insights for future reference:

```javascript
mcp__serena__write_memory({
  memory_name: "mokai_insights_snapshot",
  content: `
# MOKAI Insights Snapshot - [Date]

## Patterns Identified
- [Key patterns from analysis]

## Trend Data
- Task completion: [X]%
- Learning velocity: [Y] sections/week
- Blocker count: [Z] active

## Strategic Alerts
- [Any critical items needing attention]

## Last Analysis Date
[Date] - [X] diary notes analyzed
`
})
```

## When to Use This Command

- **Monthly**: Get big-picture view of progress
- **When feeling stuck**: Identify what's really blocking you
- **Before major decisions**: See patterns in your thinking
- **To celebrate**: Quantify how far you've come

## Important Rules:
- USE SERENA for all pattern matching (don't read files manually)
- Be honest in assessment (patterns don't lie)
- Focus on actionable insights, not just statistics
- Compare against Phase goals (are patterns moving you forward?)
- Store insights in memory for longitudinal tracking
