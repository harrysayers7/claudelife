# Quick Guide Generator

Create a concise, well-formatted guide on any topic and save it to `/Users/harrysayers/Developer/claudelife/HARRY/guides/`

## Usage

```bash
/quick-guide {topic}
```

**Example:** `/quick-guide playwright automation`

## What I'll Create

A **1-page guide** (200-300 words max) with:

1. **Quick Overview** - What it is and why it matters
2. **Step-by-Step Instructions** - How to use it (minimal code unless necessary)
3. **Conceptual Explanation** - How it works under the hood
4. **Practical Examples** - Real-world use cases in your claudelife setup

## Format Specifications

### Obsidian-Optimized Formatting

- **Bold** for key concepts and section headers
- `Inline code` for commands, file paths, and technical terms
- Code blocks only when absolutely necessary
- Callouts for important notes:
  ```markdown
  > [!tip] Pro Tip
  > Helpful context here

  > [!warning] Watch Out
  > Common pitfalls here
  ```
- Color highlighting with ==yellow highlights== for critical points
- Clear section breaks with `---`

### File Naming

Guides are saved as: `{topic-name}-guide.md`
- Example: `playwright-automation-guide.md`
- Example: `fastmcp-setup-guide.md`

### Claudelife Integration

Each guide includes:
- ✅ Relevant file paths in your codebase
- ✅ MCP server references from `.mcp.json`
- ✅ Links to existing implementations
- ✅ Environment variables needed
- ✅ Related tools/services you already use

## Guide Template Structure

```markdown
# {Topic Name}

> [!tip] Quick Summary
> One-sentence description of what this is and why you need it

---

## Quick Overview

**What is {Topic}?**
Brief explanation (2-3 sentences)

**Why use it in claudelife?**
Your specific use case (1-2 sentences)

---

## Step-by-Step Instructions

### Getting Started

1. **First step** - Clear action with context
2. **Second step** - Clear action with context
3. **Third step** - Clear action with context

### Key Configuration

- **Setting 1:** What it does and how to set it
- **Setting 2:** What it does and how to set it

---

## How It Works (Conceptual)

==Core concept explanation== in simple terms, no jargon

**The Flow:**
1. What happens first
2. What happens next
3. Final result

---

## Practical Examples

### Example 1: {Real scenario}
Brief walkthrough of actual use case

### Example 2: {Real scenario}
Brief walkthrough of actual use case

---

## In Your Setup

**Files to know:**
- `path/to/relevant/file.js` - What it does
- `path/to/another/file.js` - What it does

**MCP Integration:**
```json
"mcp-server-name": {
  // Relevant config from .mcp.json
}
```

**Related Commands:**
- `/command-name` - When to use it

---

> [!warning] Common Issues
> - Issue 1 and quick fix
> - Issue 2 and quick fix
```

## Before Creating Guide

I'll ask you:

1. **What's the topic?** (e.g., "Playwright automation", "FastMCP patterns")
2. **What do you want to learn?** (How to use it? How it works? Both?)
3. **Your use case?** (What are you trying to accomplish?)
4. **Any confusion points?** (What's unclear or causing problems?)
5. **Which folder?** (technical/databases, business/mokai, tools/playwright, etc.)

## After Creating Guide

**ALWAYS update `/Users/harrysayers/Developer/claudelife/HARRY/guides/README.md`:**

1. Add guide link under appropriate category
2. Remove "*No guides yet*" if it's the first guide in that category
3. Update "Last updated" timestamp at bottom
4. Keep entries alphabetical within categories

**Example entry:**
```markdown
- [Guide Title](folder/guide-name.md) - Brief description
```

## Quality Checks

A good guide should:
- ✅ Be readable in under 3 minutes
- ✅ No unnecessary code (plain English preferred)
- ✅ Clear visual hierarchy (bold, highlights, callouts)
- ✅ Practical for YOUR claudelife setup
- ✅ Render perfectly in Obsidian

---

**Ready to create a guide? Tell me the topic!**


IMPORTANT: Use Serena to search through the codebase. If you get any errors using Serena, retry with different
Serena tools.
