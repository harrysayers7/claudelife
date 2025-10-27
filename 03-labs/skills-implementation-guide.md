---
date: "2025-10-21"
type: lab
status: active
relation:
  - "[[labs]]"
  - "[[claudelife]]"
  - "[[SKILLz]]"
---

# Skills Implementation Guide - Claudelife

**Created**: 2025-10-21
**Status**: Phase 1 Planning
**Reference**: [SKILLz.md](../04-resources/research/SKILLz.md)

## What Are Skills?

Skills are self-contained workflow packages that Claude automatically discovers and executes when relevant, based on the description in `SKILL.md`.

**vs Slash Commands**:
- **Skills** = Auto-detected from conversation context
- **Commands** = User explicitly invokes with `/command`

**Benefits**:
- Less friction: Natural conversation vs remembering commands
- Automatic capture: Context stored without explicit logging
- Progressive disclosure: References loaded only when needed
- Token efficient: SKILL.md loads first, references on-demand
- Composable: Multiple skills work together automatically

---

## Current State

### ✅ Operational Skills
- `mokai-daily-ops/` - MOKAI business status tracking
- `mokhouse-operations/` - MOK HOUSE project management

### 🎯 Conversion Candidates

**High-value command → skill migrations**:
1. **Daily workflows**: `/extract-daily-content`, `/janitor`
2. **Memory/Knowledge**: `/remember`, `/recall`, `/graphiti-add`
3. **Business operations**: `/accountant`
4. **Vault management**: `/vault-add`
5. **Task Master integration**: Auto-trigger task updates

---

## Architecture Design

### Skill Directory Structure

```
.claude/skills/
├── README.md                   # Overview + testing guide
│
├── daily-workflow/             # Auto-trigger daily operations
│   ├── SKILL.md
│   ├── reference/
│   │   ├── templates.md
│   │   └── formatting-rules.md
│   └── scripts/
│       └── extract_content.py
│
├── knowledge-capture/          # Auto-log insights, learnings
│   ├── SKILL.md
│   ├── GRAPHITI.md            # Graphiti integration patterns
│   └── MEMORY.md              # Serena memory patterns
│
├── vault-operations/           # Obsidian vault management
│   ├── SKILL.md
│   ├── reference/
│   │   ├── frontmatter-spec.md
│   │   └── para-method.md
│   └── scripts/
│       └── validate_note.py
│
├── financial-assistant/        # Business/finance queries
│   ├── SKILL.md
│   ├── reference/
│   │   ├── tax-rates-fy2025.md
│   │   └── deduction-categories.md
│   └── scripts/
│       └── calculate_tax.py
│
├── task-orchestration/         # Task Master integration
│   ├── SKILL.md
│   ├── WORKFLOWS.md
│   └── reference/
│       └── task-patterns.md
│
├── mokai-daily-ops/            # ✅ Existing
│   ├── SKILL.md
│   ├── TRACKER.md
│   └── DIARY.md
│
└── mokhouse-operations/        # ✅ Existing
    ├── SKILL.md
    ├── resources/
    └── scripts/
```

---

## Phase 1: Foundation Skills

### 1. daily-workflow/ - Auto Daily Operations

**Triggers when user**:
- Mentions "today's diary", "daily note", "extract content"
- Asks "what did I work on today?"
- Natural end-of-day: "done for today", "wrapping up"

**SKILL.md** (concise version):
```markdown
---
name: Daily Workflow Automation
description: Automatically processes daily notes when user mentions diary entries, daily summaries, or end-of-day workflows. Extracts insights, contexts, and categorizes content. Use when user discusses daily notes, diary, or asks about today's work.
---

# Daily Workflow Automation

Auto-process daily notes: extract insights → categorize → update trackers.

## Quick Workflow
1. Detect daily note path from date
2. Extract sections: Diary, Insights, Context
3. Categorize content (wins, blockers, learnings, context)
4. Update relevant trackers (.extract-daily-content-tracker.json)
5. Store in Graphiti if significant insights

## Extraction Patterns
- **Wins**: "✅", "completed", "shipped", "won"
- **Blockers**: "⚠️", "blocked by", "issue:", "stuck on"
- **Learnings**: "learned that", "discovered", "insight:"
- **Context**: Everything else (meeting notes, research, planning)

## File References
- Daily notes: `/00 - Daily/YYYY-MM-DD - Day.md`
- Template: [templates.md](reference/templates.md)
- Formatting: [formatting-rules.md](reference/formatting-rules.md)

## Scripts
- Extract diary: `python scripts/extract_content.py <date>`

## Critical Rules
- ✅ Always preserve frontmatter (date, event)
- ✅ Use Serena MCP for pattern matching (faster than Read)
- ✅ Deduplicate insights before storing in Graphiti
- ✅ Never delete original content during extraction
```

**reference/templates.md**:
```markdown
# Daily Note Templates

## Standard Format
[Include daily-note.md template structure]

## Section Headers
- ### 🧠 Thoughts & Notes
- ### 📅 Tasks Today
- ### 📔 Diary

## Dataview Query Patterns
[Document how tasks.md queries work]
```

**scripts/extract_content.py**:
```python
#!/usr/bin/env python3
"""Extract and categorize daily note content"""
import sys
from datetime import datetime

def categorize_entry(text: str) -> str:
    """Classify entry type based on content"""
    win_indicators = ["✅", "completed", "shipped", "won"]
    blocker_indicators = ["⚠️", "blocked", "issue:", "stuck"]
    learning_indicators = ["learned", "discovered", "insight:"]

    text_lower = text.lower()
    if any(ind in text_lower for ind in win_indicators):
        return "win"
    # ... categorization logic
```

---

### 2. knowledge-capture/ - Auto-Log Insights

**Triggers when user**:
- Shares a learning: "I learned that...", "discovered..."
- Mentions a pattern: "noticed that...", "pattern..."
- Natural insights: "turns out...", "realized..."

**SKILL.md** (concise):
```markdown
---
name: Knowledge Capture
description: Automatically captures and stores insights, learnings, and patterns when user shares discoveries or reflections. Stores in Graphiti knowledge graph and Serena memory. Use when user mentions learnings, patterns, realizations, or discoveries.
---

# Knowledge Capture

Auto-detect insights → store in Graphiti + Serena memory.

## Detection Triggers
- "I learned that..."
- "Discovered..."
- "Realized..."
- "Pattern: ..."
- "Turns out..."
- "Insight:"

## Storage Strategy
1. **Graphiti** (for queryable knowledge):
   - Client preferences
   - Technical learnings
   - Business patterns
   - Project outcomes

2. **Serena Memory** (for code context):
   - System patterns
   - Code conventions
   - Tool preferences
   - Architecture decisions

## Group IDs
- `mokai` - MOKAI business insights
- `mokhouse` - MOK HOUSE creative/business
- `claudelife` - General vault/system patterns
- `finance` - Financial learnings
- `tech` - Technical discoveries

See [GRAPHITI.md](GRAPHITI.md) for storage patterns.
See [MEMORY.md](MEMORY.md) for Serena integration.

## Examples

**User**: "I learned that Nintendo prefers sweet, story-driven scores"
**Action**: Store in Graphiti (group: `mokhouse`)

**User**: "Pattern: Task Master works best with research mode for complex tasks"
**Action**: Store in Serena memory (file: `suggested_commands`)
```

**GRAPHITI.md** (referenced when needed):
```markdown
# Graphiti Integration Patterns

## When to Use Graphiti

Store in Graphiti when:
- ✅ **Queryable knowledge** (client preferences, project outcomes)
- ✅ **Relationship-based** (Client X prefers Y)
- ✅ **Time-sensitive** (temporal facts: "as of Oct 2025...")

Don't use Graphiti for:
- ❌ **Static documentation** (use Serena memory)
- ❌ **Code patterns** (use Serena memory)
- ❌ **Transient notes** (use daily diary)

## Storage Patterns

### Business Insights
```javascript
mcp__graphiti__add_memory({
  name: "Client preference - Nintendo",
  episode_body: `Nintendo prefers sweet, story-driven scores with Japanese cultural influences.

  Evidence:
  - Won "Exchange Mode" project with heartwarming tone
  - Client feedback: "Loved the adorable sigh moment"
  - Creative direction: Story-focused, culturally-informed

  Pattern: Follow reference closely, polish production values.`,
  group_id: "mokhouse",
  source: "message"
})
```

### Technical Learnings
```javascript
mcp__graphiti__add_memory({
  name: "Task Master best practices",
  episode_body: `Task Master works best with research mode enabled for complex technical tasks.

  Observations:
  - Research mode provides more informed task breakdowns
  - Especially effective for unfamiliar tech stacks
  - Worth the extra API cost for architectural decisions

  Pattern: Use --research flag for tasks requiring domain knowledge.`,
  group_id: "tech",
  source: "message"
})
```

### Project Outcomes
```javascript
mcp__graphiti__add_memory({
  name: "MOKAI Supply Nation application outcome",
  episode_body: `Completed Supply Nation certification application on 2025-10-21.

  Process:
  - Gathered compliance documents
  - Submitted via portal
  - Estimated approval: 2-4 weeks

  Next steps:
  - Follow up after 2 weeks if no response
  - Prepare for verification call
  - Update website once approved`,
  group_id: "mokai",
  source: "message"
})
```
```

**MEMORY.md** (Serena integration):
```markdown
# Serena Memory Integration

## When to Use Serena Memory

Store in Serena memory when:
- ✅ **Code architecture** (system patterns, file structure)
- ✅ **Development workflows** (suggested commands, tool preferences)
- ✅ **Static documentation** (tech stack, conventions)

## Memory Files

### suggested_commands
**Purpose**: Common commands and workflows
**Update when**: New command patterns emerge

```markdown
# Suggested Commands

## Task Master Workflows
- Use `--research` for complex tasks requiring domain knowledge
- Run `task-master analyze-complexity` before expanding all tasks
- Update subtasks with implementation notes for future reference

## MCP Server Operations
- Always verify Supabase project ID: `gshsshaodoyttdxippwx`
- Use Serena for pattern matching (faster than Read tool)
- Graphiti group IDs: mokai, mokhouse, finance, tech
```

### system_patterns_and_guidelines
**Purpose**: Architecture decisions and patterns
**Update when**: New patterns established

```markdown
# System Patterns

## Vault Organization
- 00-inbox: Default for unclear categorization
- 01-areas: Ongoing responsibilities (business/mokai, business/mokhouse)
- 02-projects: Time-bound outcomes
- 04-resources: Reference materials

## Automation Patterns
- Daily note extraction: End-of-day workflow
- Knowledge capture: Auto-store insights in Graphiti
- Task tracking: Auto-sync from conversation
```

### tech_stack
**Purpose**: Technologies and tools in use
**Update when**: New tools added

```markdown
# Tech Stack

## MCP Servers
- Serena: Code analysis, file operations, memory management
- Graphiti: Knowledge graph storage
- Supabase: Database operations (project: gshsshaodoyttdxippwx)
- Task Master: Project/task management
- Trigger.dev: Background jobs and workflows

## Vault Tools
- Obsidian: Second brain system (PARA method)
- Dataview: Dynamic queries
- Templater: Note templates
```

## Update Commands

### Write Memory
```javascript
mcp__serena__write_memory({
  memory_name: "suggested_commands",
  content: "# Updated content..."
})
```

### Read Memory
```javascript
mcp__serena__read_memory({
  memory_file_name: "suggested_commands"
})
```

### List Memories
```javascript
mcp__serena__list_memories()
```
```

---

### 3. vault-operations/ - Obsidian Management

**Triggers when user**:
- Mentions adding/creating notes
- References vault structure, PARA method
- Asks about file organization

**SKILL.md** (concise):
```markdown
---
name: Vault Operations
description: Manages Obsidian vault operations when user creates notes, asks about organization, or references PARA structure. Handles frontmatter, file placement, and metadata. Use when user mentions creating notes, vault structure, or asks where files belong.
---

# Vault Operations

Auto-manage vault: create notes → add frontmatter → organize via PARA.

## PARA Structure
- **00-inbox**: Unsorted items (default if unclear)
- **01-areas**: Ongoing responsibilities (business, p-dev)
- **02-projects**: Time-bound outcomes
- **04-resources**: Reference materials
- **99-archive**: Completed/inactive

## Note Creation Flow
1. Determine PARA category from context
2. Generate frontmatter with date
3. Create file in correct location
4. Add to vault index if needed

## Frontmatter Rules
Always include:
```yaml
---
date: "YYYY-MM-DD HH:MM"
type: [note|project|resource|area]
relation:
  - "[[labs]]"
  - "[[parent-note]]"
---
```

See [frontmatter-spec.md](reference/frontmatter-spec.md) for details.
See [para-method.md](reference/para-method.md) for categorization guide.

## File Naming
- Projects: `project-name.md`
- Daily notes: `YYYY-MM-DD - Day.md`
- Resources: `descriptive-name.md`
```

**reference/frontmatter-spec.md**:
```markdown
# Frontmatter Specification

## Required Fields

### All Notes
```yaml
---
date: "YYYY-MM-DD HH:MM"  # Creation timestamp
type: note                # note|project|resource|area
---
```

### Projects
```yaml
---
date: "2025-10-21 14:30"
type: project
status: active            # active|complete|archived
relation:
  - "[[labs]]"
  - "[[parent-area]]"
---
```

### Daily Notes
```yaml
---
date created: Mon, 10 21st 25, 2:30:42 pm
date modified: Mon, 10 21st 25, 6:24:50 am
type: daily
event: ""                 # Optional event tag
---
```

## Optional Fields
- `tags: [tag1, tag2]` - Content categorization
- `customer: "Client Name"` - For business projects
- `status: "Brief Received"` - For workflow tracking
- `paid: true/false` - For financial tracking
```

**reference/para-method.md**:
```markdown
# PARA Method Guide

## Projects (02-projects/)
**Definition**: Time-bound activities with specific outcomes

**When to use**:
- Has a defined deadline or completion criteria
- Requires multiple steps/tasks
- Will eventually be complete or archived

**Examples**:
- Building a feature
- Running a campaign
- Writing a proposal
- Completing certification

## Areas (01-areas/)
**Definition**: Ongoing responsibilities requiring sustained attention

**When to use**:
- No end date (ongoing)
- Requires regular maintenance
- Standards to maintain, not outcomes to complete

**Examples**:
- Business operations (mokai, mokhouse)
- Personal development
- Health and fitness
- Financial management

## Resources (04-resources/)
**Definition**: Reference materials and learning content

**When to use**:
- Evergreen information
- How-to guides
- Research findings
- Documentation

**Examples**:
- Command guides
- Research notes
- Code style guides
- Template libraries

## Archives (99-archive/)
**Definition**: Completed/inactive items from other categories

**When to use**:
- Project is complete
- Area is no longer active
- Resource is outdated
- Want to preserve but not actively use

## Decision Tree

1. **Is it time-bound with an outcome?** → Projects
2. **Is it ongoing with no end date?** → Areas
3. **Is it reference/learning material?** → Resources
4. **Is it no longer active?** → Archives
5. **Not sure yet?** → Inbox (00-inbox/)
```

---

## Phase 2: Domain-Specific Skills

### 4. financial-assistant/ - Business/Finance Queries

**Triggers when user**:
- Asks about taxes, deductions, income
- Mentions invoices, expenses, revenue
- Financial planning questions

**SKILL.md** (concise):
```markdown
---
name: Financial Assistant
description: Answers financial queries about Australian taxes, business deductions, income tracking. Uses Supabase for transaction data, provides tax guidance for sole traders and companies. Use when user asks about taxes, deductions, invoices, revenue, or financial planning.
---

# Financial Assistant

Auto-answer financial questions using Supabase data + tax reference.

## Capabilities
- Tax calculations (FY2025 rates)
- Deduction categorization
- Income tracking (3mo, 6mo, 12mo averages)
- Invoice queries (paid/outstanding)
- Revenue forecasting

## Data Sources
- Supabase project: `gshsshaodoyttdxippwx`
- Tables: entities, invoices, transactions
- References: [tax-rates-fy2025.md](reference/tax-rates-fy2025.md)
- Deductions: [deduction-categories.md](reference/deduction-categories.md)

## Scripts
- Tax calc: `python scripts/calculate_tax.py --income <amount>`

## Critical Rules
- ✅ Always verify Supabase project ID before queries
- ✅ Cite tax rates with "as of FY2025"
- ✅ Recommend professional advice for complex tax scenarios
- ✅ Use AUD for all amounts (no $ symbol in data)
```

**reference/tax-rates-fy2025.md**:
```markdown
# Australian Tax Rates - FY 2024/2025

## Individual Tax Brackets
| Taxable Income | Tax Rate |
|----------------|----------|
| $0 - $18,200 | 0% (tax-free threshold) |
| $18,201 - $45,000 | 19% |
| $45,001 - $135,000 | 32.5% |
| $135,001 - $190,000 | 37% |
| $190,001+ | 45% |

## Company Tax Rate
- Standard: 30%
- Small business (<$50M turnover): 25%

## GST
- 10% on most goods/services
- Exempt: Fresh food, healthcare, education

## Deduction Limits
- Home office: $0.67/hour or actual costs
- Vehicle: Log book method or cents per km (85¢ for FY2025)
- Self-education: Directly related to current income
- Tools & equipment: Instant asset write-off up to $20,000
```

**reference/deduction-categories.md**:
```markdown
# Deduction Categories - Australian Tax

## Business Expenses (100% deductible)
- **Operating costs**: Rent, utilities, software subscriptions
- **Professional services**: Accountant, lawyer, consultants
- **Marketing**: Advertising, website, business cards
- **Equipment**: Computers, office furniture, tools
- **Travel**: Business-related only (not home to office)
- **Insurance**: Business, professional indemnity, public liability
- **Bank fees**: Business account fees, merchant fees

## Partial Deductions (Apportionment required)
- **Home office**: If working from home
  - Calculate percentage of home used for business
  - Deduct: Rent/mortgage interest, utilities, insurance (proportional)
- **Vehicle**: If business + personal use
  - Log book method: Track business vs personal km
  - Cents per km: Up to 5,000 business km @ 85¢
- **Phone/Internet**: Business portion only

## Not Deductible
- Personal expenses
- Capital gains (use CGT discount instead)
- Fines and penalties
- Entertainment (meals with clients - some exceptions)
- Donations (separate tax offset)

## Record Keeping
- Keep receipts for 5 years
- Document business purpose
- Log vehicle trips
- Track home office hours
```

**scripts/calculate_tax.py**:
```python
#!/usr/bin/env python3
"""Calculate Australian income tax for FY2025"""
import argparse

TAX_BRACKETS_FY2025 = [
    (18200, 0.0),
    (45000, 0.19),
    (135000, 0.325),
    (190000, 0.37),
    (float('inf'), 0.45)
]

def calculate_tax(income: float, entity_type: str = "individual") -> dict:
    """
    Calculate tax for Australian individual or company

    Args:
        income: Taxable income in AUD
        entity_type: "individual" or "company"

    Returns:
        dict with tax, medicare_levy, total
    """
    if entity_type == "company":
        # Assume small business (25% rate)
        tax = income * 0.25
        return {
            "tax": tax,
            "medicare_levy": 0,
            "total": tax,
            "rate": "25% (small business)"
        }

    # Individual tax calculation
    tax = 0
    prev_bracket = 0

    for bracket_max, rate in TAX_BRACKETS_FY2025:
        if income > prev_bracket:
            taxable_in_bracket = min(income, bracket_max) - prev_bracket
            tax += taxable_in_bracket * rate
            prev_bracket = bracket_max
        else:
            break

    # Medicare levy (2% on income > $23,365)
    medicare_levy = max(0, income - 23365) * 0.02

    return {
        "tax": round(tax, 2),
        "medicare_levy": round(medicare_levy, 2),
        "total": round(tax + medicare_levy, 2),
        "effective_rate": round((tax + medicare_levy) / income * 100, 2)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate Australian tax")
    parser.add_argument("--income", type=float, required=True, help="Taxable income in AUD")
    parser.add_argument("--entity", choices=["individual", "company"], default="individual")

    args = parser.parse_args()
    result = calculate_tax(args.income, args.entity)

    print(f"Income: ${args.income:,.2f}")
    print(f"Tax: ${result['tax']:,.2f}")
    if result['medicare_levy'] > 0:
        print(f"Medicare Levy: ${result['medicare_levy']:,.2f}")
    print(f"Total: ${result['total']:,.2f}")
    if 'effective_rate' in result:
        print(f"Effective Rate: {result['effective_rate']}%")
```

---

### 5. task-orchestration/ - Task Master Integration

**Triggers when user**:
- Completes task naturally: "finished the auth system"
- Asks what to work on next
- Shares task progress/blockers

**SKILL.md** (concise):
```markdown
---
name: Task Orchestration
description: Auto-integrates with Task Master when user completes tasks, asks what to work on, or shares progress. Updates task status, suggests next tasks, logs implementation notes. Use when user mentions task completion, asks for priorities, or shares task blockers.
---

# Task Orchestration

Auto-sync Task Master from conversation → update status → suggest next.

## Detection Patterns
- "finished [task]" → Mark complete, get next task
- "working on [task]" → Set to in-progress
- "blocked on [task]" → Update subtask with blocker
- "what should I work on?" → Get next task

## Integration Flow
1. Detect task mention from conversation
2. Match against `.taskmaster/tasks/tasks.json`
3. Auto-update status via MCP tools
4. Log notes in subtask if implementation detail shared
5. Suggest next task if completion detected

## MCP Tools
- `mcp__task-master-ai__get_tasks` - List tasks
- `mcp__task-master-ai__set_task_status` - Update status
- `mcp__task-master-ai__update_subtask` - Log notes
- `mcp__task-master-ai__next_task` - Get next

See [WORKFLOWS.md](WORKFLOWS.md) for common patterns.
See [reference/task-patterns.md](reference/task-patterns.md) for matching logic.

## Critical Rules
- ✅ Only update if confident about task match
- ✅ Confirm with user before marking complete
- ✅ Log implementation notes verbatim (user's exact words)
- ✅ Suggest next task only if current marked complete
```

**WORKFLOWS.md**:
```markdown
# Task Master Workflows

## Daily Development Loop

### Morning: Get Next Task
**User**: "What should I work on?"

**Claude**:
1. Run `mcp__task-master-ai__next_task()`
2. Check dependencies
3. Show task details with context
4. Suggest starting subtask if available

### During Work: Log Progress
**User**: "Working on the auth middleware - using JWT strategy"

**Claude**:
1. Detect task mention
2. Run `mcp__task-master-ai__update_subtask()` with notes
3. Confirm logged

### End of Day: Mark Complete
**User**: "Finished the auth middleware"

**Claude**:
1. Detect completion pattern
2. Confirm: "Mark task X.Y as done?"
3. Run `mcp__task-master-ai__set_task_status(id, "done")`
4. Show next available task

## Blocker Handling

**User**: "Stuck on auth - need to research JWT best practices"

**Claude**:
1. Detect blocker pattern
2. Update subtask: "Blocker: Need JWT best practices research"
3. Offer to run research via `/quick-research` or MCP

## Multi-Task Sessions

**User**: "Done with task 1.2, starting 1.3"

**Claude**:
1. Mark 1.2 complete
2. Set 1.3 to in-progress
3. Log transition in both tasks
4. Show 1.3 details
```

**reference/task-patterns.md**:
```markdown
# Task Matching Patterns

## Completion Patterns
- "finished [task]"
- "completed [task]"
- "done with [task]"
- "shipped [task]"
- "[task] is working"
- "got [task] working"

## In-Progress Patterns
- "working on [task]"
- "starting [task]"
- "currently doing [task]"
- "implementing [task]"

## Blocker Patterns
- "stuck on [task]"
- "blocked by [task]"
- "[task] isn't working"
- "issue with [task]"
- "need help with [task]"

## Task Reference Formats
- By ID: "task 1.2", "1.2.3"
- By title: "the auth system", "user authentication"
- By context: "the current task", "this task"

## Matching Strategy
1. Extract task reference from user message
2. Search tasks.json for:
   - Exact ID match (highest confidence)
   - Title fuzzy match (medium confidence)
   - Context match from recent conversation (low confidence)
3. If multiple matches, ask user to clarify
4. If no match, don't auto-update (avoid false positives)

## Confidence Thresholds
- **High (>90%)**: Auto-update without confirmation
- **Medium (60-90%)**: Confirm before updating
- **Low (<60%)**: Ask user to specify task ID
```

---

## Testing & Validation

### Testing Checklist (per skill)

```markdown
## Skill Testing Protocol

### 1. Trigger Detection
- [ ] Test with exact trigger phrases from description
- [ ] Test with natural variations
- [ ] Test with negative cases (shouldn't trigger)

### 2. File References
- [ ] All reference files load correctly
- [ ] Scripts execute without errors
- [ ] File paths use forward slashes

### 3. MCP Integration
- [ ] Serena MCP calls work efficiently
- [ ] Graphiti storage succeeds
- [ ] Supabase queries return correct data

### 4. Token Efficiency
- [ ] SKILL.md under 500 lines
- [ ] References loaded only when needed
- [ ] No deeply nested references (max 1 level)

### 5. User Experience
- [ ] Auto-triggers feel natural
- [ ] Provides value vs manual command
- [ ] Doesn't over-trigger (description too broad)
```

### Validation Commands

After implementing each skill, test with:

```bash
# 1. Restart Claude Code (skills load on start)
claude-code --restart

# 2. Natural conversation test
"What should I work on for MOKAI?"  # Should trigger mokai-daily-ops

# 3. Edge case test
"I need to create a note"  # Should trigger vault-operations

# 4. Negative test
"How's the weather?"  # Should NOT trigger any skill

# 5. MCP integration test
"I learned that Prisma works better with Supabase"  # Should store in Graphiti
```

---

## Best Practices

### ✅ DO (from SKILLz.md research)

1. **Concise SKILL.md** (<500 lines)
   - Brief overview
   - Quick workflow steps
   - File references for details

2. **Progressive disclosure**
   - Basic instructions in SKILL.md
   - Advanced details in reference/ files
   - Scripts for deterministic operations

3. **Clear descriptions**
   - What + When to use
   - Third-person voice
   - Specific triggers/keywords

4. **Workflows with checklists**
   - Copy-paste progress trackers
   - Step-by-step execution
   - Validation loops

5. **Utility scripts**
   - For fragile/error-prone operations
   - Handle errors gracefully
   - No voodoo constants (document all values)

### ❌ DON'T (from research)

1. **Windows-style paths** (`\` instead of `/`)
2. **Deeply nested references** (>1 level deep)
3. **Time-sensitive info** ("as of August 2025...")
4. **Assume tools installed** (always specify dependencies)
5. **Too many options** (provide default, mention alternatives)
6. **Vague descriptions** ("Helps with documents")

---

## Migration Strategy

### Command → Skill Decision Matrix

| Command | Convert to Skill? | Why / Why Not |
|---------|------------------|---------------|
| `/extract-daily-content` | ✅ **Yes** | Daily workflow → auto-trigger |
| `/remember`, `/recall` | ✅ **Yes** | Knowledge capture → natural logging |
| `/vault-add` | ✅ **Yes** | File operations → PARA detection |
| `/accountant` | ✅ **Yes** | Financial queries → natural Q&A |
| `/mokai-status` | ⚠️ **Hybrid** | Keep as fallback, skill auto-triggers |
| `/create-command` | ❌ **No** | Explicit action, not conversational |
| `/issue-create` | ❌ **No** | GitHub integration, needs confirmation |
| `/git/commit` | ❌ **No** | Explicit version control action |

### Hybrid Model (Best of Both)

Some workflows benefit from **both** skill + command:

**Example: MOKAI Status**
- **Skill** (`mokai-daily-ops`): Auto-triggers from "What should I work on?"
- **Command** (`/mokai-status`): Manual fallback if skill missed context

**Example: Knowledge Logging**
- **Skill** (`knowledge-capture`): Auto-logs insights from conversation
- **Command** (`/remember`): Explicit manual logging if needed

---

## Rollout Plan

### Week 1: Foundation
- [ ] Create skill directory structure
- [ ] Migrate `daily-workflow/` skill
- [ ] Test with natural conversation
- [ ] Update README with testing guide

### Week 2: Knowledge Systems
- [ ] Implement `knowledge-capture/` skill
- [ ] Integrate Graphiti + Serena memory patterns
- [ ] Test auto-logging from conversation
- [ ] Document group ID conventions

### Week 3: Vault + Finance
- [ ] Deploy `vault-operations/` skill
- [ ] Deploy `financial-assistant/` skill
- [ ] Test PARA categorization
- [ ] Validate tax calculations

### Week 4: Task Integration
- [ ] Build `task-orchestration/` skill
- [ ] Integrate with Task Master MCP
- [ ] Test auto-status updates
- [ ] Refine trigger descriptions

### Ongoing: Maintenance
- [ ] Monitor skill trigger accuracy
- [ ] Refine descriptions if over/under-triggering
- [ ] Deprecate redundant slash commands
- [ ] Update Serena memory with skill patterns

---

## Success Metrics

### Skill Health Indicators

Track in `.claude/skills/.metrics.json`:

```json
{
  "skills": {
    "daily-workflow": {
      "triggers_last_30d": 45,
      "false_positives": 2,
      "avg_token_usage": 1200,
      "user_satisfaction": "high"
    },
    "knowledge-capture": {
      "triggers_last_30d": 28,
      "graphiti_stores": 23,
      "serena_updates": 5,
      "user_satisfaction": "medium"
    }
  },
  "command_deprecation": {
    "/extract-daily-content": "deprecated - use daily-workflow skill",
    "/remember": "deprecated - use knowledge-capture skill"
  }
}
```

### Performance Goals

- **Trigger accuracy**: >95% (triggers when expected)
- **False positive rate**: <5% (doesn't trigger when shouldn't)
- **Token efficiency**: SKILL.md <500 lines, references <1000 lines
- **User satisfaction**: Reduces manual command usage by 60%+

---

## Implementation Checklist

### For Each Skill

```markdown
- [ ] Create skill directory: `.claude/skills/<skill-name>/`
- [ ] Write concise SKILL.md (<500 lines)
- [ ] Add reference files (if needed, 1 level deep)
- [ ] Create utility scripts (with error handling)
- [ ] Test trigger detection (natural phrases)
- [ ] Validate MCP integration
- [ ] Update `.claude/skills/README.md`
- [ ] Add to testing guide
- [ ] Update Serena memory (if skill changes workflows)
- [ ] Deprecate redundant slash command (if applicable)
```

### Quality Gates

Before deploying skill:
1. ✅ Description tested with 5+ natural phrases
2. ✅ All file references load correctly (forward slashes)
3. ✅ Scripts execute without errors
4. ✅ MCP tools tested in isolation
5. ✅ Token usage measured (<500 lines SKILL.md)
6. ✅ User tested in real conversation
7. ✅ Documented in README
8. ✅ Serena memory updated

---

## Next Immediate Steps

### Priority 1: Daily Workflow Skill
1. Create `.claude/skills/daily-workflow/` directory
2. Write SKILL.md based on existing `/extract-daily-content` command
3. Add reference files for templates and formatting
4. Test trigger: "What did I work on today?"
5. Validate extraction logic with Serena MCP

### Priority 2: Knowledge Capture Skill
1. Create `.claude/skills/knowledge-capture/` directory
2. Design Graphiti storage patterns (GRAPHITI.md)
3. Design Serena memory patterns (MEMORY.md)
4. Test trigger: "I learned that..."
5. Validate Graphiti + Serena integration

### Priority 3: Vault Operations Skill
1. Create `.claude/skills/vault-operations/` directory
2. Document PARA categorization logic
3. Add frontmatter validation script
4. Test trigger: "Create a note for..."
5. Validate file placement accuracy

---

## Resources & References

### Documentation
- **SKILLz.md**: [04-resources/research/SKILLz.md](../04-resources/research/SKILLz.md)
- **Existing Skills**: `.claude/skills/mokai-daily-ops/`, `.claude/skills/mokhouse-operations/`
- **Slash Commands**: `.claude/commands/` (conversion candidates)
- **Serena Memories**: `.serena/memories/` (code architecture context)

### Tools & Integration
- **Serena MCP**: File operations, pattern matching, memory management
- **Graphiti MCP**: Knowledge graph storage (group IDs: mokai, mokhouse, finance, tech)
- **Supabase MCP**: Database queries (project: `gshsshaodoyttdxippwx`)
- **Task Master MCP**: Project/task management
- **Obsidian Vault**: `/Users/harrysayers/Developer/claudelife`

### Testing
- Restart Claude Code after skill changes
- Test with natural conversation (not just trigger phrases)
- Monitor token usage (`SKILL.md` <500 lines)
- Track false positives/negatives
- Refine descriptions based on behavior

---

**Status**: Ready for Phase 1 implementation. Start with `daily-workflow/` skill.
