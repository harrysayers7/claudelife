#!/bin/bash

# MCP Server Batch Testing Script
# This script helps identify which MCP server is causing JSON schema errors

echo "MCP Server Batch Testing"
echo "========================"
echo ""

# Group 1: NPX-based servers (usually stable)
echo "Testing Group 1: NPX-based servers..."
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "serena": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@agentic-ai/serena-mcp"],
      "env": {}
    },
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {"CONTEXT7_API_KEY": "$CONTEXT7_API_KEY"}
    },
    "supabase": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server-supabase@latest"],
      "env": {"SUPABASE_ACCESS_TOKEN": "$SUPABASE_ACCESS_TOKEN"}
    },
    "task-master-ai": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "$ANTHROPIC_API_KEY",
        "PERPLEXITY_API_KEY": "$PERPLEXITY_API_KEY"
      }
    }
  }
}
EOF
echo "✅ Group 1 config written to .mcp.json"
echo "Test this group in Claude Code. If it works, continue to Group 2."
echo ""
read -p "Press Enter when ready to test Group 2..."

# Group 2: Python-based servers (potential issues)
echo "Testing Group 2: Python MCP servers..."
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "upbank": {
      "type": "stdio",
      "command": "/Users/harrysayers/Developer/claudelife/.mcp/fastmcp-env/bin/python",
      "args": ["/Users/harrysayers/Developer/claudelife/.mcp/upbank_server.py"],
      "env": {
        "UPBANK_API_TOKEN": "$UPBANK_API_TOKEN",
        "UPBANK_API_BASE_URL": "https://api.up.com.au/api/v1"
      }
    }
  }
}
EOF
echo "✅ Testing upbank server alone"
echo "Test this in Claude Code. If error occurs, upbank is the problem."
echo ""
read -p "Press Enter when ready to test next Python server..."

# Test fastmcp-brain
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "fastmcp-brain": {
      "type": "stdio",
      "command": "/Users/harrysayers/Developer/claudelife/.mcp/fastmcp-env/bin/python",
      "args": ["/Users/harrysayers/Developer/claudelife/.mcp/fastmcp_server.py"],
      "env": {}
    }
  }
}
EOF
echo "✅ Testing fastmcp-brain server alone"
echo "Test this in Claude Code. If error occurs, fastmcp-brain is the problem."
echo ""
read -p "Press Enter when ready to test gptr-mcp..."

# Test gptr-mcp
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "gptr-mcp": {
      "type": "stdio",
      "command": "python",
      "args": ["/Users/harrysayers/Developer/gptr-mcp/server.py"],
      "env": {
        "OPENAI_API_KEY": "$OPENAI_API_KEY",
        "ANTHROPIC_API_KEY": "$ANTHROPIC_API_KEY",
        "TAVILY_API_KEY": "placeholder"
      }
    }
  }
}
EOF
echo "✅ Testing gptr-mcp server alone"
echo "Test this in Claude Code. If error occurs, gptr-mcp is the problem."
echo ""
read -p "Press Enter when ready to test Graphiti servers..."

# Test one graphiti server
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "graphiti-claudelife": {
      "type": "stdio",
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run", "--isolated", "--directory",
        "/Users/harrysayers/Developer/claudelife/graphiti_mcp_server",
        "--project", ".", "graphiti_mcp_server.py",
        "--transport", "stdio", "--group-id", "claudelife"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "neo4j",
        "OPENAI_API_KEY": "$OPENAI_API_KEY",
        "MODEL_NAME": "gpt-4o-mini",
        "GRAPHITI_TELEMETRY_ENABLED": "false"
      }
    }
  }
}
EOF
echo "✅ Testing graphiti-claudelife server alone"
echo "Test this in Claude Code. If error occurs, graphiti servers are the problem."
echo ""

echo "Testing complete! The problematic server should be identified."
