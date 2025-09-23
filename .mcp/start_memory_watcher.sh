#!/bin/bash

# Memory Watcher Startup Script
# Runs the file watcher in background and manages the process

PROJECT_ROOT="/Users/harrysayers/Developer/claudelife"
WATCHER_SCRIPT="$PROJECT_ROOT/.mcp/memory_watcher.py"
PID_FILE="$PROJECT_ROOT/.mcp/memory_watcher.pid"

case "$1" in
    start)
        if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            echo "🔍 Memory watcher is already running (PID: $(cat "$PID_FILE"))"
            exit 1
        fi

        echo "🚀 Starting memory watcher..."
        nohup "$WATCHER_SCRIPT" > "$PROJECT_ROOT/.mcp/memory_watcher.log" 2>&1 &
        echo $! > "$PID_FILE"
        echo "✅ Memory watcher started (PID: $!)"
        echo "📋 Log: tail -f $PROJECT_ROOT/.mcp/memory_watcher.log"
        ;;

    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                echo "🛑 Stopping memory watcher (PID: $PID)..."
                kill "$PID"
                rm -f "$PID_FILE"
                echo "✅ Memory watcher stopped"
            else
                echo "❌ Memory watcher not running"
                rm -f "$PID_FILE"
            fi
        else
            echo "❌ Memory watcher not running (no PID file)"
        fi
        ;;

    status)
        if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            echo "✅ Memory watcher is running (PID: $(cat "$PID_FILE"))"
            echo "📋 Log: tail -f $PROJECT_ROOT/.mcp/memory_watcher.log"
        else
            echo "❌ Memory watcher is not running"
        fi
        ;;

    restart)
        "$0" stop
        sleep 2
        "$0" start
        ;;

    logs)
        if [ -f "$PROJECT_ROOT/.mcp/memory_watcher.log" ]; then
            tail -f "$PROJECT_ROOT/.mcp/memory_watcher.log"
        else
            echo "❌ No log file found"
        fi
        ;;

    *)
        echo "Usage: $0 {start|stop|status|restart|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the memory watcher in background"
        echo "  stop    - Stop the memory watcher"
        echo "  status  - Check if memory watcher is running"
        echo "  restart - Restart the memory watcher"
        echo "  logs    - Show live logs"
        exit 1
        ;;
esac
