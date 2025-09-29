# Move File/Directory with Reference Updates: $ARGUMENTS

Move files or directories and automatically update all references throughout the codebase.

## Usage
- `/move-with-references "old/path" "new/path"`
- `/move-with-references "context/business" "01-areas/business"`
- `/move-with-references "scripts/old-file.js" "utils/new-file.js"`

## What This Command Does

1. **Parse Arguments**: Extract source and destination paths from arguments
2. **Validate Paths**: Check that source exists and destination is valid
3. **Move Files**: Execute the file/directory move operation
4. **Find References**: Search entire codebase for references to old path
5. **Update References**: Replace all old path references with new path
6. **Stage Changes**: Add all changes to git
7. **Show Summary**: Display what was moved and updated

## Steps

### 1. Parse and Validate Arguments
```bash
# Extract source and destination from arguments
SOURCE_PATH="$(echo '$ARGUMENTS' | cut -d' ' -f1 | tr -d '"')"
DEST_PATH="$(echo '$ARGUMENTS' | cut -d' ' -f2 | tr -d '"')"

# Validate source exists
if [ ! -e "$SOURCE_PATH" ]; then
  echo "❌ Source path does not exist: $SOURCE_PATH"
  exit 1
fi

# Check if destination parent directory exists
DEST_DIR="$(dirname "$DEST_PATH")"
if [ ! -d "$DEST_DIR" ]; then
  echo "❌ Destination directory does not exist: $DEST_DIR"
  echo "Create it first or choose a different destination"
  exit 1
fi
```

### 2. Execute Move Operation
```bash
echo "📁 Moving: $SOURCE_PATH → $DEST_PATH"
mv "$SOURCE_PATH" "$DEST_PATH"

if [ $? -eq 0 ]; then
  echo "✅ Move completed successfully"
else
  echo "❌ Move failed"
  exit 1
fi
```

### 3. Find and Update References
```bash
echo "🔍 Searching for references to update..."

# Search for references in common file types
REFERENCES=$(grep -r "$SOURCE_PATH" . \
  --include="*.md" \
  --include="*.json" \
  --include="*.js" \
  --include="*.ts" \
  --include="*.py" \
  --include="*.yaml" \
  --include="*.yml" \
  --exclude-dir=node_modules \
  --exclude-dir=.git \
  --exclude-dir=fastapi_mcp_env \
  2>/dev/null | wc -l)

if [ "$REFERENCES" -gt 0 ]; then
  echo "📝 Found $REFERENCES references to update"

  # Update references in all files
  find . -type f \( \
    -name "*.md" -o \
    -name "*.json" -o \
    -name "*.js" -o \
    -name "*.ts" -o \
    -name "*.py" -o \
    -name "*.yaml" -o \
    -name "*.yml" \
  \) \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./fastapi_mcp_env/*" \
  -exec sed -i '' "s|$SOURCE_PATH|$DEST_PATH|g" {} +

  echo "✅ Updated all references"
else
  echo "ℹ️  No references found to update"
fi
```

### 4. Stage Changes and Show Summary
```bash
echo "📤 Staging all changes..."
git add .

echo ""
echo "📋 Summary:"
echo "  Moved: $SOURCE_PATH → $DEST_PATH"
echo "  Updated: $REFERENCES file references"
echo ""
echo "🎯 Ready to commit with:"
echo "  git commit -m \"refactor: move $SOURCE_PATH to $DEST_PATH and update references\""
```

## Examples

### Move Directory
```bash
/move-with-references "old-folder" "new-structure/folder"
```

### Move File
```bash
/move-with-references "config/old-config.json" "settings/app-config.json"
```

### Move with Spaces (use quotes)
```bash
/move-with-references "My Documents/file.md" "documents/file.md"
```

## Error Handling

- **Source doesn't exist**: Command exits with error message
- **Destination parent missing**: Suggests creating directory first
- **Move fails**: Stops execution and reports error
- **No references found**: Continues successfully, notes no updates needed

## File Types Searched

The command searches and updates references in:
- Markdown files (*.md)
- JSON files (*.json)
- JavaScript/TypeScript (*.js, *.ts)
- Python files (*.py)
- YAML files (*.yaml, *.yml)

## Exclusions

Automatically excludes:
- `node_modules/`
- `.git/`
- `fastapi_mcp_env/`
- Other virtual environments

## Safety Features

- ✅ Validates paths before moving
- ✅ Uses git to track all changes
- ✅ Shows summary before completion
- ✅ Preserves file permissions
- ✅ Handles spaces in paths correctly

## Notes

- Always commit changes after running this command
- Review changes with `git diff` before committing
- Use quotes around paths with spaces
- Command works for both files and directories
- Automatically handles relative and absolute paths
