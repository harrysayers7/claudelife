# Memory System - Smart Loading Rules

## Architecture: Pragmatic Hybrid

**Core principle**: Load 8K core context + 15K domain pack = 23K typical conversation start

### Token Budgets
- **Core context (always loaded)**: 8K tokens
  - `memory/conversation-context.md` (2K): Last 2 sessions summary
  - `memory/active-entities.json` (6K): Smart entity subset with 7-day retention
- **Single domain pack**: 15K tokens (23K total)
- **Cross-domain**: 30K tokens (38K total, rare)
- **Emergency fallback**: Load all packs if gap detected (50K max)

### Domain Packs (Load on Keyword Trigger)

#### Business Pack (~15K)
**Triggers**: "MOKAI", "mokai", "cybersecurity", "compliance", "IRAP", "Essential8", "tender", "government", "revenue", "mok house", "music business"

**Contents**:
- `01-areas/business/mokai/mokai-profile.md`
- `01-areas/business/mokai/services.md`
- `01-areas/business/mokhouse/mokhouse-profile.md`
- `01-areas/business/projects.md` (active projects only)

#### Technical Pack (~15K)
**Triggers**: "MCP", "database", "supabase", "API", "FastAPI", "infrastructure", "server", "deployment", "docker", "n8n"

**Contents**:
- `context/finance/database/supabase-schema.md`
- `context/finance/database/supabase-purpose.md`
- `context/finance/database/supabase-ml-pipeline.md`
- MCP server configurations
- Infrastructure documentation

#### Automation Pack (~10K)
**Triggers**: "workflow", "automation", "trigger", "schedule", "integration", "sync"

**Contents**:
- `context/automations/workflows.md`
- `context/automations/triggers.md`
- Active automation documentation

### Smart Loading Logic

1. **Session Start**:
   - Auto-load: `conversation-context.md` + `active-entities.json` (8K)
   - Parse user's first message for keyword triggers
   - Load matching domain pack(s)

2. **Mid-Conversation Detection**:
   - If keywords appear that weren't in first message → load additional pack
   - Track loaded packs in `conversation-context.md`

3. **Gap Detection**:
   - If entity mentioned not in active-entities.json → search full entities.json
   - If found: Add to active entities, load related pack
   - If critical context missing: Fallback to load all packs

4. **Entity Pruning** (Weekly via cron):
   - Remove entities with `last_accessed > 7 days ago`
   - Keep entities with `access_count > 10` regardless of age
   - Log pruned items in `pruning_log`

### Loading Examples

**MOKAI compliance question**:
- Core (8K) + Business pack (15K) = 23K total
- Has: Company profile, services, compliance frameworks
- Missing nothing critical

**Database schema question**:
- Core (8K) + Technical pack (15K) = 23K total
- Has: Schema docs, ML pipeline, Supabase config
- Missing nothing critical

**Cross-domain (rare)**:
- "How do I automate MOKAI tender tracking in Supabase?"
- Core (8K) + Business (15K) + Technical (15K) = 38K total
- Acceptable for complex queries

**Gap detected**:
- User mentions entity not in active-entities.json
- Search full entities.json, add to active
- Load related pack immediately
- If still unclear → fallback load all packs (50K emergency mode)

### Maintenance

**Daily** (automatic):
- Update `conversation-context.md` with session summary
- Update entity `last_accessed` timestamps

**Weekly** (cron job):
- Run entity pruning (7-day retention)
- Compact entity graph if needed
- Archive old conversation contexts

**Monthly**:
- Review pack sizes (should stay ~15K each)
- Rebalance if growth detected
- Archive unused entities

### Success Metrics
- 90% conversations: <25K tokens loaded
- 10% complex conversations: <40K tokens loaded
- 0% critical context gaps
- 100% context continuity between sessions
