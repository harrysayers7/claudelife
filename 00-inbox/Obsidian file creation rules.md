---
date created: Wed, 10 8th 25, 11:55:11 am
date modified: Wed, 10 8th 25, 7:42:50 pm
---
### **Universal Obsidian Vault File Creation Standards**

```markdown
# Obsidian Vault File Creation Standards

## Core Principles

1. **Properties over tags** for classification
2. **Minimal relations** - only to existing hubs
3. **Descriptive frontmatter** for AI discoverability
4. **Consistent structure** across all areas

---

## Required Frontmatter Properties

### ALL files must include:
```yaml
---
type: [document|note|reference|template|artifact|journal|prompt]
area: [business|fitness|accounting|personal|learning|projects]
category: string  # Flexible based on area context
relation:
  - "[[primary-hub]]"  # Must be existing note from 97-tags
date created: YYYY-MM-DD
description: "One-line summary with key terms for semantic search"
---
```

---

## Property Selection Guide

### `type` - Document Classification

- **document** - Formal documents (contracts, agreements, proposals, reports)
- **note** - Working notes, meeting notes, frequently updated content
- **reference** - Static educational/learning content, stable guides, procedures
- **template** - Reusable templates
- **artifact** - Deliverables, outputs, final products
- **journal** - Dated entries, logs, daily snapshots
- **prompt** - AI instruction files

**Decision tree:**
- Static educational/reference content? → `reference`
- Changes frequently? → `note`
- Formal deliverable or official document? → `document`
- Dated snapshot or log? → `journal`
- AI instruction/role definition? → `prompt`

---

### `area` - Top-Level Domain

Choose the primary domain this content belongs to:

- **business** - Business operations, strategy, clients
- **fitness** - Training, nutrition, health tracking
- **accounting** - Financial records, tax, bookkeeping
- **personal** - Personal notes and content
- **learning** - General education not specific to other areas
- **projects** - Project-specific content

**Rule:** Every file must have ONE primary area.

---

### `category` - Sub-Classification

This is **flexible** and **context-dependent** based on area.

**Business examples:**
- context, course, contract, research, deliverable, client, proposal

**Fitness examples:**
- workout, meal-plan, progress, routine, recovery, nutrition

**Accounting examples:**
- tax, invoice, expense, receipt, reconciliation, report

**Personal examples:**
- journal, goal, reflection, idea

**Learning examples:**
- course, lesson, how-to, tutorial, notes

**Guidelines:**
- Use descriptive categories relevant to the area
- Keep categories consistent within each area
- Categories should aid filtering and organization

---

### `relation` - Explicit Connections

**CRITICAL RULE: Only use relations that already exist in 97-tags folder.**

**How to determine valid relations:**
1. Check `/97-tags/` folder for existing hub notes
2. Use ONLY notes that exist there as relations
3. **DO NOT create new relation hubs** unless explicitly instructed

**Standard relation patterns:**

```yaml
# Business content
relation:
  - "[[business]]"  # or specific client/project if it exists in 97-tags

# Fitness content
relation:
  - "[[fitness]]"

# Accounting content
relation:
  - "[[accounting]]"

# Multiple valid relations (if both exist in 97-tags)
relation:
  - "[[business]]"
  - "[[mokai]]"  # Sub-hub that exists
```

**What to do if desired relation doesn't exist:**
- **Stop and ask user:** "Should I create a new hub note in 97-tags for [X]?"
- **Wait for confirmation** before creating new relations
- **Default:** Use the most general existing hub (e.g., `[[business]]`)

**Invalid approach:**
```yaml
# ❌ NEVER DO THIS without user permission
relation:
  - "[[business-fitness-hybrid]]"  # Doesn't exist in 97-tags
  - "[[new-project-name]]"  # Not confirmed by user
```

---

### `description` - Semantic Summary

**Purpose:** Help AI understand file content at a glance for semantic search.

**Rules:**
- **One to two lines maximum**
- **Include key terms** AI should match on
- **Be specific** not generic
- **Executive summary** not full content

**Good examples:**
- "Quarterly tax reconciliation for FY2025 - GST calculations and BAS preparation"
- "Upper body strength training routine - 4 week progressive overload program"
- "Client proposal for cybersecurity assessment - scope and pricing"
- "Weekly meal prep plan - high protein, 2000 calories, 5 days"

**Bad examples:**
- "Notes" (meaningless)
- "Information about taxes" (too vague)
- "Workout" (not specific enough)
- "Context" (says nothing)

---

## Optional but Recommended Properties

### For Status Tracking:
```yaml
status: [draft|review|active|archived|complete]
archived: false  # Boolean
```

### For AI Context Loading:
```yaml
ai-context: true  # Should AI load this for context?
context-priority: [low|medium|high|critical]  # How important for AI
last-validated: YYYY-MM-DD  # When info was confirmed accurate
source-of-truth: true  # Is this the authoritative version?
```

### For Sensitive Content:
```yaml
confidential: true  # Boolean
client-facing: false  # Boolean (for business)
public: false  # Boolean (can this be shared publicly?)
```

### For Keywords (Use Sparingly):
```yaml
keywords: [acronym1, term2, alternative-name]
```

**When to add keywords:**
- Acronyms not in description
- Alternative names/terms
- Technical jargon
- Cross-references to related frameworks

**When to skip keywords:**
- Description already comprehensive
- No special terminology
- Unclear what to add

### Domain-Specific Properties

**Business:**
```yaml
client: "Client Name"
contract-id: "PROJECT-2025-001"
billable: true
revenue: 5000
```

**Fitness:**
```yaml
workout-type: [strength|cardio|flexibility|sports]
duration: 60  # minutes
intensity: [low|moderate|high]
equipment: [bodyweight|gym|home]
```

**Accounting:**
```yaml
fiscal-year: 2025
amount: 1500.00
tax-category: [income|expense|asset|liability]
gst-inclusive: true
```

**Learning:**
```yaml
completed: true
difficulty: [beginner|intermediate|advanced]
time-estimate: 3h  # hours or "45m" for minutes
```

### For Versioning:
```yaml
version: 1.0
supersedes: "[[old-document]]"
```

---

## Tags - Use Sparingly

**Purpose:** Cross-cutting themes that span multiple areas.

**When to use tags:**
- Cross-cutting concepts (#productivity, #planning)
- Technical terms (#python, #excel)
- Action states (#todo, #review, #question)
- Skills (#analysis, #writing)
- Themes that appear across areas (#health, #strategy)

**When NOT to use tags:**
- Classification (use `type` or `category` properties)
- Organization (use `area` property)
- Generic labels (#notes, #information, #context)

**Tag format:**
```yaml
tags:
  - specific-concept
  - technical-term
  - cross-cutting-theme
```

**Examples:**
```yaml
# Business strategy note
tags:
  - strategy
  - planning
  - Q4-2025

# Fitness tracking note
tags:
  - progress
  - strength
  - tracking

# Accounting procedure
tags:
  - procedure
  - compliance
  - quarterly
```

---

## File Naming Convention

**Format:** `descriptive-name-kebab-case.md`

**Rules:**
- Use kebab-case (lowercase with hyphens)
- Be descriptive but concise
- Include dates ONLY for journals (YYYY-MM-DD.md)
- No spaces or special characters

**Examples:**
```
business-plan-2025.md
squat-progression-program.md
tax-deduction-guide.md
2025-10-02.md  # Journal only
weekly-meal-prep.md
client-proposal-template.md
```

**Avoid:**
- Spaces in filenames
- Special characters (!@#$%^&*)
- ALL CAPS
- Dates in non-journal files
- Generic names (notes.md, document.md)

---

## File Location Structure

**Folder hierarchy:**
```
/01-areas/[area]/[subcategory]/
/97-tags/  # Hub notes and tag indices ONLY
```

**Examples:**
```
/01-areas/business/mokai/
/01-areas/business/mokai/context/
/01-areas/business/clients/
/01-areas/fitness/workouts/
/01-areas/fitness/nutrition/
/01-areas/accounting/tax/
/01-areas/accounting/invoices/
/97-tags/  # business.md, fitness.md, mokai.md, etc.
```

**Rules:**
- Files go in `/01-areas/[area]/` subfolders
- Hub notes ONLY in `/97-tags/`
- Don't create deep nesting (max 3 levels)

---

## 97-Tags Folder - Hub Notes Only

**CRITICAL:** The `/97-tags/` folder contains hub notes that act as central connection points.

**What goes in 97-tags:**
- Area hubs (business.md, fitness.md, accounting.md)
- Major sub-topics (mokai.md, strength-training.md, tax-2025.md)
- Concept indices (IRAP.md, essential8.md)
- Tag definitions (productivity.md, planning.md)

**What does NOT go in 97-tags:**
- Regular content files
- Working notes
- Documents
- Journals
- Templates

**When to create new hub in 97-tags:**
- **ONLY** when user explicitly requests it
- **NEVER** automatically create new hubs
- **ASK FIRST:** "Should I create a new hub note in 97-tags for [X]?"

**Structure of a hub note:**
```markdown
# Hub Name

Brief description of what this hub connects.

## Related Notes
- [[note-1]]
- [[note-2]]

## Key Concepts
- Concept explanations
- Important context
```

---

## Complete Examples

### Example 1: Business Context Document
```yaml
---
type: reference
area: business
category: context
relation:
  - "[[business]]"
  - "[[mokai]]"  # Only if mokai.md exists in 97-tags
date created: 2025-10-02
description: "Mokai business model: 51% indigenous ownership, prime contractor for government cybersecurity"
keywords: [indigenous, IPP, cybersecurity, prime-contractor]
ai-context: true
context-priority: high
last-validated: 2025-10-02
source-of-truth: true
---
```

### Example 2: Fitness Workout Log
```yaml
---
type: journal
area: fitness
category: workout
relation:
  - "[[fitness]]"
date created: 2025-10-02
journal-date: 2025-10-02
description: "Upper body strength session - bench press PR attempt and accessory work"
workout-type: strength
duration: 75
intensity: high
tags:
  - strength
  - upper-body
  - progress
---
```

### Example 3: Accounting Tax Reference
```yaml
---
type: reference
area: accounting
category: tax
relation:
  - "[[accounting]]"
date created: 2025-10-02
description: "Tax deduction guide for small business - ATO compliant expense categories"
keywords: [ATO, deductions, business-expenses, tax-return]
fiscal-year: 2025
tags:
  - compliance
  - procedure
---
```

### Example 4: Learning Course Note
```yaml
---
type: reference
area: learning
category: course
relation:
  - "[[learning]]"
date created: 2025-10-02
description: "Python data structures fundamentals - lists, dictionaries, sets, tuples"
keywords: [python, programming, data-structures]
completed: false
difficulty: beginner
time-estimate: 2h
tags:
  - python
  - programming
  - tutorial
---
```

### Example 5: Business Client Proposal
```yaml
---
type: document
area: business
category: proposal
status: draft
relation:
  - "[[business]]"
date created: 2025-10-02
date due: 2025-10-15
description: "Cybersecurity assessment proposal for Department of Defence - scope and pricing"
client: "Department of Defence"
contract-id: "DOD-2025-SEC-001"
billable: true
confidential: true
client-facing: true
tags:
  - proposal
  - government
  - cybersecurity
---
```

### Example 6: Personal Journal Entry
```yaml
---
type: journal
area: personal
category: reflection
relation:
  - "[[personal]]"
date created: 2025-10-02
journal-date: 2025-10-02
description: "Weekly reflection on goals, wins, and areas for improvement"
tags:
  - reflection
  - goals
  - weekly-review
---
```

### Example 7: AI Instruction Prompt
```yaml
---
type: prompt
area: business
category: ai-instruction
relation:
  - "[[business]]"
date created: 2025-10-02
description: "Legal advisory role for business decisions and contract review"
trigger: "!lawyer"
ai-role: legal-advisor
active: true
context-priority: critical
requires-context: ["[[business-context]]"]
---
```

---

## AI Reading Priority

When AI searches for context, it should prioritize:

**1. Files where:**
- `ai-context: true`
- `context-priority: high` or `critical`
- `source-of-truth: true`
- Recent `last-validated` date
- `area` matches current query domain

**2. Read in this order:**
- Description (quick relevance check)
- Keywords (if present)
- Frontmatter properties
- Headings and structure
- Full content

**3. Respect context priority:**
- Files in `/context/` subfolders = current operational state (highest priority)
- `source-of-truth: true` = authoritative
- Recent `last-validated` = current information
- `archived: true` = historical reference only

---

## Validation Checklist

Before creating a file, AI must verify:

- [ ] `type` is one of the valid options
- [ ] `area` is specified and valid
- [ ] `category` is appropriate for the area
- [ ] `relation` includes ONLY notes that exist in `/97-tags/`
- [ ] If desired relation doesn't exist, ASK USER before creating
- [ ] `description` is 1-2 lines and keyword-rich
- [ ] `date created` is in YYYY-MM-DD format
- [ ] Filename is kebab-case with .md extension
- [ ] File location matches area structure
- [ ] Tags (if used) are specific, not generic
- [ ] No new hub notes created without user permission

---

## Critical Rules

### ALWAYS:
- Include all required properties
- Use kebab-case for filenames
- Relate content to existing hubs in `/97-tags/`
- Write meaningful, specific descriptions
- Use properties for classification
- Ask before creating new relations/hubs

### NEVER:
- Use generic descriptions ("notes", "context", "information")
- Create new hub notes in `/97-tags/` without user permission
- Use relations that don't exist in `/97-tags/`
- Use tags for classification (use properties)
- Skip the description field
- Include dates in filenames except journals
- Use spaces or special characters in filenames

### WHEN UNCERTAIN:
- Default to `type: note` for dynamic content, `type: reference` for static
- Use most general existing hub (e.g., `[[business]]`, `[[fitness]]`)
- Skip optional properties rather than guessing
- **ASK USER** before creating new relations or hubs
- Ask for clarification on classification

---

## Creating New Hubs (97-Tags)

**When user requests a new hub:**

1. **Confirm intent:**
   - "Should I create a new hub note `[name].md` in `/97-tags/`?"
   - Explain what will be connected to it

2. **Create hub structure:**
```yaml
---
type: reference
area: [relevant-area]
category: hub
date created: YYYY-MM-DD
description: "Central hub for [topic] - connects all related content"
---

# [Hub Name]

Brief description of what this hub connects and organizes.

## Overview
[Context about this topic/area]

## Related Notes
[Will be populated as files are created]

## Key Concepts
[Important information about this topic]
```

3. **Update existing hubs:**
   - Add link to new hub in parent hub (if applicable)
   - Maintain hub hierarchy

---

## Domain-Specific Guidelines

### Business Area
**Common categories:** context, client, proposal, contract, deliverable, research, strategy
**Key properties:** client, contract-id, billable, revenue, confidential

### Fitness Area
**Common categories:** workout, nutrition, progress, routine, recovery, plan
**Key properties:** workout-type, duration, intensity, equipment

### Accounting Area
**Common categories:** tax, invoice, expense, receipt, reconciliation, report
**Key properties:** fiscal-year, amount, tax-category, gst-inclusive

### Personal Area
**Common categories:** journal, goal, reflection, idea, planning
**Key properties:** mood, energy-level, priority

### Learning Area
**Common categories:** course, lesson, tutorial, notes, reference, how-to
**Key properties:** completed, difficulty, time-estimate, platform

---

## Error Prevention

**Before writing ANY file:**

1. **Check `/97-tags/` for valid relations**
   - List available hubs
   - Confirm relation exists
   - Ask if new hub needed

2. **Verify area and category**
   - Is area correct?
   - Is category appropriate?
   - Is there a better classification?

3. **Review description**
   - Is it specific?
   - Does it include key terms?
   - Would it help AI find this file?

4. **Validate properties**
   - All required fields present?
   - Properties appropriate for area?
   - No contradictions?

---

## Quick Reference Decision Matrix

| Question | Answer |
|----------|--------|
| Is this frequently updated? | `type: note` |
| Is this static reference? | `type: reference` |
| Is this a formal deliverable? | `type: document` |
| Is this dated? | `type: journal` |
| What domain? | `area: [business/fitness/accounting/personal/learning]` |
| How to classify within area? | `category: [context-specific]` |
| What to link to? | Only existing notes in `/97-tags/` |
| Should I create new hub? | **ASK USER FIRST** |
| Use tags? | Only for cross-cutting themes |
| Keywords needed? | Only if acronyms/jargon not in description |

---

**END OF STANDARDS**
```

---

**Save this as:** `/08-context-ai-apps/claude-desktop/obsidian-file-creation-rules.md`

This universal version:
✅ Works across all your areas (business, fitness, accounting, etc.)
✅ Prevents AI from creating new relations without permission
✅ Forces AI to check `/97-tags/` for valid hubs
✅ Provides domain-specific examples
✅ Includes validation checklist
✅ Clear error prevention workflow
