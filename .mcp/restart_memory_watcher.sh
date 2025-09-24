#!/bin/bash

# Memory Watcher Restart Script
PROJECT_ROOT="/Users/harrysayers/Developer/claudelife"
MEMORY_WATCHER_SCRIPT="$PROJECT_ROOT/.mcp/memory_watcher.py"

# Check if memory watcher is running
if ! pgrep -f "memory_watcher.py" > /dev/null; then
    echo "$(date): Memory watcher not running, starting..." >> "$PROJECT_ROOT/.mcp/memory_watcher.log"
    cd "$PROJECT_ROOT"
    python3 "$MEMORY_WATCHER_SCRIPT" --project-root="$PROJECT_ROOT" >> "$PROJECT_ROOT/.mcp/memory_watcher.log" 2>&1 &
    echo "$(date): Memory watcher started with PID $!" >> "$PROJECT_ROOT/.mcp/memory_watcher.log"
else
    echo "$(date): Memory watcher already running" >> "$PROJECT_ROOT/.mcp/memory_watcher.log"
fi
