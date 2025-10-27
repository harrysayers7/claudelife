# Suggested Commands

## Serena Memory Reference

**MOKAI-Specific Patterns**: See `mokai_business_patterns` memory for:
- Diary note structure and sections
- Dashboard format and auto-update behavior
- Inbox task frontmatter requirements
- Phase 1 checklist workflow
- Slash command purposes (`/mokai-status`, `/mokai-weekly`, `/mokai-insights`, `/mokai-dump`)
- Tracking system concepts (same-day re-reading, deduplication, fuzzy matching)

## Claude Code Skills

### brainstorming
**Location**: `.claude/skills/brainstorming/SKILL.md`
**Source**: [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/brainstorming)

Transform rough ideas into fully-formed designs through structured Socratic questioning.

**When to use**:
- Before writing code or implementation plans
- When exploring different architectural approaches
- When you need to validate a design incrementally

**Invoke with**: `Skill({ command: "brainstorming" })`

**Process**: Understanding → Exploration (2-3 approaches) → Design Presentation → Documentation → Worktree Setup → Planning Handoff

**See**: `/04-resources/guides/skills/claudelife-skills-guide.md` for full documentation

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
- 18+ commands documented with usage patterns and file locations
- Automatically updated when creating new commands via `/create-command`

### Command Management
- `/create-command` - Interactive command creation wizard with prompt engineering guidance
  - Automatically documents commands in commands guide after creation
  - Enforces consistent structure with YAML frontmatter
  - Includes script & optimization analysis
  - Suggests companion shell scripts for performance (30-60x speedup)
  - Example: `/create-command` (interactive creation process)

- **NEW**: `/command-update {command-name} "changes"` - Interactive command modification assistant
  - Updates existing slash commands with validation and version tracking
  - Shows diff preview before applying changes
  - Validates frontmatter YAML, structure, links, and code syntax
  - Automatically updates documentation in `claudelife-commands-guide.md`
  - Maintains version history in command frontmatter
  - Flags when Serena memory needs updating
  - Supports three change types:
    - **Minor edits**: Typos, grammar, example clarifications
    - **Feature additions**: New options, script integration, expanded examples
    - **Major restructuring**: Purpose changes, workflow redesigns, provider migrations
  - Example: `/command-update mokai-status "add inbox task scanning"`
  - Example: `/command-update research "convert to Context7 MCP"`
  - Example: `/command-update --list` (show all available commands)
  - Use when modifying existing commands to ensure proper validation and documentation sync

### Network Management
- **NEW**: `/network-add "brief description"` - Create structured network profiles for people and businesses
  - Generates markdown files in `04-resources/network/` with complete YAML frontmatter
  - Interactive process gathers: name, entity type (person/business), relationship context, contact info, capabilities, strategic notes
  - Follows `98-templates/profile.md` template structure
  - Automatically creates sections: Summary, Relationship & Relevance, Capabilities/Expertise, Links & References, AI Context Notes
  - Properly formats frontmatter with: type, entity_type, name, relation (wikilinks to related entities), category, location, tags, relationship (to_me, strength), contact_info, aliases, date metadata
  - Integrates into relational network map for AI-assisted collaboration brainstorming
  - Example: `/network-add "Sarah Chen from Flux Studios, creative director I met at design conference"`
  - Example: `/network-add "ComplianceHub - SaaS vendor for cybersecurity compliance tracking"`
  - Use when adding new contacts (business partners, clients, collaborators, vendors) to enable AI reasoning about collaboration opportunities

### Issue Tracking System
- `/issue-create [description]` - Create tracked issue reports with sequential IDs in `01-areas/claude-code/issues/`
  - Auto-checks Serena's memory for known solutions before creating issues
  - Generates sequential IDs (001, 002, 003) with YAML frontmatter
  - Captures: type, category, severity, error messages, attempted solutions, related files
  - Categories: mcp-server, hook, script, command, database, automation, configuration
  - Severity: critical, high, medium, low
  - Uses `scan-issues.sh` script for fast ID generation (30-60x faster)
  - Example: `/issue-create "Serena MCP won't connect after config change"`
  - Use for tracking bugs, technical problems, or complex debugging sessions

- `/issue-call {ID}` - Retrieve and resolve tracked issues
  - Loads issue context, provides category-specific debugging steps
  - Guides systematic troubleshooting with tool-specific commands
  - Creates lesson learned files in `04-resources/lessons-learnt/` upon resolution
  - Suggests updating relevant slash commands with solutions
  - Updates Serena's memory with confirmation
  - Supports status updates: `/issue-call {ID} --status-update "notes"`
  - Example: `/issue-call 001` (load and debug)
  - Example: `/issue-call 001 "solution notes"` (mark resolved)
  - Use when debugging tracked issues or documenting solutions

- **NEW**: `/issue-update {ID}` - Update tracked issues with comprehensive debugging context before restarting Claude Code
  - Analyzes conversation to extract: attempted solutions, error messages, file changes, code modifications, observations, current theories
  - Updates issue frontmatter with new attempted solutions
  - Appends timestamped progress log entries with full context
  - Preserves complete LLM continuation context: next steps, ruled-out approaches, design decisions
  - Uses `scan-issues.sh` for fast issue retrieval
  - Example: `/issue-update 001` (updates issue #001 with latest context)
  - Use **before restarting Claude Code** when mid-debugging to preserve all context for seamless continuation
  - Complements `/issue-call --status-update` with comprehensive conversation analysis

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

- `/janitor` - Vault maintenance and cleanup command
  - **PERFORMANCE**: Uses `scan-archive-candidates.sh` script for instant scanning (<1 second vs 30+ seconds)
  - Moves files with `done: true` or `archive: true` to `/99-archive` directory
  - Deletes files in `/99-archive` older than 30 days
  - Provides summary of archived and deleted files
  - Use periodically (weekly/monthly) to keep vault organized
  - Preview with `npm run scan-archive` before executing
  - Example: `/janitor` (no arguments required)

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
- **NEW**: `/mokai-dump "entry text"` - Quick capture for MOKAI diary entries from Claude Code
  - AI-powered sentiment analysis automatically categorizes to: 🏆 Wins, 💡 Learnings, 🚨 Blockers, 📝 Context/Updates
  - Supports multiple entries: `/mokai-dump "entry 1" "entry 2" "entry 3"`
  - Always adds to today's diary by default
  - Optional backdating: `/mokai-dump --date=2025-10-14 "yesterday's win"` (adds to both dates)
  - No manual category selection needed
  - Creates diary from template if doesn't exist
  - Example: `/mokai-dump "Had a great call with the client, they loved our Essential Eight proposal"`
  - Example: `/mokai-dump "Learned that IRAP assessments take 2-6 months" "Stuck waiting for contractor availability"`
  - Use for quick capture throughout the day without opening Obsidian
- `/business:mokai:generate-mokai-flashcards` - Generate learning flashcards from MOKAI research docs
- `/business:mokai:update-mokai-context` - Update Serena's memory with MOKAI business changes

### MOK HOUSE Business Operations
- **NEW**: `/mokhouse-portfolio-blurb "[project details or link]"` - Generate professional portfolio project descriptions for MOK HOUSE website
  - Creates 3 catchy tagline options and 3 complete project description drafts (technical, creative, impact angles)
  - Interactive refinement with multiple options before finalizing
  - Saves to `01-areas/business/mokhouse/website/project-blurbs/[project-name]-blurb.md`
  - Automatically logs creation in `CLAUDE.md` with date, client, and file link
  - Maintains third-person perspective and impact-focused tone
  - Includes properly formatted "Appreciation" credits section
  - Example: `/mokhouse-portfolio-blurb "Just finished Repco sonic branding - 100-year campaign"`
  - Example: `/mokhouse-portfolio-blurb "[[Project Brief - Nike Commercial]]"`
  - Use after completing music production projects ready for portfolio display

### Creative Thinking & Problem Solving
- **NEW**: `/rethink` or `/rethink "[problem description]"` - Universal creative rethink framework using systems thinking
  - **Without args**: Applies framework to current conversation context automatically
  - **With args**: Analyzes explicit problem statement provided
  - **Framework steps**:
    1. 🛰️ **Zoom Out**: Identifies 2-3 higher-order system layers shaping the problem
    2. 🧩 **Break the Frame**: Challenges 3+ assumptions with alternate framings (Wild/Systemic/Elegant/Counterintuitive)
    3. 🔗 **Cross-Domain Analogies**: Imports 1-2 structural insights from unrelated fields
    4. 🚀 **Divergent Pathways**: Generates 3-5 solution paths ranked by novelty × impact (1-5 scale)
    5. 🪞 **Meta-Reflection**: Uncovers blind spots, overturned assumptions, new questions
  - **Output**: Structured markdown under 600 words with exact headers
  - **Philosophy**: Keeps purely theoretical/creative - doesn't limit to existing tech stack
  - **Serena integration**: Automatically stores novel patterns discovered
  - Example: `/rethink` (applies to current discussion)
  - Example: `/rethink "How to scale consulting without hiring more people"`
  - Example: `/rethink "Why isn't our automation reducing manual work?"`
  - Use for: Complex strategic decisions, reframing stuck problems, unconventional solution discovery
  - Perfect for: Business strategy, technical architecture, workflow optimization, creative challenges

- `/ultra-think` - Deep multi-dimensional analysis mode for complex problems
- `/challenge` - Critical argument analysis and stress-testing

### System Documentation
- `/report:document-system` - Generate comprehensive system documentation with automatic categorization

### Obsidian Vault Management
- `/obsidia` - Activate OBSIDIA mode for vault architecture and knowledge system design
- `/ingest-document` - Process and import external documents into vault

### File Management
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

### Product & Project Management
- `/create-prd` - Create Product Requirements Documents
- `/bmad {agent-name}` - Activate specialized BMAD agents (pm, architect, qa, etc.)

## Git Operations
- `git add .` - Stage changes
- `git commit -m "message"` - Commit with message
- `git push` - Push to remote
- `/git:commit "message"` - Quick add, commit, and status check via slash command
- Pre-commit hooks automatically run security scans (gitleaks, trufflehog)

## Common System Commands (macOS)
- `ls` - List directory contents
- `cd <path>` - Change directory
- `grep <pattern> <file>` - Search for pattern in files
- `find <path> -name <pattern>` - Find files by name
- `cat <file>` - Display file contents
- `open <file>` - Open file with default application
