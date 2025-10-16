# OBSIDIA Agent Test Queries

Validation test suite for the OBSIDIA orchestrator agent.

## Test 1: System Discovery (Basic)

**Query**: `/launch-agent obsidia "What systems exist for tracking MOKAI progress?"`

**Expected Behavior**:
- ✅ Checks knowledge freshness (<7 days)
- ✅ Searches existing commands via Serena
- ✅ Finds `/mokai-status`, `/mokai-dump`, `/mokai-weekly`, `/mokai-insights`
- ✅ Returns PRIMARY recommendation: `/mokai-status`
- ✅ Provides quick start example
- ✅ Progressive disclosure for alternatives

**Success Criteria**:
- Single clear answer first (not overwhelming list)
- Rationale provided (why this vs alternatives)
- No hardcoded file paths
- Response < 10K tokens

---

## Test 2: Architecture Design

**Query**: `/launch-agent obsidia "How should I build a new hook for auto-categorizing financial transactions?"`

**Expected Behavior**:
- ✅ Searches `.claude/hooks/` for similar patterns
- ✅ Identifies existing hooks (post-tool, pre-prompt types)
- ✅ Recommends `/create-hook` workflow
- ✅ Suggests MCP integrations (Supabase, UpBank)
- ✅ Evaluates if companion script needed (performance analysis)
- ✅ Provides implementation checklist

**Success Criteria**:
- References similar hook patterns found
- Clear MCP requirements listed
- Code samples use dynamic file resolution
- Includes testing strategy

---

## Test 3: Integration Troubleshooting

**Query**: `/launch-agent obsidia "My Serena MCP server isn't loading, how do I debug?"`

**Expected Behavior**:
- ✅ Provides debug workflow:
  1. `claude mcp list` - see actual loaded servers
  2. `claude mcp get serena` - check config
  3. Log file location: `~/Library/Logs/Claude/mcp-server-serena.log`
- ✅ Explains common mistake: editing `.mcp.json` instead of `~/.claude.json`
- ✅ Suggests verification steps
- ✅ Provides fix commands

**Success Criteria**:
- Specific, actionable commands
- Explains WHY (config location mistake)
- Verification step included
- No assumptions about user's setup

---

## Test 4: Optimization Analysis

**Query**: `/launch-agent obsidia "Can /mokai-status be faster with a script?"`

**Expected Behavior**:
- ✅ Analyzes current implementation (Serena pattern matching)
- ✅ Estimates performance (file count, operations)
- ✅ Calculates potential speedup
- ✅ Provides decision criteria:
  - Files scanned: ~50 diary notes
  - Current time: ~30 seconds
  - Script potential: ~2 seconds (15x faster)
- ✅ Recommendation with justification

**Success Criteria**:
- Measurable performance analysis
- Clear thresholds (20+ files or 10+ runs/day)
- Concrete recommendation (yes/no + why)
- Example script pattern if recommended

---

## Test 5: Wrong Agent Detection (Should Redirect)

**Query**: `/launch-agent obsidia "Complete MOKAI task: Read Indigenous Business section"`

**Expected Behavior**:
- ✅ Detects this is TASK EXECUTION (not discovery/design)
- ✅ Responds: "This is a task execution request. Use:"
  - `/complete-task "Read Indigenous Business section"` OR
  - `/launch-agent task-executor "..."`
- ✅ Explains OBSIDIA is for discovery, not execution
- ✅ Provides correct command to run

**Success Criteria**:
- Correctly identifies wrong agent type
- Redirects to appropriate tool
- Explains pattern: "OBSIDIA discovers → Other agents execute"
- Doesn't attempt to execute task itself

---

## Test 6: MCP Fallback Handling

**Query**: `/launch-agent obsidia "Search for all commands related to finance"` (while Serena is disabled)

**Expected Behavior**:
- ✅ Attempts Serena search first
- ✅ Catches error gracefully
- ✅ Falls back to Grep tool
- ✅ Warns user: "⚠️ Serena MCP unavailable. Using slower grep-based search. Fix Serena with: `claude mcp get serena`"
- ✅ Still returns relevant results (finance commands)

**Success Criteria**:
- No crash on MCP failure
- Automatic fallback executed
- User notified of degraded mode
- Results still useful (though slower)

---

## Test 7: Token Efficiency (Progressive Loading)

**Query**: `/launch-agent obsidia "What are all the available agents?"`

**Expected Behavior**:
- ✅ Does NOT load all 30+ agent files immediately
- ✅ Strategy:
  1. Quick scan: List `.claude/agents/` directory (500 tokens)
  2. If user wants details: Read specific agent categories
  3. Full content only if requested
- ✅ Returns organized summary (not full file contents)
- ✅ Offers progressive disclosure: "Ask me about specific category for details"

**Success Criteria**:
- Initial response < 3K tokens
- Directory structure shown (not file contents)
- User can drill down if needed
- Token budget respected (< 35K total)

---

## Test 8: Knowledge Freshness Warning

**Query**: `/launch-agent obsidia "What's new in the system?"` (when Serena memory >7 days old)

**Expected Behavior**:
- ✅ Checks `system_patterns_and_guidelines.md` last modified date
- ✅ Calculates days since update
- ✅ If > 7 days: Returns warning FIRST:
  - "⚠️ My knowledge is 7+ days old. Run `/update-serena-memory` for accurate answers."
- ✅ Still attempts to answer (but flags uncertainty)

**Success Criteria**:
- Staleness check runs at session start
- Clear warning message
- Suggests fix command
- Doesn't refuse to answer (just warns)

---

## Test 9: MCP Glossary Usage

**Query**: `/launch-agent obsidia "How do I use Serena?"` (from a new user)

**Expected Behavior**:
- ✅ Explains in plain English FIRST:
  - "**Serena** is the codebase search tool (like GitHub search for local repo)"
- ✅ Then shows MCP call example
- ✅ Includes usage example with real query
- ✅ Doesn't assume user knows MCP jargon

**Success Criteria**:
- Plain English explanation before technical details
- Clear analogy provided
- Working code example
- Welcoming to new users (not intimidating)

---

## Test 10: Multi-System Integration Design

**Query**: `/launch-agent obsidia "How do I build a workflow that syncs MOKAI client data from Supabase to Obsidian, then triggers n8n automation?"`

**Expected Behavior**:
- ✅ Identifies pattern: Database → Vault → Automation
- ✅ Lists required MCPs:
  - `mcp__supabase__*` (source data)
  - `mcp__claudelife-obsidian__*` (vault storage)
  - `mcp__n8n__*` (automation trigger)
- ✅ References similar example: MOKAI project workflow
- ✅ Provides architecture diagram (text-based)
- ✅ Implementation checklist with each integration point

**Success Criteria**:
- All required MCPs identified
- Data flow clearly explained
- Example pattern referenced
- Step-by-step integration points
- Testing strategy included

---

## Performance Benchmarks

| Test | Expected Time | Token Budget |
|------|---------------|--------------|
| Test 1: Discovery | < 5s | < 3K tokens |
| Test 2: Design | < 10s | < 10K tokens |
| Test 3: Troubleshoot | < 3s | < 2K tokens |
| Test 4: Optimization | < 8s | < 5K tokens |
| Test 5: Redirect | < 2s | < 1K tokens |
| Test 6: Fallback | < 15s | < 3K tokens |
| Test 7: Progressive | < 5s | < 3K tokens |
| Test 8: Freshness | < 1s | < 500 tokens |
| Test 9: Glossary | < 3s | < 2K tokens |
| Test 10: Multi-system | < 15s | < 15K tokens |

---

## Success Metrics

### Critical (Must Pass):
- ✅ No hardcoded file paths (all dynamic resolution)
- ✅ MCP fallback handling (no crashes on unavailable servers)
- ✅ Knowledge freshness checking (warns if >7 days old)
- ✅ Correct agent routing (redirects execution requests)
- ✅ Token efficiency (progressive loading, <35K budget)

### Important (Should Pass):
- ✅ Performance analysis accuracy (measurable criteria)
- ✅ Code sample verification (prefer Context7)
- ✅ Plain English explanations (MCP glossary used)
- ✅ Direct answer first (not overwhelming lists)
- ✅ Integration pattern matching (references examples)

### Nice-to-Have:
- ✅ Response speed < 15s per query
- ✅ Token usage < 10K per typical query
- ✅ User satisfaction (clear, actionable guidance)

---

## Running Tests

```bash
# Run each test query manually
/launch-agent obsidia "What systems exist for tracking MOKAI progress?"

# Observe:
# - Response structure (direct answer first?)
# - Token usage (check token counter)
# - File paths (any hardcoded?)
# - MCP calls (proper fallback?)
# - Clarity (plain English or jargon?)
```

## Continuous Improvement

After each test run, update `OBSIDIA-RESULTS.md` with:
- Which tests passed/failed
- Performance metrics
- Token usage breakdown
- User experience notes
- Improvement suggestions
