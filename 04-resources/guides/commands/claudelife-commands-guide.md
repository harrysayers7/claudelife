---
date: "2025-10-13 17:30"
---

# Claudelife Commands Guide

Comprehensive reference for all custom slash commands in the claudelife project.

---

### /create-command
**Created**: 2025-10-13 17:30

##### What it does:
Interactive command creation assistant that guides you through building effective, structured command files. Generates properly formatted commands with YAML frontmatter, interactive workflows, technical implementation guides, and automatic documentation integration.

##### When to use it:
Use when creating new slash commands for repetitive workflows, automation tasks, or complex operations. Ideal for standardizing command structure and ensuring best practices across the claudelife project.

**Usage**: `/create-command`
**File**: `.claude/commands/create-command.md`

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
**Created**: 2025-10-13 17:35

##### What it does:
Updates Serena MCP's memory files (`.serena/memories/`) to reflect recent codebase changes like new scripts, dependencies, MCP servers, project structure, or coding patterns. Lists current memories, identifies changes, and updates relevant categories.

##### When to use it:
Run after adding new commands, scripts, dependencies, MCP servers, or making significant project structure changes. Ensures Serena provides accurate context-aware suggestions and understands current system architecture.

**Usage**: `/update-serena-memory [optional category]`
**File**: `.claude/commands/update-serena-memory.md`

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
