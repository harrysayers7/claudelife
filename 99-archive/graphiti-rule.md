# taken from claude.md to maybe add back later

## **Graphiti Memory Capture Rules**



### ALWAYS capture to Graphiti MCP for:

- **MCP server setup/changes** - After configuring any MCP server in `.mcp.json`

- **Infrastructure installations** - After installing/configuring dev tools, frameworks, services

- **Multi-step implementations** - After completing 3+ step technical work

- **Complex debugging resolutions** - After solving non-trivial problems (3+ attempts)

- **Database schema changes** - After migrations or schema updates

- **New API/webhook creation** - After creating integration points

- **Security implementations** - After auth systems, encryption, or security features

- **Performance optimizations** - After measurable improvements

- **Automation workflows** - After creating n8n workflows, Trigger.dev tasks, cron jobs



### Automatic triggers - capture when you:

- Complete work matching keywords: "MCP", "install", "configure", "setup", "infrastructure", "migration", "deploy"

- Modify critical files: `.mcp.json`, `trigger.config.ts`, schema files, CI/CD configs, environment configs

- Run setup commands: `npm install <framework>`, `npx trigger-dev init`, database migrations, `docker-compose up`

- Solve errors that took 3+ attempts to resolve

- Create new integrations, automation workflows, or services

- Successfully complete multi-step technical implementations



### Workflow (MANDATORY):

1. **Immediately after completing work** - Don't wait for session end, capture while context is fresh

2. **Use MCP tool directly** - `mcp__graphiti-claudelife__add_memory` (NOT `/graphiti-add-memz` slash command)

3. **Include structured content**:

```markdown

# [Descriptive Title - e.g., "FastMCP UpBank Server Migration"]



## Context

[What problem was being solved or feature being added]



## Implementation Details

[Technical approach, key decisions, architecture choices]



## Configuration/Setup

[Files modified, environment variables, dependencies]



## Key Learnings

[What worked well, what didn't, gotchas encountered]



## Future Considerations

[Maintenance notes, scaling considerations, potential improvements]



## Related Systems

[Dependencies, integrations, affected services]

```

4. **Select correct group** - claudelife/mokai/mok-house/personal/finance/ai-brain based on context

5. **Use specific, searchable titles** - "Trigger.dev v4 Migration with Playwright Extension" not "Fixed automation stuff"



### Group selection:

- **claudelife** - Claude Code setup, MCP servers, personal assistant infrastructure

- **mokai** - Cybersecurity, government, compliance-related infrastructure

- **mok-house** - Music business, creative tools, content management

- **personal** - Personal workflow, productivity tools, routine automation

- **finance** - Banking integration, financial tools, accounting systems

- **ai-brain** - AI model integrations, ML pipelines, research tools



### Never skip capture for:

- ❌ "I'll remember this" - You won't, capture it now

- ❌ "It's documented elsewhere" - Graphiti makes it searchable across contexts

- ❌ "It's too simple" - If it took >3 steps, capture it

- ❌ "I'll do it later" - Do it immediately while details are fresh

- ❌ "It's just config changes" - Config knowledge is critical for future debugging



### Skip capture for:

- ✓ Trivial bug fixes or one-line changes

- ✓ Routine maintenance (updates, patches)

- ✓ Temporary debugging or experimental code

- ✓ Standard CRUD operations

- ✓ Documentation-only changes
