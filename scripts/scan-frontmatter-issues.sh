#!/bin/bash

# scan-frontmatter-issues.sh
# Fast frontmatter validation for 01-areas/, 02-projects/, 03-labs/, 04-resources/
# Returns JSON with files needing frontmatter fixes

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# Output arrays
MISSING_RELATION=()
WRONG_RELATION=()
MISSING_TYPE=()
MISSING_TAGS=()
MALFORMED_FRONTMATTER=()

# Known entity mapping (directory → expected relation)
declare -A ENTITY_MAP=(
    ["01-areas/business/mokai"]="mokai"
    ["01-areas/business/mokhouse"]="mokhouse"
    ["01-areas/business/accounting"]="accounting"
    ["01-areas/business/safia"]="safia"
    ["01-areas/business/soletrader"]="soletrader"
    ["01-areas/business/trust"]="trust"
    ["01-areas/business/crypto"]="crypto"
    ["01-areas/business/SMSF"]="SMSF"
    ["01-areas/health-fitness"]="health-fitness"
    ["01-areas/p-dev"]="p-dev"
    ["01-areas/tech"]="tech"
    ["02-projects"]="projects"
    ["03-labs"]="labs"
    ["04-resources"]="resources"
)

# Extract relation from file path
get_expected_relation() {
    local filepath="$1"

    # Check each entity pattern
    for dir in "${!ENTITY_MAP[@]}"; do
        if [[ "$filepath" == "$dir"* ]]; then
            echo "${ENTITY_MAP[$dir]}"
            return
        fi
    done

    # Fallback: extract from path
    if [[ "$filepath" =~ 01-areas/business/([^/]+) ]]; then
        echo "${BASH_REMATCH[1]}"
    elif [[ "$filepath" =~ 01-areas/([^/]+) ]]; then
        echo "${BASH_REMATCH[1]}"
    elif [[ "$filepath" =~ 02-projects/([^/]+) ]]; then
        echo "${BASH_REMATCH[1]}"
    elif [[ "$filepath" =~ 03-labs ]]; then
        echo "labs"
    elif [[ "$filepath" =~ 04-resources ]]; then
        echo "resources"
    fi
}

# Check if frontmatter has proper structure
validate_frontmatter() {
    local file="$1"
    local expected_relation="$2"

    # Check if file has frontmatter
    if ! head -1 "$file" | grep -q "^---$"; then
        MALFORMED_FRONTMATTER+=("$file")
        return
    fi

    # Extract frontmatter (between first two ---lines)
    local frontmatter
    frontmatter=$(awk '/^---$/{c++; if(c==2) exit} c==1' "$file")

    # Check for relation field
    if ! echo "$frontmatter" | grep -q "^relation:"; then
        MISSING_RELATION+=("$file|$expected_relation")
        return
    fi

    # Check if relation matches expected
    local actual_relation
    actual_relation=$(echo "$frontmatter" | grep "^relation:" | head -1)

    if ! echo "$actual_relation" | grep -q "\[\[$expected_relation\]\]"; then
        WRONG_RELATION+=("$file|expected:[[$expected_relation]]|actual:$actual_relation")
    fi

    # Check for type field (context files only)
    if [[ "$file" == *"context-"* ]]; then
        if ! echo "$frontmatter" | grep -q "^type:"; then
            MISSING_TYPE+=("$file")
        fi
    fi

    # Check for tags field (all files should have it, even if empty)
    if ! echo "$frontmatter" | grep -q "^tags:"; then
        MISSING_TAGS+=("$file")
    fi
}

# Scan all relevant directories
scan_directory() {
    local dir="$1"

    if [[ ! -d "$dir" ]]; then
        return
    fi

    while IFS= read -r -d '' file; do
        local expected_relation
        expected_relation=$(get_expected_relation "$file")

        if [[ -n "$expected_relation" ]]; then
            validate_frontmatter "$file" "$expected_relation"
        fi
    done < <(find "$dir" -name "*.md" -type f -print0)
}

# Scan all target directories
scan_directory "01-areas"
scan_directory "02-projects"
scan_directory "03-labs"
scan_directory "04-resources"

# Build JSON output
cat << EOF
{
  "missing_relation": [
$(printf '    "%s"' "${MISSING_RELATION[@]}" | paste -sd ',' -)
  ],
  "wrong_relation": [
$(printf '    "%s"' "${WRONG_RELATION[@]}" | paste -sd ',' -)
  ],
  "missing_type": [
$(printf '    "%s"' "${MISSING_TYPE[@]}" | paste -sd ',' -)
  ],
  "missing_tags": [
$(printf '    "%s"' "${MISSING_TAGS[@]}" | paste -sd ',' -)
  ],
  "malformed_frontmatter": [
$(printf '    "%s"' "${MALFORMED_FRONTMATTER[@]}" | paste -sd ',' -)
  ],
  "summary": {
    "missing_relation": ${#MISSING_RELATION[@]},
    "wrong_relation": ${#WRONG_RELATION[@]},
    "missing_type": ${#MISSING_TYPE[@]},
    "missing_tags": ${#MISSING_TAGS[@]},
    "malformed_frontmatter": ${#MALFORMED_FRONTMATTER[@]},
    "total_issues": $((${#MISSING_RELATION[@]} + ${#WRONG_RELATION[@]} + ${#MISSING_TYPE[@]} + ${#MISSING_TAGS[@]} + ${#MALFORMED_FRONTMATTER[@]}))
  }
}
EOF
