#!/bin/bash

# build-tag-library.sh
# Extracts all existing tags from vault and builds a tag library JSON
# Used by janitor to intelligently suggest tags based on content and context

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# Output file
TAG_LIBRARY=".claude/.tag-library.json"

# Temporary files
TEMP_TAGS=$(mktemp)
TEMP_TAG_CONTEXTS=$(mktemp)

# Extract all tags from markdown files
extract_tags() {
    find . -name "*.md" -type f \
        -not -path "./99-archive/*" \
        -not -path "./.git/*" \
        -not -path "./node_modules/*" \
        -exec grep -h "^tags: \[" {} \; 2>/dev/null \
        | sed 's/tags: \[//g' \
        | sed 's/\].*//g' \
        | tr ',' '\n' \
        | sed 's/^[[:space:]]*//g' \
        | sed 's/[[:space:]]*$//g' \
        | grep -v "^$" \
        | grep -v "{{" \
        | sort -u > "$TEMP_TAGS"
}

# Build tag context (which directories use which tags)
build_tag_contexts() {
    declare -A tag_contexts

    while IFS= read -r tag; do
        # Find files using this tag
        local files
        files=$(grep -r "tags:.*\b$tag\b" --include="*.md" . 2>/dev/null | grep -v "99-archive" | cut -d: -f1 || true)

        # Extract directory patterns
        local dirs
        dirs=$(echo "$files" | grep -oE "(01-areas/[^/]+/[^/]+|02-projects/[^/]+|03-labs|04-resources/[^/]+)" | sort -u)

        # Store context for this tag
        echo "$tag|$dirs" >> "$TEMP_TAG_CONTEXTS"
    done < "$TEMP_TAGS"
}

# Generate JSON library
generate_json() {
    local total_tags
    total_tags=$(wc -l < "$TEMP_TAGS" | tr -d ' ')

    echo "{"
    echo "  \"generated\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\","
    echo "  \"total_tags\": $total_tags,"
    echo "  \"tags\": {"

    local first=true
    while IFS= read -r tag; do
        # Get context directories for this tag
        local contexts
        contexts=$(grep "^$tag|" "$TEMP_TAG_CONTEXTS" | cut -d'|' -f2 | tr '\n' ',' | sed 's/,$//')

        if [[ "$first" == true ]]; then
            first=false
        else
            echo ","
        fi

        echo -n "    \"$tag\": {"
        echo -n "\"contexts\": ["
        if [[ -n "$contexts" ]]; then
            echo "$contexts" | tr ',' '\n' | sed 's/^/"/;s/$/"/' | paste -sd ',' -
        fi
        echo -n "]}"
    done < "$TEMP_TAGS"

    echo ""
    echo "  },"
    echo "  \"context_patterns\": {"
    echo "    \"mokai\": [\"cybersecurity\", \"compliance\", \"IRAP\", \"government\", \"consulting\", \"business\"],"
    echo "    \"mokhouse\": [\"music\", \"production\", \"entertainment\", \"creative\", \"client-work\"],"
    echo "    \"tech\": [\"AI\", \"automation\", \"claude-code\", \"development\", \"tools\"],"
    echo "    \"health-fitness\": [\"gym\", \"diet\", \"medical\", \"wellness\"],"
    echo "    \"p-dev\": [\"learning\", \"mindset\", \"reflection\", \"growth\"],"
    echo "    \"labs\": [\"experiment\", \"POC\", \"prototype\", \"research\", \"testing\"],"
    echo "    \"resources\": [\"reference\", \"documentation\", \"guide\"]"
    echo "  }"
    echo "}"
}

# Main execution
extract_tags
build_tag_contexts
generate_json > "$TAG_LIBRARY"

# Cleanup
rm -f "$TEMP_TAGS" "$TEMP_TAG_CONTEXTS"

# Output summary
total_tags=$(jq -r '.total_tags' "$TAG_LIBRARY" 2>/dev/null || echo "0")
echo "✅ Tag library built: $total_tags unique tags" >&2
echo "📁 Saved to: $TAG_LIBRARY" >&2
