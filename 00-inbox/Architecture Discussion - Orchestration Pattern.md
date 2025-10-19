---
date: "2025-10-17"
type: Research
status: Active Discussion
---

# Architecture Discussion: Claude Code Orchestration Pattern

## Context
Discussion about optimal architecture for claudelife - balancing sub-agents vs slash commands, conversational AI vs one-shot execution, and token efficiency.

## Key Decisions Made

### 1. Main Claude = Second Brain Orchestrator
- **You (main Claude)** should be Harry's conversational second brain
- **Sub-agents** are specialists you consult, not separate interfaces
- **Pattern**: Harry talks to you → You orchestrate → You call specialists when needed

### 2. OBSIDIA Evolution
- Originally: Massive 440-line agent prompt (token-heavy, not conversational)
- **New approach**: Lightweight orchestrator that pulls knowledge from:
  - Serena memories (system patterns, workflows)
  - Graphiti knowledge graph (component relationships)
  - Context7 (library documentation on-demand)

### 3. Sub-Agents vs Slash Commands

#### Use Slash Commands For:
- ✅ Context loading (`/mokai-primer`, `/finance-primer`)
- ✅ Workflows (`/mokhouse-create-invoice`, `/mokai-weekly`)
- ✅ Mode switching (`/mokai-strategy`, `/mokai-compliance`)
- ✅ Data operations (`/mokai-status`, `/mokai-dump`)
- ✅ Conversational continuity (context persists after loading)

#### Use Sub-Agents For:
- ✅ Complex strategic decisions (mokai-business-strategist)
- ✅ Legal/compliance review (mokai-legal-finance-advisor)
- ✅ Code architecture design (strategic-planner)
- ✅ Deep technical builds (trigger-dev-expert)
- ✅ When you need a fundamentally different thinking style

### 4. Agent-MOKAI Should Be Decomposed

**Current problem**: 669-line agent with embedded knowledge
- Too token-heavy
- Not conversational
- Hard to maintain

**Proposed solution**: Break into slash commands
```
.claude/commands/mokai/
├── mokai-primer.md              # Loads all MOKAI context
├── mokai-strategy.md            # Strategic planning mode
├── mokai-compliance.md          # Tenders/IPP mode
├── mokai-finance.md            # Financial operations mode
├── mokai-operations.md         # Daily ops mode
├── mokai-status.md            # Daily status (existing)
├── mokai-weekly.md            # Weekly review (existing)
└── mokai-insights.md          # Deep analysis (existing)
```

**Benefits**:
- Lightweight (50-100 lines each vs 669)
- Conversational (context loads once, persists)
- Flexible (mix modes as needed)
- Maintainable (update one without touching others)

### 5. Hybrid Smart Routing (Recommended Pattern)

```
Harry: "I need to invoice Panda Candy and plan MOKAI Q1"

Claude: "Two domains detected:
         1. Invoicing → I'll handle with Supabase/financial tools
         2. MOKAI planning → Launching mokai-business-strategist

         [Handles finance immediately]
         [Agent handles strategy]

         Here's both: invoice created, and here's Q1 plan..."
```

**Why this works**:
- Harry has ONE conversation partner (Claude)
- Claude understands whole life (finance, MOKAI, code, crypto, etc.)
- Claude pulls from Serena/Graphiti for context
- Claude launches specialists when truly needed
- Claude maintains continuity across agent responses

## Technical Implementation Notes

### Graphiti Integration (Added to OBSIDIA)
- 6 practical MCP workflow examples
- Pattern: Store discoveries → Query for context → Enhanced discovery
- Usage: Check graph first (fastest), fallback to Serena, then progressive discovery

### Terminology Clarifications (Added to CLAUDE.md)
- "Claude" = Claude Code (CLI), NOT Claude Desktop
- Config files:
  - Project MCP: `.mcp.json`
  - Settings: `~/.claude/settings.local.json`
  - NOT `claude_desktop_config.json`

## Next Steps

1. **Design MOKAI slash command structure**
   - Create lightweight primer command
   - Add focused mode commands (strategy, compliance, finance, ops)
   - Keep mokai-business-strategist agent for complex decisions only

2. **Update CLAUDE.md with orchestration mode**
   ```markdown
   ## Orchestration Mode

   You are Harry's second brain with domain awareness:
   - MOKAI: Business strategy, compliance, IPP → mokai-business-strategist
   - Finance: Invoicing, transactions, tax → Direct handling + financial MCPs
   - Development: Code, automation, MCP → Direct handling
   - Research: Market/crypto/tech → gpt-researcher or general-purpose

   Default: Handle directly using Serena/Graphiti context
   Escalate: Launch specialist when complexity exceeds your knowledge
   Synthesize: Maintain conversation continuity across agent responses
   ```

3. **Test the pattern**
   - Load MOKAI context via /mokai-primer
   - Have conversation about business strategy
   - See if context persists and orchestration feels natural

4. **Apply pattern to other areas**
   - Finance primer + modes
   - Crypto/research primer + modes
   - Development primer (probably not needed - default mode)

## Open Questions

1. Should OBSIDIA be merged into main CLAUDE.md as default operating mode?
2. How much of agent-mokai's embedded knowledge should move to Serena memories vs Graphiti?
3. Should each area (MOKAI, finance, etc.) have its own Graphiti instance or share one?
4. What's the right balance between "always use Graphiti first" vs "use when needed"?

## References

- OBSIDIA agent: `.claude/agents/obsidia.md`
- Agent-MOKAI: `.claude/agents/agent-mokai.md`
- CLAUDE.md: Root project instructions
- Graphiti vs Serena analysis: `00-inbox/tasks/Graphit or serena 4 rag.md`
