# Sync Commands Guide

Scan `.claude/commands/` for new commands and identify which ones haven't been added to the commands guide.

## Steps

1. Use MCP serena tool to recursively list all command files in `.claude/commands/`
2. Read the current commands guide at `/Users/harrysayers/Developer/claudelife/HARRY/guides/commands-guide.md`
3. Extract all currently documented command paths from the guide
4. Compare the lists to identify new undocumented commands
5. Present findings with category suggestions for where to add them

## Example Output

```
📋 Commands Guide Sync Report

✅ Total commands found: 85
📚 Currently documented: 82

🆕 New undocumented commands (3):
- .claude/commands/finance/add-business-keyword.md → Suggested category: Financial Commands
- .claude/commands/tm/research.md → Suggested category: Task Management
- .claude/commands/popular/ultra-think.md → Suggested category: Popular Commands

💡 Recommendations:
1. Add new commands to their suggested categories
2. Update quick reference table
3. Add usage examples if needed
```

## Implementation

Use `mcp__serena__list_dir` with recursive option to scan `.claude/commands/`, then parse the guide markdown to extract command references, compare lists, and generate the report.

IMPORTANT: Use Serena to search through the codebase. If you get any errors using Serena, retry with different
Serena tools.
