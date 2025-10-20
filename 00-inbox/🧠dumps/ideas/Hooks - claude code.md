---
type: brain dump
relation:
  - "[[97-tags/claude-code|claude-code]]"
tags:
sub-type:
effort:
location:
title: Hooks - claude code
date created: Wed, 10 15th 25, 1:26:46 pm
date modified: Wed, 10 15th 25, 1:28:10 pm
---
# 📚 Quick Research: Useful Claude Code Hooks for Claudelife, MOKAI, and MOK HOUSE

Based on research into Claude Code hooks best practices and automation patterns, here are powerful hooks that would enhance your claudelife project and business operations:

## Key Findings

### Available Hook Types in Claude Code

1. **UserPromptSubmit** - Fires when you submit a prompt
2. **PostTool** - Fires after Claude executes any tool
3. **Stop** - Fires when Claude finishes responding
4. **SubagentComplete** - Fires when Task tool subagents finish

### Hook Capabilities

- **Blocking hooks**: Can prevent execution (exit code 1 = block, 0 = allow)
- **JSON output**: Return structured data to influence Claude's behavior
- **Async automation**: Run workflows without blocking Claude
- **Context passing**: Hooks receive detailed payload about what triggered them

## Recommended Hooks for Your Projects

### 🏢 MOKAI Business Operations Hooks

#### 1. **Auto-Diary Capture Hook** (PostTool)

**Trigger**: After completing tasks or making significant changes **Purpose**: Automatically log wins, learnings, or context to MOKAI diary

```bash
# .claude/hooks/post-tool-mokai-diary-capture.sh
# Detects task completion and auto-logs to diary
# Payload includes: tool_name, args, result
# If task-master set-status --status=done → extract task and log as win
```

**Benefits**:

- Never forget to log wins
- Automatic diary population from task completions
- Reduces friction in daily status tracking

#### 2. **Client Context Loader Hook** (UserPromptSubmit)

**Trigger**: When prompt contains client/tender keywords **Purpose**: Auto-load relevant client context from Obsidian vault

```bash
# Detects: "tender", "client", "IRAP", "Essential Eight"
# Loads: Relevant MOKAI docs, compliance checklists, client history
# Returns: Enhanced context via JSON to Claude
```

**Benefits**:

- Instant access to client-specific context
- Automatic compliance checklist loading
- Reduces manual context gathering

#### 3. **Tender Document Processor Hook** (PostTool - Edit/Write)

**Trigger**: After editing tender/proposal documents **Purpose**: Auto-validation and checklist updates

```bash
# Validates: Indigenous procurement mentions, compliance sections
# Updates: MOKAI dashboard with tender progress
# Alerts: Missing required sections
```

**Benefits**:

- Ensures tender quality
- Automatic compliance checking
- Real-time dashboard updates

### 🎵 MOK HOUSE Music Business Hooks

#### 4. **Project Session Logger Hook** (Stop)

**Trigger**: End of Claude session **Purpose**: Auto-log music production session notes

```bash
# Extracts: What was worked on (tracks, mixing, mastering)
# Logs: To project-specific diary in MOK HOUSE vault
# Updates: Project status in Notion/Linear
```

**Benefits**:

- Session documentation without manual effort
- Client work tracking
- Project history for invoicing

#### 5. **Sample/Asset Reference Hook** (UserPromptSubmit)

**Trigger**: Prompt mentions audio files, samples, or assets **Purpose**: Auto-load metadata from music library

```bash
# Detects: File references, sample names
# Loads: BPM, key, genre tags from metadata
# Suggests: Compatible samples based on project context
```

**Benefits**:

- Quick sample discovery
- Metadata-aware suggestions
- Faster music production workflow

### 🧠 General Claudelife Productivity Hooks

#### 6. **Smart Context Pack Loader Hook** (UserPromptSubmit)

**Trigger**: Keywords match domain areas (business/tech/health) **Purpose**: Load relevant context packs automatically

```bash
# Already partially implemented via your existing patterns
# Enhancement: Hook-based for guaranteed loading
# Returns: Graduated context loading (10K→30K→50K)
```

**Benefits**:

- Automatic context optimization
- Token budget management
- Faster response times

#### 7. **Research Auto-Saver Hook** (PostTool - mcp__gpt-researcher__)

**Trigger**: After GPT Researcher completes **Purpose**: Auto-save, tag, and categorize research

```bash
# After: /research or /quick-research
# Saves: To /00-inbox/research/ with metadata
# Runs: /tag-keyword-DR-extractor automatically
# Updates: Knowledge graph connections
```

**Benefits**:

- Zero-friction research capture
- Automatic RAG optimization
- Knowledge graph population

#### 8. **Git Workflow Intelligence Hook** (PostTool - Edit/Write)

**Trigger**: After significant code/document changes **Purpose**: Smart commit suggestions and branch management

```bash
# Analyzes: File changes, context from transcript
# Suggests: Commit message based on actual work done
# Auto-stages: Related files for atomic commits
```

**Benefits**:

- Better commit messages
- Atomic commit grouping
- Reduced manual git operations

#### 9. **Memory Sync Validator Hook** (PostTool)

**Trigger**: After modifying critical files (commands, MCP config, package.json) **Purpose**: Enhanced version of your existing post-commit hook

```bash
# Already have: post-commit-serena-sync.sh
# Enhancement: Run on PostTool instead of post-commit
# Validates: Memory actually needs updating (diff analysis)
# Auto-runs: /update-serena-memory if critical changes detected
```

**Benefits**:

- Proactive memory updates
- Catches changes before commit
- Automatic Serena context refresh

#### 10. **Task Completion Validator Hook** (PostTool - task-master)

**Trigger**: After task-master set-status **Purpose**: Verify task actually complete before marking done

```bash
# After: task-master set-status --status=done
# Checks: Tests pass, files compiled, no TODOs in changed files
# Blocks: If validation fails (exit code 1)
# Logs: To task completion diary
```

**Benefits**:

- Quality enforcement
- Prevents premature task closure
- Automatic testing integration

## Implementation Priority

### High Priority (Immediate Value)

1. **Auto-Diary Capture Hook** - Solves MOKAI logging friction
2. **Research Auto-Saver Hook** - Completes research workflow automation
3. **Memory Sync Validator Hook** - Enhances existing automation

### Medium Priority (Business Value)

4. **Client Context Loader Hook** - MOKAI client work efficiency
5. **Tender Document Processor Hook** - MOKAI compliance automation
6. **Project Session Logger Hook** - MOK HOUSE session tracking

### Nice-to-Have (Productivity Boost)

7. **Smart Context Pack Loader Hook** - Token optimization
8. **Git Workflow Intelligence Hook** - Better version control
9. **Sample/Asset Reference Hook** - MOK HOUSE music production
10. **Task Completion Validator Hook** - Quality assurance
