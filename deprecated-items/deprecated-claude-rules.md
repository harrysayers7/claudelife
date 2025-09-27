## **Serena MCP - Semantic Code Navigation**

### ALWAYS use Serena MCP for:
- **Before any code implementation** - Understand existing structure first
- **Code exploration and debugging** - Find functions, classes, methods efficiently
- **Understanding dependencies** - See what references what before making changes
- **Refactoring preparation** - Map out code relationships before restructuring
- **Integration planning** - Understand existing patterns before adding new features
- **Token-efficient code reading** - Get targeted information without loading full files

### Automatic triggers - use Serena when you see:
- **Implementation tasks**: "implement", "add feature", "create function", "build component"
- **Code exploration**: "find", "search code", "where is", "locate function", "show me", "class definition"
- **Understanding requests**: "how does this work", "understand the structure", "see the relationships"
- **Debugging tasks**: "fix bug", "error in", "debug issue", "troubleshoot code"
- **Refactoring needs**: "refactor", "reorganize", "restructure", "clean up code"

### Workflow Integration (MANDATORY):
```
Context7 (research library docs) → Serena (understand codebase) → Implementation → Graphiti (capture learnings)
```

### Primary Workflow Steps:
1. **Structure reconnaissance**: `mcp__serena__list_dir` + `mcp__serena__get_symbols_overview`
2. **Target identification**: `mcp__serena__find_symbol` with specific patterns
3. **Relationship mapping**: `mcp__serena__find_referencing_symbols` before changes
4. **Implementation**: Use `mcp__serena__replace_symbol_body`, `mcp__serena__insert_after_symbol`
5. **Documentation**: `mcp__serena__write_memory` for complex discoveries

### Essential Tools (in order of typical usage):
- `mcp__serena__list_dir` - Project structure reconnaissance (recursive when needed)
- `mcp__serena__get_symbols_overview` - File-level structure without full content
- `mcp__serena__find_symbol` - Locate specific functions/classes/methods by name pattern
- `mcp__serena__search_for_pattern` - Regex search when symbol names unknown
- `mcp__serena__find_referencing_symbols` - Dependency analysis before making changes
- `mcp__serena__replace_symbol_body` - Complete symbol replacement (functions, classes)
- `mcp__serena__insert_after_symbol` / `mcp__serena__insert_before_symbol` - Precise code placement
- `mcp__serena__write_memory` / `mcp__serena__read_memory` - Project knowledge persistence

### Token Optimization Rules:
- ✅ **Always start with** `get_symbols_overview` for new files
- ✅ **Use `find_symbol`** instead of reading full files
- ✅ **Pattern search first** if unsure of symbol names
- ❌ **Never Read full file** without checking symbols overview first
- ❌ **Never assume structure** - always verify with Serena tools first

### Integration with Other MCPs:
- **Context7 → Serena**: Research library syntax, then understand existing codebase structure
- **Serena → Implementation**: Map code structure before making changes
- **Implementation → Graphiti**: Capture complex code discoveries and architectural insights
- **Task Master → Serena**: Use Serena to understand implementation requirements for tasks

### Skip Serena only when:
- Non-code files (configuration, markdown, data files)
- Content already fully loaded in conversation context
- Single-line edits in known exact locations
- Working exclusively with external APIs (no local code involved)****
---

---
## Context7 MCP Usage Instructions (GLOBAL SETTING)



### When to Use Context7

- Before implementing unfamiliar libraries/frameworks

- When encountering new APIs or methods

- For troubleshooting current issues

- Before suggesting alternatives



### Pre-Flight Checks

1. **Verify library exists** - Check if library is in Context7 database

2. **Check project dependencies** - Ensure library is actually installed

3. **Identify specific version** - Match Context7 docs to project version



### Intelligent Usage Pattern

1. **Resolve library ID first** - Use `resolve-library-id` with specific library name

2. **Handle failures gracefully** - If library not found, suggest alternatives or manual research

3. **Use targeted topics** - Start with specific topics, expand if needed

4. **Optimize token usage** - Start with 3000-5000 tokens, increase only if needed

5. **Validate against project** - Cross-reference with existing codebase patterns



### Error Handling

- **Library not found**: Suggest manual research or alternative libraries

- **Topic not found**: Try broader topics or related terms

- **Version mismatch**: Flag potential compatibility issues

- **Conflicting info**: Present both options with context



### Quality Assurance

- Always verify examples work with current project setup

- Flag any version-specific code that might not work

- Provide fallback options when Context7 info is insufficient

- Cross-reference with official documentation when possible
---

## **Complete Claude Code + Archon MCP Rule** (GLOBAL)



Project Scope Decision (First Priority)

ALWAYS determine project scope before implementation:

Create NEW Project When:



Standalone application/tool

Different tech stack/framework required

Doesn't align with existing project's purpose

User explicitly requests new project

Would fundamentally change existing project scope



Add to EXISTING Project When:



Feature extends current functionality

Same tech stack and dependencies

Fits existing project's domain/purpose

Bug fix or improvement to existing code

User references specific existing project



Archon Usage Decision (Second Priority)

Use Archon for tasks requiring orchestration:

Use Archon When:



Task has 3+ distinct phases

Requires 2+ different types of expertise

Would benefit from review/validation step

Multi-domain tasks (frontend + backend + database + deployment)

Complex workflows with sequential dependencies

Research + implementation phases



Direct Implementation When:



Simple, single-file scripts

Straightforward bug fixes

Basic code refactoring

Tasks within single domain of expertise



Complete Execution Flow

1. PROJECT ANALYSIS

├─ Scan existing projects for relevance

├─ Assess if task fits existing scope

└─ Decide: New project vs. existing project



2. COMPLEXITY ASSESSMENT

├─ Count distinct phases/domains needed

├─ Identify if multiple expertise areas required

└─ Decide: Archon orchestration vs. direct implementation



3. EXECUTION

If Archon needed:

├─ Agent 1: Setup/Analysis (project structure or codebase analysis)

├─ Agent 2: Core Implementation

└─ Agent 3: Testing/Validation (if warranted)

If direct implementation:

└─ Single-agent execution

---
