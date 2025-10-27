# Daily Note Template Reference

This document describes the structure and patterns used in daily notes for proper extraction and categorization.

## Template Location

Main template: [98-templates/daily-note.md](../../../98-templates/daily-note.md)

## Frontmatter Structure

```yaml
---
type: daily note
date: "YYYY-MM-DD"
day: Mon
month: Jan
year: YYYY
event: ""  # Optional: special events/occasions
---
```

## Standard Sections

### 1. Header
```markdown
# 🌤️ Day - DDth MMM YY
```

### 2. Tasks Section (Dataview)
```dataview
TASK
WHERE file.name = this.file.name
```

### 3. Events Section (Dataview)
```dataview
TABLE WITHOUT ID
  file.link as "Event",
  date as "Date",
  time as "Time",
  location as "Location"
FROM "00 - Daily"
WHERE type = "event" AND date >= date(today) AND date <= date(today) + dur(30 days)
SORT date ASC
LIMIT 10
```

### 4. Notes Section (PRIMARY EXTRACTION TARGET)
```markdown
### 🧠 Notes

[User's daily entries go here - this is what gets extracted and categorized]
```

**Extraction Pattern**:
- Scan all content between `### 🧠 Notes` header and next H3 heading (or EOF)
- Extract individual entries (paragraphs separated by blank lines)
- Classify each entry using AI
- Route to appropriate destination files

**Example entries**:
```markdown
### 🧠 Notes

Built a Supabase database for MOKAI financial tracking today. Authentication setup was tricky but got it working. Will use for invoice management system.

Had an insight about customer retention - need to focus on post-sale support rather than just acquisition. This could be a differentiator for MOK HOUSE.

Idea: Create automated workflow for extracting daily notes using MCP servers. Could classify entries by type and route to appropriate areas.
```

### 5. MOK HOUSE Projects Dashboard (Optional)
```dataview
TABLE WITHOUT ID
  file.link as "Project",
  status as "Status",
  priority as "Priority",
  client as "Client"
FROM "02-projects/mokhouse"
WHERE type = "project"
SORT priority DESC, status ASC
```

## Entry Types and Recognition Patterns

### Diary Entries
**Indicators**:
- First-person narrative ("I did...", "Today I...")
- Daily activities and events
- Project completion updates
- Meeting summaries
- Temporal markers (today, this morning, yesterday)

**Example**:
```markdown
Finished mixing the Nintendo track for the client. Took about 4 hours of tweaking the vocal chain. Client approved on first submission.
```

### Insights
**Indicators**:
- Learnings and realizations
- Patterns observed
- Reflections on experiences
- Strategic thinking
- Keywords: "learned", "realized", "insight", "noticed", "pattern"

**Example**:
```markdown
Realized that most client complaints come from unclear project scope. Need to implement detailed SOWs with acceptance criteria for every project.
```

### Context Entries
**Indicators**:
- Factual information
- Technical details
- How-to knowledge
- Configuration notes
- No emotional content
- Keywords: "setup", "configured", "installed", "works by"

**Example**:
```markdown
Supabase RLS policies work by filtering rows at the database level before they reach the application. More secure than application-level filtering.
```

### Ideas
**Indicators**:
- Future possibilities
- Feature concepts
- Business opportunities
- Process improvements
- Keywords: "could", "what if", "idea", "maybe", "potential"

**Example**:
```markdown
What if we created a Chrome extension that auto-captures Notion pages to the daily note? Could save 10 minutes per day.
```

## Nested Sections

Daily notes may include nested subsections:

```markdown
### 🧠 Notes

#### Deep Work Session
- Completed database schema design
- Implemented auth middleware

#### Client Calls
- Meeting with MOKAI prospect
- Discussed SOW for pentest engagement
```

**Extraction Rule**: Scan ALL H4, H5, H6 subsections within `### 🧠 Notes` recursively.

## Dataview Integration

Daily notes use Dataview for dynamic content:

### Tasks Query
Shows tasks associated with the daily note file.

### Events Query
Shows upcoming events from the next 30 days from the `00 - Daily/` folder where `type = "event"`.

### Projects Query (MOK HOUSE specific)
Shows active MOK HOUSE projects from `02-projects/mokhouse/` sorted by priority and status.

## Special Markers

### Tags
```markdown
#mokai #client-work #insight
```

Tags within entries help with additional routing context.

### Links
```markdown
Related to [[business/mokai/context-mokai]] and [[02-projects/mokhouse/nintendo-project]]
```

Existing links are preserved during extraction and inform secondary routing decisions.

### Priorities
```markdown
🔥 URGENT: Follow up with Supply Nation application
```

Emoji markers indicate priority and can influence routing confidence.

## Cross-Linking Format

When entries are routed to destination files, cross-links are added:

```markdown
*From:* [[04-resources/diary#25-10-21 - Mon]]
*Related:* [[business/mokai/context-mokai]]
```

This creates bidirectional navigation between daily notes and context/diary files.

## File Naming Convention

Daily note files follow this pattern:
```
🌤️ Day - DDth MMM YY.md
```

Examples:
- `🌤️ Mon - 21st Oct 25.md`
- `🌤️ Tue - 22nd Oct 25.md`
- `🌤️ Wed - 23rd Oct 25.md`

**Parsing Pattern**: Extract date from filename for dating routed entries.

## Location

All daily notes stored in: `00 - Daily/`

## Related Templates

- **Diary file template**: `04-resources/diary.md` (narrative format with date headers)
- **Context file template**: `04-resources/context.md` (factual bullets with cross-links)
- **Insights file template**: `01-areas/p-dev/insights.md` (reflective format)
- **Ideas file template**: `04-resources/ideas.md` (concept format)
