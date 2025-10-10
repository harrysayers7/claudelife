---
date created: Thu, 10 9th 25, 3:03:50 pm
date modified: Thu, 10 9th 25, 3:05:06 pm
relation:
  - "[[code]]"
---


### **Level 1: Reduce (Immediate Actions)**

#### 1. **Trim CLAUDE.md Significantly**

**Current state**: Your CLAUDE.md is likely quite large with domain packs, learned patterns, etc.

 

**Action**: Create a minimal core CLAUDE.md with only "absolute universal essentials":

- Keep: Core principles, critical rules (Serena first, FastAPI MCP usage, Supabase project ID)
- Remove: Move domain packs to priming commands instead
- Remove: Move detailed learned patterns to separate reference docs

**Target**: Reduce CLAUDE.md from ~20K+ tokens to <500 tokens

#### 2. **Create Context Priming Commands**

Instead of loading all domain packs automatically, create:

```bash
# .claude/commands/prime/mokai.md
Load MOKAI business context for cybersecurity work.
Includes: business profile, services, active projects, compliance frameworks.
```

```bash
# .claude/commands/prime/technical.md
Load technical infrastructure context.
Includes: Supabase schema, MCP servers, server infrastructure.
```

```bash
# .claude/commands/prime/automation.md
Load automation and workflow context.
Includes: UpBank sync, ML pipeline, n8n workflows, error recovery.
```

**Benefit**: Only load context when needed, not "always-on"

#### 3. **Manage MCP Servers Explicitly**

**Current**: You likely have many MCP servers enabled in `.mcp.json`

 

**Action**:

- Remove rarely-used MCPs from default config
- Create specialized configs:
    - `.mcp.json.minimal` - Core servers only (Supabase, Task Master)
    - `.mcp.json.finance` - Financial work (UpBank, Stripe, Notion)
    - `.mcp.json.dev` - Development (Serena, Context7, Trigger.dev)
- Load specific configs when needed: `claude --mcp-config .mcp.json.finance`

---

### **Level 2: Delegate (Sub-Agents)**

#### 4. **Use Sub-Agents for Heavy Token Tasks**

**Create dedicated sub-agent commands for**:

- `/load-docs` - Fetch and scrape documentation (delegates to sub-agent)
- `/research-vendor` - Research vendor compliance (delegates context7 + web search)
- `/analyze-codebase` - Heavy Serena analysis work

**Pattern**:

```markdown
# .claude/commands/load-docs.md
Launch sub-agent to fetch documentation for [library].
Sub-agent will scrape docs and return summary.
Keeps primary context clean.
```

#### 5. **Implement Context Bundles**

**Action**: Add Claude Code hooks to track work:

- Create `.claude/hooks/` directory
- Implement append-only log per session
- Add `/loadbundle` command to restore context from previous sessions

**Benefit**: Can restart Claude after context overflow, resume where you left off

---

### **Level 3: Advanced (Background Agents)**

#### 6. **Create Background Agent System**

**Use cases for Claudelife**:

- `/background-analyze` - Run complexity analysis in background
- `/background-document` - Generate system documentation while you work on implementation
- `/background-sync` - Monitor UpBank sync in background

**Pattern**:

```bash
# .claude/commands/background.md
Launch background Claude Code instance for [task].
Writes output to [file].
Primary agent continues work uninterrupted.
```

---

## Concrete Implementation Plan

### **Phase 1: Reduce (This Week)**

Update Todos

- [ ]

    Audit current CLAUDE.md token usage - measure actual size

- [ ]

    Create minimal core CLAUDE.md (<500 tokens)

- [ ]

    Create /prime/mokai.md command with Business Pack content

- [ ]

    Create /prime/technical.md command with Technical Pack content

- [ ]

    Create /prime/automation.md command with Automation Pack content

- [ ]

    Create specialized MCP configs (.mcp.json.minimal, .finance, .dev)


### **Specific Changes to Your Current Setup**

#### **Before (Current)**

```markdown
# CLAUDE.md (20,000+ tokens)
- Domain Packs (always loaded): Business (~15K), Technical (~15K), Automation (~10K)
- All Learned Patterns
- Complete business context
- Full technical details
```

#### **After (Optimized)**

```markdown
# CLAUDE.md (500 tokens)
- Core Principles (4 rules)
- Critical Database: Supabase project ID
- MCP Usage: Serena first, FastAPI rules
- Priming Instructions: Use /prime commands for context
```

```markdown
# .claude/commands/prime/mokai.md (loads on demand)
[15K Business Pack content]
```

```markdown
# .claude/commands/prime/technical.md (loads on demand)
[15K Technical Pack content]
```

---

## Immediate Next Steps

1. **Measure current context usage**

    - Count tokens in current CLAUDE.md
    - List all enabled MCP servers
    - Identify what's "always-on" vs. "sometimes needed"
2. **Create core CLAUDE.md** with only:

    ```markdown
    # Core Principles
    - Direct action, edit over create, verify success

    # Critical Rules
    - Always use Serena first for code exploration
    - Supabase project: gshsshaodoyttdxippwx
    - Use /prime commands to load domain context

    # Context Priming
    - /prime/mokai - Load business context
    - /prime/technical - Load infrastructure context
    - /prime/automation - Load workflow context
    ```

3. **Move domain packs to priming commands** - Extract current pack content into separate command files

4. **Test priming workflow**:

    ```bash
    # Start fresh session
    /clear

    # Prime for MOKAI work
    /prime/mokai

    # Now context loaded, start work
    "Review vendor compliance for Essential Eight"
    ```


Would you like me to start implementing these changes? I can:

1. Audit your current CLAUDE.md and measure token usage
2. Create the minimal core CLAUDE.md
3. Create the three priming command files
4. Set up specialized MCP configs
