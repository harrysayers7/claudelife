# Suggested Commands

## Task Management
- `task-master list` - View all tasks with status
- `task-master next` - Get next available task to work on
- `task-master show <id>` - View detailed task information
- `task-master set-status --id=<id> --status=done` - Mark task complete

## Data Synchronization
- `npm run sync-upbank` - Sync UpBank financial data
- `npm run sync-upbank-enhanced` - Enhanced UpBank sync with error recovery
- `npm run sync-context` - Sync Supabase context to local files
- `npm run sync-domain-packs` - Update domain-specific context packs
- `npm run sync-all` - Run all context sync operations

## System Monitoring
- `npm run sync-upbank-monitor` - Monitor UpBank sync status
- `npm run monitor-mcp` - Check MCP server health
- `npm run analyze-context` - Analyze context usage and token consumption
- `npm run system-health` - Run all monitoring checks

## Development Utilities
- `npm run memory-maintenance` - Clean up and optimize memory files
- `npm run setup-banking` - Initialize personal banking database schema

## Claude Code Slash Commands

### Memory & Context Management
- `/update-serena-memory` - Update Serena MCP's memory after codebase changes
- `/business:mokai:update-mokai-context` - Update MOKAI business context in Serena

### MOKAI Business Operations
- `/business:mokai:generate-mokai-flashcards` - Generate learning flashcards from MOKAI research docs
- `/business:mokai:update-mokai-context` - Update Serena's memory with MOKAI business changes

### System Documentation
- `/report:document-system` - Generate comprehensive system documentation with automatic categorization

## Git Operations
- `git add .` - Stage changes
- `git commit -m "message"` - Commit with message
- `git push` - Push to remote
- `/git:commit "message"` - Quick add, commit, and status check via slash command
- Pre-commit hooks automatically run security scans (gitleaks, trufflehog)

## Memory Sync Automation
The memory sync hook automatically detects when Serena's memory needs updating:
- **Supabase changes**: Updates to `invoices`, `entities`, `contacts` tables
- **Obsidian changes**: Edits to MOKAI docs in `01-areas/business/mokai/`
- **MCP config changes**: Updates to `.mcp.json`
- **Claude files**: Changes to `.claude/instructions/`, `.claude/agents/`, `.claude/commands/`

When detected, you'll see:
```
💾 [Source]: [What changed]
🔄 Recommendation: Update Serena's memory to reflect changes
   Run: /update-serena-memory
```

## Common System Commands (macOS)
- `ls` - List directory contents
- `cd <path>` - Change directory
- `grep <pattern> <file>` - Search for pattern in files
- `find <path> -name <pattern>` - Find files by name
- `cat <file>` - Display file contents
- `open <file>` - Open file with default application
