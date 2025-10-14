#!/bin/bash

# scan-tasks.sh
# Quickly scan tasks directory for ai-assigned tasks and their status
# Usage: ./scripts/scan-tasks.sh [--json]

TASKS_DIR="/Users/harrysayers/Developer/claudelife/00-inbox/tasks"
JSON_OUTPUT=false

# Check for --json flag
if [[ "$1" == "--json" ]]; then
    JSON_OUTPUT=true
fi

# Function to extract frontmatter value
get_frontmatter_value() {
    local file="$1"
    local key="$2"

    # Extract value from frontmatter (between --- markers)
    awk -v key="$key" '
        BEGIN { in_frontmatter=0; found=0 }
        /^---$/ {
            if (in_frontmatter == 0) {
                in_frontmatter = 1
                next
            } else {
                exit
            }
        }
        in_frontmatter && $0 ~ "^"key":" {
            sub("^"key":[[:space:]]*", "")
            print $0
            found=1
            exit
        }
    ' "$file"
}

# Arrays to store categorized tasks
declare -a eligible_tasks=()
declare -a ignored_tasks=()
declare -a done_tasks=()
declare -a no_ai_assigned=()

# Scan all markdown files
while IFS= read -r -d '' file; do
    filename=$(basename "$file")

    # Get frontmatter values
    ai_assigned=$(get_frontmatter_value "$file" "ai-assigned")
    ai_ignore=$(get_frontmatter_value "$file" "ai-ignore")
    done=$(get_frontmatter_value "$file" "Done")

    # Skip if not ai-assigned
    [[ "$ai_assigned" != "true" ]] && continue

    # Categorize based on status
    if [[ "$done" == "true" ]]; then
        done_tasks+=("$filename")
    elif [[ "$ai_ignore" == "true" ]]; then
        ignored_tasks+=("$filename")
    else
        # This is an eligible task (ai-assigned: true, Done: false, ai-ignore: false or missing)
        eligible_tasks+=("$filename")
    fi

done < <(find "$TASKS_DIR" -maxdepth 1 -name "*.md" -type f -print0)

# Output results
if [[ "$JSON_OUTPUT" == true ]]; then
    # JSON output for programmatic use
    echo "{"
    echo "  \"total_ai_assigned\": $((${#eligible_tasks[@]} + ${#ignored_tasks[@]} + ${#done_tasks[@]})),"
    echo "  \"eligible\": ["
    for i in "${!eligible_tasks[@]}"; do
        echo -n "    \"${eligible_tasks[$i]}\""
        [[ $i -lt $((${#eligible_tasks[@]} - 1)) ]] && echo "," || echo
    done
    echo "  ],"
    echo "  \"ignored\": ["
    for i in "${!ignored_tasks[@]}"; do
        echo -n "    \"${ignored_tasks[$i]}\""
        [[ $i -lt $((${#ignored_tasks[@]} - 1)) ]] && echo "," || echo
    done
    echo "  ],"
    echo "  \"done\": ["
    for i in "${!done_tasks[@]}"; do
        echo -n "    \"${done_tasks[$i]}\""
        [[ $i -lt $((${#done_tasks[@]} - 1)) ]] && echo "," || echo
    done
    echo "  ]"
    echo "}"
else
    # Human-readable output
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 Task Scan Results"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo

    echo "✅ ELIGIBLE TASKS (Ready to Execute): ${#eligible_tasks[@]}"
    if [[ ${#eligible_tasks[@]} -gt 0 ]]; then
        for task in "${eligible_tasks[@]}"; do
            echo "   • $task"
        done
    else
        echo "   (none)"
    fi
    echo

    echo "⊘ IGNORED TASKS (ai-ignore: true): ${#ignored_tasks[@]}"
    if [[ ${#ignored_tasks[@]} -gt 0 ]]; then
        for task in "${ignored_tasks[@]}"; do
            echo "   • $task"
        done
    else
        echo "   (none)"
    fi
    echo

    echo "✓ COMPLETED TASKS (Done: true): ${#done_tasks[@]}"
    if [[ ${#done_tasks[@]} -gt 0 ]]; then
        for task in "${done_tasks[@]}"; do
            echo "   • $task"
        done
    else
        echo "   (none)"
    fi
    echo

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 Summary"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Total AI-assigned tasks: $((${#eligible_tasks[@]} + ${#ignored_tasks[@]} + ${#done_tasks[@]}))"
    echo "Ready to execute: ${#eligible_tasks[@]}"
    echo "Reserved for future: ${#ignored_tasks[@]}"
    echo "Already completed: ${#done_tasks[@]}"
    echo
fi
