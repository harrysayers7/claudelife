---
created: "2025-10-18 07:00"
description: |
  Creates comprehensive issue reports with sequential IDs (001, 002, 003) in YAML format. Auto-checks Serena memory before debugging, captures technical context (type, category, severity, error messages, attempted solutions), stores in `01-areas/claude-code/issues/`, and provides structured template for efficient debugging and resolution tracking.
examples:
  - /issue-create "MCP server won't connect after config change"
  - /issue-create "Supabase migration failing with foreign key constraint"
  - /issue-create "Hook not firing for PostToolUse Edit events"
---

# Issue Create

This command creates detailed, structured issue reports for debugging Claude Code, MCP servers, hooks, scripts, and other technical problems in the claudelife ecosystem. Issues are stored with sequential numeric IDs for easy reference and tracking.

## Usage

```bash
/issue-create [optional: brief description of the issue]
```

## What This Command Does

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

This command creates issue reports that:
1. **Auto-check Serena's memory first**: Search for known solutions before creating new issues
2. **Generate sequential IDs**: Automatically assign next available ID (001, 002, 003)
3. **Capture comprehensive context**: Type, category, severity, related files, error messages
4. **Structure for resolution**: Track attempted solutions, completion status, and lessons learned
5. **Enable fast retrieval**: Companion script `scripts/scan-issues.sh` for quick searching

## Interactive Process

When you run this command, I will:

1. **Check Serena's memory first**
   ```javascript
   // Search for known solutions
   mcp__serena__list_memories()
   mcp__serena__read_memory({ memory_file_name: "relevant_memory" })
   ```
   - If similar issue found in memory, suggest solution immediately
   - Only proceed to create issue if memory doesn't help

2. **Understand the issue**
   - Ask you to describe the problem (what's broken, what's not working)
   - Clarify expected behavior vs. actual behavior
   - Identify when the issue started occurring

3. **Gather technical context**
   - **Type**: bug, enhancement, question, documentation, performance
   - **Category**: mcp-server, hook, script, command, database, automation, configuration
   - **Severity**: critical (blocking work), high (major impact), medium (workaround exists), low (minor inconvenience)
   - **Related files**: Paths to files involved (configs, scripts, hooks, etc.)
   - **Error messages**: Full error output, stack traces, logs

4. **Document attempted solutions**
   - What have you already tried?
   - Which troubleshooting steps failed?
   - Any patterns or clues observed?

5. **Generate next issue ID**
   - Use companion script: `./scripts/scan-issues.sh --next-id`
   - Format as zero-padded 3-digit number (001, 002, 003)
   - Ensure uniqueness in `01-areas/claude-code/issues/`

6. **Create issue file**
   - Template from `98-templates/issue.md`
   - Store in `01-areas/claude-code/issues/issue-{ID}-{slug}.md`
   - Slug derived from title (lowercase, hyphens, max 40 chars)

7. **Provide debugging suggestions**
   - Common solutions for this category
   - Relevant documentation links
   - MCP/tool-specific troubleshooting steps
   - Suggest creating `/issue-call {ID}` once resolved

## Issue Structure (YAML Frontmatter)

```yaml
---
title: Brief descriptive title
type:
  - issue
aliases:
  - issue-001
id: issue-001
category: mcp-server|hook|script|command|database|automation|configuration
relation: # Related issues, e.g., "blocks issue-005", "related to issue-003"
complete: false
solved: false
lesson: # Path to lesson learnt file after resolution
created: Sat, 10 18th 25, 7:00:00 am
severity: critical|high|medium|low
attempted-solutions:
  - Solution 1 that failed
  - Solution 2 that didn't work
error-messages: |
  Full error output here
  Multiple lines preserved
related-files:
  - /path/to/config.json
  - /path/to/script.sh
---

## Problem Description

[Detailed explanation of the issue]

## Expected Behavior

[What should happen]

## Actual Behavior

[What actually happens]

## Steps to Reproduce

1. Step one
2. Step two
3. Issue occurs

## Environment

- Claude Code version:
- OS:
- Relevant MCP servers:
- Other context:

## Additional Context

[Screenshots, logs, related documentation]

## Resolution

[To be filled when issue is resolved]
```

## Category Definitions

### mcp-server
Issues with MCP server connections, tools, or integration:
- Server won't start or connect
- Tools failing to execute
- Authentication/permission errors
- Tool output incorrect

### hook
Claude Code hooks not working as expected:
- Hook not firing
- Environment variables missing
- Script execution failures
- Blocking workflow unintentionally

### script
Shell or Node scripts with bugs or failures:
- Script crashes or errors
- Incorrect output
- Performance issues
- Permission problems

### command
Slash commands producing wrong results:
- Command logic errors
- Missing features
- Documentation inaccurate
- Unexpected behavior

### database
Supabase or other database issues:
- Migration failures
- Query errors
- Schema mismatches
- Connection problems

### automation
n8n workflows, scheduled tasks, triggers:
- Workflow not executing
- Incorrect data transformations
- API integration failures
- Timing/scheduling issues

### configuration
Settings, environment variables, configs:
- Invalid JSON/YAML syntax
- Missing required values
- Incorrect paths or references
- Version conflicts

## Severity Levels

### critical
- Work completely blocked
- System/service down
- Data loss risk
- Security vulnerability
- **Action**: Immediate debugging required

### high
- Major feature broken
- Significant workflow disruption
- Multiple users/systems affected
- No workaround available
- **Action**: Prioritize resolution today

### medium
- Feature partially broken
- Workaround exists but inconvenient
- Single user/system affected
- **Action**: Resolve within week

### low
- Minor inconvenience
- Enhancement request
- Documentation issue
- Edge case bug
- **Action**: Track for future improvement

## Companion Script: scan-issues.sh

For performance, use the companion script for:
- **Fast ID generation**: `./scripts/scan-issues.sh --next-id`
- **Quick searching**: `./scripts/scan-issues.sh --category=mcp-server`
- **Status filtering**: `./scripts/scan-issues.sh --unsolved`
- **JSON output**: `./scripts/scan-issues.sh --json` for programmatic use

**Performance**: 30-60x faster than scanning issues manually with grep/awk

The script will be created alongside this command and supports:
```bash
# Get next available ID
./scripts/scan-issues.sh --next-id

# Find unsolved issues
./scripts/scan-issues.sh --unsolved

# Filter by category
./scripts/scan-issues.sh --category=hook

# Filter by severity
./scripts/scan-issues.sh --severity=critical

# Search by keyword in title/description
./scripts/scan-issues.sh --search="supabase"

# JSON output for scripts
./scripts/scan-issues.sh --json
```

## Pre-Issue Checklist (Serena Memory Check)

Before creating an issue, I will check:

1. **Search Serena's memories** for related solutions
   ```javascript
   mcp__serena__list_memories()
   // Read relevant memories like:
   // - suggested_commands.md
   // - mcp_troubleshooting.md
   // - hook_patterns.md
   ```

2. **Common quick fixes to try first**:
   - **MCP issues**: Restart Claude Code, check `.mcp.json` syntax
   - **Hook issues**: Verify permissions (`chmod +x`), check debug log
   - **Script issues**: Check shebang, verify dependencies installed
   - **Command issues**: Validate YAML frontmatter syntax
   - **Database issues**: Check project ID, verify credentials

3. **Documentation references**:
   - Check `claudelife-commands-guide.md` for command patterns
   - Review `.claude/hooks/README-*.md` for hook troubleshooting
   - Consult MCP server documentation in `.mcp.json` comments

4. **Only create issue if**:
   - Quick fixes don't resolve it
   - Serena's memory doesn't have solution
   - Issue is complex enough to track
   - Solution will benefit future debugging

## Post-Resolution Workflow

After resolving an issue (via `/issue-call {ID}`), I will:

1. **Create lesson learned**
   - File: `04-resources/lessons-learnt/YYMMDD-issue-{ID}-{description}.md`
   - Format: Problem → Solution → Prevention

2. **Update issue frontmatter**
   ```yaml
   complete: true
   solved: true
   lesson: /path/to/lesson/file.md
   ```

3. **Suggest adding lesson to commands**
   - Based on category, identify relevant slash commands
   - Propose adding "Common Issues" section
   - Example: Hook issue → update `/create-hook` with troubleshooting

4. **Update Serena's memory** (with confirmation)
   - Add solution pattern to relevant memory file
   - Example: MCP connection issue → update `mcp_troubleshooting.md`
   - Ask before writing: "Should I add this to Serena's memory?"

## Output Format

I'll provide:

1. **Issue file created**
   - Path: `01-areas/claude-code/issues/issue-{ID}-{slug}.md`
   - ID assigned: `issue-{ID}`

2. **Immediate debugging suggestions**
   - Category-specific troubleshooting steps
   - Links to relevant documentation
   - Common solutions for this issue type

3. **Next steps**
   - How to use `/issue-call {ID}` for resolution
   - Where to find debug logs
   - Testing commands to run

4. **Related resources**
   - Similar issues in issue directory
   - Relevant Serena memories
   - Documentation references

## Examples

### Example 1: MCP Server Connection Issue

```
User: /issue-create "Serena MCP won't connect"

I'll check Serena's memory first...

[After checking memories]

I found a similar issue in Serena's memory: "mcp_troubleshooting.md" mentions connection issues often resolve with:
1. Restart Claude Code
2. Check `enabledMcpjsonServers` in settings.local.json
3. Verify server name matches exactly

Have you tried these? If yes, I'll create a detailed issue.

[User confirms tried, still broken]

Creating issue-001-serena-mcp-connection...

✅ Issue created: `01-areas/claude-code/issues/issue-001-serena-mcp-connection.md`

**Debugging suggestions for MCP server issues:**

1. Check debug output:
   ```bash
   # Restart with debug
   claude --mcp-debug
   ```

2. Validate .mcp.json syntax:
   ```bash
   cat .mcp.json | jq .
   ```

3. Verify server installation:
   ```bash
   which serena
   npm list -g | grep serena
   ```

**Next steps:**
- Run debugging commands above
- Check `/tmp/claude-mcp-debug.log`
- Use `/issue-call 001` to document solution once resolved
```

### Example 2: Hook Not Firing

```
User: /issue-create "Post-commit hook isn't running"

Let me check Serena's memory for hook troubleshooting...

[Found relevant memory]

Serena's memory suggests common hook issues:
1. Missing execute permissions (`chmod +x`)
2. Hook not registered in .claude/settings.json
3. Needs Claude Code restart

Quick verification:
```bash
ls -la .claude/hooks/your-hook.sh
cat .claude/settings.json | jq .hooks
```

Should I create an issue or do these solve it?

[User confirms issue persists]

Creating issue-002-hook-not-firing...

✅ Issue created: `01-areas/claude-code/issues/issue-002-hook-post-commit.md`

**Debugging suggestions for hook issues:**

1. Test hook directly:
   ```bash
   export CLAUDE_TOOL_NAME="Bash"
   export CLAUDE_TOOL_COMMAND="git commit"
   .claude/hooks/your-hook.sh
   ```

2. Check debug log:
   ```bash
   tail -50 /tmp/claude-hook-debug.log
   ```

3. Validate matcher pattern:
   - Is "Bash" the correct tool name?
   - Does regex pattern match your command?

**Next steps:**
- Run tests above
- Capture any error output
- Use `/issue-call 002` when resolved
```

### Example 3: Database Migration Failure

```
User: /issue-create "Supabase migration failing"

Checking Serena's memory for database patterns...

[No direct match found]

No similar issues in memory. Let's create a detailed issue.

**What's the exact error message?**

[User provides error]

**Which migration file?**

[User provides path]

Creating issue-003-supabase-migration-failure...

✅ Issue created: `01-areas/claude-code/issues/issue-003-supabase-migration-fk.md`

**Debugging suggestions for database issues:**

1. Check migration syntax:
   ```bash
   cat supabase/migrations/20250118_your_migration.sql
   ```

2. Test migration locally:
   ```bash
   supabase db reset
   supabase db push
   ```

3. Verify project ID:
   ```javascript
   mcp__supabase__get_project_url()
   // Should return gshsshaodoyttdxippwx
   ```

**Next steps:**
- Verify foreign key constraints exist
- Check schema compatibility
- Use `/issue-call 003` with solution
- Consider creating lesson for foreign key patterns
```

## Evaluation Criteria

A successful issue report should:

1. ✅ **Unique sequential ID**: Auto-generated, zero-padded (001, 002, 003)
2. ✅ **Complete YAML frontmatter**: All required fields populated
3. ✅ **Clear problem description**: Expected vs. actual behavior documented
4. ✅ **Technical context captured**: Error messages, related files, environment
5. ✅ **Attempted solutions logged**: What's already been tried
6. ✅ **Category correctly assigned**: Matches issue type for filtering
7. ✅ **Severity appropriately set**: Reflects actual impact and urgency
8. ✅ **Serena memory checked first**: Avoided duplicate solutions
9. ✅ **Debugging suggestions provided**: Next troubleshooting steps clear
10. ✅ **Resolution pathway established**: Clear how to update when solved

## Related Resources

- Issue template: `98-templates/issue.md`
- Issue directory: `01-areas/claude-code/issues/`
- Companion script: `scripts/scan-issues.sh`
- Resolution command: `.claude/commands/issue-call.md`
- Lessons directory: `04-resources/lessons-learnt/`
- Serena memories: `.serena/memories/`
- Commands guide: `04-resources/guides/commands/claudelife-commands-guide.md`

## Starting the Issue Creation Process

What issue would you like to report? Please describe:

1. **What's not working?** (Brief description)
2. **What should happen?** (Expected behavior)
3. **What actually happens?** (Actual behavior)
4. **When did it start?** (After config change, new install, etc.)
5. **What have you tried?** (Attempted solutions)

I'll first check Serena's memory for known solutions, then create a comprehensive issue report if needed.
