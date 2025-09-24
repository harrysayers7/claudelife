Capture learnings, patterns, and context from current session to memory:

## Pre-Steps:
1. **Check for git reminder**: Look for `.memory-capture-needed` file
2. **If reminder exists**: Include its contents in the capture context

## What to Capture:

### Learning Patterns (update CLAUDE.md "Learned Patterns"):
- **Success patterns**: What worked well in this session
- **Failure patterns**: What didn't work or caused issues
- **User preferences**: New preferences discovered from user corrections/feedback
- **Deprecated approaches**: Methods that should be avoided

### Memory Graph (update memory/graph/ files):
- **Entities**: People, projects, tools, concepts mentioned
- **Relationships**: Connections between entities
- **Temporal markers**: When things happened

### Infrastructure Changes (Graphiti):
If MCP servers, infrastructure, or significant technical work was completed, suggest using Graphiti:
- `mcp__graphiti-claudelife__add_memory` for infrastructure/MCP changes
- Include: what was done, files modified, key decisions, gotchas

## Execution:

1. **Analyze this session** for:
   - Commands that worked well vs failed
   - User corrections or preference signals
   - New tools/projects/people introduced
   - Technical implementations completed

2. **Update CLAUDE.md** "Learned Patterns" section:
   ```markdown
   ### Successful Approaches
   - [New pattern discovered]

   ### User Preferences Discovered
   - [New preference from user feedback]

   ### Deprecated Approaches
   - [Approach that failed or was corrected]
   ```

3. **Update memory graph** (if entities/relationships found):
   - memory/graph/entities.json - Add new entities
   - memory/graph/relationships.json - Add connections
   - memory/graph/timeline.json - Add temporal events

4. **Generate report** saved to memory/learning-reports/[date].md:
   ```markdown
   # Learning Report - [Date]

   ## Success Patterns (Keep doing)
   - [What worked]

   ## Failure Patterns (Stop doing)
   - [What failed]

   ## Optimizations Discovered
   - [Efficiency improvements]

   ## User Preferences Noted
   - [Preference signals]

   ## Entities Captured
   - [New entities added to graph]

   ## Relationships Mapped
   - [New connections discovered]

   ## Recommended Next Steps
   - [Based on session learnings]
   ```

## Post-Steps:
1. **Confirm what was captured**
2. **If `.memory-capture-needed` exists**: Ask if user wants to delete it
3. **Suggest Graphiti capture** if infrastructure work was completed
4. **Update memory/metrics.md** with session stats (commands used, time saved)

**Usage**: Run at end of productive sessions or when user says "remember this" or "save what we learned"
