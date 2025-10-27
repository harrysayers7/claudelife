---
relation:
  - "[[resources]]"
  - "[[resources]]"
date: "2025-10-16"
type: index
---

# Lessons Learned Index

This directory contains documented lessons from mistakes, debugging sessions, and discoveries during the Claudelife project. Each lesson helps prevent repeating the same errors.

## How to Use This Directory

### When to Add a Lesson
Create a new lesson learned when:
- You spend >30 minutes debugging something that should have been obvious
- You discover documentation/agent instructions were wrong
- You make a configuration mistake that could affect others
- You find a better workflow after struggling with the old way

### File Naming Convention
`YYYY-MM-DD-short-description.md`

Example: `2025-10-16-mcp-config-location.md`

### Required Frontmatter
```yaml
---
date: "YYYY-MM-DD"
category: [Configuration|Development|Debugging|Integration]
severity: [Critical|High|Medium|Low]
status: [Resolved|Ongoing|Documented]
tags: [relevant, tags, here]
---
```

### Template Structure
1. **Problem** - What went wrong
2. **Root Cause** - Why it happened
3. **What Went Wrong** - Failed attempts
4. **What Actually Worked** - The solution
5. **Fixes Applied** - What was changed to prevent recurrence
6. **Prevention Measures** - How to avoid in future
7. **Key Takeaways** - Main lessons
8. **Documentation Updated** - What docs were updated
9. **Time Cost** - How long it took

## Lessons Learned

### 2025-10-16: MCP Configuration Location
**Category:** Configuration
**Severity:** Critical
**Time Cost:** ~2 hours

Discovered that Claude Code uses `~/.claude.json` for MCP server configuration, NOT `.mcp.json`. The `mcp-expert` agent had incorrect instructions that led to editing the wrong files for 2+ hours.

**Key Lesson:** Always verify agent instructions against official documentation, especially for evolving tools.

**Files:** [2025-10-16-mcp-config-location.md](2025-10-16-mcp-config-location.md)

---

## Categories

### Configuration
- MCP server setup and management
- Environment variables and secrets
- Tool integrations

### Development
- Coding patterns and anti-patterns
- Architecture decisions
- Performance optimizations

### Debugging
- Problem diagnosis workflows
- Log analysis techniques
- Root cause identification

### Integration
- Third-party service setup
- API configuration
- Authentication flows

## Contributing

When documenting a new lesson:

1. Create file: `YYYY-MM-DD-description.md`
2. Use the template structure
3. Include specific examples and commands
4. Update this INDEX.md
5. Update relevant documentation (agents, Serena memory, guides)
6. Commit with message: `docs: add lesson learned - [description]`

## Related Documentation

- [Claudelife Commands Guide](../guides/commands/claudelife-commands-guide.md)
- [MCP Expert Agent](../../.claude/agents/mcp-expert.md)
- [Serena Memory: System Patterns](../../.serena/memories/system_patterns_and_guidelines.md)
