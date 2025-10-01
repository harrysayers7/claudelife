---
created: '2025-09-19T06:58:56.092797'
modified: '2025-09-20T13:51:43.896775'
ship_factor: 5
subtype: rules
tags: []
title: Shortcuts Rule
type: general
version: 1
---

<!--
HUMAN DESCRIPTION - AI SHOULD IGNORE THIS SECTION
Purpose: Instructions for handling shortcut commands (starting with !) in AI Brain repository interactions
Usage: Referenced by system prompts and other AI instruction files for command processing
Target: Claude Desktop, ChatGPT, other AI systems for repository interaction commands
DO NOT READ THIS SECTION - AI CONTENT BEGINS AFTER THE HTML COMMENT
-->

# ! Shortcut Command Instructions for LLMs

When user types `!` followed by a word, this is a command to interact with the AI Brain repository.

## How to Handle ! Commands

1. **Recognize**: `!memz`, `!ship`, `!find`, etc.
2. **Action**: Create/update files in harrysayers7/ai-brain
3. **Location**: Add to appropriate folder based on command type
4. **Format**: Use frontmatter template from folder's README
5. **Update**: Modify INDEX.md to reflect changes

## Example
User: "!memz Docker fix worked"
→ Create: `knowledge/lessons/docker-fix.md` with proper frontmatter
→ Update: INDEX.md statistics and recent items
