#!/bin/bash
# Cache MOKAI inbox tasks for faster /mokai-status

VAULT_PATH="/Users/harrysayers/Developer/claudelife"
CACHE_FILE="$VAULT_PATH/01-areas/business/mokai/.mokai-inbox-cache.json"
INBOX_PATH="$VAULT_PATH/00-inbox/tasks"

# Find all MOKAI-related tasks
MOKAI_TASKS=$(find "$INBOX_PATH" -name "*.md" -type f -print0 | while IFS= read -r -d '' file; do
    # Check if file has mokai relation (simple case-insensitive check)
    if grep -qi "mokai" "$file" 2>/dev/null; then
        filename=$(basename "$file" .md)
        done_status=$(grep "^Done:" "$file" 2>/dev/null | awk '{print $2}' || echo "false")
        priority=$(grep "^priority:" "$file" 2>/dev/null | awk '{print $2}' | tr -d '\n' || echo "")

        # Escape filename for JSON (trim newlines)
        escaped_filename=$(echo -n "$filename" | jq -Rs '.')
        escaped_path=$(echo -n "$file" | jq -Rs '.')
        escaped_priority=$(echo -n "$priority" | jq -Rs '.')

        # Output JSON object
        cat <<EOF
{
  "title": $escaped_filename,
  "done": $done_status,
  "priority": $escaped_priority,
  "path": $escaped_path
}
EOF
    fi
done | jq -s '.')

# Write cache
echo "$MOKAI_TASKS" > "$CACHE_FILE"

TASK_COUNT=$(echo "$MOKAI_TASKS" | jq 'length')
echo "✓ Cached $TASK_COUNT MOKAI tasks" >&2
