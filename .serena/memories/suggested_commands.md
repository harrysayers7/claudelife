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

## Git Operations
- `git add .` - Stage changes
- `git commit -m "message"` - Commit with message
- `git push` - Push to remote
- Pre-commit hooks automatically run security scans (gitleaks, trufflehog)

## Common System Commands (macOS)
- `ls` - List directory contents
- `cd <path>` - Change directory
- `grep <pattern> <file>` - Search for pattern in files
- `find <path> -name <pattern>` - Find files by name
- `cat <file>` - Display file contents
- `open <file>` - Open file with default application
