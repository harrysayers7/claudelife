# Formatting Rules for Daily Workflow

This document specifies exact formatting rules for transforming, routing, and storing extracted daily note entries.

## Entry Type Formatting

### Diary Entries

**Characteristics**:
- Preserve first-person narrative voice
- Include date headers
- Maintain temporal context
- Keep emotional/subjective content

**Primary Destination**: `04-resources/diary.md`

**Format**:
```markdown
## YYYY-MM-DD - Day

[Narrative entry preserved exactly as written, including "I", "today", feelings, etc.]
```

**Secondary Destinations**: `[area]/diary-[area].md` (if confidence >80%)

**Format** (area-specific diary files):
```markdown
## YYYY-MM-DD - Day

[Narrative entry preserved, but filtered to area-relevant content only]

*From:* [[00 - Daily/🌤️ Day - DDth MMM YY#🧠 Notes]]
```

**Example**:
```markdown
## 2025-10-21 - Mon

Finished mixing the Nintendo track today. Took about 4 hours of vocal chain tweaking but client approved on first submission. Feeling good about the workflow improvements I made last month - they're really paying off now.

*From:* [[00 - Daily/🌤️ Mon - 21st Oct 25#🧠 Notes]]
```

---

### Context Entries

**Characteristics**:
- Transform to third-person factual statements
- Remove dates, pronouns, temporal markers
- Remove feelings and subjective assessments
- Extract topically relevant facts only
- Rephrase for each context area (different formulation per area)

**Primary Destination**: `04-resources/context.md`

**Format**:
```markdown
- [Topic]: [Factual statement]
  *From:* [[00 - Daily/🌤️ Day - DDth MMM YY#🧠 Notes]]
```

**Secondary Destinations**: Matching `CLAUDE.md` files in specific areas (if confidence >80%)

**Format** (area-specific context files):
```markdown
- [Topic]: [Factual statement custom-formulated for this area]
  *From:* [[00 - Daily/🌤️ Day - DDth MMM YY#🧠 Notes]]
  *Related:* [[path/to/related/context-file]]
```

**Transformation Rules**:
1. **Remove pronouns**: "I built" → "Supabase database built"
2. **Remove temporal markers**: "today", "this morning", "yesterday"
3. **Remove feelings**: "Took forever" → (omit), "feeling good" → (omit)
4. **Extract facts**: "Will use for invoice management" → "for invoice management"
5. **Topic-first**: Lead with the main subject
6. **Custom formulation**: Phrase differently for each area to reflect that area's perspective

**Example Transformation**:

**Original Diary Entry**:
```markdown
Today I built a Supabase database for financial tracking for MOKAI. Took forever to set up auth but got it working. Will use for invoice management.
```

**Primary Context** (`04-resources/context.md`):
```markdown
- Supabase: Financial tracking database with auth, for invoice management
  *From:* [[00 - Daily/🌤️ Mon - 21st Oct 25#🧠 Notes]]
```

**Secondary Context** (`tech/CLAUDE.md`):
```markdown
- Supabase: Financial tracking database with auth
  *From:* [[00 - Daily/🌤️ Mon - 21st Oct 25#🧠 Notes]]
  *Related:* [[business/mokai/context-mokai]]
```

**Secondary Context** (`business/mokai/CLAUDE.md`):
```markdown
- Financial tracking system: Supabase database for invoice management
  *From:* [[00 - Daily/🌤️ Mon - 21st Oct 25#🧠 Notes]]
  *Related:* [[tech/context-tech]]
```

---

### Insights

**Characteristics**:
- Preserve reflective/analytical tone
- Keep first-person if it enhances clarity
- Include date context if relevant to understanding
- Maintain strategic/learning focus

**Primary Destination**: `01-areas/p-dev/insights.md`

**Format**:
```markdown
## YYYY-MM-DD

[Insight preserved with minimal editing, maintaining analytical depth]

*From:* [[00 - Daily/🌤️ Day - DDth MMM YY#🧠 Notes]]
```

**Secondary Destinations**: NEVER route insights to context files (insights ≠ context)

**Example**:
```markdown
## 2025-10-21

Most client complaints stem from unclear project scope. Implementing detailed SOWs with acceptance criteria for every project could prevent 80% of scope creep issues.

*From:* [[00 - Daily/🌤️ Mon - 21st Oct 25#🧠 Notes]]
```

---

### Ideas

**Characteristics**:
- Preserve speculative/creative tone
- Keep future-oriented language ("could", "what if")
- Maintain brainstorming format
- No need for dates unless time-sensitive

**Primary Destination**: `04-resources/ideas.md`

**Format**:
```markdown
- [Idea statement]
  *From:* [[00 - Daily/🌤️ Day - DDth MMM YY#🧠 Notes]]
```

**Secondary Destinations**: NEVER route ideas to context files

**Example**:
```markdown
- Chrome extension that auto-captures Notion pages to daily note - could save 10 minutes per day
  *From:* [[00 - Daily/🌤️ Mon - 21st Oct 25#🧠 Notes]]
```

---

## Cross-Linking Format

All routed entries MUST include cross-links back to the source daily note.

### Link to Daily Note
```markdown
*From:* [[00 - Daily/🌤️ Day - DDth MMM YY#🧠 Notes]]
```

**Format Components**:
- `00 - Daily/` - Folder path
- `🌤️ Day - DDth MMM YY` - Exact filename
- `#🧠 Notes` - Section anchor (optional but recommended)

### Link to Related Context Files
```markdown
*Related:* [[path/to/context-file]]
```

**When to add Related links**:
- When an entry routes to multiple context areas
- Add bidirectional links between related areas
- Limit to 1-3 most relevant related files

**Example**:
```markdown
- Supabase: Financial tracking database
  *From:* [[00 - Daily/🌤️ Mon - 21st Oct 25#🧠 Notes]]
  *Related:* [[business/mokai/context-mokai]], [[tech/context-tech]]
```

---

## Auto-Creation Rules

### Diary Files

If area-specific diary file doesn't exist, create it with frontmatter:

```markdown
---
date created: Day, MM DDth YY, HH:MM:SS am/pm
date modified: Day, MM DDth YY, HH:MM:SS am/pm
---

# [Area Name] Diary

## YYYY-MM-DD - Day

[First entry]

*From:* [[00 - Daily/🌤️ Day - DDth MMM YY#🧠 Notes]]
```

**Locations**:
- `business/mokai/diary-mokai.md`
- `business/mokhouse/diary-mokhouse.md`
- `01-areas/p-dev/learning/diary-learning.md`
- etc.

### Context Files

Context files should already exist. If missing, create with:

```markdown
---
date created: Day, MM DDth YY, HH:MM:SS am/pm
date modified: Day, MM DDth YY, HH:MM:SS am/pm
---

# [Area Name] Context

- [First context entry]
  *From:* [[00 - Daily/🌤️ Day - DDth MMM YY#🧠 Notes]]
```

---

## Frontmatter Rules

### Required Frontmatter (for auto-created files)
```yaml
---
date created: Day, MM DDth YY, HH:MM:SS am/pm
date modified: Day, MM DDth YY, HH:MM:SS am/pm
---
```

**Format**:
- Day: `Mon`, `Tue`, `Wed`, etc.
- MM: `10`, `01`, `12`, etc.
- DDth: `21st`, `02nd`, `13th`, etc.
- YY: `25`, `26`, etc.
- Time: `6:24:50 am` or `3:15:30 pm`

### Never Modify Frontmatter (for existing files)
- Preserve existing frontmatter exactly
- Only update `date modified` field on edits (if it exists)

---

## Deduplication Rules

Before appending to destination files, check for duplicates:

### Fuzzy Match Threshold: 80%

Use Levenshtein distance or similar algorithm to detect near-duplicates.

### What to Check
- **Diary entries**: Check last 30 entries in the file
- **Context entries**: Check entire file (usually smaller)
- **Insights**: Check last 50 entries
- **Ideas**: Check entire file

### Duplicate Detection Examples

**Original Entry**:
```markdown
Supabase: Financial tracking database with auth
```

**Existing Entry (DUPLICATE)**:
```markdown
Supabase: Financial tracking DB with authentication
```

**Similarity**: 85% → Skip appending, log as duplicate

**Existing Entry (NOT DUPLICATE)**:
```markdown
Supabase: Project management database
```

**Similarity**: 60% → Append as new entry

---

## Append vs Insert Rules

### Always Append (Never Prepend)
Append new entries to the END of destination files to maintain chronological order.

### Section Placement

**Diary Files**:
```markdown
## 2025-10-20 - Sun
[Older entry]

## 2025-10-21 - Mon
[Newer entry] ← APPEND HERE
```

**Context Files**:
```markdown
- Old context entry
  *From:* [[old-daily-note]]

- New context entry ← APPEND HERE
  *From:* [[new-daily-note]]
```

**Insights Files**:
```markdown
## 2025-10-20
[Older insight]

## 2025-10-21 ← APPEND HERE
[Newer insight]
```

**Ideas Files**:
```markdown
- Old idea
  *From:* [[old-daily-note]]

- New idea ← APPEND HERE
  *From:* [[new-daily-note]]
```

---

## Special Characters and Escaping

### Preserve Special Characters
- Keep emojis: `🔥`, `📊`, `✅`
- Keep formatting: `**bold**`, `*italic*`, `` `code` ``
- Keep lists: `-`, `*`, numbered lists

### Escape Only When Necessary
- Markdown link brackets: Already handled by `[[wikilink]]` format
- Code blocks: Use triple backticks when code snippets are in entries

**Example**:
```markdown
- Configured Supabase RLS with this policy:
  ```sql
  CREATE POLICY "user_access" ON invoices FOR SELECT USING (auth.uid() = user_id);
  ```
  *From:* [[00 - Daily/🌤️ Mon - 21st Oct 25#🧠 Notes]]
```

---

## Validation Checklist

Before marking extraction as complete:

- [ ] All entries classified correctly (Diary/Insight/Context/Idea)
- [ ] Confidence scores >80% for secondary routing
- [ ] Diary entries preserve narrative tone
- [ ] Context entries transformed to factual statements
- [ ] All entries have `*From:*` links
- [ ] Related context files have bidirectional links
- [ ] No duplicate entries appended
- [ ] Frontmatter preserved on existing files
- [ ] New diary files created with proper frontmatter
- [ ] Tracker updated with processed files (but NOT today's file)
- [ ] User approved routing decisions

---

## Error Handling

### Missing Files
- **Diary/Context/Insights/Ideas base files missing**: Error and halt (these should always exist)
- **Area-specific files missing**: Auto-create with frontmatter

### Malformed Entries
- **No extractable content**: Log and skip, don't error
- **Ambiguous classification**: Default to Diary, log for manual review
- **Very short entries (<10 words)**: Classify but flag for review

### Write Failures
- **Permission errors**: Error and halt
- **Concurrent edit conflicts**: Retry once, then error
- **Disk full**: Error and halt

---

## File Integrity Rules

### Never Delete Original Content
- Daily note `### 🧠 Notes` section remains untouched after extraction
- Extraction is a **copy operation**, not a move operation

### Atomic Operations
- Write to temporary file first
- Verify write success
- Rename to final destination
- Prevents partial writes

### Tracker Updates
- Update tracker ONLY after ALL entries successfully routed
- Mark files as processed ONLY if today is PAST (allow re-processing today's file)
- Store confidence scores for audit trail
