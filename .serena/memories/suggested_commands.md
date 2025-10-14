# Suggested Commands

## Serena Memory Reference

**MOKAI-Specific Patterns**: See `mokai_business_patterns` memory for:
- Diary note structure and sections
- Dashboard format and auto-update behavior
- Inbox task frontmatter requirements
- Phase 1 checklist workflow
- Slash command purposes (`/mokai-status`, `/mokai-weekly`, `/mokai-insights`)
- Tracking system concepts (same-day re-reading, deduplication, fuzzy matching)

## Task Management
- `task-master list` - View all tasks with status
- `task-master next` - Get next available task to work on
- `task-master show <id>` - View detailed task information
- `task-master set-status --id=<id> --status=done` - Mark task complete
- **NEW**: `npm run scan-tasks` - Quick scan of all ai-assigned tasks with status breakdown
- **NEW**: `npm run scan-tasks:json` - JSON output for programmatic task filtering

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
- 18 commands documented with usage patterns and file locations
- Automatically updated when creating new commands via `/create-command`

### Task Management Commands
- `/complete-task "[task-filename.md or description]"` - Execute specific task from `/00-inbox/tasks/`
  - Uses Serena MCP for codebase exploration when needed
  - Direct execution by default (add `--confirm` for approval before implementation)
  - Marks `Done: true` upon completion
  - Commits changes with descriptive message
  - Example: `/complete-task "Install GPT Researcher mcp.md"`
  - Example: `/complete-task "Fix authentication bug.md"`
  - Complements `/sort-tasks` (batch processing) with individual task execution

- `/sort-tasks` - Batch process all AI-assigned tasks in inbox
  - **PERFORMANCE**: Uses `scan-tasks.sh` script for instant task filtering (<1 second vs 30+ seconds)
  - Executes all tasks with `ai-assigned: true` sequentially
  - Skips tasks with `ai-ignore: true` (reserved for future work, not ready yet)
  - Cleans up completed tasks older than 2 weeks
  - Commits changes with summary
  - Use for automated batch processing vs. `/complete-task` for specific tasks

### Task Scanning Script (NEW)
**Script**: `./scripts/scan-tasks.sh`
**Purpose**: Instantly filter and categorize ai-assigned tasks
**Performance**: 30-60x faster than manual file reading (100+ tasks in <1 second)

**Usage**:
```bash
# Human-readable output
./scripts/scan-tasks.sh
npm run scan-tasks

# JSON output for programmatic use
./scripts/scan-tasks.sh --json
npm run scan-tasks:json
```

**Output Categories**:
- ✅ **Eligible tasks**: `ai-assigned: true`, `Done: false`, no `ai-ignore`
- ⊘ **Ignored tasks**: `ai-ignore: true` (reserved for future)
- ✓ **Completed tasks**: `Done: true`

**Benefits**:
- Fast pre-scan before running `/sort-tasks`
- Programmatic integration via JSON output
- Quick status check of pending work
- Used internally by `/sort-tasks` for performance

### Task Frontmatter Flags
Tasks in `/00-inbox/tasks/` support these frontmatter properties:
- `ai-assigned: true` - Task will be executed by `/sort-tasks` command
- `ai-ignore: true` - Task will be skipped by `/sort-tasks` (future work, not ready)
- `Done: true` - Task is completed and marked done
- If `ai-ignore` is missing, defaults to `false` (task is not ignored)

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
- `/mokai-status` - Daily strategic status command (see `mokai_business_patterns` memory for details)
- `/mokai-weekly` - End-of-week review command (see `mokai_business_patterns` memory for details)
- `/mokai-insights` - Monthly pattern analysis (see `mokai_business_patterns` memory for details)
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

### File Management (NEW)
- `/rename-file [old-path] [new-path] [--scope=directory]` - Intelligently rename/move markdown files
  - Automatically finds and updates ALL references across the vault
  - Handles Obsidian wikilinks (`[[filename]]`) and markdown links (`[text](path/file.md)`)
  - Previews all changes before applying (shows table of files to modify)
  - Recalculates relative paths when moving files between directories
  - Prevents broken links by updating references automatically
  - Optional scope parameter to limit search to specific directory
  - Example: `/rename-file meeting-notes.md client-meeting-2025-10-15.md`
  - Example: `/rename-file 00-inbox/task.md 01-areas/business/mokai/task.md`
  - Example: `/rename-file old.md new.md --scope=00-inbox` (faster scoped search)
  - Use when renaming/moving files that are referenced elsewhere in vault
  - Essential for maintaining link integrity during vault reorganization

- `/move-file` - Move files with automatic reference updates across codebase

### Analysis & Problem Solving
- `/ultra-think` - Deep multi-dimensional analysis mode for complex problems
- `/challenge` - Critical argument analysis and stress-testing

### Product & Project Management
- `/create-prd` - Create Product Requirements Documents
- `/bmad {agent-name}` - Activate specialized BMAD agents (pm, architect, qa, etc.)

## Git Operations
- `git add .` - Stage changes
- `git commit -m "message"` - Commit with message
- `git push` - Push to remote
- `/git:commit "message"` - Quick add, commit, and status check via slash command
- Pre-commit hooks automatically run security scans (gitleaks, trufflehog)

## Memory Sync Automation

### Post-Commit Hook (Automatic)
The `post-commit-serena-sync.sh` hook automatically runs after every git commit and detects when Serena's memory needs updating:

**Triggers on changes to:**
- **Slash commands**: `.claude/commands/` - New or modified commands
- **MCP configuration**: `.mcp.json` - New MCP servers or config changes
- **Package dependencies**: `package.json` - New npm scripts or dependencies
- **Project structure**: `.claude/agents/`, `07-context/`, `.serena/` - Structural changes

**Output when triggered:**
```
🔄 Serena Memory Sync Trigger
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Slash commands modified
   Files: .claude/commands/mokai-status.md
🔌 MCP configuration changed
   File: .mcp.json

💡 Recommendation: Update Serena's memory to reflect these changes
   Run: /update-serena-memory
```

**Features:**
- ✅ Non-blocking (commit always succeeds)
- ✅ Intelligent detection (only triggers on relevant changes)
- ✅ Color-coded output shows what changed
- ✅ Works alongside other hooks (Graphiti)

**Location:** `.claude/hooks/post-commit-serena-sync.sh`
**Dispatcher:** `.git/hooks/post-commit` (runs all post-commit hooks)

### Manual Sync (On-Demand)
For immediate sync or when hook doesn't catch changes:
- **Supabase changes**: Updates to `invoices`, `entities`, `contacts` tables
- **Obsidian changes**: Edits to MOKAI docs in `01-areas/business/mokai/`

Run `/update-serena-memory` manually when needed.

## Common System Commands (macOS)
- `ls` - List directory contents
- `cd <path>` - Change directory
- `grep <pattern> <file>` - Search for pattern in files
- `find <path> -name <pattern>` - Find files by name
- `cat <file>` - Display file contents
- `open <file>` - Open file with default application
