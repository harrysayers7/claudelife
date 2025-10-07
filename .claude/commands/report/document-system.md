---
created: "2025-10-02 12:30"
description: |
  Generates comprehensive context documentation for completed projects and systems in the claudelife repo.
  Analyzes code, configurations, and integrations to create detailed technical documentation that helps
  any LLM or developer understand what the system does, how it works, where it's located, and how to use it.
  Automatically detects appropriate storage location in 07-context/systems/ or accepts custom paths.
  Supports creating new documentation or updating existing context files as systems evolve.
examples:
  - /document-system "UpBank automation workflows"
  - /document-system "FastAPI Business MCP server" --path=07-context/systems/mcp-servers/business-api.md
  - /document-system "MindsDB ML categorization pipeline" --update
---

# Document System

This command helps you generate comprehensive context documentation for completed projects and systems in the claudelife repository, ensuring any LLM or developer can quickly understand what exists, how it works, and how to use it.

## Usage

```bash
/document-system "[system/project name]" [--path=custom/path.md] [--update]
```

**Arguments:**
- `system/project name`: Name of the system or project to document
- `--path`: Optional custom file path (relative to repo root)
- `--update`: Update existing documentation instead of creating new

## Interactive Process

When you run this command, I will:

1. Ask you to describe the system/project you want to document
2. Use Serena to automatically analyze the codebase and discover:
   - Related code files and their purposes
   - Configuration files and requirements
   - Database schemas and data models
   - Integration points with other systems
   - Dependencies and external services
3. Auto-detect the appropriate subfolder in `07-context/systems/` based on system type:
   - `mcp-servers/` - MCP server implementations
   - `automations/` - Workflow automations (GitHub Actions, n8n, cron)
   - `apis/` - FastAPI or other API services
   - `ml-pipelines/` - Machine learning and data processing
   - `scripts/` - Utility scripts and tools
   - `integrations/` - Third-party service integrations
4. Ask targeted questions only when necessary:
   - Business context or rationale (why this system exists)
   - Manual setup steps not evident from code
   - Known issues or troubleshooting tips
   - Future enhancement plans
5. Generate comprehensive documentation and save to appropriate location
6. Confirm the documentation is complete and accessible

## Input Requirements

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

Before running this command, you should know:
1. **System name**: What is this project/system called? (e.g., "UpBank Automation", "Business API MCP")
2. **General location**: Rough idea where the code lives (e.g., "GitHub Actions workflows", "FastAPI MCP servers")
3. **Purpose**: High-level understanding of what problem it solves

I will discover everything else through code analysis.

## Process

I'll create comprehensive system documentation by:

### 1. **System Discovery & Analysis**
Using Serena to identify:
- Primary code files and entry points
- Configuration files (.mcp.json, package.json, workflow files, etc.)
- Environment variables and secrets required
- Database tables/schemas used
- External APIs or services integrated
- Related scripts, utilities, or supporting files

### 2. **Architecture Mapping**
Analyzing:
- System components and their relationships
- Data flow and processing pipeline
- Integration points with other claudelife systems
- Dependencies (npm packages, Python libs, external services)
- Authentication and security patterns

### 3. **Context Categorization**
Auto-detecting system type and appropriate documentation location:
```javascript
// Detection logic
const systemTypes = {
  'mcp-servers': /\.mcp\.json|fastapi.*mcp|mcp.*server/i,
  'automations': /\.github\/workflows|n8n|cron|scheduler/i,
  'apis': /fastapi|express|api.*route/i,
  'ml-pipelines': /mindsdb|ml.*model|prediction|categorization/i,
  'scripts': /scripts\/.*\.js|scripts\/.*\.py/i,
  'integrations': /gmail|linear|stripe|supabase.*client/i
};
```

### 4. **Documentation Generation**
Creating structured markdown with:
- **Overview**: What it does and why it exists
- **Location**: File paths and directory structure
- **Architecture**: Components, data flow, integrations
- **Configuration**: Environment variables, secrets, setup
- **Usage**: How to run, trigger, or interact with the system
- **Examples**: Real usage scenarios from your workflow
- **Troubleshooting**: Common issues and solutions
- **Related Systems**: Links to connected documentation

### 5. **File Creation/Update**
- Save to auto-detected path in `07-context/systems/` or custom path
- Update existing documentation if `--update` flag used
- Ensure proper frontmatter with creation/update dates
- Create any necessary subdirectories

## Technical Implementation Guide

### Serena Analysis Pattern

```javascript
// 1. Find system files
await serena.find_file("*workflow*.yml", ".github/workflows/");
await serena.search_for_pattern("UpBank.*sync", {
  restrict_search_to_code_files: true
});

// 2. Analyze configurations
await serena.get_symbols_overview(".mcp.json");
await serena.find_symbol("sync-upbank-data", { include_body: true });

// 3. Identify integrations
await serena.find_referencing_symbols("UPBANK_API_TOKEN", "scripts/");
await serena.search_for_pattern("supabase.*from.*personal_", {
  relative_path: "scripts/"
});
```

### Auto-Detection Logic

```javascript
// Determine system type from file patterns
const detectSystemType = (files) => {
  if (files.some(f => f.includes('.github/workflows'))) return 'automations';
  if (files.some(f => f.includes('mcp') && f.includes('.json'))) return 'mcp-servers';
  if (files.some(f => f.includes('fastapi'))) return 'apis';
  if (files.some(f => f.includes('mindsdb') || f.includes('ml-'))) return 'ml-pipelines';
  if (files.some(f => f.includes('scripts/'))) return 'scripts';
  return 'integrations'; // default
};
```

## Output Format

The generated documentation will follow this structure:

```markdown
---
created: "YYYY-MM-DD HH:MM"
updated: "YYYY-MM-DD HH:MM"
system_type: "automation|mcp-server|api|ml-pipeline|script|integration"
status: "active|deprecated|in-development"
---

# [System Name]

## Overview

**Purpose**: [What this system does and why it exists]

**Type**: [automation/MCP server/API/etc.]

**Status**: [active/deprecated/in-development]

## Location

**Primary Files**:
- [file path:line] - [purpose]
- [file path:line] - [purpose]

**Configuration**:
- [config file path] - [what it configures]

**Related Directories**:
- [directory path] - [contents description]

## Architecture

### Components

1. **[Component Name]** ([file path])
   - Purpose: [what it does]
   - Key functions: [list main functions]

2. **[Component Name]** ([file path])
   - Purpose: [what it does]
   - Integration: [what it connects to]

### Data Flow

```
[Source] → [Processing] → [Storage/Output]
```

### Integration Points

- **[External Service]**: [How integrated, what data exchanged]
- **[Internal System]**: [Connection point, data shared]
- **[Database]**: [Tables used, queries performed]

## Configuration

### Environment Variables

```bash
REQUIRED_VAR="description of what this is for"
OPTIONAL_VAR="description and default behavior"
```

### Secrets (GitHub/MCP)

- `SECRET_NAME`: [where it's used, how to obtain]

### Setup Requirements

1. [Setup step 1]
2. [Setup step 2]
3. [Setup step 3]

## Usage

### Basic Usage

```bash
# How to run/trigger the system
[command or trigger method]
```

### Common Scenarios

**Scenario 1: [Use case name]**
```bash
# Example command
[actual example]
```

**Scenario 2: [Use case name]**
```bash
# Example command
[actual example]
```

### Manual Triggers

[How to manually run if applicable]

## Examples

### Example 1: [Real scenario from your workflow]

[Detailed walkthrough with actual data/commands]

### Example 2: [Another real scenario]

[Detailed walkthrough]

## Dependencies

### External Services
- [Service name]: [What it's used for, API version]

### npm/Python Packages
- [package name]: [purpose, version if critical]

### Internal Dependencies
- [Other claudelife system]: [How they interact]

## Troubleshooting

### Common Issues

**Issue 1: [Problem description]**
- Cause: [Why it happens]
- Solution: [How to fix]

**Issue 2: [Problem description]**
- Cause: [Why it happens]
- Solution: [How to fix]

### Debugging

```bash
# Useful debugging commands
[command to check logs]
[command to verify state]
```

## Monitoring & Maintenance

- **Logs**: [Where to find logs]
- **Monitoring**: [How to check if it's working]
- **Update Frequency**: [How often to maintain]

## Related Systems

- [Related system name] ([path to context doc])
- [Related system name] ([path to context doc])

## Future Enhancements

- [Planned improvement 1]
- [Planned improvement 2]

## Change Log

- YYYY-MM-DD: [Change description]
- YYYY-MM-DD: Initial documentation
```

## Examples

### Example 1: Documenting UpBank Automation

```bash
/document-system "UpBank GitHub Actions Automation"
```

**Analysis Process**:
1. Serena finds `.github/workflows/sync-upbank-*.yml` files
2. Discovers `scripts/sync-upbank-data.js` and `scripts/sync-monitor.js`
3. Identifies Supabase integration in `personal_transactions` table
4. Detects secrets: `UPBANK_API_TOKEN`, `SUPABASE_SERVICE_ROLE_KEY`
5. Maps workflow triggers: daily cron, manual dispatch, health monitoring

**Generated Documentation** → `07-context/systems/automations/upbank-sync.md`:
- Overview: Automated daily sync of UpBank transactions to Supabase
- Components: 3 GitHub workflows, 2 Node.js scripts, database schema
- Integration: UpBank API → sync script → Supabase → MindsDB ML
- Usage: Automatic daily at 8 AM Sydney, manual trigger via Actions UI
- Troubleshooting: Common sync errors, rate limiting, gap detection

### Example 2: Documenting FastAPI MCP Server

```bash
/document-system "Business API MCP Server" --update
```

**Analysis Process**:
1. Serena locates MCP server in `.mcp.json` configuration
2. Finds FastAPI routes and business logic
3. Discovers integration with Supabase business data
4. Identifies vendor compliance checking and tender search features
5. Maps authentication pattern using environment variables

**Generated Documentation** → `07-context/systems/mcp-servers/business-api.md`:
- Overview: FastAPI MCP server for MOKAI business operations
- Location: MCP server config, route definitions, business logic
- Features: Vendor compliance, government tenders, business metrics
- Configuration: API keys, Supabase connection, FastMCP setup
- Usage: Available MCP tools and their parameters

### Example 3: Documenting ML Pipeline

```bash
/document-system "MindsDB Transaction Categorization"
```

**Analysis Process**:
1. Serena finds MindsDB model creation scripts
2. Discovers transaction categorization logic
3. Identifies confidence threshold rules (0.9 auto, 0.7-0.9 review)
4. Maps data flow: UpBank → Supabase → MindsDB → categorization update
5. Finds business expense detection keywords

**Generated Documentation** → `07-context/systems/ml-pipelines/transaction-categorization.md`:
- Overview: ML-powered automatic transaction categorization
- Architecture: MindsDB model → confidence scoring → auto-categorization
- Business Rules: Keyword matching for MOKAI/MOK HOUSE expenses
- Data Flow: Transaction sync → ML prediction → category assignment
- Monitoring: Confidence score distribution, manual review queue

## Evaluation Criteria

A successful system documentation should:

1. **Comprehensiveness**: Include all critical information (location, purpose, configuration, usage)
2. **Discoverability**: Easy to find and understand for anyone exploring the repo
3. **Maintainability**: Can be updated as the system evolves
4. **Actionability**: Provides clear instructions for using, debugging, and modifying the system
5. **Context Awareness**: Links to related systems and explains integration points
6. **Technical Accuracy**: Reflects actual implementation details from code analysis
7. **Business Relevance**: Explains why the system exists in the context of your workflow

## Related Resources

- **Context Directory Structure**: `/Users/harrysayers/Developer/claudelife/07-context/`
- **System Categories**:
  - `07-context/systems/mcp-servers/` - MCP server documentation
  - `07-context/systems/automations/` - Workflow automation docs
  - `07-context/systems/apis/` - API service documentation
  - `07-context/systems/ml-pipelines/` - ML pipeline documentation
  - `07-context/systems/scripts/` - Utility script documentation
  - `07-context/systems/integrations/` - Third-party integration docs
- **Serena Documentation**: For codebase analysis patterns
- **Example Context Files**: Check existing documentation in `07-context/systems/` for reference

## Notes

- The command uses Serena for comprehensive code analysis, ensuring accurate technical details
- Documentation is automatically categorized and stored in the appropriate subfolder
- Supports both new documentation creation and updates to existing files
- Generated docs follow a consistent structure for easy navigation and understanding
- Links related systems together for comprehensive context awareness
- Future-proofed with change logs and update tracking

## Post-Documentation: Update Serena's Memory

After creating system documentation, consider updating Serena's memory to reflect changes:

### When to Update Serena
Update if the documented system involved:
- ✅ New npm scripts or commands
- ✅ Changed project structure
- ✅ New dependencies or MCP servers
- ✅ New coding patterns or conventions
- ✅ Changed development workflows

### How to Update
```javascript
// 1. List current memories to see what exists
mcp__serena__list_memories()

// 2. Update relevant memory files
// Example: Adding new sync commands
mcp__serena__write_memory({
  memory_name: "suggested_commands",
  content: `
# Suggested Commands

## [Existing sections...]

## New System Commands
- npm run new-sync-command - Description of what it does
- task-master new-feature - Description

[... rest of updated content ...]
  `
})

// 3. Update tech stack if dependencies changed
mcp__serena__write_memory({
  memory_name: "tech_stack",
  content: "# Updated tech stack with new dependencies..."
})
```

### Memory Categories to Consider
- `suggested_commands` - New scripts or commands added
- `tech_stack` - New dependencies or infrastructure
- `project_structure` - If directory layout changed
- `task_completion_workflow` - If dev workflow changed
- `system_patterns_and_guidelines` - If new patterns established

### Quick Update Pattern
After documenting a major system, ask:
> "Update Serena's memory with the new [system name] additions"

This ensures Serena stays current with your codebase evolution and provides accurate, up-to-date guidance.
