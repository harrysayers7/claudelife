---
date created: Tue, 10 21st 25, 6:16:13 am
date modified: Tue, 10 21st 25, 6:17:17 am
---

---

## **1. STREAMS → Continuous Work Outside Projects**

**Problem PARA doesn't solve**: Music production, creative work, and ongoing client relationships aren't "projects" (finite end date) or "areas" (ongoing responsibility). They're **streams of activity** that ebb and flow.

**Add to your structure:**
```
01-areas/
├── business/ (existing)
├── fitness/ (existing)
├── learning/ (existing)
└── streams/
    ├── music-production/
    │   ├── active-sessions/
    │   ├── client-work/
    │   └── creative-experiments/
    ├── sonic-branding/
    └── cybersecurity-consulting/ (non-MOKAI work)
```

**Why for you**: Your SAFIA work, Electric Sheep Music projects, and ad-hoc consulting don't have clear "project" boundaries but need organization. Streams capture ongoing creative/professional flows.

---

## **2. LABS → Experimental Zone**

**Problem PARA doesn't solve**: Where do half-baked ideas, automation experiments, and "what if I tried..." go? Inbox clogs fast, Resources is too formal.

**Add:**
```
02-labs/
├── automation-experiments/
│   ├── obsidian-supabase-sync.md
│   └── mcp-server-ideas.md
├── music-tech/
│   ├── new-plugin-tests.md
│   └── production-workflow-v2.md
├── ai-experiments/
└── crypto-research/
```

**Why for you**: Your automation stack (MCP servers, Supabase, n8n) + your creative tech interests (AI, music tech) = constant experimentation. Labs gives these a home without cluttering PARA.

**Automation hook**: Auto-archive Labs items older than 90 days that haven't moved to Projects/Resources.

---

## **3. TEMPO Layer → Time-Based Views Across PARA**

**Problem PARA doesn't solve**: You track daily patterns (meditation, walks, cold swims, fasting) but PARA is domain-based, not time-based. You need both.

**Add temporal dashboards that *pull from* PARA:**
```
00-inbox/
├── 01-today/ (your existing structure - good!)
├── 02-this-week/
└── 03-this-month/

Plus TEMPO queries:
- Today: Tasks from all Areas due today
- This Week: Active Projects + Weekly reviews
- This Month: Area goals + Monthly retrospectives
```

**Why for you**: Your Sunday self-audits, morning routines, and tracking systems need a temporal layer. TEMPO queries pull from PARA but organize by time.

**Automation hook**:
- Auto-populate `01-today/` with tasks from Areas/Projects every morning
- Sync with your Supabase `personal_accounts` table for financial tracking

---

## **4. EVERGREEN → Permanent Knowledge Outside PARA**

**Problem PARA doesn't solve**: Atomic, timeless notes (Zettelkasten-style) don't fit cleanly into Projects or Resources. You're already halfway there with `97-tags/`.

**Enhance your structure:**
```
05-evergreen/
├── concepts/ (atomic ideas)
│   ├── e-iso27001-control-families.md
│   ├── e-wim-hof-breathing.md
│   └── e-sonic-branding-principles.md
├── frameworks/ (mental models)
│   ├── e-para-method.md
│   └── e-spaced-repetition.md
└── principles/ (life/business rules)
    ├── e-intermittent-fasting.md
    └── e-security-first-development.md
```

**Why for you**: Your MOKAI learning (ISO controls, Essential Eight) + personal practices (Wim Hof, fasting) + music production knowledge = permanent notes that transcend projects.

**Integration with existing**: `97-tags/` becomes your MOC (Maps of Content) layer that connects Evergreen notes. Tags = hubs, Evergreen = spokes.

---

## **5. PIPELINES → Intermediate States in Processing**

**Problem PARA doesn't solve**: Not everything goes from Inbox → Archive in one step. You need intermediate states for half-processed items.

**Add sub-states:**
```
00-inbox/
├── 00-raw/ (Web Clipper dumps, voice memos)
├── 01-processing/ (being worked on)
├── 02-review/ (ready for final placement)
└── 03-hold/ (waiting on external input)
```

**Why for you**: Your Web Clipper + voice memo workflows need triage. Raw capture → processing → placement = clear pipeline.

**Automation hook**:
- Items in `00-raw/` older than 3 days? Alert to process or auto-archive
- Use MCP to auto-categorize based on content (music → streams, security → MOKAI, health → fitness)

---

## **6. VAULT-IN-VAULT → Domain Isolation**

**Problem PARA doesn't solve**: Music production brain vs. cybersecurity compliance brain have different contexts. Mixing them creates cognitive overhead.

**Your current structure already hints at this:**
```
01-areas/
├── business/mokai/ (isolated compliance vault)
├── business/mok-house/ (isolated music business)
└── personal/fitness/ (isolated health tracking)
```

**Why for you**: Keep them separate mentally. When in MOKAI mode, you don't need to see music production notes cluttering searches.

**Automation hook**: Context-aware dashboards that only show relevant domain:
- Morning: Fitness + Personal
- 10am-3pm: MOKAI + Business
- Evening: Music + Creative

---

## **7. SPACED REPETITION INTEGRATION**

**Problem PARA doesn't solve**: Your flashcards (`mokai-operations-flashcards.md`) and learning system exist separately from PARA. Integrate them.

**Add:**
```
01-areas/learning/
├── 00-active/ (current learning)
├── 01-review/ (spaced repetition tracking) ← You have this!
├── 02-mastered/ (graduated knowledge) ← You have this!
└── 03-teaching/ (ready to teach others = true mastery)
```

**Why for you**: Your MOKAI course structure already uses this! Expand it across all learning (music theory, production techniques, etc).

**Automation hook**:
- Auto-promote notes from Active → Review → Mastered based on review count
- Daily digest: "5 cards due for review today"

---

## **Recommended PARA+ Architecture for You**

```
claudelife/
├── 00-inbox/
│   ├── 00-raw/
│   ├── 01-processing/
│   └── 02-review/
│
├── 01-areas/ (EXISTING - keep structure)
│   ├── business/
│   ├── fitness/
│   └── personal/
│
├── 02-streams/ (NEW - continuous work)
│   ├── music-production/
│   ├── sonic-branding/
│   └── consulting/
│
├── 03-labs/ (NEW - experiments)
│   ├── automation/
│   ├── music-tech/
│   └── ai-research/
│
├── 04-resources/ (EXISTING)
│
├── 05-evergreen/ (NEW - permanent knowledge)
│   ├── concepts/
│   ├── frameworks/
│   └── principles/
│
├── 06-archives/ (EXISTING - done/inactive)
│
└── 97-tags/ (EXISTING - MOCs/hubs)
```

---

## **Automation Opportunities**

Your Supabase + MCP + n8n stack can power:

1. **Smart Inbox Routing**:
   - Web Clipper → Content analysis → Auto-route to Stream/Area/Lab

2. **TEMPO Queries**:
   - Dataview queries that pull from all PARA folders but display by time

3. **Review Reminders**:
   - Spaced repetition triggers via n8n → Daily digest of due cards

4. **Context Switching**:
   - Raycast command: "MOKAI mode" → Dashboard shows only MOKAI-related notes
   - "Music mode" → Only production/creative content

5. **Auto-Archive**:
   - Labs items >90 days inactive → Archive
   - Inbox items >7 days → Alert

---

## **What to Implement First**

**Phase 1 (This Week)**:
1. Add `02-streams/` for music production work
2. Add `03-labs/` for experiments
3. Create TEMPO daily query (pull today's tasks from all domains)

**Phase 2 (Next Week)**:
1. Build `05-evergreen/` and move atomic notes from Resources
2. Enhance `97-tags/` to be proper MOCs linking Evergreen notes

**Phase 3 (Month 1)**:
1. Automate inbox routing via MCP
2. Build context-switching Raycast shortcuts
3. Spaced repetition auto-promotion system

---

**Bottom line**: Your current PARA structure is solid. Add **Streams** (continuous work), **Labs** (experiments), **Evergreen** (permanent knowledge), and **TEMPO queries** (time-based views). Leverage your automation stack to make these dynamic, not static folders.

Want me to build any of these systems (DataviewJS queries, MCP automation, Raycast shortcuts)?
