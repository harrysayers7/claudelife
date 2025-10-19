---
created: "2025-10-16 14:35"
description: |
  Creates comprehensive Claude Code hooks with full ecosystem integration, Context7 verification, and testing strategy. Analyzes existing hooks, MCP servers, agents, and scripts to suggest optimal integration points. Supports all hook types (PreToolUse, PostToolUse, UserPromptSubmit, PostSystemCompletion) with complete validation and documentation workflow.
examples:
  - /create-hook "auto-commit MOKAI diary entries when tasks complete"
  - /create-hook "validate Supabase migrations before deployment"
  - /create-hook "sync Linear issues when GitHub PRs merge"
---

# Create Hook

This command helps you create production-ready Claude Code hooks that integrate deeply with your claudelife ecosystem. It validates configurations with Context7, suggests integrations with existing MCP servers and agents, identifies script optimization opportunities, and provides comprehensive testing strategies.

## Usage

```bash
/create-hook [optional: brief description of what the hook should do]
```

## What This Command Does

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

This command creates hooks that:
1. **Analyze your ecosystem**: Examine existing hooks, MCP servers, agents, and scripts
2. **Suggest integrations**: Identify opportunities to enhance existing workflows
3. **Optimize performance**: Recommend companion scripts for speed (like `scan-tasks.sh`)
4. **Validate with Context7**: Verify hook configurations against official patterns
5. **Provide testing strategy**: Include comprehensive validation and debugging steps
6. **Document thoroughly**: Create README files with usage examples and troubleshooting

## Interactive Process

When you run this command, I will:

1. **Understand your requirements**
   - Ask about the hook's purpose and trigger conditions
   - Clarify which tools/events should trigger the hook
   - Identify the desired outcome/actions

2. **Analyze existing ecosystem**
   - Scan `.claude/hooks/` for existing hooks
   - Review `.claude/agents/` for agent integration opportunities
   - Check `/scripts/` for reusable automation
   - Examine `.claude/settings.json` for current hook patterns
   - Identify MCP servers that could enhance the hook

3. **Performance optimization analysis**
   - Determine if companion scripts would accelerate the hook
   - Estimate time savings (e.g., `scan-tasks.sh` provides 30-60x speedup)
   - Suggest caching strategies for repeated operations
   - Recommend batch processing where applicable

4. **Hook type selection**
   - **PreToolUse**: Security checks, validation, logging before tool execution
   - **PostToolUse**: Auto-formatting, testing, documentation after tool use
   - **UserPromptSubmit**: Context enhancement, validation before processing user input
   - **PostSystemCompletion**: Documentation suggestions, cleanup after task completion

5. **Context7 verification**
   - Fetch official Claude Code hooks documentation
   - Validate hook configuration syntax
   - Verify environment variable patterns
   - Confirm matcher patterns and command structure

6. **Integration suggestions**
   - Identify MCP servers to leverage (Serena, Supabase, Linear, etc.)
   - Suggest agent workflows that complement the hook
   - Find script patterns to reuse
   - Recommend existing hook patterns to extend

7. **Create comprehensive hook package**
   - Hook script file (`.sh` or `.py`)
   - Settings.json configuration
   - README documentation
   - Test scenarios
   - Debug logging setup
   - Troubleshooting guide

## Hook Types Deep Dive

### PreToolUse Hooks

**When to use**: Before Claude Code executes a tool

**Common patterns**:
- Security validation (prevent committing secrets)
- File protection (block edits to critical files)
- Context enrichment (add business context to prompts)
- Logging/auditing tool usage

**Example use cases**:
- Prevent `git commit` with hardcoded API keys
- Block edits to production config files
- Add MOKAI business context when editing proposals
- Log all database operations for compliance

**Environment variables available**:
- `CLAUDE_TOOL_NAME`: Tool being executed (e.g., "Edit", "Write", "Bash")
- `CLAUDE_TOOL_FILE_PATH`: File path for file operations
- `CLAUDE_TOOL_COMMAND`: Command for Bash operations

### PostToolUse Hooks

**When to use**: After Claude Code successfully executes a tool

**Common patterns**:
- Auto-formatting code (Prettier, Black, etc.)
- Running tests after changes
- Syncing data to external systems
- Updating documentation
- Capturing workflow events to diary

**Example use cases**:
- Auto-format TypeScript files after editing
- Run `npm test` after package.json changes
- Sync completed tasks to Linear
- Auto-commit diary entries when MOKAI tasks complete
- Update Serena's memory after major structural changes

**Environment variables available**:
- Same as PreToolUse, plus:
- `CLAUDE_TOOL_SUCCESS`: "true" if tool executed successfully
- `CLAUDE_TOOL_OUTPUT`: Tool execution output

### UserPromptSubmit Hooks

**When to use**: Before processing user input

**Common patterns**:
- Context detection (identify library mentions)
- Security scanning (detect malicious patterns)
- Workflow routing (direct to specialized agents)
- Context enrichment (add relevant memories)

**Example use cases**:
- Detect library mentions and suggest Context7 lookup
- Identify MOKAI-related queries and route to agent-mokai
- Scan for sensitive data in prompts
- Add relevant Serena memories based on keywords

**Environment variables available**:
- `CLAUDE_USER_PROMPT`: The user's input text

### PostSystemCompletion Hooks

**When to use**: After completing a system-level operation

**Common patterns**:
- Documentation updates
- Cleanup operations
- Status reporting
- Analytics/tracking

**Example use cases**:
- Suggest documenting new MCP servers
- Clean up temporary files
- Report task completion statistics
- Update project dashboards

## Script & Performance Optimization

### When Scripts Accelerate Hooks

**Indicators you need a companion script**:
- Processing 10+ files per hook execution
- Parsing structured data (YAML frontmatter, JSON)
- Filtering/searching large directories
- Operations that run frequently (multiple times per hour)
- Batch operations on task lists, diary entries, or markdown files

**Performance examples**:
```bash
# Without script: 30+ seconds
for file in $(find . -name "*.md"); do
  grep -l "status: pending" "$file"
done

# With script (scan-tasks.sh): <1 second
./scripts/scan-tasks.sh --status=pending
```

**Script benefits**:
- **30-60x speedup** for file operations
- **Caching** reduces repeated API calls
- **Batch processing** for database operations
- **Background execution** for long-running tasks

### Creating Companion Scripts

I will suggest creating scripts when:
1. Hook processes 10+ markdown files
2. Hook parses YAML/JSON repeatedly
3. Hook filters task lists or diary entries
4. Hook needs to run in <1 second for UX

**Script template structure**:
```bash
#!/bin/bash
# Purpose: [What this script accelerates]
# Performance: [Time comparison]
# Cache: [Where cache is stored]

# Fast filtering with grep
# Batch operations
# Result caching
```

## Context7 Verification Process

Before finalizing any hook configuration, I will:

1. **Resolve Claude Code hooks library**
   ```javascript
   mcp__context7__resolve-library-id("claude-code hooks")
   ```

2. **Fetch official documentation**
   ```javascript
   mcp__context7__get-library-docs({
     context7CompatibleLibraryID: "/davila7/claude-code-templates",
     topic: "hook configuration syntax patterns validation",
     tokens: 5000
   })
   ```

3. **Validate against official patterns**:
   - Hook type syntax (PreToolUse, PostToolUse, etc.)
   - Matcher patterns (tool names, regex)
   - Command structure (type: "command", proper escaping)
   - Environment variable usage
   - Exit code handling

4. **Check for breaking changes**:
   - Syntax changes in Claude Code versions
   - Deprecated patterns
   - New best practices

5. **Verify integration patterns**:
   - Proper MCP tool invocation
   - Script execution permissions
   - Error handling approaches
   - Non-blocking execution

## Ecosystem Integration Analysis

### Existing Hook Patterns

I will analyze your current hooks in `.claude/hooks/`:
- `post-tool-auto-diary-capture.sh`: Pattern for diary automation
- `post-tool-memory-sync-trigger.sh`: Pattern for Serena memory updates
- `context7_detector.py`: Pattern for context enrichment
- `protect-critical-docs.json`: Pattern for security validation

### MCP Server Opportunities

I will identify which MCP servers could enhance your hook:

**Available MCP servers** (from your `.mcp.json`):
- `serena`: Code analysis, memory management
- `supabase`: Database operations, migrations
- `linear-server`: Issue tracking, task sync
- `task-master-ai`: Task management, status updates
- `gmail`: Email automation, notifications
- `github`: Repository operations, PR management
- `trigger`: Workflow automation, scheduled tasks
- `notion`: Documentation, knowledge base
- `upbank`: Financial data, transaction sync
- `memory`: Knowledge graph operations

**Example integrations**:
```javascript
// Hook triggers Serena memory update
mcp__serena__write_memory({
  memory_name: "recent_changes",
  content: "Updated authentication system"
})

// Hook syncs to Linear
mcp__linear-server__create_issue({
  title: "Security scan detected issue",
  team: "Engineering"
})

// Hook updates Supabase
mcp__supabase__execute_sql({
  query: "INSERT INTO audit_log ..."
})
```

### Agent Workflow Integration

I will suggest agent workflows that complement your hook:

**Available agents** (from `.claude/agents/`):
- `agent-mokai.md`: MOKAI business operations
- `agent-mokhouse.md`: MOK HOUSE management
- `mcp-expert.md`: MCP server development
- `code-reviewer.md`: Code quality checks
- `test-engineer.md`: Testing strategies

**Example agent integration**:
```bash
# Hook detects MOKAI context, suggests agent
if [[ "$FILE_PATH" == *"mokai"* ]]; then
  echo "💡 Consider using /agent-mokai for MOKAI-specific tasks"
fi
```

### Script Reuse Opportunities

I will identify existing scripts to leverage:

**Available scripts** (from `/scripts/`):
- `scan-tasks.sh`: Fast task filtering (30-60x speedup)
- `cache-mokai-inbox.sh`: MOKAI file caching
- `sync-upbank-data.js`: Financial data sync
- `monitor-mcp-health.js`: MCP server monitoring
- `rename-file.sh`: Safe file renaming with git

## Hook Configuration Structure

All hooks follow this pattern in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/your-hook-name.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/another-hook.sh"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/prompt-handler.py"
          }
        ]
      }
    ]
  }
}
```

### Matcher Patterns

**Specific tools**:
```json
"matcher": "Edit"           // Only Edit tool
"matcher": "Write"          // Only Write tool
"matcher": "Bash"           // Only Bash tool
```

**Multiple tools**:
```json
"matcher": "Edit|Write"                    // Edit OR Write
"matcher": "Edit|Write|MultiEdit"          // Any file operation
"matcher": "Bash|mcp__*"                   // Bash or any MCP tool
```

**Regex patterns**:
```json
"matcher": "mcp__serena__.*"               // All Serena tools
"matcher": "mcp__.*"                       // All MCP tools
"matcher": "*"                              // All tools (use sparingly)
```

## Environment Variables Reference

### All Hooks
- `CLAUDE_WORKING_DIR`: Current working directory
- `CLAUDE_SESSION_ID`: Unique session identifier

### Tool-Specific (PreToolUse, PostToolUse)
- `CLAUDE_TOOL_NAME`: Name of the tool (e.g., "Edit", "Write", "Bash")
- `CLAUDE_TOOL_FILE_PATH`: File path for file operations (Edit, Write, Read)
- `CLAUDE_TOOL_COMMAND`: Command for Bash operations
- `CLAUDE_TOOL_SUCCESS`: "true" if tool succeeded (PostToolUse only)
- `CLAUDE_TOOL_OUTPUT`: Tool output (PostToolUse only)

### Prompt-Specific (UserPromptSubmit)
- `CLAUDE_USER_PROMPT`: The user's input text

## Hook Script Best Practices

### 1. Always Exit Successfully

Hooks should **never** block the workflow unless intentionally:

```bash
#!/bin/bash
# GOOD: Always exit 0
set +e  # Don't exit on errors
your_command || true
exit 0

# BAD: Can block workflow
set -e
your_command  # If this fails, hook fails
```

### 2. Debug Logging

Always log to a debug file:

```bash
DEBUG_LOG="/tmp/claude-hook-debug.log"

log_debug() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$DEBUG_LOG"
}

log_debug "Hook started: $CLAUDE_TOOL_NAME"
log_debug "File: $CLAUDE_TOOL_FILE_PATH"
```

### 3. Fast Execution

Hooks should complete in <2 seconds:

```bash
# GOOD: Fast check
if [[ "$FILE_PATH" == *".env"* ]]; then
  echo "⚠️  Warning: Editing sensitive file"
fi

# BAD: Slow operation
npm test  # Can take minutes
```

### 4. Idempotency

Hooks should be safe to run multiple times:

```bash
# GOOD: Check before adding
if ! grep -q "$ENTRY" "$DIARY_FILE"; then
  echo "$ENTRY" >> "$DIARY_FILE"
fi

# BAD: Always appends
echo "$ENTRY" >> "$DIARY_FILE"  # Creates duplicates
```

### 5. Error Handling

Handle errors gracefully:

```bash
if [[ ! -f "$FILE_PATH" ]]; then
  log_debug "File not found: $FILE_PATH"
  exit 0  # Don't block workflow
fi

# Verify commands exist
if ! command -v jq &> /dev/null; then
  log_debug "jq not installed, skipping JSON processing"
  exit 0
fi
```

## Testing Strategy

### Manual Testing Workflow

After creating a hook, I will provide this testing checklist:

1. **Verify hook script permissions**
   ```bash
   chmod +x .claude/hooks/your-hook-name.sh
   ls -la .claude/hooks/your-hook-name.sh
   # Should show: -rwxr-xr-x
   ```

2. **Test hook script directly**
   ```bash
   # Set test environment variables
   export CLAUDE_TOOL_NAME="Edit"
   export CLAUDE_TOOL_FILE_PATH="test.md"

   # Run hook
   .claude/hooks/your-hook-name.sh

   # Check debug log
   tail -20 /tmp/claude-hook-debug.log
   ```

3. **Validate settings.json syntax**
   ```bash
   # Must parse without errors
   cat .claude/settings.json | jq .
   ```

4. **Restart Claude Code**
   ```bash
   exit
   claude
   ```

5. **Trigger hook with real action**
   ```bash
   # Example for PostToolUse Edit hook
   echo "test" > test-file.md
   # Hook should fire automatically

   # Check hook output
   # Check debug log
   tail -50 /tmp/claude-hook-debug.log
   ```

6. **Verify expected behavior**
   - Check files were modified correctly
   - Verify external systems updated (Linear, Notion, etc.)
   - Confirm no errors in debug log
   - Ensure workflow wasn't blocked

### Automated Testing

For complex hooks, I will suggest:

```bash
# Create test suite
.claude/hooks/tests/test-your-hook.sh

#!/bin/bash
# Test script for your-hook

test_basic_functionality() {
  export CLAUDE_TOOL_NAME="Edit"
  export CLAUDE_TOOL_FILE_PATH="test.md"

  # Run hook
  .claude/hooks/your-hook.sh

  # Assert expected outcome
  if [[ $? -eq 0 ]]; then
    echo "✅ Test passed"
  else
    echo "❌ Test failed"
    exit 1
  fi
}

test_basic_functionality
```

### Performance Testing

For hooks with companion scripts:

```bash
# Benchmark without script
time {
  # Your slow operation
}

# Benchmark with script
time {
  ./scripts/your-companion-script.sh
}

# Compare results
echo "Speedup: X times faster"
```

## Troubleshooting Guide Template

Every hook will include comprehensive troubleshooting:

### Hook Not Firing

1. **Restart Claude Code** (hooks only load on startup)
   ```bash
   exit
   claude
   ```

2. **Check permissions**
   ```bash
   ls -la .claude/hooks/your-hook.sh
   chmod +x .claude/hooks/your-hook.sh
   ```

3. **Validate settings.json**
   ```bash
   cat .claude/settings.json | jq .
   ```

4. **Check matcher pattern**
   - Is the tool name correct?
   - Does regex pattern match?
   - Is hook registered for right event type?

### Hook Firing But Not Working

1. **Check debug log**
   ```bash
   tail -100 /tmp/claude-hook-debug.log
   grep ERROR /tmp/claude-hook-debug.log
   ```

2. **Test script directly**
   ```bash
   export CLAUDE_TOOL_NAME="YourTool"
   export CLAUDE_TOOL_FILE_PATH="/path/to/file"
   .claude/hooks/your-hook.sh
   ```

3. **Verify dependencies**
   ```bash
   # Check required commands exist
   command -v jq
   command -v python3
   command -v node
   ```

4. **Check file paths**
   - Are paths absolute or relative?
   - Do files/directories exist?
   - Correct permissions?

### Hook Blocking Workflow

1. **Check exit code**
   ```bash
   # Hook should always exit 0
   # Even on errors (unless intentional blocking)
   ```

2. **Add timeout**
   ```bash
   # Wrap slow operations
   timeout 5s your-slow-command || true
   ```

3. **Make async**
   ```bash
   # Run in background
   your-slow-command &
   disown
   exit 0
   ```

## Output Format

I will provide:

1. **Hook script file** (`.sh` or `.py`)
   - Complete implementation
   - Debug logging
   - Error handling
   - Environment variable usage
   - Comments explaining logic

2. **Settings.json configuration**
   - Exact JSON to add to `.claude/settings.json`
   - Matcher pattern explained
   - Integration with existing hooks

3. **README documentation** (`.claude/hooks/README-your-hook.md`)
   - What the hook does
   - How it works
   - Configuration details
   - Usage examples
   - Troubleshooting guide
   - Integration points

4. **Companion script** (if needed for performance)
   - Script in `/scripts/`
   - Performance benchmarks
   - Caching implementation
   - Usage examples

5. **Test scenarios**
   - Manual testing steps
   - Automated test script
   - Expected behaviors
   - Edge cases to verify

6. **Integration suggestions**
   - MCP servers to leverage
   - Agents to complement
   - Existing hooks to extend
   - Scripts to reuse

## Examples

### Example 1: Auto-Diary Capture Hook (Existing Pattern)

**Purpose**: Automatically log MOKAI wins, learnings, and context to daily diary

**Hook type**: PostToolUse

**Triggers on**: Write, Edit, Bash

**Integration**:
- Parses task-master commands
- Detects MOKAI file edits
- Updates diary with proper sections
- Uses template for new diary files

**Performance**: No script needed (simple file operations)

**Files**:
- `.claude/hooks/post-tool-auto-diary-capture.sh`
- `.claude/hooks/README-auto-diary.md`
- Configuration in `.claude/settings.json`

### Example 2: Context7 Detector Hook (Existing Pattern)

**Purpose**: Detect library mentions and suggest Context7 lookup

**Hook type**: UserPromptSubmit

**Triggers on**: Every user prompt

**Integration**:
- Python script for text analysis
- Suggests Context7 MCP tool
- Non-blocking suggestions
- Caches common library names

**Performance**: Python script caches library names for speed

**Files**:
- `.claude/hooks/context7_detector.py`
- `.claude/hooks/README-context7-detector.md`
- Configuration in `.claude/settings.json`

### Example 3: Supabase Migration Validator (Hypothetical)

**Purpose**: Validate Supabase migrations before deployment

**Hook type**: PreToolUse

**Triggers on**: Bash (specifically supabase deploy commands)

**Integration**:
- Uses `mcp__supabase__get_advisors` for validation
- Checks migration syntax
- Verifies schema compatibility
- Blocks deployment if issues found

**Performance**: Uses Supabase MCP directly (fast)

**Files**:
- `.claude/hooks/pre-tool-supabase-validate.sh`
- `.claude/hooks/README-supabase-validator.md`
- Configuration in `.claude/settings.json`

**Testing**:
```bash
# Test by attempting migration
supabase db push
# Hook should validate before execution
```

### Example 4: Linear Task Sync Hook (Hypothetical)

**Purpose**: Sync completed Task Master tasks to Linear

**Hook type**: PostToolUse

**Triggers on**: Bash (task-master set-status --status=done)

**Integration**:
- Parses task-master output
- Uses `mcp__linear-server__create_issue`
- Updates existing Linear issues
- Adds completion timestamp

**Performance**: Batch operations for multiple tasks

**Files**:
- `.claude/hooks/post-tool-linear-sync.sh`
- `.claude/hooks/README-linear-sync.md`
- Configuration in `.claude/settings.json`

**Testing**:
```bash
# Complete a task
task-master set-status --id=1.2.3 --status=done

# Verify Linear issue created/updated
# Check debug log
tail -20 /tmp/claude-hook-debug.log
```

## Post-Creation Workflow

After creating the hook, I will:

1. **Update Commands Guide**
   - Add entry to `claudelife-commands-guide.md`
   - Document the new hook
   - Reference from related commands

2. **Suggest Serena Memory Update**
   - Remind you to run `/update-serena-memory`
   - Ensure Serena knows about new hook patterns

3. **Provide Next Steps**
   - Installation instructions
   - Testing checklist
   - Integration opportunities
   - Potential enhancements

## Evaluation Criteria

A successful hook should:

1. ✅ **Execute reliably**: No crashes, always exits cleanly
2. ✅ **Fast performance**: Completes in <2 seconds (or uses background processing)
3. ✅ **Proper integration**: Leverages relevant MCP servers and agents
4. ✅ **Validated configuration**: Context7-verified syntax and patterns
5. ✅ **Comprehensive testing**: Includes manual and automated test strategies
6. ✅ **Well documented**: README with examples and troubleshooting
7. ✅ **Non-blocking**: Only blocks workflow when intentional (security)
8. ✅ **Debug logging**: Logs to `/tmp/claude-hook-debug.log` for troubleshooting
9. ✅ **Idempotent**: Safe to run multiple times without side effects
10. ✅ **Error handling**: Gracefully handles missing files, commands, or services

## Related Resources

- Existing hooks: `.claude/hooks/`
- Hook documentation: `.claude/hooks/README-*.md`
- Settings: `.claude/settings.json`
- Scripts: `/scripts/`
- MCP servers: `.mcp.json`
- Agents: `.claude/agents/`
- Commands guide: `04-resources/guides/commands/claudelife-commands-guide.md`

## Starting the Hook Creation Process

What hook would you like to create? Please describe:

1. **Purpose**: What should the hook accomplish?
2. **Trigger**: What event/tool should trigger it?
3. **Actions**: What should happen when it fires?
4. **Integration**: Any specific MCP servers, agents, or systems to integrate?
5. **Performance**: Any special performance requirements or concerns?

I'll analyze your ecosystem, verify with Context7, suggest optimizations, and create a complete hook package with testing strategy and documentation.
