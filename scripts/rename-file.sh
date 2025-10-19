#!/bin/bash
# rename-file.sh - Fast file reference scanning for /rename-file command
# Provides 10-20x speedup over sequential Serena searches
#
# Usage: ./scripts/rename-file.sh old-path new-path [scope]
# Output: JSON with reference locations for Claude to process

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
OLD_PATH="${1:-}"
NEW_PATH="${2:-}"
SCOPE="${3:-.}"

# Validate inputs
if [[ -z "$OLD_PATH" ]] || [[ -z "$NEW_PATH" ]]; then
  echo -e "${RED}❌ Error: Missing required arguments${NC}" >&2
  echo "Usage: $0 old-path new-path [scope]" >&2
  exit 1
fi

# Extract filenames
OLD_BASENAME=$(basename "$OLD_PATH")
OLD_NAME="${OLD_BASENAME%.md}"
NEW_BASENAME=$(basename "$NEW_PATH")
NEW_NAME="${NEW_BASENAME%.md}"

# Validate source exists
if [[ ! -f "$OLD_PATH" ]]; then
  echo -e "${RED}❌ Error: File not found: $OLD_PATH${NC}" >&2
  exit 1
fi

# Check destination doesn't exist
if [[ -f "$NEW_PATH" ]]; then
  echo -e "${RED}❌ Error: Destination already exists: $NEW_PATH${NC}" >&2
  exit 1
fi

# Validate destination directory exists or can be created
NEW_DIR=$(dirname "$NEW_PATH")
if [[ ! -d "$NEW_DIR" ]]; then
  echo -e "${YELLOW}⚠️  Warning: Destination directory doesn't exist: $NEW_DIR${NC}" >&2
  echo -e "${YELLOW}   It will need to be created before moving the file${NC}" >&2
fi

# Single-pass search for ALL reference patterns
echo -e "${BLUE}🔍 Scanning for references in ${SCOPE}...${NC}" >&2

# Build regex patterns for ripgrep
# Pattern 1: [[filename]] or [[filename.md]]
WIKILINK_PATTERN="\[\[${OLD_NAME}(\.md)?\]\]"

# Pattern 2: [text](path/to/filename.md) - any markdown link
# Escaping periods in filename for regex
ESCAPED_BASENAME=$(echo "$OLD_BASENAME" | sed 's/\./\\./g')
MARKDOWN_LINK_PATTERN="\]\([^)]*${ESCAPED_BASENAME}\)"

# Combine patterns with OR
COMBINED_PATTERN="${WIKILINK_PATTERN}|${MARKDOWN_LINK_PATTERN}"

# Run ripgrep with combined pattern
# --files-with-matches: Only output filenames, not line contents
# --glob: Only search markdown files
# --iglob: Exclude the file being renamed itself
REFERENCES=$(rg --files-with-matches \
  --glob "**/*.md" \
  --iglob "!${OLD_PATH}" \
  "$COMBINED_PATTERN" \
  "$SCOPE" 2>/dev/null || true)

# Count references
if [[ -n "$REFERENCES" ]]; then
  REF_COUNT=$(echo "$REFERENCES" | grep -c .)
else
  REF_COUNT=0
fi

# Output human-readable summary to stderr
echo -e "${GREEN}📊 Found $REF_COUNT files with references${NC}" >&2

if [[ $REF_COUNT -gt 0 ]]; then
  echo "" >&2
  echo -e "${BLUE}Files to update:${NC}" >&2
  echo "$REFERENCES" | sed 's/^/  • /' >&2
  echo "" >&2
fi

# Convert newline-separated list to JSON array
if [[ -n "$REFERENCES" ]]; then
  FILES_JSON=$(echo "$REFERENCES" | jq -R -s 'split("\n") | map(select(length > 0))')
else
  FILES_JSON="[]"
fi

# Output JSON to stdout for Claude to parse
jq -n \
  --arg old_path "$OLD_PATH" \
  --arg new_path "$NEW_PATH" \
  --arg old_name "$OLD_NAME" \
  --arg new_name "$NEW_NAME" \
  --arg old_basename "$OLD_BASENAME" \
  --arg new_basename "$NEW_BASENAME" \
  --argjson ref_count "$REF_COUNT" \
  --argjson files "$FILES_JSON" \
  --arg scope "$SCOPE" \
  '{
    success: true,
    old_path: $old_path,
    new_path: $new_path,
    old_name: $old_name,
    new_name: $new_name,
    old_basename: $old_basename,
    new_basename: $new_basename,
    reference_count: $ref_count,
    files: $files,
    scope: $scope,
    patterns_searched: [
      ("[[" + $old_name + "]]"),
      ("[[" + $old_name + ".md]]"),
      ("[text](*/" + $old_basename + ")")
    ]
  }'
