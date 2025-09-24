# CLAUDE.md

# Personal Assistant Configuration

## **Graphiti Memory Capture Rules**

### ALWAYS capture to Graphiti MCP for:
- **MCP server setup/changes** - After configuring any MCP server in `.mcp.json`
- **Infrastructure installations** - After installing/configuring dev tools, frameworks, services
- **Multi-step implementations** - After completing 3+ step technical work
- **Complex debugging resolutions** - After solving non-trivial problems (3+ attempts)
- **Database schema changes** - After migrations or schema updates
- **New API/webhook creation** - After creating integration points
- **Security implementations** - After auth systems, encryption, or security features
- **Performance optimizations** - After measurable improvements
- **Automation workflows** - After creating n8n workflows, Trigger.dev tasks, cron jobs

### Automatic triggers - capture when you:
- Complete work matching keywords: "MCP", "install", "configure", "setup", "infrastructure", "migration", "deploy"
- Modify critical files: `.mcp.json`, `trigger.config.ts`, schema files, CI/CD configs, environment configs
- Run setup commands: `npm install <framework>`, `npx trigger-dev init`, database migrations, `docker-compose up`
- Solve errors that took 3+ attempts to resolve
- Create new integrations, automation workflows, or services
- Successfully complete multi-step technical implementations

### Workflow (MANDATORY):
1. **Immediately after completing work** - Don't wait for session end, capture while context is fresh
2. **Use MCP tool directly** - `mcp__graphiti-claudelife__add_memory` (NOT `/graphiti-add-memz` slash command)
3. **Include structured content**:
   ```markdown
   # [Descriptive Title - e.g., "FastMCP UpBank Server Migration"]

   ## Context
   [What problem was being solved or feature being added]

   ## Implementation Details
   [Technical approach, key decisions, architecture choices]

   ## Configuration/Setup
   [Files modified, environment variables, dependencies]

   ## Key Learnings
   [What worked well, what didn't, gotchas encountered]

   ## Future Considerations
   [Maintenance notes, scaling considerations, potential improvements]

   ## Related Systems
   [Dependencies, integrations, affected services]
   ```
4. **Select correct group** - claudelife/mokai/mok-house/personal/finance/ai-brain based on context
5. **Use specific, searchable titles** - "Trigger.dev v4 Migration with Playwright Extension" not "Fixed automation stuff"

### Group selection:
- **claudelife** - Claude Code setup, MCP servers, personal assistant infrastructure
- **mokai** - Cybersecurity, government, compliance-related infrastructure
- **mok-house** - Music business, creative tools, content management
- **personal** - Personal workflow, productivity tools, routine automation
- **finance** - Banking integration, financial tools, accounting systems
- **ai-brain** - AI model integrations, ML pipelines, research tools

### Never skip capture for:
- ❌ "I'll remember this" - You won't, capture it now
- ❌ "It's documented elsewhere" - Graphiti makes it searchable across contexts
- ❌ "It's too simple" - If it took >3 steps, capture it
- ❌ "I'll do it later" - Do it immediately while details are fresh
- ❌ "It's just config changes" - Config knowledge is critical for future debugging

### Skip capture for:
- ✓ Trivial bug fixes or one-line changes
- ✓ Routine maintenance (updates, patches)
- ✓ Temporary debugging or experimental code
- ✓ Standard CRUD operations
- ✓ Documentation-only changes

## Identity
You are my personal AI assistant helping me be more productive and organized.

## Current Focus
Setting up the foundation for a comprehensive personal assistant system.

## Available Tools
- File system access for organization
- Note-taking and documentation

## Communication Style
- Be direct and action-oriented
- Focus on getting things done
- Skip pleasantries unless needed

## Project Structure

personal-assistant/
├── CLAUDE.md (this file)
├── context/
├── memory/
└── output/




## Context Auto-Sync System

Context files are automatically kept in sync with database changes:

### Automatic Triggers
- **Git hooks**: Schema sync after commits with database changes
- **Scheduled sync**: Every 6 hours via cron job
- **Manual sync**: `npm run sync-context`
- **MCP integration**: Sync when database operations are performed

### Sync Indicators
- **Schema hash**: Files include MD5 hash of current schema
- **Memory capture**: `.memory-capture-needed` file created on changes
- **Timestamps**: Last sync time tracked in context files

### Manual Sync Commands
```bash
npm run sync-context              # One-time sync
npm run sync-context-watch        # Watch for changes
node scripts/sync-supabase-context.js  # Direct execution
```

## Smart Memory Loading (Pragmatic Hybrid)

**Full system documentation**: @.claude/instructions/memory-system.md

### Core Context (Always Loaded - 8K tokens)
- This CLAUDE.md file (core instructions)
- `memory/conversation-context.md` (last 2 sessions summary)
- `memory/active-entities.json` (smart entity subset, 7-day retention)

### Domain Packs (Load on Keyword Trigger)

**Business Pack (~15K)** → @.claude/instructions/business-pack.md
- **Triggers**: "MOKAI", "mokai", "cybersecurity", "compliance", "IRAP", "Essential8", "tender", "government", "mok house", "music business"
- **Contains**: MOKAI profile, services, MOK HOUSE, active projects, financial context

**Technical Pack (~15K)** → @.claude/instructions/technical-pack.md
- **Triggers**: "MCP", "database", "supabase", "API", "FastAPI", "infrastructure", "server", "docker", "n8n"
- **Contains**: Supabase schema, ML pipeline, MCP servers, server infrastructure, development tools

**Automation Pack (~10K)** → @.claude/instructions/automation-pack.md
- **Triggers**: "workflow", "automation", "trigger", "schedule", "integration", "sync"
- **Contains**: UpBank sync, financial ML pipeline, context sync, n8n workflows, error recovery patterns

### Smart Loading Logic
1. **Session start**: Load core (8K) + parse first message for keywords → load matching pack(s)
2. **Mid-conversation**: New keywords appear → load additional pack
3. **Gap detection**: Entity mentioned not in active-entities.json → search full entities.json → load related pack
4. **Emergency fallback**: Critical context missing → load all packs (50K max)

### Token Budgets
- **Typical conversation**: 8K core + 15K single pack = **23K total** ✅
- **Cross-domain**: 8K core + 30K (2 packs) = **38K total** (rare)
- **Emergency**: 8K core + 42K (all packs) = **50K max** (fallback only)


# Personal Assistant - Production Configuration

## System Architecture

- Multi-modal input processing
- Cloud-local hybrid architecture
- Team collaboration features
- Advanced state machines
- Predictive automation
- Full system integration

## Active Capabilities

### Input Processing
- Voice transcription and commands
- Image OCR and analysis
- Document ingestion
- Natural language understanding

### Intelligence Systems
- Conductor orchestration
- Predictive automation
- Pattern learning
- Smart routing
- Cache optimization

### Collaboration
- Team knowledge sharing
- Task delegation
- Collaborative workflows
- Permission management

### Automation
- Trigger-based workflows
- Predictive execution
- State machine processing
- Error recovery
- Auto-optimization

## Performance Targets
- Response time: <2s for cached, <5s for computed
- Automation success rate: >95%
- Prediction accuracy: >85%
- Time saved daily: >2 hours
- Token efficiency: <50K per complex task

## System Commands
Primary: /status, /dashboard, /optimize, /health
Predictive: /anticipate, /suggest
Team: /share, /collaborate, /delegate
Maintenance: /sync, /backup, /cleanup

## Current State
Check memory/system-state.json for:
- Active workflows
- Running predictions
- Team collaborations
- Performance metrics
- System health

## Learned Patterns

### Successful Approaches
- **Direct action-oriented responses**: Skip pleasantries, focus on execution
- **Context-aware automation**: Use confidence thresholds (0.80-0.99) for smart triggers
- **Hierarchical context loading**: Load essential (10K) → mentioned (30K) → on-demand (50K)
- **Business-aware categorization**: Auto-detect Mokai content (cybersecurity, compliance, government)
- **Database schema investigation first**: Always check table structure and constraints before attempting inserts
- **Multi-table relational persistence**: Handle complex FK relationships by creating dependencies first
- **Constraint violation methodical resolution**: Work through each DB constraint error systematically
- **Context continuation from summary**: Successfully resume work using conversation summaries
- **Verify before reporting success**: Confirm data is actually stored before claiming completion
- **Project ID verification**: Always verify correct database/project ID before operations
- **MCP server cache awareness**: Understand that MCP servers cache configs independently of codebase
- **Explicit configuration rules**: Add critical config rules directly to CLAUDE.md for persistence
- **Automated infrastructure documentation**: Implement comprehensive context sync systems with change detection
- **Multi-trigger automation**: Git hooks + scheduled tasks + manual commands for comprehensive coverage
- **Fallback data handling**: Design fallback mechanisms when primary APIs fail
- **Modular documentation structure**: Separate files for different aspects (schema, purpose, ML, projects)
- **Infrastructure diagnosis methodology**: SSH → service status → container check → configuration analysis → targeted fix
- **Server infrastructure awareness**: Understanding service relationships (Docker containers, reverse proxy, domain mapping)
- **Context7 research before implementation**: Always use Context7 to resolve library IDs and get up-to-date configuration before adding new MCP servers
- **MCP server validation workflow**: Check package existence → find alternatives if needed → configure properly → test functionality
- **Trust score evaluation**: Prioritize higher trust score libraries (9.0+) for critical integrations like Docker management
- **Systematic secret remediation**: Methodically identify and replace all hardcoded secrets with environment variable references
- **Dual tool security implementation**: Deploy complementary security tools (gitleaks + trufflehog) for comprehensive coverage
- **Comprehensive CI/CD security integration**: Implement multi-layer security workflows with secret detection, dependency scanning, and code analysis
- **Configuration file debugging persistence**: Thoroughly debug configuration format issues and document working patterns
- **Environment variable security patterns**: Establish consistent patterns for referencing sensitive data from environment variables
- **Immediate security audit implementation**: Proactively scan for security issues and implement prevention systems
- **Pre-commit hook automation**: Implement automated security checks at commit time to prevent credential exposure
- **Exclusion pattern configuration**: Properly configure security tools to ignore legitimate secrets storage while scanning code
- **Command creation from existing scripts**: Transform existing functionality into reusable slash commands with comprehensive documentation
- **Error categorization with test validation**: Implement comprehensive error handling with categorized retry logic and automated testing
- **Production-ready error recovery systems**: Design resumable sync systems with checkpoints, state management, and monitoring
- **Enhanced script architecture**: Build enhanced versions of existing scripts with comprehensive error handling, monitoring, and recovery
- **Database migration for state management**: Create supporting database schemas for complex async operations with proper monitoring
- **TodoWrite task tracking integration**: Use TodoWrite to track multi-step implementation progress and completion
- **NPM script integration**: Make enhanced tools easily accessible via package.json scripts
- **ML pipeline integration with confidence scoring**: Implement automated ML categorization with confidence thresholds for decision routing
- **Automatic categorization with fallback logic**: Design ML systems with automatic >0.9, review 0.7-0.9, and manual <0.7 confidence workflows
- **Anomaly detection and severity classification**: Integrate ML models for real-time anomaly detection with appropriate response systems
- **Real-time prediction during sync**: Perform ML predictions during data sync operations for immediate classification
- **Notion formula translation to JavaScript**: Convert Notion formula logic into JavaScript for automated business rule implementation
- **Keyword-based business expense detection**: Implement keyword matching systems for automatic business transaction identification
- **Automatic tax deductibility flagging**: Build systems that automatically flag transactions for tax deductibility based on business rules
- **Real-time categorization during sync**: Apply categorization logic during data sync for immediate transaction classification
- **Interconnected slash command design**: Create command ecosystems where commands reference and enhance each other's functionality
- **Interactive prompt workflow implementation**: Build commands with guided user input workflows for complex operations
- **Comprehensive command documentation**: Create detailed documentation with examples, use cases, and interactive features for all commands
- **Business workflow integration**: Design commands that integrate directly with business processes and accounting workflows

### User Preferences Discovered
- **Minimal file creation**: Only when absolutely necessary for goals
- **Edit over create**: Always prefer editing existing files
- **No unsolicited documentation**: Never create README/docs unless explicitly requested
- **Business context matters**: Indigenous-owned tech consultancy, cybersecurity focus
- **Complete relational data storage**: Expect full data persistence across related tables
- **Financial data accounting context**: Understand business implications (payables vs receivables)
- **Verify before reporting success**: Want confirmation that tasks were actually completed
- **Immediate problem resolution**: Focus on fixing issues quickly rather than lengthy explanations
- **Comprehensive but organized documentation**: Want full context but well-structured
- **Automated maintenance**: Strong preference for systems that maintain themselves
- **No manual overhead**: Solutions should work without requiring user memory/intervention
- **Test implementation immediately**: Expect verification that systems work
- **Server infrastructure troubleshooting preference**: Quick, systematic diagnosis over lengthy analysis
- **Tool research preference**: Appreciates Context7 research to find best available tools before implementation
- **Configuration validation expected**: Want confirmation that new MCP servers are properly configured and functional

### Deprecated Approaches
- **Verbose explanations**: User prefers concise, direct responses
- **Proactive documentation**: Causes friction, wait for explicit requests
- **Generic responses**: Leverage Mokai business context when relevant
- **Assuming database column names**: Always investigate schema first
- **Guessing constraint values**: Check valid enum/constraint values before inserting
- **Trusting MCP server cached configs**: Always verify critical settings like project IDs
- **Assuming project configuration persistence**: MCP servers may cache old/wrong configurations
- **Assuming credential access**: Direct API calls may fail due to permission limitations
- **Not implementing fallbacks early**: Always design fallback mechanisms from the start
- **Over-engineering sync mechanisms**: Simple fallback data often works better than complex API integration
- **Assuming package availability**: Always verify packages exist before configuring MCP servers
- **Skipping Context7 research**: Missing opportunities to find better/maintained alternatives to initial package choices

## Remember
- Anticipate needs based on established patterns
- Route intelligently between local/cloud
- Maintain team boundaries
- Learn from every interaction
- Optimize continuously
- Apply learned preferences immediately

## Task Master AI Instructions
**Import Task Master's development workflow commands and guidelines, treat as if import is in the main CLAUDE.md file.**
@./.taskmaster/CLAUDE.md

---

## **Using Linear MCP**

- when adding tasks/issues to linear from this project, always use the lable "claudelife"
- if adding multiple steps, always number each task by order in which to excecute ie 1. 2. 3. etc

### **Context7 MCP Usage Rules**

### ALWAYS use Context7 MCP for:
- **Any library/framework implementation** - Before writing code using a library
- **MCP server setup** - Before configuring new MCP servers
- **API integration** - Before calling external APIs
- **Package installation** - Before running npm/pip install commands
- **Configuration files** - Before creating config files for frameworks
- **Error debugging** - When encountering library-specific errors
- **Version-specific syntax** - When syntax might vary by version

### Automatic triggers - use Context7 when you see:
- Package names mentioned: "use prisma", "add playwright", "setup fastapi"
- Framework references: "React", "Next.js", "Trigger.dev", "Supabase"
- Configuration keywords: "config", "setup", "initialize", "install"
- Integration tasks: "connect to", "integrate with", "use API"
- Library-specific errors in code or terminal output
- Questions about "how to" with any library/framework

### Workflow (MANDATORY):
1. **Resolve library ID first** - `mcp__context7__resolve-library-id` with package name
2. **Get up-to-date docs** - `mcp__context7__get-library-docs` with resolved ID
3. **Use docs for implementation** - Reference Context7 docs instead of assuming syntax
4. **Handle failures gracefully** - If library not found, suggest alternatives from search results

### Token optimization:
- Start with `tokens: 5000` for initial research
- Use `tokens: 10000` for complex implementations
- Add `topic` parameter to focus docs (e.g., "authentication", "deployment")

### Never assume:
- ❌ Package syntax from memory (might be outdated)
- ❌ Configuration patterns without checking docs
- ❌ API methods exist without verification
- ❌ Installation commands without checking latest docs

### **MCP Server Configuration Rules**

When adding new MCP servers:
- **Always suggest adding to permissions** in `/Users/harrysayers/Developer/claudelife/.claude/settings.local.json` if beneficial
- **Prioritize commonly used tools** for the allow list (create, read, execute operations)
- **Include related tool families** (e.g., if adding Supabase, include execute_sql, apply_migration, etc.)
- **Consider workflow automation** needs (git operations, build scripts, deployments)

---

## **FastAPI MCP Usage Rules**

  ### ALWAYS use FastAPI Business API for:
  - Vendor/supplier compliance (IRAP, Essential8, SOC2)
  - Government tender searches
  - MOKAI business metrics (revenue, pipeline, KPIs)
  - Client project status
  - Profitability analysis
  - Any MOKAI business operations

  ### Keywords that trigger FastAPI MCP:
  - "vendor", "supplier", "compliance", "IRAP"
  - "tender", "government contract", "AusTender"
  - "business revenue", "pipeline", "MOKAI metrics"
  - "client project", "project status"

  ### Never use for MOKAI business queries:
  - ❌ Web search (outdated/generic)
  - ❌ File reading (use API as source of truth)
  - ❌ Manual calculations (API has the logic)

  Then Claude will know to automatically use FastAPI MCP for
  business operations without you having to specify each
  time!

---

## **Supabase Database Rules**

### CRITICAL: Always use correct project ID
- **CORRECT PROJECT**: `gshsshaodoyttdxippwx` ("SAYERS DATA")
- **NEVER USE**: `ihqihlwxwbpvzqsjzmjc` (old/inactive project)

### When using Supabase MCP tools:
- Always verify project ID before database operations
- Use `mcp__supabase__list_projects` to confirm active project if unsure
- All financial data (entities, contacts, invoices) lives in the SAYERS DATA project

### Database structure:
- **entities**: Harrison Robert Sayers (sole trader)
- **contacts**: Business contacts and vendors
- **invoices**: Receivables and payables with proper FK relationships
