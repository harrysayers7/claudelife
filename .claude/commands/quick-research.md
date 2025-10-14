---
created: "2025-10-13 10:50"
description: |
  Quick web search using GPT Researcher to research a specific topic or automatically research the current conversation context.
  Optimized for speed over depth - provides fast, relevant information with search snippets.
  Use for quick context when working on unfamiliar technologies, debugging issues, or making implementation decisions.
examples:
  - /quick-research "FastAPI dependency injection patterns"
  - /quick-research "Trigger.dev timezone handling"
  - /quick-research
---

# Quick Research

This command uses GPT Researcher's quick search tool to gather fast, relevant information about a specific topic or automatically research the current conversation context.

## Usage

```bash
/quick-research [optional topic]
/quick-research
```

**With argument**: Research the specified topic
**Without argument**: Automatically research the context from your last message

## When to Use

Use this command when you need:
- **Quick context** on unfamiliar technologies or libraries
- **Fast answers** to specific technical questions
- **Best practices** for implementation patterns
- **Debugging guidance** for issues you're encountering
- **Validation** of technical approaches
- **Up-to-date information** without deep analysis

**Use `/quick-research` for**: Speed and immediate answers
**Use `/research` for**: Comprehensive analysis with detailed reports

## How It Works

### With Argument (Explicit Topic)
```bash
/quick-research "Trigger.dev scheduled tasks with timezone handling"
```
Directly searches for the specified topic and returns relevant snippets.

### Without Argument (Context-Aware)
```bash
/quick-research
```
Analyzes your **last message** to understand the current topic/problem, then automatically researches that context.

## Process

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

When you run this command, I will:

1. **Determine research topic**
   - If argument provided: Use the specified topic
   - If no argument: Analyze your last message to identify the main topic, problem, or question

2. **Execute quick search**
   ```javascript
   mcp__gpt-researcher__quick_search({
     query: "determined topic or explicit argument"
   })
   ```

3. **Format results with:**
   - **Summary** at the start explaining relevance
   - **Key findings** with relevant snippets
   - **Suggested next steps** when applicable
   - Inline display for immediate use

4. **Memory consideration** (if highly relevant)
   - If findings establish important patterns for claudelife, I'll ask if you want to update Serena's memory
   - Otherwise, results are displayed inline only

## Output Format

### Summary
A concise overview of the findings and how they relate to your context.

### Key Findings
- Bullet points with the most relevant information
- Code snippets or examples when available
- Direct answers to your question

### Next Steps (when applicable)
Actionable recommendations based on the research:
- Implementation suggestions
- Related topics to explore
- Potential considerations

### Memory Update Prompt (if relevant)
If findings would benefit Serena's understanding:
> "These findings seem relevant to [memory category]. Would you like me to update Serena's memory?"

## Examples

### Example 1: Explicit Topic - Quick Technical Answer

```bash
/quick-research "FastAPI dependency injection patterns"
```

**Output:**
```
📚 Quick Research: FastAPI Dependency Injection Patterns

FastAPI uses Python's type hints and the Depends() function for dependency injection:

Key Findings:
• Use Depends() to declare dependencies in route parameters
• Dependencies are automatically resolved and injected at request time
• Can create reusable dependencies for auth, database connections, configuration
• Supports nested dependencies and async dependencies
• Type hints provide automatic validation and IDE support

Basic Pattern:
```python
from fastapi import Depends, FastAPI

def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
async def read_items(db = Depends(get_db)):
    return db.query_items()
```

Next Steps:
• Check how dependencies are used in your existing MCP servers
• Consider creating shared dependencies for auth/database access
• Use FastAPI's dependency injection for cleaner route handlers
```

### Example 2: Context-Aware Research

**Your last message:**
> "I'm getting a 422 error when calling the Supabase MCP tool with execute_sql"

```bash
/quick-research
```

**Output:**
```
📚 Quick Research: Supabase MCP 422 Errors with execute_sql

Analyzing your Supabase MCP error...

Key Findings:
• 422 errors indicate request validation failures
• Common causes with Supabase execute_sql:
  - Missing required project_id parameter
  - Incorrect project_id format (should be lowercase alphanumeric)
  - Malformed SQL query syntax
  - Missing query parameter entirely
• Supabase MCP requires both project_id and query parameters

Quick Fix:
```javascript
// Correct format
mcp__supabase__execute_sql({
  project_id: "gshsshaodoyttdxippwx",  // Your SAYERS DATA project
  query: "SELECT * FROM transactions LIMIT 10"
})
```

Next Steps:
• Verify you're using project_id: "gshsshaodoyttdxippwx"
• Check that your SQL query is valid PostgreSQL syntax
• Share the exact MCP call that's failing for specific debugging
```

### Example 3: Implementation Decision Support

**Your last message:**
> "Should I use Trigger.dev or n8n for syncing UpBank transactions?"

```bash
/quick-research
```

**Output:**
```
📚 Quick Research: Trigger.dev vs n8n for Bank Transaction Sync

Comparing automation platforms for your UpBank sync workflow...

Key Findings:
• **Trigger.dev** strengths:
  - Better for complex retry logic and error handling
  - Built-in queue management for rate limiting
  - Type-safe TypeScript workflows
  - Superior observability and debugging

• **n8n** strengths:
  - Visual workflow builder
  - Quick webhook setup
  - Good for simple API integrations
  - Lower initial complexity

Recommendation for UpBank Sync:
✓ Use **Trigger.dev** if you need:
  - ML categorization after sync
  - Sophisticated error recovery
  - Transaction batching with retry logic
  - Long-running processing tasks

✓ Use **n8n** if you need:
  - Simple webhook receiver
  - Forward to another system
  - Quick prototype without code

Next Steps:
• Given your ML categorization needs, Trigger.dev is likely better
• n8n could receive webhooks and trigger Trigger.dev tasks
• Consider hybrid: n8n for webhooks → Trigger.dev for processing
```

### Example 4: Debugging Context

**Your last message:**
> "My FastMCP server isn't showing up in Claude Desktop even after restart"

```bash
/quick-research
```

**Output:**
```
📚 Quick Research: FastMCP Server Not Appearing in Claude Desktop

Troubleshooting FastMCP server visibility issues...

Key Findings:
• Common causes for MCP servers not appearing:
  1. Server not properly configured in .mcp.json or ~/.claude/claude_desktop_config.json
  2. Server not enabled in Claude Code settings (enabledMcpjsonServers)
  3. Server crashing on startup (check logs)
  4. Wrong command/path in server configuration
  5. Missing environment variables

Debugging Steps:
1. Check server is in correct config file:
   - Project servers: `.mcp.json`
   - Global servers: `~/.claude/claude_desktop_config.json`

2. Verify server is enabled (Claude Code):
   - Check `~/.claude/settings.local.json`
   - Add server name to `enabledMcpjsonServers` array

3. Test server manually:
   ```bash
   # Test if server starts
   python -m your_mcp_server
   ```

4. Check Claude Desktop logs for startup errors

Next Steps:
• Share your .mcp.json configuration
• Check if server name is in enabledMcpjsonServers
• Test server starts without errors
```

## Best Practices

1. **Be specific with topics** - More specific queries yield better results
2. **Use without arguments mid-conversation** - Perfect for quick context when stuck
3. **Follow up with questions** - Quick research is a starting point, not the full answer
4. **Use for speed, `/research` for depth** - Choose based on your needs
5. **Verify critical information** - Always validate important technical decisions

## Use Case Scenarios

### Unfamiliar Technologies
You're working with a library you haven't used before:
```bash
/quick-research "Zod schema validation with transform"
```

### Debugging Issues
Something's not working as expected:
```bash
/quick-research  # analyzes your error message automatically
```

### Implementation Decisions
Choosing between approaches:
```bash
/quick-research "async vs sync database queries in FastAPI"
```

### Best Practices
Want to follow standards:
```bash
/quick-research "Python async error handling patterns"
```

### API Usage
Understanding how to use an API:
```bash
/quick-research "Supabase RLS policies for multi-tenant apps"
```

## Memory Integration

After quick research, I may suggest updating Serena's memory if findings:
- Establish patterns you'll use repeatedly
- Clarify important technical approaches
- Document solutions to recurring problems
- Provide reusable code patterns

You can request memory updates by saying:
> "Add this to Serena's memory under [category]"

## Related Commands

- `/research` - Comprehensive deep research with detailed reports
- `/update-serena-memory` - Update Serena's memory with important findings
- `/document-system` - Create comprehensive system documentation
- `/coding:implement` - Implement solutions based on research findings

## Notes

- **Quick search is optimized for speed** - Uses web snippets rather than deep analysis
- **Best for immediate answers** - When you need context fast to continue working
- **Context-aware mode** - Automatically understands what you're working on from your last message
- **No file saving** - Results displayed inline (unlike `/research` which saves to vault)
- Requires GPT Researcher MCP server configured with appropriate API keys

## Tips for Better Quick Research

**Good topics:**
- "FastAPI OAuth2 password flow example"
- "Trigger.dev batch processing patterns"
- "Supabase migration best practices"

**Less effective topics:**
- "Python" (too broad)
- "How do I code?" (unclear intent)
- "Best practices" (needs context)

**Context-aware usage:**
Simply run `/quick-research` when you're stuck - I'll figure out what you need help with based on your last message!
