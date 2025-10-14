#!/bin/bash
# Quickly scan vault for files eligible for archiving
# Usage: ./scripts/scan-archive-candidates.sh [--json]

# Function to extract frontmatter value
get_frontmatter_value() {
    local file="$1"
    local key="$2"
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

# Base directory
BASE_DIR="/Users/harrysayers/Developer/claudelife"

# Directories to scan (exclude /99-archive)
SCAN_DIRS=(
    "$BASE_DIR/00-inbox"
    "$BASE_DIR/00-Bases"
    "$BASE_DIR/01-areas"
    "$BASE_DIR/02-projects"
    "$BASE_DIR/04-resources"
    "$BASE_DIR/07-context"
)

# Arrays to store results
declare -a archive_candidates=()
declare -a done_files=()
declare -a archive_marked=()

# Check if JSON output requested
JSON_OUTPUT=false
if [[ "$1" == "--json" ]]; then
    JSON_OUTPUT=true
fi

# Scan each directory
for dir in "${SCAN_DIRS[@]}"; do
    if [[ ! -d "$dir" ]]; then
        continue
    fi

    # Find all .md files
    while IFS= read -r file; do
        # Skip if file doesn't exist or isn't readable
        [[ ! -f "$file" ]] && continue

        # Extract frontmatter values
        done_value=$(get_frontmatter_value "$file" "done")
        archive_value=$(get_frontmatter_value "$file" "archive")
        Done_value=$(get_frontmatter_value "$file" "Done")  # Alternative capitalization

        # Normalize values to lowercase for comparison
        done_value=$(echo "$done_value" | tr '[:upper:]' '[:lower:]')
        archive_value=$(echo "$archive_value" | tr '[:upper:]' '[:lower:]')
        Done_value=$(echo "$Done_value" | tr '[:upper:]' '[:lower:]')

        # Check if file should be archived
        if [[ "$done_value" == "true" ]] || [[ "$Done_value" == "true" ]]; then
            archive_candidates+=("$file")
            done_files+=("$file")
        elif [[ "$archive_value" == "true" ]]; then
            archive_candidates+=("$file")
            archive_marked+=("$file")
        fi
    done < <(find "$dir" -type f -name "*.md" 2>/dev/null)
done

# Scan /99-archive for old files (>30 days)
ARCHIVE_DIR="$BASE_DIR/99-archive"
declare -a old_archive_files=()

if [[ -d "$ARCHIVE_DIR" ]]; then
    while IFS= read -r file; do
        old_archive_files+=("$file")
    done < <(find "$ARCHIVE_DIR" -type f -name "*.md" -mtime +30 2>/dev/null)
fi

# Output results
if [[ "$JSON_OUTPUT" == true ]]; then
    # JSON output
    echo "{"
    echo "  \"archive_candidates\": ["
    for i in "${!archive_candidates[@]}"; do
        # Make path relative for cleaner output
        rel_path="${archive_candidates[$i]#$BASE_DIR/}"
        echo -n "    \"$rel_path\""
        if [[ $i -lt $((${#archive_candidates[@]} - 1)) ]]; then
            echo ","
        else
            echo ""
        fi
    done
    echo "  ],"
    echo "  \"done_files\": ["
    for i in "${!done_files[@]}"; do
        rel_path="${done_files[$i]#$BASE_DIR/}"
        echo -n "    \"$rel_path\""
        if [[ $i -lt $((${#done_files[@]} - 1)) ]]; then
            echo ","
        else
            echo ""
        fi
    done
    echo "  ],"
    echo "  \"archive_marked\": ["
    for i in "${!archive_marked[@]}"; do
        rel_path="${archive_marked[$i]#$BASE_DIR/}"
        echo -n "    \"$rel_path\""
        if [[ $i -lt $((${#archive_marked[@]} - 1)) ]]; then
            echo ","
        else
            echo ""
        fi
    done
    echo "  ],"
    echo "  \"old_archive_files\": ["
    for i in "${!old_archive_files[@]}"; do
        rel_path="${old_archive_files[$i]#$BASE_DIR/}"
        # Get file age in days
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            file_date=$(stat -f "%Sm" -t "%Y-%m-%d" "$file" 2>/dev/null)
        else
            # Linux
            file_date=$(stat -c "%y" "$file" 2>/dev/null | cut -d' ' -f1)
        fi
        echo -n "    {\"path\": \"$rel_path\", \"modified\": \"$file_date\"}"
        if [[ $i -lt $((${#old_archive_files[@]} - 1)) ]]; then
            echo ","
        else
            echo ""
        fi
        file="${old_archive_files[$i]}"
    done
    echo "  ],"
    echo "  \"summary\": {"
    echo "    \"total_archive_candidates\": ${#archive_candidates[@]},"
    echo "    \"done_files\": ${#done_files[@]},"
    echo "    \"archive_marked\": ${#archive_marked[@]},"
    echo "    \"old_archive_files\": ${#old_archive_files[@]}"
    echo "  }"
    echo "}"
else
    # Human-readable output
    echo "🧹 Archive Candidate Scan Results"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    if [[ ${#archive_candidates[@]} -eq 0 ]]; then
        echo "✨ No files found eligible for archiving"
    else
        echo "📦 Files to Archive (${#archive_candidates[@]} total):"
        echo ""

        if [[ ${#done_files[@]} -gt 0 ]]; then
            echo "  ✓ Done files (${#done_files[@]}):"
            for file in "${done_files[@]}"; do
                rel_path="${file#$BASE_DIR/}"
                echo "    - $rel_path"
            done
            echo ""
        fi

        if [[ ${#archive_marked[@]} -gt 0 ]]; then
            echo "  📁 Archive marked (${#archive_marked[@]}):"
            for file in "${archive_marked[@]}"; do
                rel_path="${file#$BASE_DIR/}"
                echo "    - $rel_path"
            done
            echo ""
        fi
    fi

    if [[ ${#old_archive_files[@]} -gt 0 ]]; then
        echo "🗑️  Old Archive Files (>30 days, ${#old_archive_files[@]} total):"
        for file in "${old_archive_files[@]}"; do
            rel_path="${file#$BASE_DIR/}"
            if [[ "$OSTYPE" == "darwin"* ]]; then
                file_date=$(stat -f "%Sm" -t "%Y-%m-%d" "$file" 2>/dev/null)
            else
                file_date=$(stat -c "%y" "$file" 2>/dev/null | cut -d' ' -f1)
            fi
            echo "    - $rel_path (modified: $file_date)"
        done
        echo ""
    else
        echo "✨ No old files in archive (>30 days)"
        echo ""
    fi

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Summary: ${#archive_candidates[@]} to archive, ${#old_archive_files[@]} to delete"
fi
