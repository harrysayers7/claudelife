---
description: Update Serena MCP's memory after adding new files, scripts, dependencies, or changing project structure
tags: [serena, memory, mcp, documentation, maintenance]
---

# Update Serena Memory

Update Serena MCP's memory files to reflect recent changes in the codebase.

## Usage

```bash
/update-serena-memory
/update-serena-memory [category]
```

## When to Use

Run this command after:
- ✅ Adding new npm scripts or commands
- ✅ Changing project structure significantly
- ✅ Adding/removing major dependencies
- ✅ Establishing new coding patterns or conventions
- ✅ Adding new MCP servers
- ✅ Changing completion workflows
- ✅ Creating new slash commands
- ✅ Implementing new automation workflows

## How It Works

1. **List current memories** to see what exists
2. **Identify changes** that need to be reflected
3. **Update relevant memory categories** with new information
4. **Verify updates** were successfully saved

## Memory Categories

- `suggested_commands` - npm scripts, CLI tools, common commands
- `tech_stack` - Dependencies, frameworks, infrastructure
- `project_structure` - Directory layout and organization
- `task_completion_workflow` - Development workflows and processes
- `system_patterns_and_guidelines` - Coding patterns and best practices
- `code_style_and_conventions` - Style guides and conventions
- `project_overview` - High-level project description

## Execution Steps

### Step 1: List Current Memories

```javascript
mcp__serena__list_memories()
```

Review what memory files currently exist and their purposes.

### Step 2: Identify What Changed

Ask yourself:
- What new scripts or commands were added?
- Did project structure change?
- Were new dependencies or MCP servers added?
- Are there new coding patterns to document?
- Did development workflows change?

### Step 3: Update Relevant Memories

For each identified change, update the appropriate memory category:

#### Example: New npm Scripts

```javascript
mcp__serena__read_memory({
  memory_name: "suggested_commands"
})

// Then update with new content
mcp__serena__write_memory({
  memory_name: "suggested_commands",
  content: `
# Suggested Commands

[... existing content ...]

## New Scripts Added
- npm run sync-upbank - Sync UpBank transactions to Supabase
- npm run categorize-transactions - Run ML categorization on uncategorized transactions
- npm run sync-database-context - Update database schema documentation

[... rest of content ...]
  `
})
```

#### Example: New MCP Server

```javascript
mcp__serena__read_memory({
  memory_name: "tech_stack"
})

mcp__serena__write_memory({
  memory_name: "tech_stack",
  content: `
# Tech Stack

[... existing content ...]

## MCP Servers
- **claudelife-business-api**: FastAPI server for MOKAI business operations
- **claudelife-financial-api**: FastAPI server for financial data and ML categorization
- **trigger**: Trigger.dev automation workflows
- **supabase**: Database operations and migrations

[... rest of content ...]
  `
})
```

#### Example: New Project Structure

```javascript
mcp__serena__read_memory({
  memory_name: "project_structure"
})

mcp__serena__write_memory({
  memory_name: "project_structure",
  content: `
# Project Structure

[... existing content ...]

## New Directories
- 07-context/systems/ - System documentation and technical context
- scripts/ml/ - Machine learning pipeline scripts
- .github/workflows/ - CI/CD automation workflows

[... rest of content ...]
  `
})
```

#### Example: New Coding Patterns

```javascript
mcp__serena__read_memory({
  memory_name: "system_patterns_and_guidelines"
})

mcp__serena__write_memory({
  memory_name: "system_patterns_and_guidelines",
  content: `
# System Patterns and Guidelines

[... existing content ...]

## Error Handling Patterns
- All sync operations use retry logic with exponential backoff
- Confidence thresholds: >0.9 auto, 0.7-0.9 review, <0.7 manual
- State management for resumable operations

## ML Integration Patterns
- Real-time prediction during data sync
- Automatic categorization with fallback logic
- Anomaly detection with severity classification

[... rest of content ...]
  `
})
```

### Step 4: Verify Updates

After updating, verify the changes were saved:

```javascript
mcp__serena__read_memory({
  memory_name: "suggested_commands"
})
```

Confirm the new content is present.

## Interactive Mode

If no specific category is provided, guide the user through:

1. **Review recent changes**
   - Check git log for recent commits
   - Review package.json for new scripts
   - Check .mcp.json for new MCP servers
   - Review new files in key directories

2. **Ask clarifying questions**
   - "What new functionality was added?"
   - "Were any new commands or scripts created?"
   - "Did the project structure change?"
   - "Are there new patterns or conventions to document?"

3. **Suggest memory categories to update**
   - Based on identified changes, recommend which memories need updates

4. **Execute updates**
   - Update each identified memory category
   - Verify changes were saved

## Examples

### After Adding New Slash Commands

```bash
/update-serena-memory
```

```
🔍 Detected changes:
- 3 new slash commands in .claude/commands/finance/
- Updated finance workflow patterns

📝 Updating memories:
✅ suggested_commands - Added finance slash commands
✅ task_completion_workflow - Added finance management workflow

✨ Serena's memory updated successfully!
```

### After Major Infrastructure Change

```bash
/update-serena-memory
```

```
🔍 Detected changes:
- New MCP server: claudelife-financial-api
- New npm scripts: sync-upbank, categorize-transactions
- New ML pipeline in scripts/ml/

📝 Updating memories:
✅ tech_stack - Added FastAPI MCP server and ML dependencies
✅ suggested_commands - Added data sync and ML scripts
✅ system_patterns_and_guidelines - Added ML integration patterns

✨ Serena's memory updated successfully!
```

### Updating Specific Category

```bash
/update-serena-memory suggested_commands
```

Only updates the `suggested_commands` memory with recent command additions.

## Best Practices

1. **Update immediately after major changes** - Don't let memory get stale
2. **Be specific** - Include exact commands, file paths, and usage examples
3. **Maintain existing structure** - Don't completely rewrite, add to existing content
4. **Include context** - Explain why new patterns or commands exist
5. **Verify accuracy** - Read back the memory to ensure updates are correct

## Periodic Maintenance

Run quarterly or after:
- Major feature additions
- Significant refactoring
- New team members joining
- Technology stack changes

## Related Commands

- `/document-system` - Create comprehensive system documentation
- `/check-memory-reminders` - Check for git-generated memory update reminders
- `/remember` - Capture session learnings to memory graph

## Notes

- Serena's memory is separate from the knowledge graph (memory/graph/)
- Memory files are stored in `.serena/memories/`
- Updates should be cumulative, not replacements
- Memory helps Serena provide better context-aware suggestions
