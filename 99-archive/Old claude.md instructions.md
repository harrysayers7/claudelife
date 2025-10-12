---
date created: Sun, 10 12th 25, 5:31:30 am
date modified: Sun, 10 12th 25, 5:35:34 am
---
omain Packs (Load on Keyword Trigger)

**Business Pack (~15K)** → .claude/instructions/business-pack.md
- **Triggers**: "MOKAI", "mokai", "cybersecurity", "compliance", "IRAP", "Essential8", "tender", "government", "mok house", "music business"
- **Contains**: MOKAI profile, services, MOK HOUSE, active projects, financial context

**Technical Pack (~15K)** → .claude/instructions/technical-pack.md
- **Triggers**: "MCP", "database", "supabase", "API", "FastAPI", "infrastructure", "server", "docker", "n8n"
- **Contains**: Supabase schema, ML pipeline, MCP servers, server infrastructure, development tools

**Automation Pack (~10K)** → .claude/instructions/automation-pack.md
- **Triggers**: "workflow", "automation", "trigger", "schedule", "integration", "sync"
- **Contains**: UpBank sync, financial ML pipeline, context sync, n8n workflows, error recovery patterns

Advanced Loading Patterns (From Context Engineering)
- **Predictive loading**: Pattern recognition to preload relevant context
- **Graduated loading**: Essential (10K) → mentioned entities (30K) → full context (50K)
- **Context compression**: Summarize older context when approaching token limits
- **Confidence thresholds**: Load context based on relevance confidence scores (0.8+ auto-load)

### Token Budgets
- **Typical conversation**: 8K core + 15K single pack = **23K total** ✅
- **Cross-domain**: 8K core + 30K (2 packs) = **38K total** (rare)
- **Emergency**: 8K core + 42K (all packs) = **50K max** (fallback only)
ontext File References
- **Core Context**: `memory/conversation-context.md`, `memory/active-entities.json`
- **Business Pack**: `.claude/instructions/business-pack.md`
- **Technical Pack**: `.claude/instructions/technical-pack.md`
- **Automation Pack**: `.claude/instructions/automation-pack.md`

### Active Entity Management
- **7-day retention window**: Entities mentioned in last 7 days stay in `active-entities.json`
- **Smart entity subset**: Key business contacts, recent projects, active workflows
- **Gap detection**: When entity mentioned but not in active → search full `entities.json` → load related pack
- **Automatic refresh**: Entity activity updates retention window
FastAPI MCP Usage Rules**

  ### ALWAYS use FastAPI Business API for:
  - Vendor/supplier compliance (IRAP, Essential8, SOC2)
  - Government tender searches
  - MOKAI business metrics (revenue, pipeline, KPIs)
  - Client project status
  - Profitability analysis
  - Any MOKAI business operations

  ### Keywords that trigger FastAPI MCP:
  - "vendor", "supplier", "compliance", "IRAP"
  - "tender", "government contract", "AusTender"
  - "business revenue", "pipeline", "MOKAI metrics"
  - "client project", "project status"

  ### Never use for MOKAI business queries:
  - ❌ Web search (outdated/generic)
  - ❌ File reading (use API as source of truth)
  - ❌ Manual calculations (API has the logic)

  Then Claude will know to automatically use FastAPI MCP for
  business operations without you having to specify each
  time!
