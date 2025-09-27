#!/usr/bin/env python3
"""
MCP Server Schema Validator
Tests MCP servers by running them and validating their tool schemas
"""

import json
import subprocess
import sys
from pathlib import Path

def test_server_schema(name, command, args, env=None):
    """Test a single MCP server's schema"""
    print(f"\n Testing {name}...")

    # Create test input to list tools
    test_input = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 1
    }

    try:
        # Build full command
        full_command = [command] + args

        # Run the server and send test input
        result = subprocess.run(
            full_command,
            input=json.dumps(test_input) + "\n",
            capture_output=True,
            text=True,
            env=env,
            timeout=5
        )

        if result.returncode != 0:
            print(f"  ❌ Failed to run: {result.stderr[:200]}")
            return False

        # Try to parse the response
        try:
            # MCP servers might return multiple JSON objects, try to parse lines
            for line in result.stdout.split('\n'):
                if line.strip() and line.startswith('{'):
                    response = json.loads(line)
                    if 'result' in response and 'tools' in response['result']:
                        tools = response['result']['tools']
                        print(f"  ✅ Found {len(tools)} tools")

                        # Check each tool's schema
                        for i, tool in enumerate(tools):
                            if 'inputSchema' in tool:
                                schema = tool['inputSchema']
                                # Basic schema validation
                                if not isinstance(schema, dict):
                                    print(f"    ⚠️  Tool {i} ({tool.get('name', 'unknown')}): Invalid schema type")
                                if '$schema' in schema:
                                    # Check if it's the correct draft
                                    if '2020-12' not in schema['$schema']:
                                        print(f"    ⚠️  Tool {i} ({tool.get('name', 'unknown')}): Wrong schema draft: {schema['$schema']}")
                        return True
        except json.JSONDecodeError as e:
            print(f"  ⚠️  Invalid JSON response: {e}")
            print(f"     Raw output: {result.stdout[:500]}")

    except subprocess.TimeoutExpired:
        print(f"  ⚠️  Server timeout")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    return False

# Test Python-based servers that are most likely to have schema issues
servers_to_test = [
    {
        "name": "upbank",
        "command": "/Users/harrysayers/Developer/claudelife/.mcp/fastmcp-env/bin/python",
        "args": ["/Users/harrysayers/Developer/claudelife/.mcp/upbank_server.py"],
    },
    {
        "name": "fastmcp-brain",
        "command": "/Users/harrysayers/Developer/claudelife/.mcp/fastmcp-env/bin/python",
        "args": ["/Users/harrysayers/Developer/claudelife/.mcp/fastmcp_server.py"],
    },
]

print("MCP Server Schema Validation")
print("============================")

for server in servers_to_test:
    test_server_schema(
        server["name"],
        server["command"],
        server["args"],
        server.get("env")
    )
