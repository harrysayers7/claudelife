#!/usr/bin/env python3
"""Test script for UpBank MCP server"""

import os
import subprocess
import json
import time

# Set environment variables
os.environ["UPBANK_API_TOKEN"] = "up:yeah:cD6zlJoDh4BjqRjo5Of3FTdMPbJyS6ntLNqjc2yaVqixflXhPTG8qF6nQVQ1UFAe2MRH0lBZ4w4bTvV4RhisPNwHqYarxyTetQbG1xqxCd1LRLXihIea92CVw9pLt2C0"
os.environ["UPBANK_API_BASE_URL"] = "https://api.up.com.au/api/v1"

def test_mcp_command(command):
    """Test an MCP command with the UpBank server"""
    python_path = "./fastmcp-env/bin/python"
    server_path = "./upbank_server.py"

    process = subprocess.Popen(
        [python_path, server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(input=json.dumps(command))

    if stderr:
        print(f"Error: {stderr}")
        return None

    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        print(f"Invalid JSON response: {stdout}")
        return None

def main():
    print("Testing UpBank MCP Server...")

    # Test 1: List available tools
    print("\n1. Testing tools/list...")
    response = test_mcp_command({
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 1
    })

    if response:
        tools = response.get("result", {}).get("tools", [])
        print(f"Available tools: {len(tools)}")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")

    # Test 2: Ping API
    print("\n2. Testing ping_api...")
    response = test_mcp_command({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "ping_api",
            "arguments": {}
        },
        "id": 2
    })

    if response:
        result = response.get("result", {}).get("content", [])
        if result:
            print("API ping successful!")
            print(result[0].get("text", ""))

    # Test 3: Get accounts
    print("\n3. Testing get_accounts...")
    response = test_mcp_command({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_accounts",
            "arguments": {}
        },
        "id": 3
    })

    if response:
        result = response.get("result", {}).get("content", [])
        if result:
            print("Accounts retrieved!")
            print(result[0].get("text", ""))

if __name__ == "__main__":
    main()
