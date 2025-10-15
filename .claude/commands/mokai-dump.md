---
created: "2025-10-15 12:50"
description: |
  Quick capture command for MOKAI diary entries. Analyzes your input using AI sentiment/content analysis and automatically categorizes entries under the correct section (Wins, Learnings, Blockers, Context). Supports multiple entries in one command and optional date specification. Always adds to today's diary by default, with option to specify different dates.
examples:
  - /mokai-dump "Had a great call with the client, they loved our Essential Eight proposal"
  - /mokai-dump "Learned that IRAP assessments take 2-6 months" "Stuck waiting for contractor availability"
  - /mokai-dump --date=2025-10-14 "Yesterday's win: closed the deal"
---

# MOKAI Dump

This command provides quick capture for MOKAI diary entries without opening Obsidian. You type your thoughts, and I'll analyze the content/sentiment to automatically categorize and append entries to the correct section in today's MOKAI daily note.

## Usage

```bash
# Single entry (auto-categorized)
/mokai-dump "your entry here"

# Multiple entries (each auto-categorized independently)
/mokai-dump "entry 1" "entry 2" "entry 3"

# Specify a different date (also adds to today)
/mokai-dump --date=2025-10-14 "entry for Oct 14"
```

## What This Command Does

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

1. **Analyzes each entry** using AI to determine category based on:
   - Sentiment (positive = Win, negative = Blocker, neutral = Context)
   - Keywords (learned/discovered = Learning, stuck/waiting = Blocker, achieved/won = Win)
   - Intent (informational = Context, achievement = Win, challenge = Blocker, insight = Learning)

2. **Determines target diary note**:
   - Default: Today's date (`/01-areas/business/mokai/diary/YYYY-MM-DD-mokai-daily.md`)
   - If `--date` specified: Adds to that date AND today's date (for cross-reference)

3. **Appends to correct section**:
   - 🏆 Wins
   - 💡 Learnings
   - 🚨 Blockers
   - 📝 Context/Updates

4. **Creates diary note if it doesn't exist** (uses template from `/98-templates/mokai-note.md`)

## Supported Sections

This command auto-categorizes to these sections only:
- **🏆 Wins**: Achievements, successes, positive outcomes
- **💡 Learnings**: Insights, discoveries, new knowledge
- **🚨 Blockers**: Challenges, obstacles, waiting situations
- **📝 Context/Updates**: General information, status updates, neutral observations

**Not supported** (use manual entry):
- What I Did Today
- 🎯 Tomorrow's Focus
- 🤖 Agent-Mokai Discussion (requires thoughtful placement)

## Process

I'll help you capture MOKAI diary entries by:

1. **Parse your input**:
   - Extract entries (quoted strings)
   - Identify optional `--date` parameter
   - Get today's date for default target

2. **Analyze each entry** using AI:
   ```javascript
   // Sentiment analysis
   if (entry contains "won", "achieved", "success", "great", "closed") → Win
   if (entry contains "learned", "discovered", "realized", "understand") → Learning
   if (entry contains "stuck", "blocked", "waiting", "can't", "issue") → Blocker
   if (entry neutral or informational) → Context

   // Consider overall sentiment
   positive sentiment + achievement language → Win
   neutral sentiment + insight language → Learning
   negative sentiment + obstacle language → Blocker
   informational tone → Context
   ```

3. **Locate or create diary note**:
   ```bash
   # Default target: today
   TARGET="/01-areas/business/mokai/diary/$(date +%Y-%m-%d)-mokai-daily.md"

   # If --date specified, also target that date
   if [[ $DATE_PARAM ]]; then
     ADDITIONAL_TARGET="/01-areas/business/mokai/diary/${DATE_PARAM}-mokai-daily.md"
   fi

   # If file doesn't exist, copy from template
   if [[ ! -f $TARGET ]]; then
     cp /98-templates/mokai-note.md $TARGET
     # Add frontmatter with journal metadata
   fi
   ```

4. **Append to correct section**:
   ```javascript
   // Read the diary file
   const diaryContent = readFile(targetPath);

   // Find the section heading (e.g., "## 🏆 Wins")
   const sectionRegex = new RegExp(`## ${emoji} ${category}\\n\\n([\\s\\S]*?)(?=\\n## |$)`);

   // Append new bullet point
   const newEntry = `- ${entryText}`;
   const updatedContent = diaryContent.replace(
     sectionRegex,
     (match, existingContent) => {
       // Remove trailing empty bullet if exists
       const cleaned = existingContent.replace(/^-\s*$/gm, '').trim();
       return `## ${emoji} ${category}\n\n${cleaned}\n${newEntry}\n`;
     }
   );

   // Write back to file
   writeFile(targetPath, updatedContent);
   ```

5. **Provide confirmation**:
   - Show each entry with detected category
   - Confirm which diary note(s) were updated
   - Show the full path for verification

## Output Format

```
Analyzing entries...

Entry 1: "Had a great call with the client, they loved our Essential Eight proposal"
→ Detected: 🏆 Win

Entry 2: "Learned that IRAP assessments take 2-6 months"
→ Detected: 💡 Learning

Entry 3: "Stuck waiting for contractor availability"
→ Detected: 🚨 Blocker

✅ Added to /01-areas/business/mokai/diary/2025-10-15-mokai-daily.md:
   - 🏆 Wins: 1 entry
   - 💡 Learnings: 1 entry
   - 🚨 Blockers: 1 entry
```

## Examples

### Example 1: Single Win Entry

**Command**:
```bash
/mokai-dump "Closed the Essential Eight assessment deal with Department of Finance - $15k contract"
```

**Analysis**:
- Keywords: "Closed", "deal" → Achievement language
- Sentiment: Positive (financial win)
- Category: 🏆 Win

**Result**:
```markdown
## 🏆 Wins

- Closed the Essential Eight assessment deal with Department of Finance - $15k contract
```

### Example 2: Multiple Entries (Mixed Categories)

**Command**:
```bash
/mokai-dump "Won the tender for pen testing services" "Discovered that IPP threshold is actually $80k not $100k" "Can't finalize contractor agreement until legal review completes"
```

**Analysis**:
1. "Won the tender..." → 🏆 Win
2. "Discovered that..." → 💡 Learning
3. "Can't finalize..." → 🚨 Blocker

**Result**:
```markdown
## 🏆 Wins

- Won the tender for pen testing services

## 💡 Learnings

- Discovered that IPP threshold is actually $80k not $100k

## 🚨 Blockers

- Can't finalize contractor agreement until legal review completes
```

### Example 3: Backdated Entry

**Command**:
```bash
/mokai-dump --date=2025-10-14 "Yesterday closed the IRAP assessment proposal"
```

**Analysis**:
- Category: 🏆 Win
- Adds to BOTH 2025-10-14 AND 2025-10-15 (today)

**Result**:
```
✅ Added to /01-areas/business/mokai/diary/2025-10-14-mokai-daily.md:
   - 🏆 Wins: 1 entry

✅ Added to /01-areas/business/mokai/diary/2025-10-15-mokai-daily.md:
   - 🏆 Wins: 1 entry (cross-referenced from 2025-10-14)
```

### Example 4: Context/Update Entry

**Command**:
```bash
/mokai-dump "Met with Supply Nation auditor to discuss certification renewal process"
```

**Analysis**:
- Neutral sentiment
- Informational (no achievement, learning, or blocker)
- Category: 📝 Context/Updates

**Result**:
```markdown
## 📝 Context/Updates

- Met with Supply Nation auditor to discuss certification renewal process
```

## Categorization Decision Tree

```
Entry Analysis:
├─ Contains achievement keywords (won, closed, achieved, success)?
│  └─ Positive sentiment? → 🏆 Win
│
├─ Contains learning keywords (learned, discovered, realized, understand)?
│  └─ Insight or knowledge? → 💡 Learning
│
├─ Contains blocker keywords (stuck, blocked, waiting, can't, issue)?
│  └─ Negative sentiment or obstacle? → 🚨 Blocker
│
└─ Neutral/informational tone?
   └─ No clear win/learning/blocker → 📝 Context/Updates
```

## Edge Cases

### New Diary Note Creation

If today's diary note doesn't exist:
1. Copy template from `/98-templates/mokai-note.md`
2. Add frontmatter:
   ```yaml
   ---
   journal: Mokai Daily 🟣
   journal-date: YYYY-MM-DD
   ---
   ```
3. Append entry to appropriate section

### Ambiguous Categorization

If entry could fit multiple categories:
- Prioritize: Win > Learning > Blocker > Context
- Example: "Learned we won the tender" → 🏆 Win (achievement takes precedence)

### Empty Bullet Cleanup

Before appending, remove any empty placeholder bullets:
```markdown
## 🏆 Wins

-  ← Remove this empty bullet
```

## Evaluation Criteria

A successful dump should:

1. **Accurate categorization**: AI correctly identifies sentiment and intent (>90% accuracy)
2. **Proper formatting**: Entries appear as clean bullet points with no extra whitespace
3. **Section placement**: Entry appears under correct emoji section heading
4. **File creation**: If diary note doesn't exist, properly creates from template with frontmatter
5. **Date handling**: Correctly adds to today by default, and both dates when `--date` specified
6. **Multiple entries**: Each entry independently analyzed and categorized
7. **No manual intervention**: Command completes without asking for category confirmation

## Related Resources

- MOKAI diary template: `/98-templates/mokai-note.md`
- MOKAI diary directory: `/01-areas/business/mokai/diary/`
- Agent instructions: `.claude/agents/agent-mokai.md`
- Daily note structure documented in MOKAI tracking system

## Technical Implementation Notes

### Sentiment Analysis Approach

Use a combination of:
1. **Keyword matching**: Fast detection of obvious wins/blockers/learnings
2. **Contextual analysis**: Understanding nuance (e.g., "can't wait to start" is positive despite "can't")
3. **Tone detection**: Formal vs. casual, frustrated vs. neutral
4. **Business context**: Understanding MOKAI-specific terms (tender, IPP, IRAP, etc.)

### File Manipulation Safety

- Always read entire file before modification
- Use regex with proper section boundary detection
- Preserve all other content unchanged
- Verify write succeeded before confirming to user
- Handle concurrent modifications gracefully (file locking if needed)

### Performance Considerations

- Single file read/write per diary note (batch all entries)
- AI analysis can process multiple entries in parallel
- Template copy only happens once per new diary note
- No external API calls required (local file operations only)
