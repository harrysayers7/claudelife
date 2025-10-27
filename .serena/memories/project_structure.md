# Claudelife Project Structure

## Overview
This is the claudelife project - a comprehensive personal management system using Obsidian as the vault. It contains business operations, training systems, financial tracking, and personal knowledge management.

## Core Directory Structure (PARA Method)

### 00 - Daily/
Daily notes following the format: `YYYY-MM-DD - Day.md`
- Contains daily reflections, energy levels, sleep quality, stress tracking
- Used by OBSIDIA Training System for context-aware workout planning
- Frontmatter fields: `energy_morning`, `sleep_quality`, `stress_level`, `soreness`

### 01-areas/
Ongoing responsibilities and life areas:
- `business/mokai/` - MOKAI business operations and context
- `business/mokhouse/` - MOK HOUSE business operations
- `business/SMSF/` - Self-Managed Super Fund documentation
- `business/accounting/` - Accounting and financial management
- `health-fitness/training/` - **OBSIDIA Training System data**
  - `workouts/` - Daily workout logs (format: `🏋️YYYY-MM-DD.md`)
  - `programs/` - Historical training programs
  - `config/` - Personal training overrides
  - `progress/` - Analytics and progress reports
  - `injuries/` - Injury tracking data
- `tech/ai/` - AI systems, research, and integrations
- `tech/mac/` - Mac-related configurations

### 02-projects/
Active, time-bound projects with clear outcomes:
- `mokhouse/` - Active MOK HOUSE projects with client work

### 03-labs/
🧪 Brainstorming, experiments, creative ventures, building things

### 04-resources/
Reference materials and documentation:
- `guides/` - How-to guides and documentation
  - `commands/claudelife-commands-guide.md` - Slash command documentation
  - `skills/` - Claude Skills documentation
  - `technical/databases/sayers-data-database-guide.md` - Database schemas
- `lessons-learnt/` - Lessons from issues and fixes
- `network/` - Contact information and relationship notes
- `research/` - Research notes and findings
- `vault/` - Sensitive information (credentials, etc.)

### 07-context/
System documentation and context files:
- `systems/skills/` - Comprehensive system documentation
  - `obsidia-training.md` - OBSIDIA Training System documentation (1,089 lines)

### 98-templates/
Obsidian templates for content creation:
- `workout.md` - Workout logging template for OBSIDIA (177 lines)
  - Creates files with format: `🏋️YYYY-MM-DD.md`
  - Includes pre-workout check-in, exercise tables, XP calculation sections

### 99-archive/
Completed or inactive items

## Key Infrastructure

### .claude/
Claude Code configuration and customizations:
- `commands/` - Slash commands for repeated workflows
  - `mokai/` - MOKAI-specific commands
  - `mokhouse/` - MOK HOUSE-specific commands
  - `report/` - Documentation generation commands
- `skills/` - Claude Skills (progressive disclosure system)
  - `obsidia-training/` - **Training intelligence system**
    - `SKILL.md` - Main orchestrator (265 lines)
    - `programs/current-program.yaml` - 8-week hypertrophy block (218 lines)
    - `config/` - XP rules, exercise library, injury keywords
    - `scripts/` - Python automation (plan_session.py, calculate_xp.py)
    - `reference/` - Educational guides (progression.md, recovery.md)
- `settings.local.json` - Tool permissions and MCP server enablement

### .serena/
Serena MCP memory storage:
- `memories/` - Persistent knowledge base
  - `project_structure.md` - This file
  - `mokai_business_patterns.md` - MOKAI business context
  - `project_overview.md` - High-level project overview
  - `suggested_commands.md` - Commonly used commands
  - `system_patterns_and_guidelines.md` - Development patterns
  - `tech_stack.md` - Technology stack documentation

### .mcp.json
Project-specific MCP server configurations:
- Supabase integration (SAYERS DATA project)
- Task Master AI
- Serena code intelligence
- Context7 for library documentation

## OBSIDIA Training System

**Location**: `.claude/skills/obsidia-training/` (Skill) + `01-areas/health-fitness/training/` (Data)

**What It Is**: Intelligent training session planner with context-aware auto-regulation, XP gamification, and injury pattern detection.

**Auto-Activation**: Triggers when user mentions: "gym", "workout", "training", "exercise", "lift"

**Core Features**:
1. **Session Planning**: Generates 3 workout options (Standard, Adapted, Recovery) based on daily note context
2. **XP Tracking**: Gamification with multipliers for RPE, form quality, exercise type, achievements
3. **Injury Detection**: NLP-based pain keyword scanning with temporal pattern analysis
4. **Progress Analytics**: Volume, intensity, frequency tracking with progressive overload recommendations

**File Naming Convention**:
- Workout logs: `🏋️YYYY-MM-DD.md` (emoji format)
- Legacy support: `YYYY-MM-DD-workout.md` (old format)

**Integration**:
- Reads daily note frontmatter (`energy_morning`, `sleep_quality`, `stress_level`, `soreness`)
- Uses Templater to create workout files from `98-templates/workout.md`
- Python scripts for session planning and XP calculation

**Why Skills Pattern**: Progressive disclosure architecture - loads config/scripts from filesystem instead of dumping everything in context. Auto-activates on keywords, saves tokens, works alongside existing systems.

## Server Infrastructure

**Primary Server**: 134.199.159.190 (sayers-server)
- n8n automation platform
- Supabase local instance
- Ubuntu, 4 CPU, 7.8GB RAM

**Database**: Supabase project `gshsshaodoyttdxippwx` (SAYERS DATA)
- Financial entities and transactions
- Business contacts and relationships
- Invoice tracking for MOKAI/MOK HOUSE

## Development Patterns

### File Creation Preferences
- **Edit over create**: Always prefer modifying existing files
- **No unsolicited docs**: Only create documentation when explicitly requested
- **PARA alignment**: New files should fit into the PARA structure

### Markdown Frontmatter
All `.md` files should include:
```yaml
---
date: "YYYY-MM-DD HH:MM"
---
```

### MCP Server Updates
When adding new MCP servers:
1. Add to `.mcp.json` (project) or `~/.mcp.json` (global)
2. Add credentials to `.mcp.json` (ensure it's in `.gitignore`)
3. Add to `enabledMcpjsonServers` in `~/.claude/settings.local.json`
4. Restart Claude Code
5. Verify with `ListMcpResourcesTool`

### Slash Command Updates
When modifying slash commands:
1. Update command file in `.claude/commands/`
2. Immediately update `04-resources/guides/commands/claudelife-commands-guide.md`
3. Verify documentation reflects changes

## Technology Stack

- **Vault**: Obsidian (PARA method organization)
- **AI Assistant**: Claude Code + Skills + MCP servers
- **Automation**: n8n (self-hosted)
- **Database**: Supabase (PostgreSQL)
- **Code Intelligence**: Serena MCP
- **Task Management**: Task Master AI
- **Training Intelligence**: OBSIDIA (Claude Skill)

## Common Workflows

### MOKAI Business Operations
- Daily context updates in `01-areas/business/mokai/diary/YYYY-MM-DD-mokai-daily.md`
- Business profile in `mokai-profile.md`
- Contract templates in `docs/contracts/`

### MOK HOUSE Operations
- Project management via Notion ESM integration
- Invoice creation via Supabase
- Portfolio documentation in `website/project-blurbs/`

### Training Workflow
1. OBSIDIA auto-activates on "gym", "workout" keywords
2. Reads daily note for readiness metrics
3. Generates session plan (Standard/Adapted/Recovery)
4. User logs workout in `🏋️YYYY-MM-DD.md` file
5. Run `calculate_xp.py` for gamification
6. Progress tracked in weekly summaries

## Important Notes

- **Never edit `tasks.json` manually** - use Task Master commands
- **Never edit `.serena/memories/` directly** - use Serena write_memory tool
- **Never commit secrets** - use environment variables
- **Default new file location**: `00-inbox/` unless specified otherwise
- **Archive folder**: `99-archive/` is ignored unless explicitly requested

---

*Last Updated: 2025-10-21*
*Updated by: OBSIDIA Training System implementation*
