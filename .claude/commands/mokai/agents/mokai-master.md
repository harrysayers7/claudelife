---
created: "2025-10-17 14:30"
updated: "2025-10-21 10:15"
version_history:
  - version: "1.4"
    date: "2025-10-21 10:15"
    changes: "Added Hybrid Command-Skill Architecture section documenting Claude Code Skills integration - mokai-daily-ops skill for automatic assistance alongside explicit commands"
  - version: "1.3"
    date: "2025-10-21 09:30"
    changes: "Added MOKAI Command Ecosystem section documenting /mokai-status, /mokai-weekly, /mokai-wins, /mokai-dump integration with tracker, diary, and dashboard systems"
  - version: "1.2"
    date: "2025-10-17 16:15"
    changes: "Clarified Graphiti vs Serena decision matrix - Graphiti for facts/relationships (What/Who), Serena for processes/patterns (How), excluded Financial Standards until validated"
  - version: "1.1"
    date: "2025-10-17 15:45"
    changes: "Added hybrid knowledge storage (automatic Graphiti + suggested Serena)"
  - version: "1.0"
    date: "2025-10-17 14:30"
    changes: "Initial creation with hybrid lazy-smart loading"
description: |
  MOKAI Master Primer - Loads essential MOKAI business context into the conversation using hybrid lazy-smart loading.

  Capabilities:
    - Loads core business model, Indigenous thresholds, service timelines
    - Queries Graphiti for active clients, contractors, tenders (if recent data exists)
    - Reads current dashboard for weekly focus and priorities
    - Maps knowledge sources (Graphiti, Serena, Operations Guide) for intelligent querying
    - Hybrid knowledge storage: automatic Graphiti (relationships), suggested Serena (patterns)
    - Enables conversational MOKAI assistance without heavy sub-agent invocation

  Outputs:
    - MOKAI domain context loaded into main conversation
    - Current business status snapshot (phase, focus, recent wins)
    - Smart routing instructions for deeper queries
    - Automatic knowledge capture during conversations
    - Ready for strategic, compliance, finance, or operations discussions
examples:
  - /mokai-master
  - /mokai-master --refresh (reload current state)
---

# MOKAI Master Primer

This command loads essential MOKAI business context into the main conversation, enabling intelligent business assistance without invoking heavy sub-agents. Uses hybrid lazy-smart loading for token efficiency while maintaining comprehensive domain awareness.

## Purpose

Transform the main Claude conversation into a MOKAI-aware business partner by:
- Loading core business model and Indigenous procurement advantages
- Establishing knowledge source hierarchy (Graphiti → Serena → Operations Guide)
- Checking current business status (dashboard, phase focus)
- Enabling smart routing to specialized knowledge as needed

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

## Shortcut Name Rules

When user says:
- **"MK"** or **"mk"** → means **MOKAI** (this business)
- **"MH"** or **"mh"** → means **MOK HOUSE**
- **"PC"** → means **Panda Candy**

## Usage

```bash
/mokai-master           # Load MOKAI context
/mokai-master --refresh # Reload current state (dashboard, Graphiti)
```

## What Gets Loaded

### Immediate Load (Always - ~1,200 tokens)

1. **Business Model Essentials**
   - Core services: Cybersecurity (pen testing, GRC, IRAP, architecture reviews)
   - Operating model: Prime contractor managing compliance/insurance/assurance
   - Unique value: Indigenous-owned enabling direct procurement (IPP, Exemption 16, Supply Nation)
   - Future vision: Automation consulting, managed solutions, SaaS compliance products

2. **Indigenous Procurement Thresholds**
   - IPP Direct Procurement: Under $80,000 (no tender required)
   - Mandatory Set-Aside (MSA): $80k-$200k (must offer to Indigenous businesses first)
   - Exemption 16: ANY size contract (direct award with value for money)
   - Supply Nation: 51%+ Aboriginal ownership required (annual audit)

3. **Service Delivery Standards**
   - Essential Eight Assessment: 5 days
   - IRAP Assessment: 2-6 months (4 phases)
   - Penetration Testing: 4-6 weeks
   - GRC Consulting: 4-8 weeks (risk assessment)

4. **Financial Operations Standards**
   - Services margin: 20-40% (e.g., $800/day contractor → $1,000-$1,300 client rate)
   - Products margin: 10-15% (software/hardware reselling)
   - Cash flow: Pay contractors Net 14, clients pay Net 30+
   - Insurance: PI $1M-$5M, PL $10M, Workers Comp, Cyber Liability

5. **Current Phase Focus**
   - Read: `/01-areas/business/mokai/mokai-dashboard.md` (This Week's Focus section)
   - Phase 1 Foundation status (if active)

### Smart Context Check (Conditional - ~1,000 tokens if exists)

If Graphiti has recent MOKAI data (last 7 days):
- Load active clients
- Load available contractors
- Load current tender opportunities

Else: Skip, query on demand during conversation

### Lazy Load (During Conversation)

Query these sources intelligently based on user questions:

1. **Graphiti Knowledge Graph** (fastest - check first)
   - Client relationships, contractor capabilities
   - Service patterns, tender requirements
   - Business insights from past conversations
   - Vendor/product relationships

2. **Serena Memories** (fast - check second)
   - `mokai_business_patterns.md` - Persistent MOKAI patterns
   - `suggested_commands.md` - Available workflows
   - System-level knowledge

3. **Operations Guide** (moderate - query specific sections)
   - Location: `/01-areas/business/mokai/docs/research/📘 - OPERATIONS GUIDE.md`
   - Use Serena search for specific procedures only when needed
   - Don't read entire guide, query relevant sections

4. **Live Data** (when current state matters)
   - Dashboard: `/01-areas/business/mokai/mokai-dashboard.md`
   - Diary: `/01-areas/business/mokai/diary/YYYY-MM-DD.md`
   - Supabase: Project `gshsshaodoyttdxippwx` (financial data)

## Process

When `/mokai-master` is executed:

### Step 1: Load Core Knowledge

Output to user:
```
✅ MOKAI Master Context Loading...

📊 Business Model: Indigenous technology consultancy (cybersecurity focus)
🎯 Indigenous Advantages: IPP (<$80k), MSA ($80k-$200k), Exemption 16 (any size)
⏱️  Service Timelines: E8 (5 days), IRAP (2-6mo), PenTest (4-6wk), GRC (4-8wk)
💰 Margins: Services (20-40%), Products (10-15%)
```

### Step 2: Check Current Business Status

Read dashboard for:
- This Week's Focus
- Recent Wins
- Current Blockers
- Phase 1 status (if active)

Output to user:
```
📅 Current Focus: [This Week's Focus from dashboard]
🏆 Recent Wins: [Top 2-3 wins]
🚧 Active Blockers: [Current blockers if any]
```

### Step 3: Smart Graphiti Check

Query Graphiti for recent MOKAI entities:
```javascript
// Search for active clients, contractors, tenders from last 7 days
mcp__graphiti-mokai__search_nodes({
  query: "clients contractors tenders active recent"
})
```

If results found:
```
🔗 Graphiti Context: Loaded 3 clients, 2 contractors, 1 tender
```

Else:
```
🔗 Graphiti: No recent data, will query on demand
```

### Step 4: Establish Knowledge Sources

Output to user:
```
📚 Knowledge Sources Mapped:
  1. Graphiti (fastest) - Client/contractor relationships, patterns
  2. Serena Memories - Business patterns, workflows
  3. Operations Guide - Detailed procedures (query on demand)
  4. Live Data - Dashboard, diary, Supabase

Ready for MOKAI discussions: strategy, compliance, finance, operations
```

### Step 5: Smart Routing Intelligence

Enable intelligent query routing based on user questions:

**Client/Contractor Questions** → Query Graphiti first
```javascript
mcp__graphiti-mokai__search_nodes({
  query: "[client_name] [contractor_name] capabilities projects"
})
```

**Procedure Questions** → Query Serena for Operations Guide section
```javascript
mcp__serena__search_for_pattern({
  substring_pattern: "IRAP Assessment|Tender Response|Contractor Vetting",
  relative_path: "01-areas/business/mokai/docs/research/📘 - OPERATIONS GUIDE.md",
  context_lines_after: 20
})
```

**Current Status Questions** → Read dashboard/diary
```javascript
mcp__serena__search_for_pattern({
  substring_pattern: "This Week's Focus|Recent Wins|Blockers",
  relative_path: "01-areas/business/mokai/mokai-dashboard.md",
  context_lines_after: 10
})
```

**Strategic Questions** → Consider escalating to sub-agent
```
"This involves complex strategic trade-offs. Should I engage mokai-business-strategist?"
```

### Step 6: Hybrid Knowledge Storage (Automatic + Suggested)

Enable intelligent knowledge capture during MOKAI conversations using hybrid approach:

#### Automatic Storage (Silent - Graphiti)

**What gets stored automatically:**
- Client/contractor mentions and relationships
- Rate updates and availability changes
- Project outcomes and learnings
- Tender requirements discovered
- Client-specific preferences

**Detection triggers:**
```javascript
// Automatic Graphiti storage when detecting:
- "Client X needs..." / "Client X prefers..."
- "Contractor Y rate is $X/day"
- "Department Z requires..."
- "Tender ABC needs..."
- "We worked with..." / "Project involved..."

// Example automatic storage:
User: "John Smith's rate is now $900/day, not $800"

Claude: [Detects: contractor rate update]
        [Automatically stores in Graphiti]
        🔗 Updated: John Smith → $900/day

        (Continues conversation seamlessly)
```

**Graphiti storage pattern:**
```javascript
mcp__graphiti-mokai__add_memory({
  content: `During MOKAI discussion on ${date}:

  Entity: ${entity_name} (${entity_type})
  Relationship: ${relationship_description}
  Context: ${conversation_context}

  Example: "Contractor John Smith increased rate to $900/day.
  Available Q1 2025. Specializes in IRAP assessments, holds PROTECTED clearance."`
})
```

#### Suggested Storage (Ask User - Serena)

**What gets suggested for Serena:**
- New business process patterns
- Strategic decision frameworks
- "We always..." / "Standard practice is..."
- Lessons learned that apply broadly
- Workflow improvements

**Detection triggers:**
```javascript
// Suggest Serena storage when detecting:
- "We always..." / "Our standard approach..."
- "Going forward, let's..."
- "This worked well, we should..."
- "The pattern I've noticed is..."
- "From now on..."

// Example suggested storage:
User: "Going forward, we'll always require 30% deposit for IRAP assessments over $100k"

Claude: [Detects: new business pattern]

        💡 Pattern Detected

        Should I store this in Serena as a standard MOKAI practice?
        - Pattern: "IRAP deposits: 30% required for projects >$100k"
        - Category: Financial operations
        - Applies to: All future IRAP work

        [Yes] [No, just this project] [Customize pattern]
```

**Serena storage pattern:**
```javascript
// If user confirms:
mcp__serena__write_memory({
  memory_name: "mokai_business_patterns",
  content: `## Financial Operations

### IRAP Assessment Deposits
- **Threshold**: Projects >$100k
- **Deposit**: 30% upfront
- **Rationale**: Cash flow protection for long-duration assessments
- **Added**: ${date}
- **Context**: [Link to conversation/decision]`
})
```

#### Knowledge Capture Decision Matrix

**Graphiti = "What/Who" (Facts & Relationships)**
Store factual, relational data that represents entities and their connections:

| Category | Storage | Action | Examples |
|---|---|---|---|
| **Team & People** | Graphiti | Auto | "Harry Sayers (CEO, 51% owner)", "Jack Bell (CTO, contractor network)" |
| **Services & Pricing** | Graphiti | Auto | "Essential Eight: 5 days", "IRAP: 2-6 months, 4 phases" |
| **Indigenous Procurement** | Graphiti | Auto | "IPP: <$80k", "MSA: $80k-$200k", "Exemption 16: any size" |
| **Current Business State** | Graphiti | Auto | "Phase 1: Foundation", "Blocker: Jack's trust setup" |
| **Client Requirements** | Graphiti | Auto | "DoD requires PROTECTED clearance" |
| **Contractor Rates** | Graphiti | Auto | "John Smith $900/day, IRAP specialist" |
| **Project Outcomes** | Graphiti | Auto | "Tender ABC won for $200k" |
| **Client Preferences** | Graphiti | Auto | "Acme Corp wants 4-week turnaround" |
| **Vendor Relationships** | Graphiti | Auto | "Partner with Vendor X for firewalls" |

**Serena = "How" (Processes & Patterns)**
Store process patterns, workflows, and "how-to" knowledge for reuse:

| Category | Storage | Action | Examples |
|---|---|---|---|
| **Contractor Management** | Serena | Suggest | "Vet contractors: Check clearance, verify certifications, test engagement" |
| **Project Delivery** | Serena | Suggest | "IRAP workflow: Kickoff → Assessment → Report → Debrief" |
| **Quality Assurance** | Serena | Suggest | "Jack reviews all deliverables before client submission" |
| **Client Communication** | Serena | Suggest | "DoD prefers weekly status reports on IRAP" |
| **New Process Patterns** | Serena | Suggest | "Always use 30% deposit for IRAP >$100k" |
| **Strategic Decisions** | Serena | Suggest | "Focus on MSA tier ($80k-$200k) for Q1" |
| **Lessons Learned** | Serena | Suggest | "Schedule IRAP assessments 2 weeks out minimum" |
| **Meeting Best Practices** | Serena | Suggest | "Kickoff meetings: Tech + business stakeholders present" |

**Exclusions & Special Cases:**

| Type | Storage | Reasoning |
|---|---|---|
| **Financial Standards** (margins, payment terms) | Neither (for now) | Not yet validated - exclude until confirmed accurate |
| **One-time notes** | Neither | "Check email for tender deadline" - transient, not reusable |
| **Speculative information** | Neither | Wait for confirmation before storing |

#### End-of-Conversation Summary (Optional)

At natural conversation breaks, optionally suggest knowledge capture:

```
💾 Knowledge Capture Summary

I noticed we discussed:
1. ✅ Auto-stored in Graphiti:
   - Client: Department of Defence (PROTECTED clearance required)
   - Contractor: John Smith ($900/day, available Q1)

2. 💡 Patterns detected (store in Serena?):
   - "DoD IRAP projects require weekly status reports"
   - "Always schedule IRAP assessments 2 weeks out minimum"

Would you like me to store these patterns for future MOKAI work? [Yes/No/Customize]
```

## Smart Detection Examples

### Example 1: Tender Question

```
User: "Should we bid on this $150k IRAP tender for Department of Defence?"

Claude (with /mokai-master loaded):
1. Detect: tender + compliance domain
2. Query Graphiti: "Department of Defence IRAP contractors"
3. Check Serena: bid/no-bid criteria from Operations Guide
4. Apply core knowledge: $150k = MSA range, IRAP = 2-6 months

Response: "Based on MOKAI context:
- $150k falls in MSA range ($80k-$200k) - Indigenous advantage
- IRAP timeline: 2-6 months (need contractor availability)
- [Graphiti result: Available IRAP-certified contractors]
- DoD likely requires PROTECTED clearance
- Recommendation: [strategic analysis]"
```

### Example 2: Client Relationship Question

```
User: "What's our relationship with Client X?"

Claude (with /mokai-master loaded):
1. Query Graphiti: "Client X projects services history"
2. If found: Return relationship context
3. If not found: Check Supabase for client records

Response: "[Graphiti/Supabase context about Client X]"
```

### Example 3: Service Delivery Question

```
User: "What's the Essential Eight assessment process?"

Claude (with /mokai-master loaded):
1. Check core knowledge: 5-day timeline loaded
2. User wants detailed process → Query Operations Guide via Serena

Response: "Essential Eight Assessment (5 days):
[Retrieved from Operations Guide via Serena search]
- Day 1: Kickoff meeting
- Days 2-4: Assessment execution
- Day 5: Report delivery and debrief"
```

## Output Format

After loading `/mokai-master`, provide:

```
✅ MOKAI Master Context Loaded

📊 Business Model: Indigenous tech consultancy (cybersecurity)
🎯 Indigenous Advantages: IPP, MSA, Exemption 16
⏱️  Service Timelines: E8 (5d), IRAP (2-6mo), PenTest (4-6wk), GRC (4-8wk)
💰 Financial Standards: Services 20-40%, Products 10-15%

📅 Current Focus: [This Week's Focus]
🏆 Recent Wins: [Top wins]
🚧 Blockers: [If any]

🔗 Graphiti: [Loaded X clients, Y contractors, Z tenders | Query on demand]
📚 Knowledge Sources: Graphiti → Serena → Ops Guide → Live Data

Ready for MOKAI strategy, compliance, finance, or operations discussions.
```

## Refresh Command

Use `--refresh` to reload current state without reloading core knowledge:

```bash
/mokai-master --refresh
```

This re-reads:
- Dashboard (updated weekly focus, wins, blockers)
- Graphiti recent data
- Today's diary note

Useful after:
- Running `/mokai-status` or `/mokai-weekly` (updates dashboard)
- Major business developments (new client, tender win)
- Weekly planning sessions

## Evaluation Criteria

A successful `/mokai-master` load should:

1. ✅ **Core Knowledge Accessible**
   - Can answer Indigenous threshold questions immediately
   - Can provide service timelines without querying
   - Can explain business model without reading files

2. ✅ **Current Context Loaded**
   - Knows this week's focus
   - Aware of recent wins and blockers
   - Has phase status if Phase 1 active

3. ✅ **Smart Routing Enabled**
   - Queries Graphiti for client/contractor questions
   - Uses Serena for Operations Guide sections
   - Reads live data when current state matters
   - Suggests sub-agent for complex strategy

4. ✅ **Token Efficient**
   - Upfront load: 1,200-2,500 tokens (depending on Graphiti)
   - No unnecessary file reads
   - Queries on demand based on questions

5. ✅ **Conversational Ready**
   - Main Claude maintains conversation continuity
   - No sub-agent invocation for standard questions
   - Escalates to specialist only when truly complex

## Related Resources

- MOKAI Dashboard: `/01-areas/business/mokai/mokai-dashboard.md`
- Operations Guide: `/01-areas/business/mokai/docs/research/📘 - OPERATIONS GUIDE.md`
- Diary Location: `/01-areas/business/mokai/diary/YYYY-MM-DD.md`
- Serena Memories: `.serena/memories/mokai_business_patterns.md`
- Graphiti MCP: `mcp__graphiti-mokai__*` tools
- Sub-agents: `.claude/agents/mokai-business-strategist.md`, `.claude/agents/mokai-legal-finance-advisor.md`

## Hybrid Command-Skill Architecture

MOKAI uses **both Claude Code Skills and Slash Commands** for different workflows:

### 🎯 Skills (Automatic Assistance)
Skills auto-trigger when user discusses relevant topics. No explicit invocation needed.

**Location**: `.claude/skills/mokai-daily-ops/`

- **`mokai-daily-ops`** - Auto-manages daily status when user mentions:
  - MOKAI tasks, progress, or status
  - "What should I work on?"
  - Wins, blockers, learnings
  - Task priorities
  - Workflow: Scans diary → Scans inbox tasks → Updates tracker → Updates dashboard → Reports strategic status
  - **References**: See [SKILL.md](.claude/skills/mokai-daily-ops/SKILL.md) for full workflow
  - **Same workflow as `/mokai-status`** but auto-detected vs manually invoked

### 🔵 Commands (Explicit Rituals)
Commands are user-invoked for structured, intentional workflows.

**When to use commands**:
- `/mokai-master` - Explicit context loading when starting MOKAI work
- `/mokai-weekly` - Weekly review ritual (every Friday)
- `/mokai-status` - Manual status check (fallback if skill doesn't trigger)
- `/mokai-wins` - Quick win logging
- `/mokai-dump` - Bulk diary entry with AI categorization

### 🔄 How They Work Together

**Typical flow**:
1. User says: "Let's work on MOKAI" → `/mokai-master` (manual)
2. User says: "What should I focus on?" → `mokai-daily-ops` skill (auto)
3. User shares achievement → `mokai-daily-ops` logs it automatically
4. Friday → User runs `/mokai-weekly` (manual ritual)

**Skills advantages**:
- ✅ No need to remember commands
- ✅ Natural conversation flow
- ✅ Automatic context capture
- ✅ Progressive disclosure (loads references only when needed)

**Commands advantages**:
- ✅ Explicit control over timing
- ✅ Clear ritual structure
- ✅ Guaranteed execution
- ✅ Familiar workflow

## MOKAI Command Ecosystem

After loading `/mokai-master`, you have access to these specialized commands:

### Daily Operations Commands
- **`/mokai-status`** - Read diary notes, extract updates, provide strategic status with dynamic task management
  - Uses Serena for pattern matching in diary files
  - Updates Phase 1 checklist automatically
  - Scans `/00-inbox/tasks/` for MOKAI tasks (grouped by priority: urgent/high/normal)
  - Updates dashboard with wins/blockers/focus (deduplicates automatically)
  - Reads tracker (`.mokai-tracker.json`) to track processed files and current phase/week
  - Provides strategic status report with next action guidance

- **`/mokai-wins`** - Quick win logging to today's diary note
  - Finds or creates today's diary note from template
  - Adds win to "🏆 Wins" section
  - Fast (<30 seconds), no manual diary editing needed

- **`/mokai-dump`** - Quick capture with AI categorization
  - Analyzes sentiment/content to auto-categorize entries (Wins/Learnings/Blockers/Context)
  - Supports multiple entries in one command
  - Creates diary note from template if doesn't exist
  - Optional `--date` parameter for backdated entries

### Weekly Review Commands
- **`/mokai-weekly`** - Weekly review and planning
  - Uses Serena to aggregate week's diary notes
  - Analyzes Phase 1 checklist progress (completed vs. incomplete)
  - Compares week-over-week trends (if memory exists)
  - Interactive reflection (asks for biggest win, blocker, progress rating)
  - Updates Phase 1 checklist (marks completed, rolls forward incomplete)
  - Stores insights in Serena memory (`mokai_progress_metrics`, `mokai_weekly_insights`)
  - Updates tracker (increments week, sets new currentWeekStart)

### Strategic Commands
- **`/mokai-insights`** - Extract patterns and insights (if implemented)
- **`/mokai-bas`** - BAS/accounting support (if implemented)

### Sub-Agents (Complex Analysis)
- **`mokai-business-strategist`** - Strategic trade-offs, market positioning, growth planning
- **`mokai-legal-finance-advisor`** - Legal/financial guidance, contract review, compliance structures

### Key Integration Points

**Tracker System** (`.mokai-tracker.json`):
- Stores: processedFiles (diary dates), currentWeekStart, weekInPhase, lastProcessed
- Used by: `/mokai-status`, `/mokai-weekly`
- Prevents re-processing stable diary entries (but always re-reads today's note)

**Diary System** (`/01-areas/business/mokai/diary/`):
- Format: `YYYY-MM-DD-mokai-daily.md`
- Sections: What I Did Today, 💡 Learnings, 🏆 Wins, 🚨 Blockers, 📝 Context/Updates, 🎯 Tomorrow's Focus
- Template: `/98-templates/mokai-note.md`
- Frontmatter: `journal: Mokai Daily 🟣`, `journal-date: YYYY-MM-DD`

**Phase 1 Checklist** (`/01-areas/business/mokai/status/phase-1-foundation.md`):
- Tracks week-by-week learning goals
- Updated by: `/mokai-status` (auto-check completed tasks), `/mokai-weekly` (roll forward incomplete)
- Provides: This Week's Focus for dashboard

**Dashboard** (`/01-areas/business/mokai/mokai-dashboard.md`):
- Sections: This Week's Focus, Inbox Tasks, Recent Wins, Blockers, Weekly Scorecard
- Updated by: `/mokai-status`, `/mokai-weekly`
- Deduplicates wins/blockers automatically (fuzzy match 80%+)

**Inbox Tasks** (`/00-inbox/tasks/*.md`):
- Frontmatter filter: `relation: mokai`, `type: Task`
- Status field: `Done: true/false`
- Priority: `urgent|high|low` (or empty = normal)
- Scanned by `/mokai-status` to surface urgent items

## Notes

- **Persistence**: Context persists for entire conversation
- **Refresh**: Use `--refresh` to update current state
- **Token cost**: ~1,200-2,500 tokens upfront, minimal per-question
- **Scalability**: As MOKAI grows, we query intelligently vs. loading everything
- **Graphiti integration**: Automatically leverages knowledge graph when available
- **Sub-agent escalation**: Only suggest for truly complex strategic decisions
