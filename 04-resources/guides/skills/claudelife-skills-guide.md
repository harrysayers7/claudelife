---
date: "2025-10-22 12:30"
---

# Claudelife Skills Guide

This guide documents all Claude Code Skills installed in the Claudelife project.

## What are Skills?

Skills are specialized workflows that Claude Code can invoke to handle specific types of tasks. They're stored in `.claude/skills/` and can be activated using the Skill tool.

## Available Skills

### brainstorming
**Location**: `.claude/skills/brainstorming/SKILL.md`
**Source**: [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/brainstorming)

**Purpose**: Transform rough ideas into fully-formed designs through structured questioning, alternative exploration, and codebase awareness.

**When to use**:
- Before writing code or implementation plans
- When you have a rough idea that needs refining
- When exploring different architectural approaches
- When you need to validate a design incrementally
- When designing features for existing codebases
- When brainstorming needs to respect established patterns or business rules

**Phases**:
1. **Understanding** - Explore codebase patterns with Serena; gather purpose, constraints, criteria through one question at a time
2. **Exploration** - Propose 2-3 different approaches grounded in existing codebase patterns
3. **Design Presentation** - Present design in 200-300 word sections with codebase integration points
4. **Design Documentation** - Write design doc to `docs/plans/`
5. **Worktree Setup** - Set up isolated workspace (uses git worktrees)
6. **Planning Handoff** - Create implementation plan

**Key Features**:
- **Serena MCP integration**: Explores existing code patterns and architectural decisions
- **Graphiti MCP integration**: Gathers business context, entity relationships, and learned patterns
- Uses AskUserQuestion tool for structured multiple-choice decisions
- Incremental validation of design sections
- Codebase-grounded approach recommendations
- Flexible progression (can go backward when needed)
- YAGNI principle (ruthlessly remove unnecessary features)

**NEW: Codebase-Aware Design**:
The brainstorming skill now integrates with Serena and Graphiti MCPs to understand:
- Existing architectural patterns in your codebase
- How similar features are currently implemented
- Business context and established patterns
- Entity relationships and system constraints
- This ensures designs are grounded in reality and aligned with existing work

**How to invoke**:
```javascript
Skill({ command: "brainstorming" })
```

**Example checklist**:
```
Brainstorming Progress:
- [ ] Phase 1: Understanding (purpose, constraints, criteria gathered)
- [ ] Phase 2: Exploration (2-3 approaches proposed and evaluated)
- [ ] Phase 3: Design Presentation (design validated in sections)
- [ ] Phase 4: Design Documentation (design written to docs/plans/)
- [ ] Phase 5: Worktree Setup (if implementing)
- [ ] Phase 6: Planning Handoff (if implementing)
```

---

## Installing New Skills

### From superpowers repository

```bash
# Download the skill file
curl -s https://raw.githubusercontent.com/obra/superpowers/main/skills/<skill-name>/SKILL.md > .claude/skills/<skill-name>/SKILL.md

# Update this guide
# Add documentation for the new skill
```

### From other sources

1. Create directory: `mkdir -p .claude/skills/<skill-name>`
2. Add `SKILL.md` file with frontmatter containing `name` and `description`
3. Document the skill in this guide
4. Update Serena memory if the skill affects workflows

---

## Skill Best Practices

1. **Announce usage**: Always state when you're using a skill ("I'm using the brainstorming skill...")
2. **Follow the process**: Complete each phase before moving to the next
3. **Go backward when needed**: Don't force forward if requirements are unclear
4. **Use structured questions**: Leverage AskUserQuestion for choices with trade-offs
5. **Validate incrementally**: Get feedback on each section of design/output

---

## Related Resources

- [Superpowers Repository](https://github.com/obra/superpowers) - Collection of reusable skills
- [Skills Creation Guide](.serena/memories/skills_creation_guide.md) - How to create custom skills
- [Commands Guide](../commands/claudelife-commands-guide.md) - Slash commands vs skills

---

**Last Updated**: 2025-10-22
