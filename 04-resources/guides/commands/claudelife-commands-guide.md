---
date: "2025-10-13 17:30"
date created: Tue, 10 14th 25, 4:45:52 pm
date modified: Thu, 10 16th 25, 3:19:44 pm
---

# Claudelife Commands Guide

Comprehensive reference for all custom slash commands in the claudelife project. Keep instructions to below 100 words if possible.

---
- [[#/create-command|/create-command]]
- [[#/create-hook|/create-hook]]
- [[#/command-update|/command-update]]
- [[#/extract-context|/extract-context]]
- [[#/research|/research]]
- [[#/rename-file|/rename-file]]
- [[#/quick-research|/quick-research]]
- [[#/update-serena-memory|/update-serena-memory]]
- [[#/obsidia|/obsidia]]
- [[#/bmad|/bmad]]
- [[#/tag-keyword-DR-extractor|/tag-keyword-DR-extractor]]
- [[#/document-system|/document-system]]
- [[#/mokhouse-project|/mokhouse-project]]
- [[#/mokhouse-create-project|/mokhouse-create-project]]
- [[#/mokhouse-update-status|/mokhouse-update-status]]
- [[#/mokhouse-create-invoice|/mokhouse-create-invoice]]
- [[#/mokhouse-mark-paid|/mokhouse-mark-paid]]
- [[#/ingest-document|/ingest-document]]
- [[#/extract-diary|/extract-diary]]
- [[#/extract-insights|/extract-insights]]
- [[#/challenge|/challenge]]
- [[#/create-prd|/create-prd]]
- [[#/move-file|/move-file]]
- [[#/ultra-think|/ultra-think]]
- [[#/mokai-status|/mokai-status]]
- [[#/mokai-wins|/mokai-wins]]
- [[#/mokai-dump|/mokai-dump]]
- [[#/mokai-weekly|/mokai-weekly]]
- [[#/mokai-insights|/mokai-insights]]
- [[#/complete-task|/complete-task]]
- [[#/janitor|/janitor]]
- [[#/sort-tasks|/sort-tasks]]
- [[#/launch-agent|/launch-agent]]
- [[#/mokhouse-portfolio-blurb|/mokhouse-portfolio-blurb]]
- [[#/analyze-portfolio-style|/analyze-portfolio-style]]

---

### /create-command
**Created**: 2025-10-13 17:30
**Updated**: 2025-10-15

##### What it does:
Interactive command creation assistant that guides you through building effective, structured command files. Includes script & optimization analysis to identify performance bottlenecks and suggest companion shell scripts for speed improvements. Generates commands with YAML frontmatter, confirms optimizations before implementing, and automatically documents new commands.

##### When to use it:
Use when creating new slash commands for repetitive workflows, automation tasks, or complex operations. The optimizer analyzes if companion scripts (like `scan-tasks.sh`) could provide 30-60x speedup for file-heavy or batch operations.

**Usage**: `/create-command`
**File**: `.claude/commands/create-command.md`

---

### /create-hook
**Created**: 2025-10-16 14:35

##### What it does:
Creates production-ready Claude Code hooks with full ecosystem integration. Analyzes existing hooks/MCP servers/agents/scripts, validates configurations with Context7, suggests performance optimizations (companion scripts for 30-60x speedup), and provides comprehensive testing strategies. Supports all hook types (PreToolUse, PostToolUse, UserPromptSubmit, PostSystemCompletion) with complete documentation workflow.

##### When to use it:
Use when creating hooks for automation (auto-diary capture, security validation, workflow triggers). The command analyzes your ecosystem to suggest MCP integrations (Serena, Linear, Supabase), identifies script reuse opportunities, verifies hook syntax against official patterns, and generates testing strategies with troubleshooting guides.

**Usage**: `/create-hook [optional: description]`
**File**: `.claude/commands/create-hook.md`

---

### /command-update
**Created**: 2025-10-15 13:15

##### What it does:
Interactive command modification assistant for updating existing slash commands. Shows diff preview before applying, validates structure/frontmatter/links, maintains version history, auto-updates documentation in claudelife-commands-guide.md, and flags when Serena memory needs sync. Supports minor edits, feature additions, and major restructuring.

##### When to use it:
Use when modifying existing commands to fix bugs, add features, improve clarity, or restructure workflows. Ensures all changes are validated, documented, and tracked with version history. Automatically syncs documentation and identifies when `/update-serena-memory` is needed.

**Usage**: `/command-update {command-name} "changes"` or `/command-update --list`
**File**: `.claude/commands/command-update.md`

---

### /extract-context
**Created**: 2025-10-13 17:35

##### What it does:
Scans daily notes in `/00 - Daily`, extracts content from Context sections, and consolidates them into `/04-resources/context.md` with wiki links. Uses incremental tracking to only process new or modified files, skipping empty sections.

##### When to use it:
Use after adding context information to daily notes to build a centralized context file for AI reference and personal knowledge management. Run periodically to keep context file up-to-date.

**Usage**: `/extract-context`
**File**: `.claude/commands/extract-context.md`

---

### /research
**Created**: 2025-10-13 17:35

##### What it does:
Conducts deep web research using GPT Researcher with COSTAR prompt engineering framework. Generates comprehensive reports with citations, actionable insights, and automatically saves to vault with optimized metadata (keywords, tags, sources) for RAG retrieval.

##### When to use it:
Use for thorough research on technical topics, business strategy, market analysis, or implementation decisions. Ideal when you need evidence-based findings with multiple sources and detailed analysis. Prefer this over `/quick-research` for comprehensive investigation.

**Usage**: `/research "[topic]"`
**File**: `.claude/commands/research.md`

---

### /rename-file
**Created**: 2025-10-15 09:30
**Performance**: 10-20x faster with companion script `rename-file.sh`

##### What it does:
Intelligently renames markdown files and automatically updates all references across the vault. Uses fast bash script for single-pass reference scanning (1-2 seconds vs 15-30 seconds). Handles both Obsidian wikilinks `[[filename]]` and markdown links `[text](path/file.md)`. Provides preview before applying and ensures no broken links.

##### When to use it:
Use when renaming or moving markdown files that are referenced elsewhere in your vault. Essential for maintaining link integrity when reorganizing notes, clarifying filenames, or moving files between directories. Fast enough for interactive use even in large vaults.

**Usage**: `/rename-file [old-path] [new-path] [--scope=directory]`
**File**: `.claude/commands/rename-file.md`
**Script**: `scripts/rename-file.sh` (automatic, 10-20x speedup)

---

### /quick-research
**Created**: 2025-10-13 17:35

##### What it does:
Fast web search using GPT Researcher for immediate answers and context. Can research explicit topics or automatically analyze your last message to determine research context. Returns relevant snippets inline without saving to vault.

##### When to use it:
Use when you need quick context on unfamiliar technologies, debugging guidance, or fast validation of technical approaches. Run without arguments during conversation to research current topic automatically. Prefer this over `/research` for speed.

**Usage**: `/quick-research [optional topic]`
**File**: `.claude/commands/quick-research.md`

---

### /update-serena-memory
**Created**: 2025-10-13 17:35 | **Updated**: 2025-10-15 (Intelligent auto-update with confidence scoring)

##### What it does:
Updates Serena MCP's memory files (`.serena/memories/`) to reflect recent codebase changes. **NEW**: `--auto` flag enables intelligent change detection with confidence-based decisions (HIGH: auto-update, MEDIUM: ask confirmation, LOW: skip). Post-commit hook now creates trigger file for HIGH-confidence changes (80-100), auto-updating Serena in next Claude Code session without user action.

##### When to use it:
Run after adding new commands, scripts, MCP servers, or major changes. **NEW**: Use `--auto` for smart detection. Post-commit hook handles HIGH-confidence updates automatically (new commands/MCP servers). For MEDIUM-confidence (modified commands, patterns), run `/update-serena-memory --auto` to review. Manual mode still available for specific categories.

**Usage**: `/update-serena-memory`, `/update-serena-memory --auto`, `/update-serena-memory [category]`
**File**: `.claude/commands/update-serena-memory.md`
**Hook**: `.claude/hooks/post-commit-serena-sync.sh` (automatic trigger creation)

---

### Post-Commit Hooks (Automated)
**Created**: 2025-10-15

The claudelife system includes intelligent post-commit hooks that run automatically after git commits:

##### 1. Post-Commit Serena Sync (`.claude/hooks/post-commit-serena-sync.sh`)
Analyzes commits and intelligently decides when to update Serena's memory:
- **HIGH confidence (80-100)**: Creates trigger file (`.serena-auto-update-trigger.json`) for automatic update
- **MEDIUM confidence (50-79)**: Suggests running `/update-serena-memory --auto`
- **LOW confidence (0-49)**: Silent skip

**Triggers**: New commands (+85), MCP servers (+85), agent changes (+85), modified commands (+25), experimental commits (-20)

##### 2. Post-System-Completion (`.claude/hooks/post-system-completion.sh`)
Detects substantial feature completions and suggests documentation:
- **HIGH confidence (80+)**: Substantial system completion detected
- **MEDIUM confidence (65-79)**: Feature addition detected
- **LOW-MEDIUM confidence (50-64)**: Consider if documentation needed

**Triggers**: `feat:` commits (+30), 5+ new files (+40), system-related files (+25), config changes (+15), reduces for fix/refactor/chore (-30)

**Suggestion**: Recommends `/document-system "[system name]"` to capture context while fresh

**Integration**: Both hooks run automatically via `.git/hooks/post-commit` dispatcher

---

### Context7 Smart Detection Hook (Automated)
**Created**: 2025-10-16

Intelligent prompt analysis hook that detects when to use Context7 MCP for up-to-date library documentation.

##### How it works:
Analyzes every prompt using multi-factor confidence scoring:
- **Library Detection (40%)**: Identifies fast-moving frameworks (Next.js, React Query, Trigger.dev, Prisma, etc.) and complex API libraries (FastAPI, Stripe, Supabase, etc.)
- **Version Sensitivity (30%)**: Detects "new feature", "latest", version mentions, "breaking change", "migration"
- **Documentation Signals (30%)**: Catches "how do I", "example", "implement", "api reference", etc.

##### Confidence Levels:
- **HIGH (80%+)**: 🎯 Strong recommendation with specific usage guidance
- **MEDIUM-HIGH (65-79%)**: 📚 Gentle suggestion to consider Context7
- **MEDIUM (50-64%)**: 💡 Subtle hint
- **LOW (<50%)**: No suggestion shown

##### Example Triggers:
```
✅ HIGH: "How do I use the new Next.js after() function?"
  → Confidence: 0.9 (library + version + doc signal)
  → Output: "🎯 Detected next.js - Context7 highly recommended for latest docs"

✅ MEDIUM-HIGH: "How does Prisma's interactive transactions API work?"
  → Confidence: 0.7 (library + doc signal)
  → Output: "📚 Consider using Context7 for up-to-date prisma documentation"

❌ LOW: "What's the difference between async and sync in Python?"
  → Confidence: 0.3 (generic concept, no specific library)
  → No suggestion
```

##### Smart Filtering:
- **Excluded**: Stable languages (JavaScript, Python, TypeScript), generic concepts, architecture discussions
- **Prioritized**: Fast-moving frameworks, version-specific queries, API implementation questions
- **Ignored**: Prompts already containing "context7"

##### Configuration:
**File**: `.claude/hooks/context7_detector.py`
**Hook Type**: `UserPromptSubmit` (runs before every message)
**Requirements**: Python 3.6+, no external dependencies

##### Customization:
Edit `context7_detector.py` to:
- Add libraries to `FAST_MOVING_LIBS` or `COMPLEX_API_LIBS`
- Adjust confidence thresholds in `generate_reminder()`
- Add custom detection patterns to `VERSION_PATTERNS` or `DOCUMENTATION_SIGNALS`

##### Testing:
```bash
# Test detection manually
python3 .claude/hooks/context7_detector.py "How do I use Next.js after function?"

# View JSON output
python3 .claude/hooks/context7_detector.py "Implement Stripe checkout with latest API" | jq
```

**Documentation**: `.claude/hooks/README-context7-detector.md`
**Integration**: Configured in `.claude/settings.json` under `hooks.UserPromptSubmit`

---

### /obsidia
**Created**: 2025-10-13 17:35

##### What it does:
Activates OBSIDIA mode - an intelligent Obsidian vault architect specializing in knowledge architecture, learning system engineering, automation design, and vault analysis. Provides structural improvements, Dataview queries, Templater scripts, and integration workflows.

##### When to use it:
Use for vault structure optimization, designing spaced repetition workflows, creating automation queries, analyzing knowledge patterns, or building integration systems between vault and external tools (Supabase, Notion, MCP servers).

**Usage**: `/obsidia [task description]`
**File**: `.claude/commands/obsidia.md`

---

### /bmad
**Created**: 2025-10-13 17:35

##### What it does:
Activates BMAD agents by loading agent configuration files from `.claude/.bmad-core/agents/`. Each agent has specific expertise (Product Manager, Architect, QA, etc.) and dedicated commands. Agent stays active until `/exit`.

##### When to use it:
Use when you need specialized expertise for product management, system architecture, backlog management, or agile workflows. Each agent provides role-specific guidance and templates.

**Usage**: `/bmad {agent-name}`
**File**: `.claude/commands/bmad.md`

---

### /tag-keyword-DR-extractor
**Created**: 2025-10-13 17:35

##### What it does:
Scans markdown files for `research-type: deep research` in frontmatter and intelligently extracts 5-7 keywords (for RAG optimization), 3-5 tags (prioritizing existing vault tags), and a concise 1-2 sentence description. Updates frontmatter automatically.

##### When to use it:
Use after creating research documents to optimize them for semantic search and vault discovery. Run periodically on research files to ensure proper metadata for RAG retrieval and knowledge graph connections.

**Usage**: `/tag-keyword-DR-extractor`
**File**: `.claude/commands/tag-keyword-DR-extractor.md`

---

### /document-system
**Created**: 2025-10-13 17:35

##### What it does:
Generates comprehensive context documentation for completed projects and systems. Uses Serena to analyze code, configurations, and integrations. Auto-detects storage location in `07-context/systems/` subfolders. Creates detailed technical docs explaining what, how, where, and usage.

##### When to use it:
Use after completing major features, MCP servers, automations, or integration projects to create permanent context documentation. Ensures any LLM or developer can understand system architecture, purpose, and usage patterns.

**Usage**: `/document-system "[system name]" [--path=custom/path] [--update]`
**File**: `.claude/commands/report/document-system.md`

---

### /mokhouse-project
**Created**: 2025-10-13 17:35

##### What it does:
Specialized command for MOK HOUSE (Harry's music production business) project management and workflow automation. Integrates with music-specific tools and workflows.

##### When to use it:
Use for MOK HOUSE music production projects, client work coordination, or music business operations.

**Usage**: `/mokhouse-project [args]`
**File**: `.claude/commands/mokhouse/mokhouse-project.md`

---

## MOK HOUSE Project Lifecycle Commands

### /mokhouse-create-project
**Created**: 2025-10-16 11:45

##### What it does:
Automates MOK HOUSE project creation from client brief emails (Phase 1). Searches Gmail, fetches Google Doc briefs, creates formatted Obsidian project files with frontmatter, generates AI creative suggestions (composer-level jingle/sonic branding direction), and produces SUNO prompts (<1000 chars). Handles full brief-to-project pipeline with proper callouts, H2 headings, and Harrison's composer number (#3).

##### When to use it:
Use when client brief emails arrive from Electric Sheep Music, Panda Candy, or new customers. Creates production-ready project files with AI-powered creative direction, sound design ideas, and music generation prompts. Run once per new project brief.

**Usage**: `/mokhouse-create-project "Brief context or customer name"`
**File**: `.claude/commands/mokhouse/mokhouse-create-project.md`
**Integration**: Gmail + Google Drive + Obsidian

---

### /mokhouse-update-status
**Created**: 2025-10-16 11:52

##### What it does:
Updates MOK HOUSE project status throughout lifecycle (Phase 2). Handles status transitions (Brief Received → Submitted → PO Received → Invoiced → Complete), award decisions, and metadata updates. Uses Obsidian patch operations for fast, surgical updates to project frontmatter fields.

##### When to use it:
Use when work progresses: mark as "Submitted" after demo delivery, "PO Received" when purchase order arrives, record award decisions with fees/APRA status. Can run multiple times per project. Fast operation (<10 seconds).

**Usage**: `/mokhouse-update-status "[project name] status update details"`
**File**: `.claude/commands/mokhouse/mokhouse-update-status.md`
**Integration**: Obsidian

---

### /mokhouse-create-invoice
**Created**: 2025-10-16 12:00

##### What it does:
Creates invoices for MOK HOUSE projects across Stripe, Supabase, and Obsidian (Phase 3). Handles customer lookup/setup, GST calculation (per customer preference), duplicate detection, multi-system coordination. Requires explicit user approval before creating. Supports both existing customers (Electric Sheep, Panda Candy) and new customer onboarding with flexible payment terms.

##### When to use it:
Use when PO arrives from client. Looks up customer preferences (14-day terms, no GST for ESM/Panda Candy), presents confirmation, creates Stripe invoice (product → price → finalize), records in Supabase with relationships, updates Obsidian project. Provides payment link and dashboard URLs. Stops immediately if any step fails.

**Usage**: `/mokhouse-create-invoice "[PO details, project name, customer]"`
**File**: `.claude/commands/mokhouse/mokhouse-create-invoice.md`
**Integration**: Stripe + Supabase + Obsidian
**Entity**: MOK HOUSE PTY LTD (550e8400-e29b-41d4-a716-446655440002)

---

### /mokhouse-mark-paid
**Created**: 2025-10-16 12:10

##### What it does:
Marks MOK HOUSE invoices as paid and completes project lifecycle (Phase 4). Updates payment status across Obsidian (paid: true, Date Paid, status: "Complete") and Supabase (paid_amount, status: "paid", paid_on). Simple, fast operation for closing completed projects.

##### When to use it:
Use when payment received from client. Identifies project by name/customer/invoice number, confirms payment date (defaults to today), updates both systems atomically. Completes project lifecycle. Takes <30 seconds.

**Usage**: `/mokhouse-mark-paid "[project name or invoice details]"`
**File**: `.claude/commands/mokhouse/mokhouse-mark-paid.md`
**Integration**: Obsidian + Supabase

---

### /ingest-document
**Created**: 2025-10-13 17:35

##### What it does:
Processes various document formats (PDF, Word, Excel, PowerPoint, email threads) to extract text, preserve structure, analyze content, and integrate into knowledge base. Creates tasks, links entities, and triggers relevant workflows.

##### When to use it:
Use when importing external documents into claudelife vault. Automatically extracts key information, categorizes content, and creates appropriate vault structure.

**Usage**: `/ingest-document [document-path]`
**File**: `.claude/commands/ingest-document.md`

---

### /extract-diary
**Created**: 2025-10-13 17:35

##### What it does:
Scans daily notes in `/00 - Daily`, extracts content from Diary sections, and consolidates them into `/04-resources/diary.md` with wiki links. Uses incremental tracking similar to `/extract-context`.

##### When to use it:
Use after adding diary entries to daily notes to build a centralized diary file for personal reflection and temporal analysis. Run periodically to keep diary file updated.

**Usage**: `/extract-diary`
**File**: `.claude/commands/extract-diary.md`

---

### /extract-insights
**Created**: 2025-10-13 17:35

##### What it does:
Scans daily notes in `/00 - Daily`, extracts content from `### 💡 Insights` sections, and consolidates them into `/01-areas/p-dev/insights.md` with wiki links. Tracks processed files to avoid re-scanning.

##### When to use it:
Use after capturing insights in daily notes to consolidate learnings into a central insights file for knowledge management and personal development tracking.

**Usage**: `/extract-insights`
**File**: `.claude/commands/extract-insights.md`

---

### /challenge
**Created**: 2025-10-13 17:35

##### What it does:
Activates intelligent challenge mode to stress-test arguments with critical reasoning. Restates the argument, presents strongest counterpoints, identifies hidden premises, offers alternative perspectives, and provides a verdict on the argument's strength.

##### When to use it:
Use when you need rigorous evaluation of ideas, claims, or decisions. Ideal for testing business strategies, technical approaches, or any argument that needs critical analysis before commitment.

**Usage**: `/challenge "[idea/claim to test]"`
**File**: `.claude/commands/popular/challenge.md`

---

### /create-prd
**Created**: 2025-10-13 17:35

##### What it does:
Creates comprehensive Product Requirements Documents (PRDs) for new features. Acts as experienced Product Manager to define problem statements, user needs, specifications, scope, and success metrics based on product context and JTBD documentation.

##### When to use it:
Use when planning new features or products. Creates structured PRDs that capture the what, why, and how without technical implementation details. Supports template-based or interactive creation.

**Usage**: `/create-prd [feature-name] | --template | --interactive`
**File**: `.claude/commands/popular/create-prd.md`

---

### /move-file
**Created**: 2025-10-13 17:35

##### What it does:
Moves files or directories and automatically updates all references throughout the codebase. Searches for old path references, replaces with new path, stages changes in git, and provides a summary of updates.

##### When to use it:
Use when reorganizing project structure or renaming files to avoid breaking references. Ensures all imports, links, and path references are updated automatically across the entire codebase.

**Usage**: `/move-file "old/path" "new/path"`
**File**: `.claude/commands/popular/move-file.md`

---

### /ultra-think
**Created**: 2025-10-13 17:35

##### What it does:
Activates deep analysis and problem-solving mode with multi-dimensional thinking. Analyzes problems from technical, business, user, risk, and strategic perspectives. Explores solution space comprehensively with trade-off analysis and implementation roadmaps.

##### When to use it:
Use for complex decision-making, architectural design, or when facing multi-faceted challenges requiring systematic, comprehensive analysis. Ideal for high-stakes decisions or novel problem domains.

**Usage**: `/ultra-think "[problem or question]"`
**File**: `.claude/commands/popular/ultra-think.md`

---

## MOKAI Business Management Commands

### /mokai-status
**Created**: 2025-10-14 | **Updated**: 2025-10-14 (Inbox task scanning + Serena MCP)

##### What it does:
Daily strategic status command that reads unprocessed diary notes, **scans MOKAI task files in /00-inbox/tasks/ grouped by priority (urgent/high/normal)**, extracts wins/blockers/learnings/tasks using Serena pattern matching, dynamically updates Phase 1 checklist via fuzzy task matching (auto-marks completed tasks), updates dashboard automatically, retrieves Serena memory for week-over-week comparison, and provides strategic guidance on what to work on RIGHT NOW. **Prioritizes urgent inbox tasks over routine Phase 1 tasks**. Uses `.mokai-tracker.json` for incremental processing (only reads new notes).

##### When to use it:
Run every morning (30 seconds) to get your strategic direction. **Safe to run multiple times per day** - today's diary note is always re-read to capture same-day updates, with deduplication preventing duplicate entries. Automatically processes only new diary notes from previous days + scans all MOKAI task files in inbox. Fuzzy matching detects task completion (e.g., "finished reading Indigenous section" matches checklist task). Acts as accountability partner telling you exactly what to focus on today, with urgent inbox tasks surfaced prominently.

**Usage**: `/mokai-status`
**File**: `.claude/commands/mokai-status.md`
**Requires**: Serena MCP
**Diary Location**: `01-areas/business/mokai/diary/YYYY-MM-DD.md`
**Inbox Tasks**: `/00-inbox/tasks/*.md` (frontmatter: `type: Task`, `relation: mokai`, `Done: false`, `priority: urgent|high|low`)

---

### /mokai-wins
**Created**: 2025-10-14

##### What it does:
Quick win logging command that creates or appends to today's diary note (`YYYY-MM-DD.md`). Finds or creates "## 🏆 Wins" section, adds win as bullet point, and provides quick celebration message with next priority based on current week's Phase 1 focus. Ensures wins are logged immediately (not forgotten later).

##### When to use it:
Use throughout the day immediately after completing tasks (30 seconds). Multiple times per day is encouraged. Builds positive momentum and ensures all wins are captured in diary for weekly aggregation. No need to open diary file manually - command handles everything.

**Usage**: `/mokai-wins [win description]`
**Example**: `/mokai-wins Completed reading Indigenous Business section of Ops Guide`
**File**: `.claude/commands/mokai-wins.md`

---

### /mokai-dump
**Created**: 2025-10-15 12:50

##### What it does:
Quick capture command for MOKAI diary entries. Analyzes your input using AI sentiment/content analysis and automatically categorizes entries under the correct section (🏆 Wins, 💡 Learnings, 🚨 Blockers, 📝 Context/Updates). Supports multiple entries in one command. Always adds to today's diary by default, with optional `--date` parameter to add to different dates (adds to both dates).

##### When to use it:
Use throughout the day for quick capture from Claude Code without opening Obsidian. Perfect for logging wins, learnings, blockers, or context on-the-go. Faster than manual diary editing. Supports batch entry: `/mokai-dump "entry 1" "entry 2" "entry 3"`.

**Usage**: `/mokai-dump "entry text"` or `/mokai-dump --date=YYYY-MM-DD "entry"`
**File**: `.claude/commands/mokai-dump.md`

---

### /mokai-weekly
**Created**: 2025-10-14 | **Updated**: 2025-10-14 (Inbox task tracking + Serena MCP)

##### What it does:
End-of-week review command that aggregates entire week's diary notes via Serena pattern matching, **counts completed MOKAI inbox tasks this week**, counts Phase 1 checklist task completion rate, compares week-over-week trends from Serena memory, interactively asks 3 reflection questions, updates Phase 1 checklist (marks completed, rolls forward incomplete with "from Week X" notation), updates dashboard's Weekly Scorecard, stores metrics in `mokai_progress_metrics` memory (including inbox task counts), stores insights in `mokai_weekly_insights` memory, and provides strategic pep talk with honest assessment.

##### When to use it:
Run every Friday afternoon or Sunday evening (10 minutes) for comprehensive weekly review. First run creates memory, subsequent runs show trends. Stores historical data for longitudinal analysis including inbox task completion patterns. Essential for maintaining strategic direction and catching persistent blockers early (5+ consecutive days).

**Usage**: `/mokai-weekly`
**File**: `.claude/commands/mokai-weekly.md`
**Requires**: Serena MCP
**Memory Files**: `mokai_progress_metrics.md`, `mokai_weekly_insights.md`
**Inbox Tasks**: Scans `/00-inbox/tasks/*.md` for completed MOKAI tasks this week

---

### /mokai-insights
**Created**: 2025-10-14

##### What it does:
Deep pattern analysis command that scans ALL MOKAI diary notes (not just unprocessed) using Serena pattern matching. Performs frequency analysis (top blockers by mention count and dates, top learning themes, win patterns), trend analysis (weekly completion rate, blocker persistence, learning velocity), pattern detection (recurring themes, task completion patterns), and provides strategic recommendations (what's working, what needs attention, emerging patterns, next week predictions).

##### When to use it:
Run monthly for big-picture view, when feeling stuck to identify root causes, before major decisions to see data-backed patterns, or before phase transitions (Day 30). Complements `/mokai-weekly` by analyzing long-term trends across all history. Identifies persistent blockers that need escalation (mentioned 5+ consecutive days).

**Usage**: `/mokai-insights`
**File**: `.claude/commands/mokai-insights.md`
**Requires**: Serena MCP
**Reads**: All diary notes in `01-areas/business/mokai/diary/`

---

### /complete-task
**Created**: 2025-10-15 03:25

##### What it does:
Executes a specific task from `/00-inbox/tasks/` that you designate by filename or description. Uses Serena for codebase exploration, implements the task directly (no confirmation unless requested), marks `Done: true` upon completion, and commits changes with descriptive message.

##### When to use it:
Use when you want to complete a specific task from your inbox immediately. Simply reference the task filename or description. Default behavior is direct execution; add `--confirm` or state "confirm before executing" if you want approval before implementation.

**Usage**: `/complete-task "[task-filename.md or description]"`
**File**: `.claude/commands/complete-task.md`

---

## Task Management Commands

### /janitor
**Created**: 2025-10-15 04:12 | **Updated**: 2025-10-15 04:18 (scan-archive-candidates.sh integration)

##### What it does:
Maintenance command that cleans up the claudelife vault by archiving completed/archived files and purging old archives. Uses `scan-archive-candidates.sh` script for instant scanning (<1 second), moves files with `done: true` or `archive: true` to `/99-archive`, then deletes files in `/99-archive` older than 30 days. **Performance**: 30-60x faster than MCP scanning.

##### When to use it:
Use periodically (weekly/monthly) to keep the vault organized and prevent clutter. Ideal for automated maintenance of completed tasks, archived notes, and old reference materials. Use `npm run scan-archive` to preview files before running `/janitor`.

**Usage**: `/janitor`
**Pre-scan**: `npm run scan-archive` (preview candidates)
**File**: `.claude/commands/janitor.md`
**Script**: `scripts/scan-archive-candidates.sh`

---

### /sort-tasks
**Created**: 2025-10-12 11:45 | **Updated**: 2025-10-15 (ai-ignore flag, scan-tasks.sh integration)

##### What it does:
Automates task management by executing all AI-assigned tasks (`ai-assigned: true`) sequentially from `/00-inbox/tasks/`. Uses `scan-tasks.sh` script for instant task filtering (<1 second vs 30+ seconds), skips tasks marked with `ai-ignore: true` (reserved for future work), verifies completion before marking `Done: true`, cleans up completed tasks older than 2 weeks, and commits changes with summary. **Performance**: 30-60x faster task scanning.

##### When to use it:
Use for batch processing of all AI-assigned tasks in your inbox. Runs unattended through all eligible tasks, respects ai-ignore flag for future tasks, handles failures gracefully, and cleans up old completed tasks automatically. Use `npm run scan-tasks` first to preview what will be executed. Complements `/complete-task` which handles individual task execution.

**Usage**: `/sort-tasks`
**Pre-scan**: `npm run scan-tasks` (preview eligible tasks)
**File**: `.claude/commands/sort-tasks.md`
**Script**: `scripts/scan-tasks.sh`

---

### /launch-agent
**Created**: 2025-10-15 10:15

##### What it does:
Launches specialized Claude Code sub-agents with your task description and automatic conversation context. Streamlines agent invocation for all agent types: mokai-business-strategist, trigger-dev-expert, mcp-integration-engineer, code-reviewer, task-orchestrator, strategic-planner, general-purpose, and others. Confirms agent activation immediately.

##### When to use it:
Use when you need specialized expertise for business strategy (MOKAI), technical development (Trigger.dev, MCP), code quality, task management, or complex research. Start fresh conversations for unrelated tasks. Agent receives full context automatically - just specify agent type and task description.

**Usage**: `/launch-agent <agent-type> "<task-description>"`
**Example**: `/launch-agent mokai-business-strategist "analyze government tender opportunity"`
**File**: `.claude/commands/launch-agent.md`

---

### /mokhouse-portfolio-blurb
**Created**: 2025-10-16 15:30 | **Updated**: 2025-10-16 17:00 (50-word limit, "Harry" format)

##### What it does:
Generates professional portfolio project descriptions with AUTOMATIC SELF-LEARNING. Reads `portfolio-style-guide.md` before generating options, creates 3 tagline and description drafts (max 50 words each), tracks your selections, and AUTOMATICALLY analyzes patterns every 3 blurbs (3rd, 6th, 9th, etc.). Uses "Harry" instead of full name for personal, approachable tone. Shows analysis summary and asks permission before updating style guide.

##### When to use it:
Use after completing music production projects ready for portfolio display. Command automatically learns your preferences - after every 3 blurbs, it shows what it learned and asks if you want to update the style guide. All descriptions strictly limited to 50 words maximum. Gets smarter automatically without manual intervention.

**Usage**: `/mokhouse-portfolio-blurb "[project details or link to project files]"`
**Example**: `/mokhouse-portfolio-blurb "Just finished Repco sonic branding - 100-year campaign"`
**File**: `.claude/commands/mokhouse-portfolio-blurb.md`
**Style Guide**: `01-areas/business/mokhouse/website/portfolio-style-guide.md`

---

### /analyze-portfolio-style
**Created**: 2025-10-16 16:15

##### What it does:
Analyzes all MOK HOUSE portfolio blurbs to detect writing patterns from your selections. Examines which tagline/description options you chose, identifies tone and word choice trends, calculates confidence scores, and updates `portfolio-style-guide.md` with discovered patterns. Requires minimum 3 blurbs with selection tracking metadata. **NOTE**: Analysis now runs automatically every 3 blurbs in `/mokhouse-portfolio-blurb`.

##### When to use it:
Use manually only if you want to analyze patterns outside the automatic 3-blurb cycle (e.g., after manually editing multiple blurbs). Use `--report-only` flag to preview without updating. Most users won't need to run this manually since `/mokhouse-portfolio-blurb` handles it automatically.

**Usage**: `/analyze-portfolio-style` or `/analyze-portfolio-style --report-only`
**File**: `.claude/commands/analyze-portfolio-style.md`
**Updates**: `01-areas/business/mokhouse/website/portfolio-style-guide.md`

---
