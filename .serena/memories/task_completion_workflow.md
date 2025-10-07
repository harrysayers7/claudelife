# Task Completion Workflow

## When a Task is Completed

### 1. Testing (if applicable)
- Run relevant test scripts from package.json
- Verify automation scripts work correctly
- Test MCP server connections if modified

### 2. Code Quality
- Pre-commit hooks automatically run:
  - gitleaks (secret scanning)
  - trufflehog (credential detection)
- Fix any security issues before committing

### 3. Documentation
- Update CLAUDE.md if system behavior changed
- Update README.md for user-facing changes
- Create/update relevant slash commands in `.claude/commands/`
- Update domain pack context files if business logic changed

### 4. Context Synchronization
- Run `npm run sync-context` to update Supabase context
- Run `npm run sync-domain-packs` to update domain-specific packs
- Or run `npm run sync-all` for comprehensive sync

### 5. Task Master Updates
- Update task status: `task-master set-status --id=<id> --status=done`
- Add implementation notes: `task-master update-subtask --id=<id> --prompt="notes"`
- Get next task: `task-master next`

### 6. Git Workflow
- Stage changes: `git add .`
- Commit with semantic message: `git commit -m "feat: description"`
- Push to remote: `git push`

### 7. System Health Check (for major changes)
- Run `npm run system-health` to verify:
  - Context usage analysis
  - MCP server health
- Monitor UpBank sync if financial integration changed

## Special Cases

### New MCP Server Added
1. Add to `.mcp.json` with proper configuration
2. Add to `enabledMcpjsonServers` in `~/.claude/settings.local.json`
3. Restart Claude Code
4. Verify with `ListMcpResourcesTool`

### Database Schema Changes
1. Create migration SQL files
2. Test with `npm run setup-banking` or equivalent
3. Update context sync scripts
4. Run sync to propagate changes

### Automation Script Updates
1. Test script manually first
2. Update cron jobs or n8n workflows if scheduled
3. Document in slash commands if user-facing
