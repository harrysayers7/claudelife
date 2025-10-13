# Project Structure

## Root Directory Layout
```
claudelife/
├── .claude/                    # Claude Code configuration
│   ├── commands/              # Custom slash commands
│   ├── instructions/          # Domain-specific context packs
│   ├── hooks/                # Post-tool execution hooks
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
├── 01-areas/                 # Areas of responsibility (PARA method)
│   ├── business/             # Business entities (mokai, mokhouse, etc.)
│   ├── health-fitness/       # Health and fitness tracking
│   ├── p-dev/               # Personal development
│   └── tech/                # Technical areas (ai, mac, ableton)
├── 00-inbox/                 # Incoming items and daily notes
├── 04-resources/             # Reference materials and guides
│   └── guides/              # Documentation guides
│       └── commands/        # Command reference documentation
├── 07-context/               # System context documentation
│   └── systems/             # System-specific context files
├── 08-context-ai-apps/       # AI app configurations
└── CLAUDE.md                 # Main system instructions
```

## Key Directories

### Configuration & Setup
- `.claude/` - Claude Code settings, commands, context packs, hooks
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

### Business Areas (PARA Method)
- `01-areas/business/` - Business entities with context files
  - `mokai/` - MOKAI cybersecurity consultancy
  - `mokhouse/` - MOK HOUSE music production
  - `accounting/`, `safia/`, `soletrader/`, `trust/`, `crypto/`, `SMSF/`
- `01-areas/health-fitness/` - Health tracking with context files
  - `diet/`, `gym/`, `medical/`
- `01-areas/p-dev/` - Personal development with context files
  - `learning/`, `mindset/`, `psychedelics/`
- `01-areas/tech/` - Technical areas with context files
  - `ai/`, `mac/`, `ableton/`
- `00-inbox/` - Daily notes and temporary items
- `04-resources/guides/` - Documentation and reference guides
  - `commands/` - Comprehensive command documentation

## Context File Pattern
Each area subfolder contains a `context-{name}.md` file with:
- `type: context` frontmatter property
- `relation: [[name]]` links for knowledge graph
- Consistent structure across all areas

## File Patterns
- `.env` - Secrets (git-ignored)
- `.mcp.json` - MCP server configuration (git-ignored)
- `CLAUDE.md` - System instructions (tracked)
- `CLAUDE.local.md` - Personal context (git-ignored)
- `package.json` - npm scripts and dependencies
- `context-*.md` - Area context files (tracked)
