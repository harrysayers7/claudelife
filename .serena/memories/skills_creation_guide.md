# Skills Creation Guide

## Reference Document
Complete guide for creating Claude Code Skills is available at:
`04-resources/research/SKILLz.md`

## Quick Reference

### Skill Structure
```
skill-name/
├── SKILL.md              # Main instructions (YAML frontmatter + markdown)
├── reference.md          # Optional: Additional reference material
├── examples.md           # Optional: Usage examples
└── scripts/              # Optional: Executable scripts
    └── helper.py
```

### SKILL.md Template
```markdown
---
name: Skill Name (max 64 chars)
description: What the skill does and when to use it (max 1024 chars). Use third person.
---

# Skill Name

## Quick Start
[Basic usage instructions]

## Advanced Features
[Link to additional files if needed]
```

### Key Principles
1. **Concise is key** - Only add context Claude doesn't already have
2. **Set appropriate degrees of freedom** - Match specificity to task fragility
3. **Test with all models** - Haiku, Sonnet, and Opus
4. **Progressive disclosure** - Keep SKILL.md under 500 lines, split into separate files
5. **Workflows for complex tasks** - Provide checklists Claude can track

### Description Best Practices
- Write in third person (not "I" or "you")
- Include what the skill does AND when to use it
- Be specific with key terms and triggers
- Example: "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."

### Common Patterns
- **Template pattern**: Provide output format templates
- **Examples pattern**: Show input/output pairs
- **Conditional workflow**: Guide through decision points
- **Feedback loops**: Validate → fix → repeat

### File Organization
- Keep references one level deep from SKILL.md
- Use forward slashes in paths (not backslashes)
- Name files descriptively
- Include table of contents for files >100 lines

### Skills with Code
- Solve, don't punt - handle errors in scripts
- Provide utility scripts for reliability
- Use visual analysis when possible
- Create verifiable intermediate outputs
- List required packages in SKILL.md

### Location in Claudelife
Skills are stored in: `.claude/skills/`

### Creating Skills with Claude
1. Complete task without a skill first
2. Identify reusable patterns
3. Ask Claude to create a skill capturing the pattern
4. Review for conciseness
5. Test with fresh Claude instance
6. Iterate based on observation

For complete details, see: `04-resources/research/SKILLz.md`
