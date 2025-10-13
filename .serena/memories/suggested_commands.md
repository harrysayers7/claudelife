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

### Command Documentation
**NEW**: All commands are documented in `/04-resources/guides/commands/claudelife-commands-guide.md`
- Comprehensive reference with "What it does" and "When to use it" sections
- 17 commands documented with usage patterns and file locations
- Automatically updated when creating new commands via `/create-command`

### Research & Knowledge Management
- `/research $ARGUMENTS` - Conduct deep research using GPT Researcher MCP with COSTAR framework optimization
  - Automatically saves research to `/00-inbox/research/` with proper metadata
  - Extracts keywords, tags, and descriptions optimized for RAG retrieval
  - Example: `/research "Claude Code best practices ensuring up to date with oct 13"`

- `/quick-research [optional topic]` - Quick web search for immediate context and answers
  - **With argument**: Research specified topic (e.g., `/quick-research "FastAPI dependencies"`)
  - **Without argument**: Automatically researches context from your last message
  - Uses `quick_search` for speed over depth
  - Perfect for debugging, unfamiliar tech, or quick implementation guidance
  - Displays inline without saving to vault
  - Example: `/quick-research` (analyzes last message) or `/quick-research "Trigger.dev timezone handling"`

### Memory & Context Management
- `/update-serena-memory` - Update Serena MCP's memory after codebase changes
- `/business:mokai:update-mokai-context` - Update MOKAI business context in Serena
- `/tag-keyword-DR-extractor` - Extract keywords and tags from deep research files for RAG optimization

### Daily Note Extraction
- `/extract-context` - Extract context from daily notes to `/04-resources/context.md`
- `/extract-insights` - Extract insights from daily notes to `/01-areas/p-dev/insights.md`
- `/extract-diary` - Extract diary entries to `/04-resources/diary.md`

### MOKAI Business Operations
- `/business:mokai:generate-mokai-flashcards` - Generate learning flashcards from MOKAI research docs
- `/business:mokai:update-mokai-context` - Update Serena's memory with MOKAI business changes

### System Documentation
- `/report:document-system` - Generate comprehensive system documentation with automatic categorization

### Command Creation
- `/create-command` - Interactive command creation wizard with prompt engineering guidance
  - **NEW**: Automatically documents commands in commands guide after creation
  - Enforces consistent structure with YAML frontmatter
  - Includes post-creation documentation step

### Obsidian Vault Management
- `/obsidia` - Activate OBSIDIA mode for vault architecture and knowledge system design
- `/ingest-document` - Process and import external documents into vault

### Analysis & Problem Solving
- `/ultra-think` - Deep multi-dimensional analysis mode for complex problems
- `/challenge` - Critical argument analysis and stress-testing

### Product & Project Management
- `/create-prd` - Create Product Requirements Documents
- `/bmad {agent-name}` - Activate specialized BMAD agents (pm, architect, qa, etc.)

### File Management
- `/move-file` - Move files with automatic reference updates across codebase

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
