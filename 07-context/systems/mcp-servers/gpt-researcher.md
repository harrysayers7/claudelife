---
created: "2025-10-12 20:25"
updated: "2025-10-12 20:25"
system_type: "mcp-server"
status: "active"
---

# GPT Researcher MCP Server

## Overview

**Purpose**: Provides deep web research capabilities to Claude Code through the Model Context Protocol (MCP). Unlike standard search tools that return raw results requiring manual filtering, GPT Researcher autonomously explores and validates numerous sources, delivering high-quality, relevant, and up-to-date information optimized for LLM context usage.

**Type**: MCP Server (Python-based FastMCP)

**Status**: Active

**Key Benefits**:
- Higher quality research results than standard search
- Optimized context usage (reduces token waste)
- Comprehensive source validation
- Autonomous research agent behavior
- ~30 second research time for deep queries

## Location

**Primary Repository**: `/Users/harrysayers/Developer/gptr-mcp/`

**Primary Files**:
- `/Users/harrysayers/Developer/gptr-mcp/server.py` - Main MCP server implementation with FastMCP
- `/Users/harrysayers/Developer/gptr-mcp/utils.py` - Utility functions for response handling and research storage
- `/Users/harrysayers/Developer/gptr-mcp/requirements.txt` - Python dependencies
- `/Users/harrysayers/Developer/gptr-mcp/.env` - Environment configuration (gitignored)
- `/Users/harrysayers/Developer/gptr-mcp/.env.example` - Example environment template

**Configuration Files**:
- `/.mcp.json:103-111` - MCP server configuration in claudelife project
- `/.claude/settings.local.json:33` - Enabled in Claude Code settings

**Virtual Environment**: `/Users/harrysayers/Developer/gptr-mcp/.venv/` (Python 3.11+)

## Architecture

### Components

1. **FastMCP Server** (`server.py`)
   - Purpose: MCP protocol implementation and tool registration
   - Key functions:
     - `research_resource(topic)` - MCP resource for cached research access
     - `deep_research(query)` - Comprehensive web research tool
     - `quick_search(query)` - Fast search optimized for speed
     - `write_report(research_id, custom_prompt)` - Generate formatted reports
     - `get_research_sources(research_id)` - Retrieve research sources
     - `get_research_context(research_id)` - Get full research context
     - `research_query(topic, goal, report_format)` - MCP prompt template
     - `run_server()` - Server initialization with transport detection

2. **Research Utilities** (`utils.py`)
   - Purpose: Helper functions for research operations
   - Key functions:
     - `research_store` - In-memory cache for research results
     - `create_success_response()` / `create_error_response()` - Response formatting
     - `handle_exception()` - Error handling and logging
     - `get_researcher_by_id()` - Retrieve researcher instances
     - `format_sources_for_response()` - Format sources for MCP responses
     - `format_context_with_sources()` - Combine context with citations
     - `store_research_results()` - Cache research for reuse
     - `create_research_prompt()` - Generate research prompts

3. **GPT Researcher Core** (External Library)
   - Library: `gpt-researcher>=0.14.0`
   - Purpose: Autonomous research agent with source validation
   - Features: Multi-source research, content validation, summarization

### Data Flow

```
User Query → Claude Code
    ↓
MCP Protocol (STDIO)
    ↓
FastMCP Server (server.py)
    ↓
GPT Researcher Agent
    ↓
┌─────────────────────────────┐
│ Web Search (Tavily API)     │
│ → Multiple Sources          │
│ → Content Validation        │
│ → Relevance Filtering       │
└─────────────────────────────┘
    ↓
Research Context + Sources
    ↓
In-Memory Cache (research_store)
    ↓
MCP Response → Claude Code
```

### Integration Points

- **Claude Code**: STDIO transport via MCP configuration
- **OpenAI API**: Powers GPT Researcher's analysis and summarization (gpt-4o-mini default)
- **Tavily API**: Primary web search provider for gathering sources
- **FastMCP Framework**: MCP protocol implementation (v2.12.4+)

## Configuration

### Environment Variables

**Required**:
```bash
OPENAI_API_KEY="sk-..."           # OpenAI API for GPT Researcher analysis
TAVILY_API_KEY="tvly-..."         # Tavily API for web search
```

**Optional**:
```bash
# GPT Researcher Configuration
EMBEDDING="openai:text-embedding-3-small"    # Embedding model
STRATEGIC_LLM="openai:gpt-4o-mini"          # Strategic research LLM
MAX_ITERATIONS="2"                           # Research depth (2=faster, 3+=deeper)

# Anthropic (if using Claude for research)
ANTHROPIC_API_KEY="sk-ant-..."

# Server Configuration
LOG_LEVEL="INFO"                             # Logging level
PORT="8000"                                  # Port for SSE/HTTP transport
MCP_TRANSPORT="stdio"                        # Transport mode (stdio/sse/streamable-http)
```

### MCP Configuration (.mcp.json)

Location: `/Users/harrysayers/Developer/claudelife/.mcp.json:103-111`

```json
{
  "mcpServers": {
    "gpt-researcher": {
      "type": "stdio",
      "command": "/Users/harrysayers/Developer/gptr-mcp/.venv/bin/python",
      "args": ["/Users/harrysayers/Developer/gptr-mcp/server.py"],
      "env": {
        "OPENAI_API_KEY": "$OPENAI_API_KEY",
        "TAVILY_API_KEY": "$TAVILY_API_KEY"
      }
    }
  }
}
```

### Claude Code Settings

Location: `/.claude/settings.local.json:33`

```json
{
  "enabledMcpjsonServers": [
    "gpt-researcher"
  ]
}
```

### Setup Requirements

1. **Python 3.11+** (Required by gpt-researcher >=0.14.0)
2. **Install dependencies**:
   ```bash
   cd /Users/harrysayers/Developer/gptr-mcp
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Verify installation**:
   ```bash
   python server.py
   # Should show: "Starting GPT Researcher MCP Server with stdio transport..."
   ```

5. **Enable in Claude Code**:
   - Add to `.mcp.json` (already configured)
   - Add to `.claude/settings.local.json` enabledMcpjsonServers (already configured)
   - Restart Claude Code

## Usage

### Available MCP Tools

After restarting Claude Code, the following tools become available:

1. **`mcp__gpt-researcher__deep_research(query: str)`**
   - Conducts comprehensive web research (~30 seconds)
   - Returns research ID, context, sources, and source URLs
   - Use for: Time-sensitive info, complex topics, detailed analysis
   - Example: Stock prices, current events, technical documentation

2. **`mcp__gpt-researcher__quick_search(query: str)`**
   - Fast web search with snippets
   - Optimized for speed over depth
   - Returns: Search results with excerpts
   - Use for: Quick lookups, simple queries

3. **`mcp__gpt-researcher__write_report(research_id: str, custom_prompt?: str)`**
   - Generates formatted report from research
   - Requires research_id from deep_research
   - Optional custom prompt for specific report formats
   - Returns: Full report with costs and sources

4. **`mcp__gpt-researcher__get_research_sources(research_id: str)`**
   - Retrieves sources from completed research
   - Returns: Formatted sources and URLs

5. **`mcp__gpt-researcher__get_research_context(research_id: str)`**
   - Gets full research context
   - Returns: Complete research context text

### MCP Resources

- **`research://{topic}`** - Direct resource access to cached research results

### MCP Prompts

- **`research_query(topic, goal, report_format)`** - Generate structured research prompts

### Common Scenarios

**Scenario 1: Quick Research for Decision Making**
```javascript
// User: "What's the current state of NVIDIA stock?"
mcp__gpt-researcher__deep_research({
  query: "NVIDIA stock performance Q4 2024 analyst opinions recent developments"
})

// Returns:
// {
//   research_id: "uuid-123",
//   query: "...",
//   context: "NVIDIA (NVDA) Current Status: Price $942.89...",
//   sources: [...],
//   source_urls: [...]
// }
```

**Scenario 2: Generate Comprehensive Report**
```javascript
// After deep_research completes
mcp__gpt-researcher__write_report({
  research_id: "uuid-123",
  custom_prompt: "Create an investment analysis report with pros and cons"
})

// Returns formatted report with sources
```

**Scenario 3: Fast Lookup**
```javascript
// User: "What's the capital of Australia?"
mcp__gpt-researcher__quick_search({
  query: "capital of Australia"
})

// Returns quick search results
```

### Manual Triggers

From command line (for testing):
```bash
cd /Users/harrysayers/Developer/gptr-mcp
source .venv/bin/activate
python server.py
# Server runs in STDIO mode, ready for MCP client
```

## Examples

### Example 1: Stock Research for Investment Decision

**User Request**: "Research NVIDIA for potential investment"

**Claude Code Workflow**:
1. Triggers: `mcp__gpt-researcher__deep_research("NVIDIA stock analysis Q4 2024")`
2. Waits ~30 seconds for research
3. Receives comprehensive context with:
   - Current stock price and performance
   - Recent earnings data
   - Product announcements (Blackwell platform)
   - Analyst consensus and price targets
   - Market position and competitors
4. Formats response with citations
5. Can optionally generate report via `write_report()`

**Actual Output Example** (from README):
```markdown
## NVIDIA (NVDA) Current Status

### Recent Stock Performance
- Current price: $942.89
- YTD performance: +90.4%
- Market cap: ~$2.32 trillion

### Recent Key Developments
1. Blackwell AI Platform: 4x performance improvement
2. Q1 FY2025 Earnings: $26B revenue (+262% YoY)
3. Supply chain expansion with TSMC

### Analyst Consensus
- Strong Buy: 37 analysts
- Average price target: $1,042
- Key thesis: AI infrastructure dominance
```

### Example 2: Technical Documentation Research

**User Request**: "How do I configure Trigger.dev scheduled tasks with timezones?"

**Claude Code Workflow**:
1. `mcp__gpt-researcher__deep_research("Trigger.dev scheduled tasks cron timezone configuration")`
2. GPT Researcher:
   - Searches official docs
   - Validates code examples
   - Finds relevant API patterns
3. Returns verified information with source links
4. Claude Code synthesizes answer with examples

### Example 3: Current Events for Context

**User Request**: "What happened with the latest Apple event?"

**Quick Research Workflow**:
```javascript
mcp__gpt-researcher__quick_search({
  query: "Apple October 2024 event announcements"
})
```

Returns recent headlines and snippets instantly.

## Dependencies

### External Services
- **OpenAI API** - GPT-4o-mini for research analysis and summarization
- **Tavily API** - Web search and source retrieval
- **Alternative search engines supported**: Bing, Google, DuckDuckGo, etc.

### Python Packages (requirements.txt)
```
gpt-researcher>=0.14.0          # Core research agent
python-dotenv                    # Environment management
fastmcp>=2.8.0                  # MCP protocol framework
fastapi>=0.103.1                # Web framework (for SSE transport)
uvicorn>=0.23.2                 # ASGI server
pydantic>=2.3.0                 # Data validation
loguru>=0.7.0                   # Enhanced logging
httpx>=0.24.0                   # HTTP client for testing
sseclient-py>=1.7.0             # SSE client for testing
```

### Internal Dependencies
- **claudelife MCP configuration** - Connects server to Claude Code
- **Claude Code MCP client** - Consumes research tools

## Troubleshooting

### Common Issues

**Issue 1: Tools not appearing in Claude Code**
- **Cause**: Claude Code hasn't connected to MCP server
- **Solution**:
  1. Verify `.mcp.json` configuration is correct
  2. Check `enabledMcpjsonServers` includes "gpt-researcher"
  3. **Restart Claude Code completely**
  4. Look for tools icon in Claude Code interface

**Issue 2: "OPENAI_API_KEY not found" error**
- **Cause**: Environment variables not properly configured
- **Solution**:
  1. Check `.mcp.json` env section has proper keys
  2. Verify keys are actual values, not placeholders
  3. Test manually: `cd /Users/harrysayers/Developer/gptr-mcp && python server.py`

**Issue 3: Research takes too long or times out**
- **Cause**: Deep research iterating too many sources
- **Solution**:
  1. Adjust `MAX_ITERATIONS=2` in `.env` for faster results
  2. Use `quick_search` instead of `deep_research` for simple queries
  3. Increase timeout if needed in Claude Code settings

**Issue 4: Poor quality research results**
- **Cause**: Wrong search engine or limited API quota
- **Solution**:
  1. Verify Tavily API key is valid and has quota
  2. Consider upgrading Tavily plan for more searches
  3. Switch `STRATEGIC_LLM` to gpt-4o for higher quality analysis

**Issue 5: Python version incompatibility**
- **Cause**: gpt-researcher >=0.14.0 requires Python 3.11+
- **Solution**:
  ```bash
  python --version  # Check version
  # If < 3.11, install Python 3.11+ and recreate venv
  brew install python@3.11
  cd /Users/harrysayers/Developer/gptr-mcp
  rm -rf .venv
  python3.11 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

### Debugging

**Check server status**:
```bash
cd /Users/harrysayers/Developer/gptr-mcp
source .venv/bin/activate
python server.py
# Should output: "Starting GPT Researcher MCP Server with stdio transport..."
```

**Verify MCP configuration**:
```bash
cat /Users/harrysayers/Developer/claudelife/.mcp.json | grep -A 10 "gpt-researcher"
```

**Test API keys**:
```bash
cd /Users/harrysayers/Developer/gptr-mcp
source .venv/bin/activate
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OpenAI:', bool(os.getenv('OPENAI_API_KEY'))); print('Tavily:', bool(os.getenv('TAVILY_API_KEY')))"
```

**Check Claude Code MCP logs**:
```bash
# Claude Code doesn't expose MCP logs directly
# Verify connection by checking if tools appear after restart
```

## Monitoring & Maintenance

- **Logs**: STDIO output to Claude Code console (not persisted)
- **Monitoring**: Tools should appear in Claude Code after restart
- **Research cache**: In-memory only, cleared on server restart
- **Update Frequency**:
  - Check for gpt-researcher updates: `pip list --outdated | grep gpt-researcher`
  - Monitor Tavily API usage in dashboard
  - OpenAI API costs tracked per research operation

## Transport Modes

GPT Researcher supports multiple transport protocols:

| Transport | Use Case | Auto-Detection |
|-----------|----------|----------------|
| **STDIO** | Claude Desktop, Local MCP | Default for local |
| **SSE** | Docker, web clients, n8n | Auto in Docker |
| **Streamable HTTP** | Modern web deployments | Manual config |

**Current Configuration**: STDIO (Claude Code)

**Alternative Transports**:
```bash
# SSE for web/n8n integration
export MCP_TRANSPORT=sse
python server.py
# Binds to 0.0.0.0:8000 with /sse endpoint

# Docker with SSE
docker-compose up -d
# Auto-detects Docker, uses SSE
```

## Related Systems

- **Context7 MCP** (`/.mcp.json:3-8`) - Library documentation lookup
- **Perplexity API** (in Task Master) - Alternative research provider
- **Web search tools** - Standard MCP search (GPT Researcher provides superior quality)

## Performance Characteristics

- **Deep Research**: ~30 seconds average
- **Quick Search**: ~5 seconds average
- **Context Window**: Optimized, typically 2-5k tokens
- **Source Count**: 5-10 validated sources per research
- **Cost**:
  - OpenAI API: ~$0.01-0.03 per deep research
  - Tavily API: 1 search credit per research

## Security Considerations

1. **API Keys**: Stored in `.mcp.json` with environment variable references
2. **Local Storage**: Research cache is in-memory only (not persisted)
3. **Network**: STDIO transport = local process communication (no external exposure)
4. **Data**: Research results not logged or stored permanently

## Future Enhancements

- [ ] Add persistent research cache with SQLite
- [ ] Support multiple search providers (Bing, Google) via config
- [ ] Implement research session management for multi-step research
- [ ] Add cost tracking and budget limits
- [ ] Create custom report templates
- [ ] Integrate with claudelife knowledge base for context-aware research
- [ ] Add research result storage in Supabase for historical reference

## Change Log

- 2025-10-12: Initial documentation created
- 2025-09-24: GPT Researcher MCP installed and configured in claudelife
