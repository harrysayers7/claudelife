#!/bin/bash

# Manual sync script for ai-brain tasks file
# Usage: ./scripts/sync-ai-brain.sh

echo "🔄 Syncing tasks-ai-management.md from ai-brain repo..."

# Create directory if it doesn't exist
mkdir -p context/external

# Download the file
curl -sSL https://raw.githubusercontent.com/harrysayers7/ai-brain/main/ai/context/tasks-ai-management.md \
  -o context/external/tasks-ai-management.md

if [ $? -eq 0 ]; then
  echo "✅ File synced successfully to context/external/tasks-ai-management.md"

  # Check if there are changes
  if git diff --exit-code context/external/tasks-ai-management.md > /dev/null 2>&1; then
    echo "📝 No changes detected"
  else
    echo "📝 Changes detected. You can commit them with:"
    echo "   git add context/external/tasks-ai-management.md"
    echo "   git commit -m '🔄 Sync tasks-ai-management.md from ai-brain repo'"
  fi
else
  echo "❌ Failed to sync file"
  exit 1
fi
