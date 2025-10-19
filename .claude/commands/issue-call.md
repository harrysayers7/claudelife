---
created: "2025-10-18 07:15"
description: |
  Retrieves and resolves tracked issues by ID. Loads issue context, suggests solutions based on category and error patterns, guides through debugging steps, updates issue status when solved, creates lessons learnt files in `04-resources/lessons-learnt/`, and suggests adding solutions to relevant slash commands and Serena's memory.
examples:
  - /issue-call 001
  - /issue-call 023 "found the solution - needed to restart MCP server"
  - /issue-call 015 --status-update "still investigating, tried X and Y"
---

# Issue Call

This command retrieves and helps resolve tracked issues from `01-areas/claude-code/issues/`. It loads the issue context, provides debugging guidance, updates resolution status, and creates lessons learned for future reference.

## Usage

```bash
/issue-call {ID}                           # Load issue for debugging
/issue-call {ID} "solution description"    # Mark resolved with solution
/issue-call {ID} --status-update "notes"   # Update progress without resolving
```

## What This Command Does

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

This command handles issue resolution by:
1. **Loading issue context**: Read full issue details including error messages, attempted solutions
2. **Analyzing issue patterns**: Identify common solutions based on category and error type
3. **Suggesting debugging steps**: Category-specific troubleshooting workflows
4. **Guiding resolution**: Walk through systematic debugging process
5. **Capturing lessons**: Create structured lesson files for future reference
6. **Updating documentation**: Suggest adding solutions to commands and Serena memory

## Interactive Process

When you run this command, I will:

1. **Retrieve issue file**
   ```bash
   # Use companion script for fast lookup
   ./scripts/scan-issues.sh --id={ID}
   ```
   - Load from `01-areas/claude-code/issues/issue-{ID}-*.md`
   - Parse YAML frontmatter for metadata
   - Display issue context clearly

2. **Analyze issue context**
   - **Category**: Determine troubleshooting approach (MCP, hook, script, etc.)
   - **Severity**: Prioritize debugging steps
   - **Error messages**: Parse for common patterns
   - **Attempted solutions**: Avoid suggesting already-tried fixes
   - **Related files**: Identify relevant configs, scripts, logs

3. **Check issue status**
   - If `solved: true`: Display resolution and lesson learned
   - If `complete: true` but not solved: Show last status update
   - If `complete: false`: Begin debugging process

4. **Provide category-specific debugging**

   ### For MCP Server Issues (category: mcp-server)
   ```bash
   # 1. Verify server installation
   which {server-name}
   npm list -g | grep {server-name}

   # 2. Check configuration syntax
   cat .mcp.json | jq '.mcpServers["{server-name}"]'

   # 3. Verify enabled in settings
   cat ~/.claude/settings.local.json | jq '.enabledMcpjsonServers'

   # 4. Debug connection
   claude --mcp-debug
   tail -50 /tmp/claude-mcp-debug.log

   # 5. Test MCP tool directly
   # In Claude Code session, try calling tool
   mcp__{server-name}__list_resources()
   ```

   ### For Hook Issues (category: hook)
   ```bash
   # 1. Check permissions
   ls -la .claude/hooks/{hook-name}.sh
   chmod +x .claude/hooks/{hook-name}.sh

   # 2. Validate settings.json
   cat .claude/settings.json | jq '.hooks'

   # 3. Test hook directly
   export CLAUDE_TOOL_NAME="Edit"
   export CLAUDE_TOOL_FILE_PATH="test.md"
   .claude/hooks/{hook-name}.sh

   # 4. Check debug log
   tail -100 /tmp/claude-hook-debug.log
   grep ERROR /tmp/claude-hook-debug.log

   # 5. Verify matcher pattern
   # Does hook type match? (PreToolUse, PostToolUse, etc.)
   # Does matcher regex match tool name?
   ```

   ### For Script Issues (category: script)
   ```bash
   # 1. Verify shebang
   head -1 scripts/{script-name}.sh

   # 2. Check permissions
   ls -la scripts/{script-name}.sh
   chmod +x scripts/{script-name}.sh

   # 3. Test with debug output
   bash -x scripts/{script-name}.sh

   # 4. Verify dependencies
   # Check required commands exist
   command -v jq
   command -v awk

   # 5. Check paths
   # Verify all referenced files exist
   # Ensure paths are absolute, not relative
   ```

   ### For Command Issues (category: command)
   ```bash
   # 1. Validate YAML frontmatter
   head -20 .claude/commands/{command-name}.md

   # 2. Check for syntax errors
   # Ensure no broken markdown syntax
   # Verify code blocks properly closed

   # 3. Test command logic
   # Run command with test input
   /{command-name} "test case"

   # 4. Compare to working commands
   # Check similar commands for patterns
   ls -la .claude/commands/

   # 5. Verify documentation updated
   grep "{command-name}" 04-resources/guides/commands/claudelife-commands-guide.md
   ```

   ### For Database Issues (category: database)
   ```javascript
   // 1. Verify project ID
   await mcp__supabase__get_project_url()
   // Should return: gshsshaodoyttdxippwx

   // 2. Test connection
   await mcp__supabase__list_tables()

   // 3. Check migration syntax
   // Review SQL file for syntax errors

   // 4. Validate schema
   await mcp__supabase__execute_sql({
     query: "SELECT * FROM information_schema.tables"
   })

   // 5. Check advisors
   await mcp__supabase__get_advisors({ type: "security" })
   await mcp__supabase__get_advisors({ type: "performance" })
   ```

   ### For Automation Issues (category: automation)
   ```bash
   # 1. Check n8n workflow status
   # Visit: http://134.199.159.190:5678

   # 2. Verify webhook URLs
   # Check workflow webhook endpoints

   # 3. Test API connections
   # Validate credentials and endpoints

   # 4. Check execution logs
   # Review n8n execution history

   # 5. Validate data transformations
   # Test with sample payloads
   ```

   ### For Configuration Issues (category: configuration)
   ```bash
   # 1. Validate JSON/YAML syntax
   cat config.json | jq .
   yamllint config.yaml

   # 2. Check environment variables
   env | grep {RELEVANT_VAR}

   # 3. Verify file paths
   ls -la {referenced-path}

   # 4. Check for typos
   # Common: server name mismatches
   # Common: incorrect path separators

   # 5. Compare to working config
   # Diff against known-good configuration
   ```

5. **Guide systematic debugging**
   - Walk through steps one at a time
   - Capture output from each step
   - Identify patterns or clues
   - Suggest next steps based on findings
   - Adjust approach based on results

6. **When solution found**
   - Ask: "What was the root cause?"
   - Ask: "What fixed it?"
   - Ask: "How can we prevent this in the future?"

## Resolution Workflow

When issue is resolved:

1. **Update issue file**
   ```yaml
   ---
   complete: true
   solved: true
   lesson: 04-resources/lessons-learnt/251018-issue-{ID}-{slug}.md
   ---

   ## Resolution

   **Root cause**: [What was wrong]

   **Solution**: [What fixed it]

   **Prevention**: [How to avoid in future]
   ```

2. **Create lesson learned file**
   - Path: `04-resources/lessons-learnt/YYMMDD-issue-{ID}-{description}.md`
   - Format:
   ```markdown
   ---
   date: "2025-10-18 07:30"
   issue-id: issue-{ID}
   category: {category}
   severity: {severity}
   ---

   # Lesson: {Title}

   ## Problem

   [What was the issue - include error messages]

   ## Root Cause

   [Why it happened - technical explanation]

   ## Solution

   [What fixed it - specific steps taken]

   ```bash
   # Commands used to resolve
   specific-command-here
   ```

   ## Prevention

   [How to avoid this in the future]

   ### For Users:
   - Check X before doing Y
   - Always verify Z

   ### For System:
   - Add validation for X
   - Create automated check for Y

   ## Related

   - Issue: [[issue-{ID}-{slug}]]
   - Category: {category}
   - Similar issues: [[issue-{related-id}]]
   ```

3. **Suggest command updates**

   Based on category, identify relevant commands to update:

   | Category | Suggested Commands |
   |----------|-------------------|
   | mcp-server | Add to "MCP Troubleshooting" section |
   | hook | Update `/create-hook` troubleshooting guide |
   | script | Add to script patterns documentation |
   | command | Update `/create-command` best practices |
   | database | Add to Supabase integration patterns |
   | automation | Document in n8n workflow guide |
   | configuration | Update config validation section |

   **Example suggestion**:
   ```
   💡 Should I add this to `/create-hook` troubleshooting?

   I'll add a new section:

   ### Common Issue: Hook Not Firing After Permission Change

   **Symptom**: Hook stops working after git pull or file sync

   **Solution**: Re-apply execute permissions
   ```bash
   chmod +x .claude/hooks/*.sh
   ```

   **Prevention**: Add to git pre-commit hook to verify permissions

   Would you like me to update `/create-hook`? (yes/no)
   ```

4. **Update Serena's memory** (with confirmation)

   ```
   💾 Should I add this solution to Serena's memory?

   File: `.serena/memories/hook_troubleshooting.md`

   Addition:
   ```markdown
   ### Permission Issues After File Sync

   **Problem**: Hooks stop firing after git operations
   **Solution**: Re-apply execute permissions with `chmod +x .claude/hooks/*.sh`
   **Prevention**: Add permission verification to git hooks
   ```

   Add to Serena's memory? (yes/no)
   ```

5. **Link lesson to issue**
   - Update issue frontmatter with lesson path
   - Add bidirectional links (issue ↔ lesson)
   - Tag lesson with category for future searching

## Status Update (Without Resolving)

For ongoing investigations:

```bash
/issue-call 015 --status-update "tried restarting MCP server, still failing"
```

Updates issue file with:
```markdown
## Progress Log

**2025-10-18 07:30**: Tried restarting MCP server, still failing
**2025-10-18 08:15**: Checked .mcp.json syntax - valid
**2025-10-18 09:00**: Discovered: missing from enabledMcpjsonServers array
```

Keeps `complete: false` until fully resolved.

## Fast Issue Lookup (Companion Script)

For performance, the companion script provides:

```bash
# Get specific issue
./scripts/scan-issues.sh --id=023

# List unsolved issues
./scripts/scan-issues.sh --unsolved

# Search by keyword
./scripts/scan-issues.sh --search="mcp"

# Filter by category
./scripts/scan-issues.sh --category=hook

# Filter by severity
./scripts/scan-issues.sh --severity=critical

# JSON output for automation
./scripts/scan-issues.sh --json
```

**Performance**: 30-60x faster than manual file operations

## Output Format

I'll provide:

1. **Issue context loaded**
   ```
   📋 Issue #001: Serena MCP Connection Failure
   Category: mcp-server | Severity: high | Status: unsolved
   Created: 2025-10-18 07:00

   **Problem**: Serena MCP server won't connect after config update

   **Error**: "Failed to connect to MCP server: serena"

   **Attempted**:
   - Restarted Claude Code (failed)
   - Checked .mcp.json syntax (valid)
   - Verified server installed (confirmed)
   ```

2. **Debugging guidance**
   ```
   🔍 Debugging Steps for MCP Server Issues:

   Step 1: Verify enabledMcpjsonServers
   Run: cat ~/.claude/settings.local.json | jq '.enabledMcpjsonServers'

   Expected: ["serena", ...other servers]

   What do you see?
   ```

3. **Solution capture** (when resolved)
   ```
   ✅ Issue resolved!

   **Root cause**: Missing from enabledMcpjsonServers array
   **Solution**: Added "serena" to settings.local.json
   **Prevention**: Check enabledMcpjsonServers when adding MCP servers

   Creating lesson learned file...
   ✅ Lesson created: 04-resources/lessons-learnt/251018-issue-001-mcp-enabled.md

   💡 Suggestions:
   - Add to `/create-hook` MCP troubleshooting section
   - Update Serena memory: mcp_troubleshooting.md

   Proceed with updates? (yes/no)
   ```

## Examples

### Example 1: Debugging MCP Connection

```
User: /issue-call 001

📋 Issue #001: Serena MCP Connection Failure
Category: mcp-server | Severity: high | Status: unsolved

**Problem**: Serena won't connect after .mcp.json update

**Error**:
```
Failed to connect to MCP server: serena
Error: ENOENT: no such file or directory
```

**Attempted**:
- Restarted Claude Code ❌
- Validated .mcp.json syntax ✅
- Checked server installation ✅

🔍 Let's debug systematically:

**Step 1**: Verify enabledMcpjsonServers
```bash
cat ~/.claude/settings.local.json | jq '.enabledMcpjsonServers'
```

What's the output?

[User provides: Missing "serena" from array]

**Found it!** The server exists but isn't enabled.

**Step 2**: Add to enabledMcpjsonServers
```json
{
  "enabledMcpjsonServers": ["serena", "supabase", "linear-server"]
}
```

**Step 3**: Restart Claude Code
```bash
exit
claude
```

Try connecting now. Does it work?

[User confirms: Works!]

✅ Issue resolved! Creating lesson...

**Solution Summary**:
- Root cause: Server not in enabledMcpjsonServers array
- Fix: Added "serena" to settings.local.json
- Prevention: Always check enabledMcpjsonServers when adding MCP servers

📝 Lesson created: `04-resources/lessons-learnt/251018-issue-001-mcp-enabled.md`

💡 Should I:
1. Add to Serena's memory (mcp_troubleshooting.md)?
2. Update `/create-hook` with this pattern?

Proceed? (yes/no)
```

### Example 2: Hook Permission Issue

```
User: /issue-call 005

📋 Issue #005: Post-commit hook not firing
Category: hook | Severity: medium | Status: unsolved

**Problem**: Hook worked yesterday, stopped after git pull

**Error**: None visible

**Attempted**:
- Checked settings.json ✅
- Verified matcher pattern ✅
- Restarted Claude Code ❌

🔍 Debugging hook issues:

**Step 1**: Check permissions
```bash
ls -la .claude/hooks/post-commit.sh
```

What do you see?

[User provides: -rw-r--r-- (no execute)]

**Found it!** Lost execute permissions during git pull.

**Step 2**: Fix permissions
```bash
chmod +x .claude/hooks/post-commit.sh
```

**Step 3**: Verify
```bash
ls -la .claude/hooks/post-commit.sh
# Should show: -rwxr-xr-x
```

**Step 4**: Test hook
```bash
export CLAUDE_TOOL_NAME="Bash"
export CLAUDE_TOOL_COMMAND="git commit"
.claude/hooks/post-commit.sh
```

Does it execute now?

[User confirms: Works!]

✅ Resolved! Creating lesson...

**Solution**:
- Root cause: Git pull didn't preserve execute permissions
- Fix: chmod +x .claude/hooks/*.sh
- Prevention: Add git hook to verify permissions

📝 Lesson: `04-resources/lessons-learnt/251018-issue-005-hook-perms.md`

💡 Suggestions:
1. Add to `/create-hook` troubleshooting: "Permission Issues After Git Operations"
2. Create pre-commit hook to verify permissions
3. Update Serena memory: hook_patterns.md

Proceed with updates? (yes/no)
```

### Example 3: Status Update (Not Resolved)

```
User: /issue-call 012 --status-update "checked migration syntax, no errors found"

📋 Issue #012: Supabase Migration Foreign Key Failure
Category: database | Severity: high | Status: in progress

**Updated progress log**:
```markdown
## Progress Log

**2025-10-18 09:00**: Initial investigation - foreign key constraint error
**2025-10-18 10:30**: Checked migration syntax, no errors found
```

Current status: Still investigating

**Next debugging steps**:

1. Verify referenced table exists:
   ```javascript
   await mcp__supabase__execute_sql({
     query: "SELECT * FROM information_schema.tables WHERE table_name = 'referenced_table'"
   })
   ```

2. Check column types match:
   ```javascript
   await mcp__supabase__execute_sql({
     query: "SELECT column_name, data_type FROM information_schema.columns WHERE table_name IN ('table1', 'table2')"
   })
   ```

3. Test migration locally:
   ```bash
   supabase db reset
   supabase db push
   ```

Try these steps and run `/issue-call 012` with findings.
```

## Evaluation Criteria

A successful issue resolution should:

1. ✅ **Load issue context completely**: All metadata, errors, and attempts visible
2. ✅ **Provide category-specific debugging**: Tailored steps for issue type
3. ✅ **Guide systematically**: One step at a time, adjusting based on results
4. ✅ **Capture root cause**: Clear explanation of why issue occurred
5. ✅ **Document solution**: Specific steps that resolved the problem
6. ✅ **Create lesson learned**: Structured file for future reference
7. ✅ **Suggest prevention**: How to avoid issue recurring
8. ✅ **Update relevant commands**: Add troubleshooting to appropriate docs
9. ✅ **Sync Serena's memory**: Add solution patterns with confirmation
10. ✅ **Link bidirectionally**: Issue ↔ lesson ↔ commands ↔ memory

## Related Resources

- Issue directory: `01-areas/claude-code/issues/`
- Lessons directory: `04-resources/lessons-learnt/`
- Companion script: `scripts/scan-issues.sh`
- Creation command: `.claude/commands/issue-create.md`
- Commands guide: `04-resources/guides/commands/claudelife-commands-guide.md`
- Serena memories: `.serena/memories/`
- MCP config: `.mcp.json`
- Hook configs: `.claude/settings.json`

## Starting the Issue Resolution Process

Provide the issue ID to retrieve:

```bash
/issue-call {ID}                    # Load and debug
/issue-call {ID} "solution notes"   # Mark resolved
/issue-call {ID} --status-update "progress notes"  # Update status
```

I'll load the issue, provide category-specific debugging guidance, and help you systematically resolve it with lesson creation and documentation updates.
