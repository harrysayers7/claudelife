---
created: "2025-10-19 11:50"
description: |
  Updates tracked issues with latest troubleshooting attempts, error messages, code changes, and observations before restarting Claude Code. Appends timestamped progress to issue files, updates frontmatter with new attempted solutions, and preserves full context for LLM continuation. Uses scan-issues.sh for fast lookup and maintains comprehensive debugging history.
examples:
  - /issue-update 001
  - /issue-update 023
  - /issue-update 015
---

# Issue Update

This command updates existing tracked issues in `01-areas/claude-code/issues/` with the latest troubleshooting attempts, observations, and context before restarting Claude Code. Designed to preserve full debugging context for seamless LLM continuation.

## Usage

```bash
/issue-update {ID}
```

## What This Command Does

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

This command captures mid-debugging context by:
1. **Loading current issue state**: Fast retrieval using `scan-issues.sh`
2. **Analyzing conversation history**: Extract what was attempted since last update
3. **Capturing comprehensive context**: Errors, file changes, theories, observations
4. **Updating issue file**: Add to progress log + frontmatter attempted-solutions
5. **Preserving LLM context**: Everything needed to resume debugging after restart

## Interactive Process

When you run this command, I will:

1. **Retrieve issue file quickly**
   ```bash
   # Use companion script for fast lookup
   ./scripts/scan-issues.sh --id={ID}
   ```
   - Load from `01-areas/claude-code/issues/issue-{ID}-*.md`
   - Parse current state (attempted solutions, progress log, severity)
   - Display issue summary

2. **Analyze current conversation context**

   I'll review our conversation to extract:

   ### Attempted Solutions
   - Commands executed (with output)
   - Code modifications made (file paths + changes)
   - Configuration changes attempted
   - Tools/MCP calls that failed/succeeded
   - Debugging steps taken

   ### Error Messages
   - Full error output encountered
   - Stack traces observed
   - Warning messages seen
   - MCP/tool error responses
   - Log file excerpts

   ### File Changes
   - Files created/modified/deleted
   - Configuration updates (`.mcp.json`, `settings.json`, etc.)
   - Script modifications
   - Code edits attempted

   ### Observations & Theories
   - Patterns noticed
   - Hypotheses about root cause
   - Things that partially worked
   - Unexpected behaviors
   - Clues discovered

   ### Current State
   - Where debugging stands now
   - What's been ruled out
   - What still needs investigation
   - Next logical steps to try

3. **Present extracted context for confirmation**

   ```
   📋 Issue #023: Supabase Migration Foreign Key Failure

   I found these updates from our conversation:

   **Attempted Solutions (to add to frontmatter)**:
   - Checked migration syntax with VSCode SQL linter - no errors found
   - Verified foreign key column types match (both uuid)
   - Tested migration in local Supabase instance - works locally
   - Checked production schema with execute_sql - table exists

   **New Error Messages**:
   ```
   Error: insert or update on table "invoices" violates foreign key constraint
   DETAIL: Key (entity_id)=(abc123) is not present in table "entities"
   ```

   **Files Modified**:
   - supabase/migrations/20251019_add_invoices.sql (tested locally)
   - .env.local (added SUPABASE_PROJECT_REF for testing)

   **Key Observations**:
   - Migration works locally but fails in production
   - Entity abc123 exists in local but not in production
   - Suggests data sync issue between environments
   - Production may be missing seed data

   **Current Theory**:
   Root cause is missing entity data in production, not migration syntax.

   **Next Steps to Try**:
   1. Query production for entity abc123
   2. Check if seed data ran in production
   3. May need to create missing entities first

   Add this to issue #023? (yes/edit/no)
   ```

4. **Update issue file comprehensively**

   ### Frontmatter Updates
   ```yaml
   attempted-solutions:
     - Solution 1 (original)
     - Solution 2 (original)
     - NEW: Checked migration syntax - no errors
     - NEW: Verified column types match
     - NEW: Tested locally - works
     - NEW: Checked production schema - table exists
   ```

   ### Progress Log Addition
   ```markdown
   ## Progress Log

   **2025-10-18 09:00**: Initial investigation - foreign key error
   **2025-10-19 11:50**: **[COMPREHENSIVE UPDATE]**

   ### Attempted Since Last Update:
   1. ✅ Migration syntax validation (VSCode SQL linter) - clean
   2. ✅ Column type verification - both uuid, matching
   3. ✅ Local testing - migration succeeds
   4. ✅ Production schema check - entities table exists

   ### Error Context:
   ```
   Error: insert or update on table "invoices" violates foreign key constraint
   DETAIL: Key (entity_id)=(abc123) is not present in table "entities"
   ```

   ### Files Modified:
   - `supabase/migrations/20251019_add_invoices.sql` (validated)
   - `.env.local` (added test config)

   ### Key Discovery:
   Entity `abc123` exists locally but missing in production. Migration syntax is correct - this is a **data sync issue**, not a schema issue.

   ### Current Theory:
   Production database missing seed data that exists in local environment.

   ### Next Investigation Steps:
   1. Query production: `SELECT * FROM entities WHERE id = 'abc123'`
   2. Check seed data execution history in production
   3. Identify missing entities and create them OR update migration to handle missing data

   ### LLM Continuation Context:
   - Migration file is correct
   - Problem is environment-specific (production vs local)
   - Need to decide: Add missing entities OR make migration more defensive
   - Consider: Should migration include entity creation OR assume entities exist?
   ```

5. **Preserve full debugging state**

   The update ensures the next LLM session has:
   - ✅ Complete history of what was tried
   - ✅ All error messages with full context
   - ✅ File paths and changes made
   - ✅ Current working theory
   - ✅ Logical next steps
   - ✅ Design decisions to consider
   - ✅ Environment-specific findings

## Update Structure

### Frontmatter Additions

```yaml
---
# Existing fields preserved
attempted-solutions:
  - [Original solutions remain]
  - NEW: [Latest attempt 1]
  - NEW: [Latest attempt 2]
  - NEW: [Latest attempt 3]

# Update timestamp
updated: "2025-10-19 11:50"
---
```

### Progress Log Format

```markdown
## Progress Log

[Previous entries preserved]

**YYYY-MM-DD HH:MM**: **[COMPREHENSIVE UPDATE]**

### Attempted Since Last Update:
1. ✅/❌ [Action taken] - [Result]
2. ✅/❌ [Action taken] - [Result]

### Error Messages Encountered:
```
[Full error output with context]
```

### Files Modified:
- `path/to/file.ext` (description of change)
- `path/to/config.json` (what was updated)

### Code Changes:
```language
// Relevant code snippets that were added/modified
```

### Key Observations:
- [Pattern noticed]
- [Unexpected behavior]
- [Clue discovered]

### Current Theory:
[Hypothesis about root cause based on evidence]

### Ruled Out:
- [What's definitely not the problem]
- [Dead ends investigated]

### Next Steps:
1. [Logical next action]
2. [Alternative approach to try]
3. [Information still needed]

### LLM Continuation Context:
[Specific notes for next session: decisions to make, context to remember, things to consider]
```

## Fast Issue Lookup (Script Integration)

The command uses `scan-issues.sh` for performance:

```bash
# Quick ID lookup (30-60x faster than manual)
./scripts/scan-issues.sh --id=023

# Get issue file path
./scripts/scan-issues.sh --id=023 --json | jq -r '.path'
```

## Context Extraction Strategy

I'll analyze the conversation for:

### 1. Commands Executed
Extract all bash commands with outputs:
- What was run
- Exit codes
- Error messages
- Successful outputs

### 2. Tool/MCP Calls
Track all tool invocations:
- Which tools were called
- Parameters used
- Success/failure
- Response data

### 3. Code Modifications
Identify file operations:
- Read (files examined)
- Write (new files created)
- Edit (changes made to existing files)
- Delete (files removed)

### 4. Error Analysis
Capture error patterns:
- Full error text
- Stack traces
- Warning messages
- Related log excerpts

### 5. Hypothesis Evolution
Track thinking progression:
- Initial theories
- What was ruled out
- New theories formed
- Evidence for/against

### 6. Decision Points
Identify choices made:
- Design decisions
- Implementation approaches
- Workarounds chosen
- Trade-offs considered

## Output Format

I'll provide:

1. **Issue loaded**
   ```
   📋 Issue #023: Supabase Migration FK Failure
   Category: database | Severity: high | Status: unsolved
   Last updated: 2025-10-18 10:30

   Current attempted solutions: 4
   Progress log entries: 2
   ```

2. **Extracted context summary**
   ```
   📊 Context Extracted from Conversation:

   ✅ Commands executed: 5
   ❌ Errors encountered: 2 unique
   📝 Files modified: 3
   💡 Observations: 4
   🔍 Current theory: Data sync issue
   ```

3. **Preview of updates**
   ```
   📝 Will add to issue:

   **Frontmatter**:
   - 3 new attempted solutions

   **Progress Log**:
   - Comprehensive update with all context
   - 5 attempted actions
   - 2 error messages
   - 3 file changes
   - 4 key observations
   - Current theory + next steps

   Approve updates? (yes/edit/no)
   ```

4. **Updated issue confirmation**
   ```
   ✅ Issue #023 updated successfully!

   Updated: 01-areas/claude-code/issues/issue-023-supabase-fk.md

   Added:
   - 3 attempted solutions to frontmatter
   - Comprehensive progress log entry
   - Full error context
   - File change history
   - Current theory and next steps

   Ready to restart Claude Code with full context preserved.
   ```

## Examples

### Example 1: MCP Server Debug Session

```
User: /issue-update 001

📋 Issue #001: Serena MCP Won't Connect
Category: mcp-server | Severity: high | Status: unsolved
Last updated: 2025-10-18 07:00

Analyzing conversation for updates...

📊 Found:
- 6 commands executed
- 3 configuration changes
- 2 error messages
- 1 key discovery

📝 Extracted Context:

**Attempted Solutions**:
- Verified .mcp.json syntax with jq - valid
- Checked enabledMcpjsonServers - "serena" is present
- Restarted Claude Code - still failing
- Verified serena package installed globally - confirmed
- Checked Node.js version - v20.10.0 (compatible)
- Tested with --mcp-debug flag - found connection error

**Error Messages**:
```
Failed to connect to MCP server: serena
Error: spawn serena ENOENT
at Process.ChildProcess._handle.onexit (node:internal/child_process:283:19)
```

Debug log excerpt:
```
[MCP] Attempting to spawn: serena
[MCP] Command not found in PATH
[MCP] PATH: /usr/local/bin:/usr/bin:/bin
```

**Files Modified**:
- `~/.claude/settings.local.json` (verified serena in enabledMcpjsonServers)
- `.mcp.json` (no changes, syntax validated)

**Key Discovery**:
`serena` command exists (`which serena` returns path) but MCP server can't find it. PATH issue - npm global bin not in MCP's PATH environment.

**Current Theory**:
MCP server subprocess doesn't inherit full shell PATH. Need to specify absolute path to serena binary in .mcp.json instead of relying on command name.

**Next Steps**:
1. Get serena absolute path: `which serena`
2. Update .mcp.json to use absolute path instead of "serena"
3. Restart and test

Add this to issue #001? (yes/edit/no)

[User: yes]

✅ Issue updated!

**Frontmatter added**:
- Verified .mcp.json syntax
- Checked enabledMcpjsonServers
- Restarted with --mcp-debug
- Verified package installation
- Tested absolute path theory

**Progress log updated** with full debugging session context.

Ready for Claude Code restart with complete context.
```

### Example 2: Hook Not Firing

```
User: /issue-update 005

📋 Issue #005: Post-commit hook not executing
Category: hook | Severity: medium | Status: unsolved

Analyzing conversation...

📊 Found:
- 4 debugging commands
- 1 file permission change
- 3 observations
- Current theory identified

📝 Extracted Context:

**Attempted Solutions**:
- Checked settings.json hook configuration - correct
- Verified matcher pattern matches "Bash" tool - matches
- Tested hook manually with env vars - executes successfully
- Changed permissions to 755 - already had execute bit
- Checked hook file encoding - UTF-8, no BOM

**Files Modified**:
- `.claude/hooks/post-commit.sh` (permissions verified)
- `.claude/settings.json` (checked, no changes needed)

**Observations**:
1. Hook executes perfectly when called manually with correct env vars
2. Hook doesn't fire during actual git commits via Claude Code
3. No errors in hook debug log - suggests hook never triggered
4. Other hooks (pre-commit) work fine

**Current Theory**:
The matcher pattern works, permissions are correct, hook script is valid. The issue is likely that `Bash` tool with `git commit` command isn't matching because:
- Commits might use a different tool name internally
- Command string might include additional flags we're not matching

**Next Steps**:
1. Add debug logging to ALL hook events to see what's actually firing
2. Check if tool name is "Bash" or something else for commits
3. Try wildcard matcher pattern temporarily to catch everything
4. Review hook execution logs during actual commit

**LLM Context for Continuation**:
- Hook script itself is proven working (manual test passed)
- Configuration syntax is correct (other hooks work)
- Problem is specifically with matching git commit events
- Need to identify actual tool name/command for commits

Add to issue #005? (yes/edit/no)

[User: yes]

✅ Updated successfully!

Issue ready for debugging continuation after restart.
```

### Example 3: Database Query Performance

```
User: /issue-update 012

📋 Issue #012: Supabase query timeout on large tables
Category: database | Severity: high | Status: unsolved

📊 Context extracted:
- 8 queries tested
- 3 index strategies attempted
- Performance measurements recorded
- Design decision needed

📝 Update:

**Attempted Solutions**:
- Added index on created_at column - 40% improvement but still slow
- Tried composite index (entity_id, created_at) - 60% improvement
- Tested LIMIT clause - works but doesn't solve root issue
- Analyzed query plan with EXPLAIN - seq scan on large table
- Attempted partial index WHERE created_at > '2024-01-01' - 75% improvement
- Tested materialized view approach - fast but complex to maintain

**Performance Data**:
| Approach | Query Time | Improvement | Complexity |
|----------|-----------|-------------|------------|
| No index | 4500ms | baseline | low |
| Single index | 2700ms | 40% | low |
| Composite index | 1800ms | 60% | low |
| Partial index | 1125ms | 75% | medium |
| Materialized view | 180ms | 96% | high |

**Files Modified**:
- `supabase/migrations/20251019_add_indexes.sql` (multiple index strategies)
- Tested queries in MCP but not committed yet

**Key Findings**:
1. Partial index dramatically improves performance for recent data queries
2. 90% of queries are for data from last 3 months
3. Materialized view is fastest but adds maintenance complexity
4. Current query pattern doesn't actually need full table access

**Design Decision Needed**:
Should we:
A) Use partial index (recent data only) - simpler, good enough
B) Implement materialized view - faster, more maintenance
C) Refactor queries to be more specific - best long-term, requires code changes

**Current Recommendation**:
Option A (partial index) for quick win, then Option C (refactor) in next sprint.

**Next Steps**:
1. Get user approval on approach
2. Finalize migration with chosen strategy
3. Test in production with realistic load
4. Monitor query performance metrics

Add to issue #012? (yes/edit/no)

[User: yes]

✅ Issue updated with performance analysis and decision context.

All options documented for continuation after restart.
```

## Evaluation Criteria

A successful issue update should:

1. ✅ **Load issue quickly**: Use scan-issues.sh for fast retrieval
2. ✅ **Extract complete context**: All commands, errors, changes, observations
3. ✅ **Preserve error messages**: Full text with surrounding context
4. ✅ **Track file changes**: Every modification with description
5. ✅ **Document theories**: Current hypothesis and evidence
6. ✅ **Identify next steps**: Logical actions for continuation
7. ✅ **Update frontmatter**: Add new attempted solutions
8. ✅ **Append progress log**: Comprehensive timestamped entry
9. ✅ **Enable LLM continuation**: Everything needed to resume debugging
10. ✅ **Maintain history**: Never overwrite, only append

## Related Resources

- Issue directory: `01-areas/claude-code/issues/`
- Companion script: `scripts/scan-issues.sh`
- Issue creation: `.claude/commands/issue-create.md`
- Issue resolution: `.claude/commands/issue-call.md`
- Issue template: `98-templates/issue.md`

## Starting the Issue Update Process

Provide the issue ID to update:

```bash
/issue-update {ID}
```

I'll analyze our conversation, extract all relevant debugging context (commands, errors, file changes, observations, theories), and update the issue file with a comprehensive progress entry so you can seamlessly continue debugging after restarting Claude Code.
