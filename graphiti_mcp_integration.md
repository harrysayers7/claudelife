# Graphiti MCP Server Integration

## Overview
The Graphiti MCP server is now successfully installed and configured to work with Claude Code. This integration provides persistent knowledge graph capabilities that can capture, store, and retrieve information from your development sessions.

## Installation Details

### Components Installed
- **Graphiti MCP Server**: `/Users/harrysayers/Developer/claudelife/graphiti_mcp_server/`
- **Dependencies**: Installed via `uv` package manager
- **Configuration**: Added to `.mcp.json` with `claudelife` group ID

### Configuration
The MCP server is configured with:
- **Transport**: stdio (direct communication with Claude Code)
- **Neo4j Database**: bolt://localhost:7687
- **LLM Provider**: OpenAI (gpt-4o-mini)
- **Group ID**: "claudelife" (namespaces this project's knowledge)
- **Telemetry**: Disabled for privacy

## Available Tools
Once Claude Code is restarted, these tools will be available:

### Core Functions
- `mcp__graphiti__add_episode` - Add knowledge episodes (text/JSON/messages)
- `mcp__graphiti__search_nodes` - Search entity nodes and summaries
- `mcp__graphiti__search_facts` - Search relationships/facts between entities
- `mcp__graphiti__get_episodes` - Retrieve recent episodes
- `mcp__graphiti__get_status` - Check server and Neo4j connection status

### Management Functions
- `mcp__graphiti__delete_episode` - Remove specific episodes
- `mcp__graphiti__delete_entity_edge` - Remove entity relationships
- `mcp__graphiti__clear_graph` - Clear all data and rebuild indices

## Usage Examples

### Adding Knowledge
```javascript
// Add a development session
mcp__graphiti__add_episode({
  name: "Implement user authentication",
  episode_body: "Completed JWT-based authentication system using bcrypt for password hashing...",
  source: "text"
})

// Add structured project data
mcp__graphiti__add_episode({
  name: "Project metadata",
  episode_body: JSON.stringify({
    project: "claudelife",
    technologies: ["Python", "Neo4j", "Graphiti"],
    status: "active"
  }),
  source: "json"
})
```

### Searching Knowledge
```javascript
// Search for authentication-related information
mcp__graphiti__search_nodes({
  query: "authentication JWT bcrypt"
})

// Find relationships between technologies
mcp__graphiti__search_facts({
  query: "Python Neo4j integration"
})
```

## Integration with Personal Assistant

The Graphiti knowledge graph automatically enhances the personal assistant system by:

1. **Session Memory**: Automatically capturing development sessions and decisions
2. **Project Context**: Building relationships between technologies, tasks, and outcomes
3. **Learning**: Improving responses based on past interactions and patterns
4. **Cross-Session Continuity**: Maintaining context across different Claude Code sessions

## Next Steps

1. **Restart Claude Code** to load the new MCP server
2. **Test the integration** by trying some of the available tools
3. **Begin using** the knowledge capture in your development workflow
4. **Monitor** the knowledge graph growth via Neo4j Desktop

## Troubleshooting

### If tools don't appear after restart:
- Check that Neo4j Desktop is running
- Verify `.mcp.json` configuration is valid
- Check Claude Code console for MCP connection errors

### If Neo4j connection fails:
- Ensure Neo4j Desktop is running on localhost:7687
- Verify username/password are correct (neo4j/neo4j)
- Check firewall settings

### For performance issues:
- Adjust `SEMAPHORE_LIMIT` in `.env` file (lower for rate limiting)
- Monitor Neo4j memory usage in desktop app

## Files Created/Modified

- `graphiti_mcp_server/` - Complete MCP server installation
- `graphiti_mcp_server/.env` - Environment configuration
- `.mcp.json` - Added Graphiti server configuration
- `test_graphiti_mcp.py` - Test script for validation
- `graphiti_mcp_integration.md` - This documentation

The Graphiti knowledge graph is now ready to enhance your development workflow with persistent, queryable memory!