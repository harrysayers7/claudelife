# System Patterns and Guidelines

## Architecture Patterns

### Context File Pattern (NEW - October 2025)
- **Standardized context files**: Each business/area subfolder contains `context-{name}.md`
- **Consistent frontmatter**:
  ```yaml
  type: [context]
  relation: ["[[name]]", "[[alternative-name]]"]
  date created: [timestamp]
  date modified: [timestamp]
  ```
- **Knowledge graph integration**: Relations enable vault-wide connections
- **Coverage**: Applied across business (8 entities), health-fitness (3 areas), p-dev (3 areas), tech (3 areas)
- **Total**: 17+ context files for comprehensive area coverage
- **Purpose**: Centralized context for each area accessible to AI and knowledge graph

### Command Documentation Pattern (NEW - October 2025)
- **Centralized guide**: `/04-resources/guides/commands/claudelife-commands-guide.md`
- **Required format**:
  ```markdown
  ### /command-name
  **Created**: YYYY-MM-DD HH:MM

  ##### What it does:
  [2-3 sentences, max 50 words]

  ##### When to use it:
  [2-3 sentences, max 50 words]

  **Usage**: `/command-name [args]`
  **File**: `.claude/commands/command-name.md`
  ```
- **Automatic documentation**: `/create-command` enforces post-creation documentation
- **Coverage**: 18+ commands documented with clear use cases and functionality
- **Discovery**: Single source of truth for all available commands

### Command Update Workflow Pattern (NEW - October 2025)
- **Version tracking**: All command modifications tracked in frontmatter `version_history`
- **Diff preview**: Show before/after changes before applying
- **Validation suite**: 
  - Frontmatter YAML syntax validation
  - Command structure integrity checks
  - Broken link detection (file paths in examples)
  - Code block syntax validation
- **Auto-documentation sync**: Changes automatically update `claudelife-commands-guide.md`
- **Memory sync flagging**: Identifies when Serena memory needs updating
- **Change categories**:
  - **Minor edits**: Typos, grammar, clarifications (patch version)
  - **Feature additions**: New options, script integration (minor version)
  - **Major restructuring**: Purpose/workflow changes (major version)
- **Workflow**: Load → Analyze → Preview diff → Validate → Apply → Sync docs → Flag memory
- **Command**: `/command-update {command-name} "description of changes"`
- **Safety**: Always shows diff before applying, git commit with descriptive message

### MCP Server Configuration Pattern (CRITICAL - October 2025)
**LESSON LEARNED: Claude Code uses ~/.claude.json NOT .mcp.json**

- **Correct config location**: `~/.claude.json` (managed by CLI)
- **NEVER manually edit**: Use `claude mcp add` CLI exclusively
- **Wrong file trap**: `.mcp.json` exists but is NOT used by Claude Code
- **Verification command**: `claude mcp list` shows actual loaded servers
- **Configuration format in ~/.claude.json**:
  ```json
  {
    "server-name": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "package@latest"],
      "env": {"API_KEY": "value"}
    }
  }
  ```
- **Add servers via CLI**:
  ```bash
  claude mcp add --transport stdio <name> --env KEY=val -- command args
  ```
- **Common mistake**: Editing `~/.mcp.json` or `.mcp.json` won't affect Claude Code
- **Debug workflow**:
  1. `claude mcp list` - see what's actually loaded
  2. `claude mcp get <name>` - check specific server config
  3. `~/Library/Logs/Claude/mcp-server-<name>.log` - view connection logs
- **Context7 integration**: Use Context7 MCP to research MCP documentation before configuring
- **Hook automation**: UserPromptSubmit hook detects library questions and suggests Context7

### Context Engineering
- **Domain pack system**: Business, Technical, and Automation packs (~15K each)
- **Smart loading**: Keyword-triggered context loading to optimize token usage
- **Active entity tracking**: 7-day retention window in `active-entities.json`
- **Graduated loading**: Essential (10K) → mentioned entities (30K) → full context (50K max)

### Claude Code Hooks System
- **Post-tool execution hooks**: Monitor tool executions for data changes
- **UserPromptSubmit hooks**: Analyze user prompts before processing (e.g., Context7 detector)
- **Memory sync automation**: Auto-detect when Serena's memory needs updating
- **Pattern-based triggers**: Match tool names/arguments to detect critical changes
- **Hook configuration**: Defined in `.claude/settings.local.json`
- **Hook scripts**: Executable Python/bash scripts in `.claude/hooks/`
- **Primary hooks**:
  - `context7_detector.py` - Detects library documentation needs, suggests Context7 MCP
  - `cache-mokai-inbox.sh` - Auto-updates MOKAI inbox cache on file changes

### Research Workflow Pattern
- **COSTAR framework**: Context, Objective, Style, Tone, Audience, Response optimization
- **Deep research integration**: GPT Researcher MCP for comprehensive web research
- **Automatic vault storage**: Research saved to `/00-inbox/research/` with metadata
- **RAG optimization**: Keyword and tag extraction following tag-keyword-DR-extractor rules
- **Template-based**: Uses `98-templates/research.md` for consistent structure
- **Metadata extraction**:
  - Keywords: 5-7 specific terms for semantic search
  - Tags: 3-5 tags prioritizing existing vault connections
  - Sources: 3-5 most authoritative references
  - Category: Research domain area
  - Description: 1-2 sentence summary

### Automation Patterns
- **Error recovery**: Checkpoint-based resumable sync operations
- **Fallback mechanisms**: Multiple retry strategies with exponential backoff
- **State management**: Database-backed state for long-running operations
- **Monitoring**: Health checks and dashboard monitoring

### Database Design
- **Supabase as source of truth**: Project ID `gshsshaodoyttdxippwx`
- **FK relationships**: Proper foreign keys for data integrity
- **Context sync**: Bidirectional sync between database and local files
- **Schema migrations**: SQL files in `migrations/` directory

## Development Guidelines

### Security First
- **Never hardcode secrets**: Use environment variables
- **Pre-commit scanning**: Automated with gitleaks and trufflehog
- **Exclusion patterns**: Configure `.trufflehog.yaml` and `.gitleaks.toml`
- **Regular audits**: System health checks include security validation

### Token Optimization
- **Context budgets**: Typical 23K, max 50K tokens
- **Lazy loading**: Load context only when keywords detected
- **Compression**: Summarize older context when approaching limits
- **Smart caching**: MCP servers maintain independent caches

### Memory Management
- **Serena memory files**: Located in `.serena/memories/`
- **Update triggers**: Changes to critical data sources (Supabase, MOKAI docs, MCP config, slash commands)
- **Automated reminders**: Hooks notify when memory update recommended
- **Update command**: `/update-serena-memory` refreshes Serena's context
- **Memory categories**: project_overview, tech_stack, suggested_commands, system_patterns, etc.

### Error Handling
- **Categorized errors**: Transient, permanent, rate-limit handling
- **Retry logic**: Exponential backoff with jitter
- **State preservation**: Checkpoint progress for resumability
- **User notification**: Clear error messages with recovery suggestions

### Testing Approach
- **Manual verification**: Test scripts before automation
- **Incremental rollout**: Test in dev before production
- **Monitoring**: Track success rates and error patterns
- **Rollback ready**: Maintain previous versions for quick reversion

### Slash Command Development
- **Template-based creation**: Use `/create-command` for structured command design
- **Frontmatter required**: YAML metadata with created date, description, examples
- **Prompt engineering**: Apply COSTAR or similar frameworks for complex commands
- **Interactive workflows**: Ask clarifying questions before execution
- **Serena integration**: Commands that modify codebase should trigger memory updates
- **Post-creation documentation**: Automatically document in commands guide with "What it does" / "When to use it" format
- **Version control**: Use `/command-update` for modifications to maintain version history
- **Change validation**: All updates validated (structure, YAML, links, code syntax) before applying
- **Documentation sync**: Command updates automatically sync to `claudelife-commands-guide.md`

## Design Patterns in Use

### Research & Knowledge Management
- **COSTAR optimization**: Transform simple queries into comprehensive research prompts
- **Prompt engineering**: Apply proven frameworks (COSTAR, CLEAR, QUEST) for quality
- **Automatic vault integration**: All research saved with proper metadata
- **RAG-ready metadata**: Keywords and tags optimized for semantic search
- **Source credibility**: Prioritize recent, authoritative sources
- **Structured output**: Consistent format with executive summary, analysis, recommendations

### ML Pipeline Pattern
- **Confidence scoring**: Auto (>0.9), review (0.7-0.9), manual (<0.7)
- **Real-time classification**: During data sync operations
- **Anomaly detection**: Severity-based routing
- **Feedback loops**: Improve models based on corrections

### Business Rule Automation
- **Keyword matching**: Automatic expense categorization
- **Formula translation**: Notion formulas → JavaScript
- **Tax flagging**: Automatic deductibility detection
- **Workflow integration**: Direct accounting system updates

### Hook-Based Automation
- **Event-driven updates**: React to tool executions automatically
- **Context freshness**: Maintain up-to-date agent knowledge
- **Pattern detection**: Smart triggers based on tool patterns
- **User prompts**: Non-intrusive reminders for manual actions

### Knowledge Organization (PARA Method)
- **Context files**: Each area/subfolder has dedicated context file
- **Consistent structure**: Standardized frontmatter across all context files
- **Relation links**: Enable knowledge graph connections
- **Area coverage**: Business entities, health areas, personal dev, technical domains
