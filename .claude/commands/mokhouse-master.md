---
created: "2025-10-18 19:30"
updated: "2025-10-18 19:30"
version_history:
  - version: "1.0"
    date: "2025-10-18 19:30"
    changes: "Initial creation - MOK HOUSE master context loader"
description: |
  MOK HOUSE Master Primer - Loads essential MOK HOUSE business context into the conversation.

  Capabilities:
    - Loads core business model (MOK Music + MOK Studio divisions)
    - Queries Graphiti for client relationships, project outcomes, team members
    - Reads current dashboard for financial overview and weekly focus
    - Maps knowledge sources (Graphiti, Dashboard, Projects) for intelligent querying
    - Automatic knowledge capture for client preferences and project learnings
    - Music-focused context with ESM/Panda Candy submission workflow

  Outputs:
    - MOK HOUSE domain context loaded into main conversation
    - Current business status snapshot (financials, active projects, wins)
    - Smart routing instructions for deeper queries
    - Automatic knowledge capture during conversations
    - Ready for creative, client, or project discussions
examples:
  - /mokhouse-master
  - /mokhouse-master --refresh
---

# MOK HOUSE Master Primer

This command loads essential MOK HOUSE business context into the main conversation, enabling intelligent creative business assistance without invoking heavy sub-agents.

## Purpose

Transform the main Claude conversation into a MOK HOUSE-aware creative partner by:
- Loading core business model and Indigenous positioning
- Establishing knowledge source hierarchy (Graphiti → Dashboard → Projects)
- Checking current business status (financials, active projects)
- Enabling smart routing to specialized knowledge as needed

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

## Shortcut Name Rules

When user says:
- **"MH"** or **"mh"** → means **MOK HOUSE** (this business, all caps, two words)
- **"PC"** → means **Panda Candy**
- **"MK"** or **"mk"** → means **MOKAI**

**Voice Transcription Note**: When Harry says "mock house" or "mok house", he means **MOK HOUSE**.

## Usage

```bash
/mokhouse-master           # Load MOK HOUSE context
/mokhouse-master --refresh # Reload current state (dashboard, Graphiti)
```

## What Gets Loaded

### Immediate Load (Always - ~1,500 tokens)

1. **Business Model Essentials**
   - **MOK Music**: Composition, sonic branding, sound design, voice-over, live bookings
   - **MOK Studio**: Branding, digital design, web, social content, paid media (future division)
   - Target market: Government/corporate with RAP and IPP commitments
   - Positioning: Boutique creative between large agencies and small studios

2. **Indigenous Positioning**
   - 100% Indigenous-owned (Harry Sayers)
   - Supply Nation certification pending
   - Eligible for IPP procurement pathways
   - Compliance-ready delivery (WCAG, government procurement)

3. **Pricing Context**
   - **MOK Music**: $5,000–$30,000+ per project
   - **MOK Studio** (future):
     - Branding: $7,500–$35,000
     - Websites: $10,000–$50,000
     - Retainers: $5,000–$15,000/month

4. **ESM/Panda Candy Submission Workflow**
   - Harry submits demo to ESM or Panda Candy
   - Competes against 3-4 other composers
   - Agency sends demos to client for selection
   - **If Won**: Usage fee ($2,500–$8,000)
   - **If Not Won**: Demo fee ($250–$1,000)

5. **Team Structure**
   - **Harry Sayers**: Owner, Composer, Director (100% shareholder)
   - **Kell Mendoza**: Operations Director, co-decisions with Harry
   - **Glenn**: ESM Producer/Creative Director
   - **Kate Stenhouse**: ESM Project Manager

6. **Current Financial Status**
   - Read: `/01-areas/business/mokhouse/mokhouse-dashboard.md`
   - Load: Total Paid, Outstanding, Active Projects
   - Show: This Week's Focus, Recent Wins

### Smart Context Check (Conditional - ~800 tokens if exists)

If Graphiti has recent MOK HOUSE data (last 7 days):
- Load client relationships and preferences
- Load recent project outcomes
- Load team member context

Else: Skip, query on demand during conversation

### Lazy Load (During Conversation)

Query these sources intelligently based on user questions:

1. **Graphiti Knowledge Graph** (fastest - check first)
   - Client relationships and creative preferences
   - Project outcomes and budgets
   - Team member roles and expertise
   - Winning patterns (why projects were won)
   - Invoice/PO numbers for specific projects

2. **Dashboard** (fast - check second)
   - Location: `/01-areas/business/mokhouse/mokhouse-dashboard.md`
   - Financial overview (paid, outstanding, pending)
   - Active projects and priorities
   - Recent wins and client relationships

3. **Project Files** (moderate - query specific projects)
   - Location: `/02-projects/mokhouse/`
   - Individual project details (briefs, creative direction, financials)
   - Client feedback and learnings
   - Technical requirements

4. **Diary Notes** (when timeline matters)
   - Location: `/01-areas/business/mokhouse/diary/YYYY-MM-DD-mokhouse-daily.md`
   - Daily creative work, client communications
   - Wins, learnings, insights
   - Context for future conversations

5. **Context Files** (detailed business info)
   - Location: `/01-areas/business/mokhouse/context-mokhouse.md`
   - `/01-areas/business/mokhouse/mokhouse-profile.md`
   - Business model details, financial context

## Process

When `/mokhouse-master` is executed:

### Step 1: Load Core Knowledge

Output to user:
```
✅ MOK HOUSE Master Context Loading...

📊 Business Model: Creative house (MOK Music + MOK Studio)
🎯 Divisions: Music (active), Studio (future branding/design)
💰 Music Pricing: $5k-$30k+ projects | $250-$1k demo fees | $2.5k-$8k usage fees
🏆 Indigenous Advantage: 100% Indigenous-owned, Supply Nation pending
👤 Team: Harry (Owner/Composer), Kell (Operations), Glenn (ESM), Kate (ESM)
```

### Step 2: Check Current Business Status

Read dashboard for:
- Financial overview (paid, outstanding, pending)
- This Week's Focus
- Recent Wins
- Active Projects

Output to user:
```
💰 Financials: $X paid | $X outstanding | $X pending
🎵 Active Projects: [Count and key projects]
🏆 Recent Wins: [Top 1-2 wins]
📅 This Week's Focus: [From dashboard]
```

### Step 3: Smart Graphiti Check

Query Graphiti for recent MOK HOUSE entities:
```javascript
// Search for clients, projects, team members from last 7 days
mcp__graphiti__search_memory_nodes({
  query: "MOK HOUSE clients projects team creative preferences",
  max_nodes: 10
})
```

If results found:
```
🔗 Graphiti Context: Loaded X clients, Y projects, Z team members
```

Else:
```
🔗 Graphiti: No recent data, will query on demand
```

### Step 4: Establish Knowledge Sources

Output to user:
```
📚 Knowledge Sources Mapped:
  1. Graphiti (fastest) - Client relationships, project outcomes, team
  2. Dashboard - Financial overview, active projects, priorities
  3. Project Files - Detailed briefs, creative direction, financials
  4. Diary - Daily creative work, learnings, timeline context

Ready for MOK HOUSE discussions: creative, clients, projects, financials
```

### Step 5: Smart Routing Intelligence

Enable intelligent query routing based on user questions:

**Client/Project Financial Questions** → Query Graphiti + Dashboard
```javascript
// Example: "How much was the Nintendo job?"
mcp__graphiti__search_memory_facts({
  query: "Nintendo budget invoice usage fee",
  max_facts: 5
})

// Fallback: Read project file
mcp__serena__find_file({
  file_mask: "*nintendo*.md",
  relative_path: "02-projects/mokhouse"
})
```

**Creative Direction Questions** → Read Project Files
```javascript
// Example: "What was the Nintendo brief?"
mcp__serena__search_for_pattern({
  substring_pattern: "CREATIVE DIRECTION|TONE & EMOTION",
  relative_path: "02-projects/mokhouse/036-nintendo",
  context_lines_after: 20
})
```

**Financial Overview Questions** → Read Dashboard
```javascript
// Example: "What's outstanding?"
Read: /01-areas/business/mokhouse/mokhouse-dashboard.md
```

**Timeline Questions** → Query Diary
```javascript
// Example: "What did I work on last week?"
mcp__serena__list_dir({
  relative_path: "01-areas/business/mokhouse/diary",
  recursive: false
})
```

### Step 6: Automatic Knowledge Capture (Graphiti)

Enable intelligent knowledge capture during MOK HOUSE conversations:

**What gets stored automatically (silent):**
- Client creative preferences and feedback
- Project outcomes (won/lost, budgets, invoice numbers)
- Team member expertise and roles
- Winning patterns ("Won because X, Y, Z")
- Creative direction that resonated
- Technical requirements and formats

**Detection triggers:**
```javascript
// Automatic Graphiti storage when detecting:
- "Nintendo wants..." / "Client prefers..."
- "We won this project because..."
- "Invoice #ABC123 for $X"
- "Glenn suggested..." / "Kate mentioned..."
- "This creative direction worked well..."
- "PO number XYZ for project ABC"

// Example automatic storage:
User: "Won Nintendo Exchange Mode - $3,250 usage fee. Client loved the sweet, endearing tone."

Claude: [Detects: project win with creative insight]
        [Automatically stores in Graphiti]
        🔗 Stored: Nintendo Exchange Mode win ($3,250)
        💡 Pattern: "Sweet, endearing tone" resonates with Nintendo

        (Continues conversation seamlessly)
```

**Graphiti storage pattern:**
```javascript
mcp__graphiti__add_memory({
  name: "MOK HOUSE project outcome - Nintendo Exchange Mode",
  episode_body: `During MOK HOUSE discussion on 2025-10-18:

  Project: Nintendo Exchange Mode
  Client: Nintendo (via Electric Sheep Music)
  Outcome: WON
  Budget: $3,250 usage fee
  Creative Direction: Sweet, endearing, story-focused
  Client Feedback: "Loved the tone - adorable sigh at the end"
  Why Won: Followed reference track closely, polished production
  Invoice: [Invoice number]
  PO: [PO number if available]

  Pattern: Nintendo responds well to heartwarming, story-driven scores with Japanese influences.`,
  group_id: "mokhouse",
  source: "message"
})
```

**What to capture for each project:**
- Client name and preferences
- Budget (demo fee, usage fee, total)
- Won/Lost status and why
- Invoice/PO numbers
- Creative direction that worked
- Client feedback (quoted)
- Team members involved
- Technical requirements

## Smart Detection Examples

### Example 1: Financial Question

```
User: "How much was the Nintendo job?"

Claude (with /mokhouse-master loaded):
1. Query Graphiti: "Nintendo budget usage fee invoice"
2. If found: Return from Graphiti
3. If not found: Read 02-projects/mokhouse/036-nintendo/251017-nintendo.md

Response: "Nintendo Exchange Mode:
- Usage Fee: $3,250 (won)
- Demo Fee: $650
- Invoice #: [from metadata]
- Status: [Current status]"
```

### Example 2: Creative Direction Question

```
User: "What was the Nintendo brief about?"

Claude (with /mokhouse-master loaded):
1. Query Graphiti: "Nintendo creative direction tone"
2. Read project file for detailed brief
3. Return creative direction + client feedback

Response: "Nintendo Exchange Mode brief:
- Tone: Sweet, endearing, story-focused
- Client want: 'Like reference but better'
- Key: Heartwarming score with 'adorable sigh' moment
- Instrumentation: Piano, strings, taiko, woodwinds
[Full creative details from project file]"
```

### Example 3: Winning Pattern Analysis

```
User: "Why did we win the GWM project?"

Claude (with /mokhouse-master loaded):
1. Query Graphiti: "GWM project won creative direction"
2. Read project file for client feedback
3. Identify winning factors

Response: "GWM Tank 500 win factors:
- [Creative approach that resonated]
- [Client feedback]
- [Technical execution]
Pattern: [What made this successful]"
```

### Example 4: Team Context

```
User: "Who should I contact at ESM for this brief?"

Claude (with /mokhouse-master loaded):
1. Check loaded team context
2. Query Graphiti for ESM contacts

Response: "ESM team contacts:
- Glenn: Producer/Creative Director (creative discussions)
- Kate Stenhouse: Project Manager (briefs, deadlines, admin)
Use for: [Context-appropriate recommendation]"
```

## Output Format

After loading `/mokhouse-master`, provide:

```
✅ MOK HOUSE Master Context Loaded

📊 Business: MOK Music (active) + MOK Studio (future)
🎵 Submission Model: ESM/Panda Candy → Demo fee ($250-$1k) or Usage fee ($2.5k-$8k)
💰 Financials: $X paid | $X outstanding | $X pending
👤 Team: Harry, Kell, Glenn (ESM), Kate (ESM)

🎵 Active Projects: [Count and key submissions]
🏆 Recent Wins: [Top wins]
📅 This Week's Focus: [From dashboard]

🔗 Graphiti: [Loaded X clients, Y projects | Query on demand]
📚 Knowledge Sources: Graphiti → Dashboard → Projects → Diary

Ready for MOK HOUSE creative, client, or project discussions.
```

## Refresh Command

Use `--refresh` to reload current state without reloading core knowledge:

```bash
/mokhouse-master --refresh
```

This re-reads:
- Dashboard (updated financials, wins, focus)
- Graphiti recent data
- Today's diary note (if exists)

Useful after:
- Winning/completing a project
- Sending invoices or receiving payments
- Major creative developments
- Weekly planning sessions

## Evaluation Criteria

A successful `/mokhouse-master` load should:

1. ✅ **Core Knowledge Accessible**
   - Can answer ESM/Panda Candy workflow questions immediately
   - Can provide pricing context without querying
   - Can explain business model and divisions
   - Knows team members and their roles

2. ✅ **Current Context Loaded**
   - Knows this week's focus and active projects
   - Aware of financial status (paid, outstanding, pending)
   - Has recent wins loaded

3. ✅ **Smart Routing Enabled**
   - Queries Graphiti for client/project questions
   - Reads Dashboard for financial overview
   - Accesses Project Files for creative details
   - Checks Diary for timeline context

4. ✅ **Token Efficient**
   - Upfront load: 1,500-2,500 tokens (depending on Graphiti)
   - No unnecessary file reads
   - Queries on demand based on questions

5. ✅ **Conversational Ready**
   - Main Claude maintains conversation continuity
   - Automatic knowledge capture for learnings
   - No sub-agent invocation needed for standard questions

## Related Resources

- MOK HOUSE Dashboard: `/01-areas/business/mokhouse/mokhouse-dashboard.md`
- Profile: `/01-areas/business/mokhouse/mokhouse-profile.md`
- Context: `/01-areas/business/mokhouse/context-mokhouse.md`
- Projects: `/02-projects/mokhouse/`
- Diary: `/01-areas/business/mokhouse/diary/YYYY-MM-DD-mokhouse-daily.md`
- Graphiti MCP: `mcp__graphiti__*` tools (consider creating mokhouse-specific group)

## When to Use Specialized Commands

After loading `/mokhouse-master`, you can activate focused modes:

- **Create project**: `/mokhouse-create-project` (existing command)
- **Create invoice**: `/mokhouse-create-invoice` (existing command)
- **Update status**: `/mokhouse-update-status` (existing command)
- **Mark paid**: `/mokhouse-mark-paid` (existing command)
- **Portfolio work**: `/mokhouse-portfolio-blurb` (existing command)

## Notes

- **Persistence**: Context persists for entire conversation
- **Refresh**: Use `--refresh` to update current state
- **Token cost**: ~1,500-2,500 tokens upfront, minimal per-question
- **Scalability**: As MOK HOUSE grows, query intelligently vs. loading everything
- **Graphiti integration**: Automatically captures client preferences and project learnings
- **Music-focused**: Primary context is MOK Music; MOK Studio is future expansion
- **Voice transcription**: "mock house"/"mok house" → **MOK HOUSE**
