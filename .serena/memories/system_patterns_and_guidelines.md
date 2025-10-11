# System Patterns and Guidelines

## Architecture Patterns

### Context Engineering
- **Domain pack system**: Business, Technical, and Automation packs (~15K each)
- **Smart loading**: Keyword-triggered context loading to optimize token usage
- **Active entity tracking**: 7-day retention window in `active-entities.json`
- **Graduated loading**: Essential (10K) → mentioned entities (30K) → full context (50K max)

### MCP Server Strategy
- **Project-specific servers**: Configured in `.mcp.json` (git-ignored)
- **Global servers**: Configured in `~/.mcp.json`
- **Explicit enablement**: All servers must be listed in `enabledMcpjsonServers`
- **Specialized functions**: Supabase, Notion, Gmail, UpBank, Stripe, etc.

### Claude Code Hooks System
- **Post-tool execution hooks**: Monitor tool executions for data changes
- **Memory sync automation**: Auto-detect when Serena's memory needs updating
- **Pattern-based triggers**: Match tool names/arguments to detect critical changes
- **Hook configuration**: Defined in `.claude/settings.json`
- **Hook scripts**: Executable bash scripts in `.claude/hooks/`
- **Primary hooks**:
  - `post-tool-memory-sync-trigger.sh` - Monitors Supabase/Obsidian/MCP changes

### Automation Patterns
- **Error recovery**: Checkpoint-based resumable sync operations
- **Fallback mechanisms**: Multiple retry strategies with exponential backoff
- **State management**: Database-backed state for long-running operations
- **Monitoring**: Health checks and dashboard monitoring

### Database Design
- **Supabase as source of truth**: Project ID `gshsshaodoyttdxippwx`
- **FK relationships**: Proper foreign keys for data integrity
- **Context sync**: Bidirectional sync between database and local files
- **Schema migrations**: SQL files in `migrations/` directory

## Development Guidelines

### Security First
- **Never hardcode secrets**: Use environment variables
- **Pre-commit scanning**: Automated with gitleaks and trufflehog
- **Exclusion patterns**: Configure `.trufflehog.yaml` and `.gitleaks.toml`
- **Regular audits**: System health checks include security validation

### Token Optimization
- **Context budgets**: Typical 23K, max 50K tokens
- **Lazy loading**: Load context only when keywords detected
- **Compression**: Summarize older context when approaching limits
- **Smart caching**: MCP servers maintain independent caches

### Memory Management
- **Serena memory files**: Located in `.serena/memories/`
- **Update triggers**: Changes to critical data sources (Supabase, MOKAI docs, MCP config)
- **Automated reminders**: Hooks notify when memory update recommended
- **Update command**: `/update-serena-memory` refreshes Serena's context
- **Memory categories**: project_overview, tech_stack, suggested_commands, system_patterns, etc.

### Error Handling
- **Categorized errors**: Transient, permanent, rate-limit handling
- **Retry logic**: Exponential backoff with jitter
- **State preservation**: Checkpoint progress for resumability
- **User notification**: Clear error messages with recovery suggestions

### Testing Approach
- **Manual verification**: Test scripts before automation
- **Incremental rollout**: Test in dev before production
- **Monitoring**: Track success rates and error patterns
- **Rollback ready**: Maintain previous versions for quick reversion

## Design Patterns in Use

### ML Pipeline Pattern
- **Confidence scoring**: Auto (>0.9), review (0.7-0.9), manual (<0.7)
- **Real-time classification**: During data sync operations
- **Anomaly detection**: Severity-based routing
- **Feedback loops**: Improve models based on corrections

### Business Rule Automation
- **Keyword matching**: Automatic expense categorization
- **Formula translation**: Notion formulas → JavaScript
- **Tax flagging**: Automatic deductibility detection
- **Workflow integration**: Direct accounting system updates

### Hook-Based Automation
- **Event-driven updates**: React to tool executions automatically
- **Context freshness**: Maintain up-to-date agent knowledge
- **Pattern detection**: Smart triggers based on tool patterns
- **User prompts**: Non-intrusive reminders for manual actions
