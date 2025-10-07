# Project Structure

## Root Directory Layout
```
claudelife/
├── .claude/                    # Claude Code configuration
│   ├── commands/              # Custom slash commands
│   ├── instructions/          # Domain-specific context packs
│   └── settings.local.json    # Tool permissions, MCP enablement
├── .taskmaster/               # Task Master AI files
│   ├── tasks/                # Task database and files
│   ├── docs/                 # PRDs and documentation
│   └── config.json           # AI model configuration
├── scripts/                   # Automation scripts
│   ├── sync-upbank-enhanced.js
│   ├── sync-supabase-context.js
│   ├── sync-domain-packs.js
│   └── monitor-mcp-health.js
├── context/                   # System context files
│   └── finance/              # Financial context
├── memory/                    # AI learning data
│   ├── conversation-context.md
│   └── active-entities.json
├── automation-system/         # Automation configurations
├── 01-areas/                 # Business areas (MOKAI, MOK HOUSE)
├── 00-inbox/                 # Incoming items and daily notes
├── 04-resources/             # Reference materials
├── 08-context-ai-apps/       # AI app configurations
└── CLAUDE.md                 # Main system instructions
```

## Key Directories

### Configuration & Setup
- `.claude/` - Claude Code settings, commands, context packs
- `.taskmaster/` - Task management system
- `.github/` - GitHub workflows (CI/CD, security)

### Code & Scripts
- `scripts/` - Automation utilities (sync, monitoring, maintenance)
- `utils/` - Shared utility functions
- `shared/` - Shared resources across projects

### Data & Context
- `context/` - System context for AI operations
- `memory/` - Learning data and entity tracking
- `migrations/` - Database schema migrations

### Business Areas
- `01-areas/business/mokai/` - MOKAI business files
- `01-areas/business/mok-house/` - MOK HOUSE files
- `00-inbox/` - Daily notes and temporary items

## File Patterns
- `.env` - Secrets (git-ignored)
- `.mcp.json` - MCP server configuration (git-ignored)
- `CLAUDE.md` - System instructions (tracked)
- `CLAUDE.local.md` - Personal context (git-ignored)
- `package.json` - npm scripts and dependencies
