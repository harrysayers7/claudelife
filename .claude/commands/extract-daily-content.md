---
created: "2025-10-17 10:00"
updated: "2025-10-19 11:00"
version_history:
  - version: "1.1"
    date: "2025-10-19 11:00"
    changes: "Diary → Context transformation: Extract facts, remove narrative, bullet point format for context files"
  - version: "1.0"
    date: "2025-10-17 10:00"
    changes: "Initial creation with AI-powered routing system"
description: |
  Smart extraction system that analyzes daily note entries and routes them to appropriate files.

  This command:
    - Scans daily notes for content in ### 🧠 Notes sections
    - Uses AI to classify entries (Diary/Insight/Context/Idea)
    - Analyzes relevance to all areas in 01-areas/ (business, health, tech, etc.)
    - Routes to multiple destinations based on confidence (>80%)
    - Transforms diary narratives into factual context entries
    - Shows reasoning for each routing decision
    - Requires manual approval before committing
    - Creates cross-links between main files and area-specific files
    - Auto-creates diary files for each area as needed (diary-[area].md)

  Context files receive factual bullet points (no dates, no narrative).
  Diary files preserve original narrative with date headers.
examples:
  - /extract-daily-content
---

# Extract Daily Content (Smart AI Routing)

This command uses AI to intelligently classify and route your daily notes to the right places across your knowledge system.

## Usage

```bash
/extract-daily-content
```

## What This Command Does

**IMPORTANT**: This command uses AI classification with manual override. You'll review the routing plan before any changes are committed.

### Process Flow

1. **Scan daily notes** in `/Users/harrysayers/Developer/claudelife/00 - Daily`
2. **Extract entries** from `### 🧠 Notes` sections
3. **AI Classification** for each entry:
   - Classify type (Diary/Insight/Context/Idea)
   - Analyze relevance to all 24 context areas
   - Determine routing destinations with confidence scores
4. **Extract & Reformulate**:
   - **For CONTEXT files**: Transform diary narrative → factual knowledge
     - Extract only topically relevant facts (tools, decisions, patterns, technical details)
     - Rephrase to third-person, remove dates/pronouns/temporal markers
     - Remove: feelings, uncertainty, filler words, personal asides
     - Format: Bullet points with cross-links (no date headers)
   - **For DIARY files**: Keep original narrative format with date headers
5. **Present routing plan** with reasoning and reformulated content
6. **Manual approval** (y/n/edit)
7. **Execute routing** and create cross-links with reformulated content
8. **Update tracker** with processing details

## Routing Rules

### 1. Diary Entries
- **Primary**: `04-resources/diary.md` (always)
- **Secondary** (if >80% confidence): `[area]/diary-[area].md`
  - Example: `business/mokai/diary-mokai.md`
  - Auto-created if doesn't exist

### 2. Insights
- **Primary**: `01-areas/p-dev/insights.md` (always)
- **Secondary**: Never to context files (insights ≠ context)

### 3. Context Entries
- **Primary**: `04-resources/context.md` (always)
- **Secondary** (if >80% confidence): Matching `context-*.md` files
  - Must be Context-type to route to context files
  - Can go to multiple context files

### 4. Ideas
- **Primary**: `04-resources/ideas.md` (always)
- **Secondary**: Never to context files

## Available Context Areas (24 files)

The AI will check relevance against all these areas:

**Business** (8):
- `business/mokai/context-mokai.md`
- `business/mokhouse/context-mokhouse.md`
- `business/accounting/context-accounting.md`
- `business/crypto/context-crypto.md`
- `business/soletrader/context-soletrader.md`
- `business/SMSF/context-smsf.md`
- `business/safia/context-safia.md`
- `business/trust/context-trust.md`

**Personal Development** (3):
- `p-dev/learning/context-learning.md`
- `p-dev/mindset/context-mindset.md`
- `p-dev/psychedelics/context-psychedelics.md`

**Health & Fitness** (4):
- `health-fitness/context-health-fitness.md`
- `health-fitness/diet/context-diet.md`
- `health-fitness/medical/context-medical.md`
- `health-fitness/gym/context-gym.md`

**Tech** (5):
- `tech/context-tech.md`
- `tech/ableton/context-ableton.md`
- `tech/mac/context-mac.md`
- `tech/ai/context-ai.md`
- `tech/ai/research-ai/context-engineering/context-engineering.md`

**Other** (3):
- `claude-code/context-claudecode.md`
- `harry/context-harry.md`
- `people/context-people.md`

## AI Classification Examples

### Example 1: MOKAI Business Context
**Entry**: "MOKAI uses Indigenous procurement advantage for direct government access under IPP"

**AI Response**:
```json
{
  "type": "context",
  "confidence": 0.96,
  "reasoning": "Factual information about business practice",
  "routing": {
    "primary": "04-resources/context.md",
    "secondary": [
      {
        "file": "business/mokai/context-mokai.md",
        "confidence": 0.98,
        "reasoning": "Direct MOKAI business strategy reference"
      },
      {
        "file": "harry/context-harry.md",
        "confidence": 0.87,
        "reasoning": "Personal Indigenous identity context"
      }
    ]
  }
}
```

### Example 2: MOK HOUSE Project Diary
**Entry**: "Finished mixing Nintendo Family Friends - client approved final version"

**AI Response**:
```json
{
  "type": "diary",
  "confidence": 0.94,
  "reasoning": "Daily activity log, project completion",
  "routing": {
    "primary": "04-resources/diary.md",
    "secondary": [
      {
        "file": "business/mokhouse/diary-mokhouse.md",
        "confidence": 0.97,
        "reasoning": "MOK HOUSE client project completion"
      }
    ]
  }
}
```

### Example 3: Health Insight
**Entry**: "Realized that morning workouts give me more energy throughout the day"

**AI Response**:
```json
{
  "type": "insight",
  "confidence": 0.91,
  "reasoning": "Personal discovery about health routine",
  "routing": {
    "primary": "01-areas/p-dev/insights.md",
    "secondary": []
  }
}
```
*Note: Insights never go to context files, even if health-related*

### Example 4: Multi-Area Context
**Entry**: "Use SMSF contributions for crypto investments with proper ATO documentation"

**AI Response**:
```json
{
  "type": "context",
  "confidence": 0.93,
  "reasoning": "Financial strategy information",
  "routing": {
    "primary": {
      "file": "04-resources/context.md",
      "content": "- SMSF contributions strategy: Crypto investments with ATO compliance\n  *From:* [[04-resources/diary#25-10-19 - Sun]]\n  *Related:* [[business/SMSF/context-smsf]], [[business/crypto/context-crypto]], [[business/accounting/context-accounting]]"
    },
    "secondary": [
      {
        "file": "business/SMSF/context-smsf.md",
        "confidence": 0.96,
        "reasoning": "SMSF investment strategy",
        "content": "- Investment approach: Crypto assets via SMSF contributions with ATO documentation\n  *From:* [[04-resources/diary#25-10-19 - Sun]]\n  *Related:* [[business/crypto/context-crypto]], [[business/accounting/context-accounting]]",
        "relatedContextFiles": ["business/crypto/context-crypto.md", "business/accounting/context-accounting.md"]
      },
      {
        "file": "business/crypto/context-crypto.md",
        "confidence": 0.92,
        "reasoning": "Crypto investment approach",
        "content": "- Crypto investment method: SMSF contributions with proper ATO compliance\n  *From:* [[04-resources/diary#25-10-19 - Sun]]\n  *Related:* [[business/SMSF/context-smsf]], [[business/accounting/context-accounting]]",
        "relatedContextFiles": ["business/SMSF/context-smsf.md", "business/accounting/context-accounting.md"]
      },
      {
        "file": "business/accounting/context-accounting.md",
        "confidence": 0.84,
        "reasoning": "ATO compliance requirement",
        "content": "- ATO compliance: Documentation required for SMSF crypto investments\n  *From:* [[04-resources/diary#25-10-19 - Sun]]\n  *Related:* [[business/SMSF/context-smsf]], [[business/crypto/context-crypto]]",
        "relatedContextFiles": ["business/SMSF/context-smsf.md", "business/crypto/context-crypto.md"]
      }
    ]
  }
}
```

### Example 5: Diary → Context Transformation

**Diary Entry**: "Today I built a Supabase database for financial tracking for MOKAI. Took forever to set up auth but got it working. Will use for invoice management."

**AI Response**:
```json
{
  "type": "context",
  "confidence": 0.88,
  "reasoning": "Technical implementation detail with business context",
  "routing": {
    "primary": {
      "file": "04-resources/context.md",
      "content": "- Supabase database implemented for financial tracking\n  *From:* [[04-resources/diary#25-10-19 - Sun]]\n  *Related:* [[tech/context-tech]], [[business/mokai/context-mokai]]"
    },
    "secondary": [
      {
        "file": "tech/context-tech.md",
        "confidence": 0.94,
        "reasoning": "Database technology stack",
        "content": "- Supabase: Financial tracking database with auth\n  *From:* [[04-resources/diary#25-10-19 - Sun]]\n  *Related:* [[business/mokai/context-mokai]]",
        "relatedContextFiles": ["business/mokai/context-mokai.md"]
      },
      {
        "file": "business/mokai/context-mokai.md",
        "confidence": 0.91,
        "reasoning": "MOKAI financial infrastructure",
        "content": "- Financial tracking system: Supabase database for invoice management\n  *From:* [[04-resources/diary#25-10-19 - Sun]]\n  *Related:* [[tech/context-tech]]",
        "relatedContextFiles": ["tech/context-tech.md"]
      }
    ]
  }
}
```
*Note: Same diary entry becomes different factual statements for each context area. Personal details ("took forever", feelings) removed.*

## Manual Override Workflow

### Interactive Approval

After AI analysis, you'll see:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Extraction Plan for [[25-10-17 - Fri]]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Entry 1: "MOKAI uses Indigenous procurement..."
  Type: Context (96% confidence)
    Reason: Factual business practice information

  Primary: 04-resources/context.md
  Secondary:
    ✓ business/mokai/context-mokai.md (98%)
      → Direct MOKAI business strategy reference
    ✓ harry/context-harry.md (87%)
      → Personal Indigenous identity context

Entry 2: "Finished mixing Nintendo track..."
  Type: Diary (94% confidence)
    Reason: Daily activity log, project completion

  Primary: 04-resources/diary.md
  Secondary:
    ✓ business/mokhouse/diary-mokhouse.md (97%)
      → MOK HOUSE client project completion

Entry 3: "Need to buy milk tomorrow"
  Type: Diary (99% confidence)
    Reason: Personal task/reminder

  Primary: 04-resources/diary.md
  Secondary: None

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Actions: [y]es / [n]o / [e]dit / [s]kip entry
```

### Edit Mode

If you choose `edit`, you can:
- Change entry type
- Add/remove routing destinations
- Adjust which files receive the content
- Skip specific entries

## Cross-Linking Format

### In Main Files

**Primary destination** (`04-resources/context.md`):
```markdown
### [[25-10-17 - Fri]]

MOKAI uses Indigenous procurement advantage for direct government access under IPP

*Also in:* [[business/mokai/context-mokai]], [[harry/context-harry]]

---
```

### In Area Context Files

**Context file format** (`business/mokai/context-mokai.md`):
```markdown
- Accountant recommended trust structure for MOKAI financial protection
  *From:* [[04-resources/diary#25-10-17 - Fri]]
  *Related:* [[business/accounting/context-accounting]]
```

*Note: Context files use bullet points (no date headers). Content is reformulated as factual statements.*

### In Area Diary Files

**Diary file format** (`business/mokhouse/diary-mokhouse.md`):
```markdown
## [[25-10-17 - Fri]]

Completed mixing for Nintendo Family Friends track. Client approved final version.

*From:* [[04-resources/diary#25-10-17 - Fri]]

---
```

*Note: Diary files preserve date headers and original narrative format.*

## Auto-Created Diary Files

When a diary entry is routed to an area for the first time, a diary file is created:

**File**: `business/mokai/diary-mokai.md`

```markdown
---
type: diary
area: mokai
date created: "2025-10-17 10:00"
---
# MOKAI Diary

Business-related diary entries for MOKAI operations.

---

## [[25-10-17 - Fri]]

Had productive meeting with MOKAI client about IRAP assessment

*From:* [[04-resources/diary#25-10-17 - Fri]]

---
```

## Tracking System

**Tracker Location**: `/Users/harrysayers/Developer/claudelife/.claude/commands/.extract-daily-content-tracker.json`

**Tracker Format**:
```json
{
  "last_scan": "2025-10-17T10:00:00Z",
  "processed_files": {
    "25-10-17 - Fri.md": {
      "extracted_at": "2025-10-17T10:00:00Z",
      "modified_at": "2025-10-17T09:30:00Z",
      "entries_processed": 5,
      "routing": [
        {
          "entry": "MOKAI uses Indigenous...",
          "type": "context",
          "confidence": 0.96,
          "destinations": [
            "04-resources/context.md",
            "business/mokai/context-mokai.md",
            "harry/context-harry.md"
          ]
        },
        {
          "entry": "Finished mixing Nintendo...",
          "type": "diary",
          "confidence": 0.94,
          "destinations": [
            "04-resources/diary.md",
            "business/mokhouse/diary-mokhouse.md"
          ]
        }
      ]
    }
  }
}
```

## Implementation Steps

### 1. Load Tracker & Scan Notes

```javascript
const trackerPath = '.claude/commands/.extract-daily-content-tracker.json';
const dailyNotesPath = '00 - Daily';

// Load or create tracker
let tracker = loadTracker(trackerPath);

// Find new/modified daily notes
const notesToProcess = findNewOrModifiedNotes(dailyNotesPath, tracker);
```

### 2. Extract & Classify Entries

```javascript
for (const note of notesToProcess) {
  const content = readFile(note);

  // Extract ### 🧠 Notes section
  const thoughtsMatch = content.match(/###\s*🧠\s*Notes\n([\s\S]*?)(?=\n##|\n---|$)/);

  if (!thoughtsMatch) continue;

  // Parse entries (bullets or paragraphs)
  const entries = parseEntries(thoughtsMatch[1]);

  // Classify each entry with AI
  for (const entry of entries) {
    const classification = await classifyWithAI(entry, contextAreas);
    routingPlan.push({ note, entry, classification });
  }
}
```

### 3. AI Classification & Extraction Prompt

```
You are analyzing a personal note entry for classification, routing, and content extraction.

Entry: "{entry}"

Context Areas Available:
- Business: MOKAI (Indigenous cybersecurity consultancy), MOK HOUSE (music production), accounting, crypto, SMSF, soletrader, safia, trust
- Personal Dev: learning, mindset, psychedelics
- Health & Fitness: general, diet, medical, gym
- Tech: general, ableton, mac, ai, engineering
- Other: claude-code, harry (personal identity), people

Task:
1. Classify the entry type (diary/insight/context/idea)
2. Provide confidence (0-1)
3. Explain reasoning
4. Identify ALL relevant context areas (>0.8 confidence)
5. **For CONTEXT files, transform diary narrative into factual knowledge:**
   - Extract ONLY sentences/phrases relevant to that specific area
   - Rephrase to third-person factual statements
   - Example: "Today I built a Supabase database for MOKAI" → "Supabase database used for financial tracking (MOKAI)"
   - Remove: dates, personal pronouns (I, me, my), temporal markers (today, yesterday)
   - Remove: feelings, uncertainty, filler words ("like", "I guess", "probably")
   - Keep: tools/tech used, decisions made, patterns discovered, technical details
   - Format: Single bullet point with cross-links (NO date headers)
6. **For DIARY files, keep original narrative format**
   - Preserve first-person voice and temporal context
   - Include date headers (## [[YYYY-MM-DD - Day]])

Rules:
- Only Context-type entries go to context-*.md files
- Diary entries can go to diary-*.md files
- Insights only go to insights.md (never context files)
- Be precise with confidence scores
- **Each context destination gets custom factual extraction**
- **Include cross-links to source diary + all related context files**

Output JSON format:
{
  "type": "context|diary|insight|idea",
  "confidence": 0.95,
  "reasoning": "Why this classification",
  "routing": {
    "primary": {
      "file": "main file path",
      "content": "Full diary entry (original for diary, factual for context)"
    },
    "secondary": [
      {
        "file": "area/context-area.md",
        "confidence": 0.96,
        "reasoning": "Why this area is relevant",
        "content": "Factual bullet point with cross-links",
        "relatedContextFiles": ["other/context-files.md", "another/context.md"]
      }
    ]
  }
}

Example for "Today I built a Supabase database for MOKAI financial tracking":
{
  "secondary": [
    {
      "file": "tech/context-tech.md",
      "content": "- Supabase: Financial tracking database\n  *From:* [[04-resources/diary#25-10-19 - Sun]]\n  *Related:* [[business/mokai/context-mokai]]",
      "relatedContextFiles": ["business/mokai/context-mokai.md"]
    },
    {
      "file": "business/mokai/context-mokai.md",
      "content": "- Financial tracking system: Supabase database for invoice management\n  *From:* [[04-resources/diary#25-10-19 - Sun]]\n  *Related:* [[tech/context-tech]]",
      "relatedContextFiles": ["tech/context-tech.md"]
    }
  ]
}
```

### 4. Present Plan & Get Approval

```javascript
// Show routing plan
console.log(formatRoutingPlan(routingPlan));

// Get user input
const response = await getUserInput('Proceed? (y/n/e/s): ');

if (response === 'y') {
  executeRouting(routingPlan);
} else if (response === 'e') {
  editRoutingPlan(routingPlan);
} else if (response === 's') {
  // Skip specific entries
}
```

### 5. Execute Routing

```javascript
for (const plan of routingPlan) {
  // Append to primary destination
  appendWithCrossLinks(plan.classification.routing.primary, plan.entry, plan.classification.routing.secondary);

  // Append to secondary destinations
  for (const dest of plan.classification.routing.secondary) {
    if (dest.confidence >= 0.8) {
      // Auto-create diary file if needed
      if (dest.file.includes('diary-') && !fileExists(dest.file)) {
        createDiaryFile(dest.file);
      }

      appendWithBacklink(dest.file, plan.entry, plan.classification.routing.primary);
    }
  }
}
```

### 6. Update Tracker

```javascript
tracker.processed_files[note.filename] = {
  extracted_at: new Date().toISOString(),
  modified_at: note.modifiedTime,
  entries_processed: entries.length,
  routing: routingPlan.map(p => ({
    entry: p.entry.substring(0, 50) + '...',
    type: p.classification.type,
    confidence: p.classification.confidence,
    destinations: [
      p.classification.routing.primary,
      ...p.classification.routing.secondary.map(s => s.file)
    ]
  }))
};

saveTracker(trackerPath, tracker);
```

## Edge Cases Handled

- **Empty thoughts section**: Skip file
- **No clear classification**: Ask user for manual classification
- **Low confidence (<60%)**: Flag for review
- **Conflicting areas**: Show all matches, let user decide
- **New context areas**: Automatically detect new `context-*.md` files
- **Malformed entries**: Parse gracefully, flag issues
- **Duplicate content**: Check if entry already exists in destination

## Evaluation Criteria

A successful extraction should:

1. ✅ Correctly classify entry types (>90% accuracy over time)
2. ✅ Route to appropriate areas with good confidence
3. ✅ Show clear reasoning for routing decisions
4. ✅ Allow easy manual override
5. ✅ Create valid cross-links bidirectionally
6. ✅ Auto-create diary files with proper frontmatter
7. ✅ Track all routing decisions
8. ✅ Handle incremental runs efficiently
9. ✅ Maintain file integrity across all destinations
10. ✅ Respect >80% confidence threshold for secondary routing

## Troubleshooting

**Issue**: AI misclassifies entries
- **Check**: Review reasoning in routing plan
- **Solution**: Use edit mode to correct, AI will learn from patterns

**Issue**: Too many secondary destinations
- **Check**: Are confidence scores too low?
- **Solution**: Increase threshold in code (currently 0.8)

**Issue**: Diary files not being created
- **Check**: Does entry have diary type?
- **Solution**: Verify auto-creation logic, check file permissions

**Issue**: Missing cross-links
- **Check**: Were files created successfully?
- **Solution**: Verify append operations, check for write errors

## Related Commands

- Archive: `/extract-insights` (old single-purpose command)
- Archive: `/extract-context` (old single-purpose command)
- Archive: `/extract-diary` (old single-purpose command)
- Related: `/update-serena-memory` (memory system)
- Related: `/document-system` (system documentation)

## Maintenance

### View Tracker

```bash
cat .claude/commands/.extract-daily-content-tracker.json | jq '.processed_files | to_entries | last'
```

### Reset Tracker (Force Re-extraction)

```bash
rm .claude/commands/.extract-daily-content-tracker.json
```

### View All Diary Files

```bash
find 01-areas -name "diary-*.md" -type f
```

### Check Context File Coverage

```bash
find 01-areas -name "context-*.md" -type f | wc -l
```

---

**Ready to intelligently extract and route your daily content!**
