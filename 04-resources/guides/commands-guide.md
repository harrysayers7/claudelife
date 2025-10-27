# Claudelife Commands Reference Guide

> [!tip] Quick Summary
> Complete reference for all available slash commands in your claudelife setup, organized by category with usage examples and when to use each one.

---
tags: [resources, guides, documentation]
relation:
  - "[[resources]]"
  - "[[resources]]"

## 📚 Popular Commands

### `/popular:learn`
**What it does:** Analyzes your interaction history and updates learned patterns in CLAUDE.md.
**When to use:** End of day or after completing significant tasks to capture what worked/didn't work.

### `/popular:brain-drump`
**What it does:** Captures unstructured thoughts and organizes them into tasks, ideas, questions, and concerns.
**When to use:** When you have scattered thoughts and need help organizing them into actionable items.

### `/popular:quick-guide`
**What it does:** Creates a 1-page Obsidian-optimized guide on any technical topic (200-300 words max).
**When to use:** When you need quick reference documentation for tools, patterns, or concepts you'll use repeatedly.

---

## 💼 Financial Commands

### `/finance:add-business-transaction`
**What it does:** Manually adds a business transaction to Supabase with proper categorization and tax flags.
**When to use:** Recording cash expenses, credit card charges, or manual entries not synced from UpBank.

### `/finance:add-invoice`
**What it does:** Parses PDF invoices and adds them to your financial database (single file or directory).
**When to use:** Processing vendor invoices from Dropbox or local folders for expense tracking.

### `/finance:add-business-keyword`
**What it does:** Adds keyword rules for automatic business expense detection during syncs.
**When to use:** After manually categorizing a transaction that should auto-detect as business in future.

### `/finance:remove-business-keyword`
**What it does:** Removes a keyword from business expense auto-detection rules.
**When to use:** When a keyword is causing false positives in business expense flagging.

### `/finance:show-business-keywords`
**What it does:** Displays all active business expense detection keywords and rules.
**When to use:** Reviewing or auditing your automatic expense categorization setup.

### `/finance:show-business-transactions`
**What it does:** Lists recent business transactions with amounts and categories.
**When to use:** Monthly review, tax prep, or checking business expense tracking accuracy.

---

## 🔗 Integration Commands

### `/linear-add`
**What it does:** Creates a Linear issue from conversation context with structured formatting.
**When to use:** Converting discussion points, bugs, or features into trackable Linear issues.

### `/linear-retrieve`
**What it does:** Fetches Linear issue details by ID or search query.
**When to use:** When you need to reference or update existing Linear issues during work.

### `/sync-upbank`
**What it does:** Syncs UpBank transactions, accounts, and categories to Supabase with ML categorization.
**When to use:** Daily morning routine or monthly reconciliation for financial tracking.

### `/sync-database-context`
**What it does:** Updates Supabase schema documentation files with latest database state.
**When to use:** After database migrations or when schema docs feel outdated.

---

## 🎯 Task Management (Task Master)

### Core Workflow

**`/tm:next`** - Shows next available task based on dependencies and status.
**`/tm:show {id}`** - Displays detailed task information with subtasks and dependencies.
**`/tm:set-status/to-done {id}`** - Marks task as complete.
**`/tm:set-status/to-in-progress {id}`** - Marks task as actively being worked on.

### Task Creation & Updates

**`/tm:add-task {description}`** - Creates new task with AI-generated details.
**`/tm:update-task {id} {changes}`** - Updates single task with new information.
**`/tm:update {from-id} {changes}`** - Updates multiple tasks from a starting ID.

### Task Analysis

**`/tm:analyze-complexity`** - Analyzes tasks and generates expansion recommendations.
**`/tm:complexity-report`** - Shows complexity analysis with expansion suggestions.
**`/tm:expand {id}`** - Breaks task into subtasks (add `--research` for enhanced).
**`/tm:expand-all`** - Expands all eligible tasks into subtasks.

### Project Setup

**`/tm:init`** - Initializes Task Master in current project.
**`/tm:parse-prd {file}`** - Generates tasks from Product Requirements Document.
**`/tm:models`** - Views or configures AI models for task generation.

---

## 🧠 Memory & Learning

### `/remember`
**What it does:** Explicitly saves important information to memory for future reference.
**When to use:** Capturing user preferences, project decisions, or workflow patterns.

### `/auto-remember`
**What it does:** Automatically captures conversation context and updates memory.
**When to use:** Enable for continuous learning mode during extended work sessions.

### `/recall`
**What it does:** Retrieves relevant information from memory based on query.
**When to use:** When you need to reference past decisions or learned patterns.

### `/check-memory-reminders`
**What it does:** Reviews pending reminders and memory-flagged items.
**When to use:** Start of work session to see if anything needs attention.

### `/memory-metrics`
**What it does:** Shows memory system performance and storage stats.
**When to use:** Monitoring memory health or troubleshooting memory issues.

---

## 🔧 Utility Commands

### `/compact`
**What it does:** Compresses context to essentials, saves full state to checkpoints.
**When to use:** When approaching token limits (75%+) during long conversations.

### `/commit {message}`
**What it does:** Quick git add and commit with conventional commit format.
**When to use:** Rapid commits during development (follows feat:/fix:/docs: pattern).

### `/primer`
**What it does:** Analyzes project structure, reads key files, explains architecture.
**When to use:** First time working on a project or after long break from codebase.

### `/ultra-think {problem}`
**What it does:** Deep multi-dimensional analysis with systematic reasoning and multiple solutions.
**When to use:** Complex architectural decisions or when you need thorough problem analysis.

### `/create-command`
**What it does:** Interactive command file creator with prompt engineering best practices.
**When to use:** Creating new reusable commands for repetitive tasks.

### `/create-prd {feature}`
**What it does:** Creates Product Requirements Document from feature description.
**When to use:** Planning new features before implementation.

---

## 🤖 Automation & Workflows

### `/trigger-automation {workflow}`
**What it does:** Triggers n8n workflows on sayers-server (134.199.159.190).
**When to use:** Running automated processes like email processing or data syncs.

### `/control-panel`
**What it does:** Central dashboard for system status and automation management.
**When to use:** Monitoring overall system health and active workflows.

### `/anticipate`
**What it does:** Predicts next likely actions based on context and patterns.
**When to use:** When you want proactive suggestions for next steps.

---

## 🔍 Specify Workflow (Feature Development)

### `/specify {feature-description}`
**What it does:** Creates feature spec from natural language, initializes branch and spec file.
**When to use:** Starting new feature development with proper specification.

### Supporting Commands:
- `/specify:plan` - Creates implementation plan
- `/specify:analyze` - Analyzes technical feasibility
- `/specify:clarify` - Asks clarifying questions
- `/specify:tasks` - Breaks spec into tasks
- `/specify:implement` - Guides implementation

---

## 📝 Document Processing

### `/ingest-document {path}`
**What it does:** Processes documents and extracts structured information for memory.
**When to use:** Adding external documentation, contracts, or reference materials.

### `/process-image {path}`
**What it does:** Analyzes images and extracts actionable information.
**When to use:** Processing screenshots, diagrams, or visual documentation.

---

## 🔄 System Commands

### `/daily-review`
**What it does:** Reviews day's progress, updates metrics, generates insights.
**When to use:** End of workday to track productivity and capture learnings.

### `/team-collab`
**What it does:** Facilitates team collaboration features and knowledge sharing.
**When to use:** Working on shared projects or coordinating with team members.

### `/tasks-ai`
**What it does:** AI-powered task suggestions and workflow optimization.
**When to use:** When you need intelligent task prioritization or workflow improvements.

### `/voice-setup`
**What it does:** Configures voice input and transcription features.
**When to use:** Setting up or troubleshooting voice command capabilities.

---

## 🚀 Quick Reference Table

| Command | Category | Frequency | Purpose |
|---------|----------|-----------|---------|
| `/popular:learn` | Learning | Daily | Capture patterns |
| `/sync-upbank` | Finance | Daily | Bank sync |
| `/tm:next` | Tasks | Multiple/day | Next task |
| `/compact` | Utility | As needed | Token management |
| `/commit` | Dev | Multiple/day | Quick commits |
| `/linear-add` | Integration | As needed | Track issues |
| `/ultra-think` | Analysis | Weekly | Deep analysis |
| `/create-command` | Meta | As needed | Build tools |

---

## 💡 Pro Tips

**Daily Workflow:**
1. Start: `/check-memory-reminders`, `/tm:next`
2. During: `/commit`, `/tm:set-status/to-done`
3. End: `/sync-upbank`, `/popular:learn`, `/daily-review`

**Monthly Review:**
1. `/finance:show-business-transactions`
2. `/tm:complexity-report`
3. `/memory-metrics`

**Context Management:**
- Use `/compact` at 75% tokens
- Use `/primer` when switching projects
- Use `/popular:quick-guide` for documentation

**Task Master Flow:**
1. `/tm:parse-prd` → `/tm:analyze-complexity`
2. `/tm:expand-all --research`
3. `/tm:next` → work → `/tm:set-status/to-done`
4. Repeat until project complete

---

**Related Resources:**
- Command files: `/Users/harrysayers/Developer/claudelife/.claude/commands/`
- Task Master docs: `@.taskmaster/CLAUDE.md`
- Main config: `/Users/harrysayers/Developer/claudelife/CLAUDE.md`

---

> [!warning] Important Notes
> - Always use proper command syntax with forward slashes
> - Many commands have interactive prompts - follow the guidance
> - Financial commands write to production Supabase - double check inputs
> - Task Master commands may take 30-60 seconds if using AI features
