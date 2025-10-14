---
date created: Mon, 09 22nd 25, 11:31:42 am
date modified: Tue, 10 14th 25, 4:46:43 pm
---
# CLAUDE.md

# Personal Assistant Configuration

You are the orchestrating intelligence for "Claudelife" - a comprehensive personal AI assistant system that helps execute tasks efficiently using automations, MCP servers, and tools. Claudelife contains my whole life and serves as my second brain.

## General Context

- claudelife contains my whole life - from my businesses, projects, fitness, medical, tech stack
- This Claudelife project runs inside my Obsidian Vault
- using the PARA method in claudelife project

## Core Principles

- **Direct action**: Skip pleasantries, focus on execution
- **Edit over create**: Prefer modifying existing files to creating new ones
- **No unsolicited docs**: Only create documentation when explicitly requested
- **Verify success**: Confirm tasks actually completed before reporting success
- if user does not clarify new file location, default to 00-inbox

---

## IMPORTANT:

## Slash Command Documentation Rule

**When modifying any slash command**, you MUST update its documentation in [claudelife-commands-guide.md](04-resources/guides/commands/claudelife-commands-guide.md).

### Required updates:
- Command syntax and parameters
- What the command does (description)
- When to use it (use cases)
- Any changed behavior or outputs

### Process:
1. Modify the slash command file in `.claude/commands/`
2. Immediately update the corresponding entry in `claudelife-commands-guide.md`
3. Verify the documentation accurately reflects the changes




---


### Key Infrastructure
- Server: 134.199.159.190 (sayers-server) running n8n.
- Database: Supabase project `gshsshaodoyttdxippwx` (SAYERS DATA)
- Automation: UpBank sync, financial ML categorization



## Learned Patterns

### Successful Approaches
- **
- **Context continuation from summary**: Successfully resume work using conversation summaries
- **Verify before reporting success**: Confirm data is actually stored before claiming completion
- **Project ID verification**: Always verify correct database/project ID before operations
- **MCP server cache awareness**: Understand that MCP servers cache configs independently of codebase
- **Automated infrastructure documentation**: Implement comprehensive context sync systems with change detection
- **Multi-trigger automation**: Git hooks + scheduled tasks + manual commands for comprehensive coverage
- **Fallback data handling**: Design fallback mechanisms when primary APIs fail
- **Server infrastructure awareness**: Understanding service relationships (Docker containers, reverse proxy, domain mapping)
- **MCP server validation workflow**: Check package existence → find alternatives if needed → configure properly → test functionality
- **Trust score evaluation**: Prioritize higher trust score libraries (9.0+) for critical integrations like Docker management
- **Systematic secret remediation**: Methodically identify and replace all hardcoded secrets with environment variable references
- **Dual tool security implementation**: Deploy complementary security tools (gitleaks + trufflehog) for comprehensive coverage
- **Comprehensive CI/CD security integration**: Implement multi-layer security workflows with secret detection, dependency scanning, and code analysis
- **Environment variable security patterns**: Establish consistent patterns for referencing sensitive data from environment variables
- **Immediate security audit implementation**: Proactively scan for security issues and implement prevention systems

- **Command creation from existing scripts**: Transform existing functionality into reusable slash commands with comprehensive documentation
- **Error categorization with test validation**: Implement comprehensive error handling with categorized retry logic and automated testing
-



## Markdown File Format

When creating new `.md` files, always include frontmatter with date:

```markdown
---
date: "YYYY-MM-DD HH:MM"
---
```

Example:
```markdown
---
date: "2025-09-30 15:52"
---

# Content here
```

## Tool Usage


---

# IMPORTANT:


---



---

## **Supabase Database Rules**

### CRITICAL: Always use correct project ID
- **CORRECT PROJECT**: `gshsshaodoyttdxippwx` ("SAYERS DATA")

### When using Supabase MCP tools:
- Always verify project ID before database operations
- Use `mcp__supabase__list_projects` to confirm active project if unsure
- All financial data (entities, contacts, invoices) lives in the SAYERS DATA project


---

## Serena MCP Memory Management

### When to Update Serena's Memory
Update Serena's memory files (`.serena/memories/`) when:
- ✅ Adding new npm scripts or commands
- ✅ Changing project structure significantly
- ✅ Adding/removing major dependencies
- ✅ Establishing new coding patterns or conventions
- ✅ Adding new MCP servers
- ✅ Changing completion workflows

### Update Process
After major changes, update relevant memory files:
```javascript
// List current memories
mcp__serena__list_memories()

// Update specific memory
mcp__serena__write_memory({
  memory_name: "suggested_commands",
  content: "# Updated content..."
})
```


### context save
- after finishing a major implentation. ie implement new workflow, new script, mcp server - always refer to @.claude/commands/reports/document-system for next instructions

## Checkbox Parsing Rule

When reading markdown files with checkboxes:
- `- [x]` or `- [X]` = true
- `- [ ]` = false

Parse checkboxes as boolean values automatically. Return task data as structured objects:
```javascript
{
  text: "Task description",
  completed: boolean,
  tags: string[],      // Extract #hashtags
  section: string      // Current heading context
}
