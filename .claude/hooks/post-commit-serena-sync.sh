#!/bin/bash

# Post-commit hook to intelligently update Serena's memory
# Only triggers when relevant files are modified

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get changed files from last commit
CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD)

# Flags for what needs updating
UPDATE_COMMANDS=false
UPDATE_MCP=false
UPDATE_STRUCTURE=false
UPDATE_TECH_STACK=false

# Check for command changes
if echo "$CHANGED_FILES" | grep -q ".claude/commands/"; then
  UPDATE_COMMANDS=true
fi

# Check for MCP config changes
if echo "$CHANGED_FILES" | grep -q ".mcp.json"; then
  UPDATE_MCP=true
fi

# Check for package.json changes (new scripts or dependencies)
if echo "$CHANGED_FILES" | grep -q "package.json"; then
  UPDATE_TECH_STACK=true
fi

# Check for structural changes (new directories, major refactoring)
if echo "$CHANGED_FILES" | grep -q ".claude/agents/\|07-context/\|.serena/"; then
  UPDATE_STRUCTURE=true
fi

# If nothing relevant changed, exit silently
if [ "$UPDATE_COMMANDS" = false ] && [ "$UPDATE_MCP" = false ] && [ "$UPDATE_STRUCTURE" = false ] && [ "$UPDATE_TECH_STACK" = false ]; then
  exit 0
fi

# Print what needs updating
echo ""
echo -e "${BLUE}🔄 Serena Memory Sync Trigger${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$UPDATE_COMMANDS" = true ]; then
  echo -e "${YELLOW}📝 Slash commands modified${NC}"
  echo "   Files: $(echo "$CHANGED_FILES" | grep ".claude/commands/" | tr '\n' ' ')"
fi

if [ "$UPDATE_MCP" = true ]; then
  echo -e "${YELLOW}🔌 MCP configuration changed${NC}"
  echo "   File: .mcp.json"
fi

if [ "$UPDATE_TECH_STACK" = true ]; then
  echo -e "${YELLOW}📦 Package dependencies changed${NC}"
  echo "   File: package.json"
fi

if [ "$UPDATE_STRUCTURE" = true ]; then
  echo -e "${YELLOW}🏗️  Project structure modified${NC}"
  echo "   Files: $(echo "$CHANGED_FILES" | grep -E ".claude/agents/|07-context/|.serena/" | tr '\n' ' ')"
fi

echo ""
echo -e "${GREEN}💡 Recommendation:${NC} Update Serena's memory to reflect these changes"
echo -e "   Run: ${BLUE}/update-serena-memory${NC}"
echo ""

exit 0
