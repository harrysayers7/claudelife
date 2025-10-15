#!/bin/bash

# Post-commit hook to intelligently update Serena's memory
# Uses confidence scoring to auto-update or prompt user

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get changed files from last commit
CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD)
COMMIT_MSG=$(git log -1 --pretty=%B)

# Confidence scoring (0-100)
CONFIDENCE=0

# Flags for what changed
UPDATE_COMMANDS=false
UPDATE_MCP=false
UPDATE_STRUCTURE=false
UPDATE_TECH_STACK=false
NEW_COMMAND=false
MODIFIED_COMMAND=false

# Detect new vs modified commands
if echo "$CHANGED_FILES" | grep -q ".claude/commands/"; then
  UPDATE_COMMANDS=true
  # Check if new file (added in this commit)
  NEW_COMMAND_FILES=$(git diff-tree --no-commit-id --name-status -r HEAD | grep "^A.*\.claude/commands/" | cut -f2)
  if [ -n "$NEW_COMMAND_FILES" ]; then
    NEW_COMMAND=true
    CONFIDENCE=$((CONFIDENCE + 40))  # New command = HIGH confidence
  else
    MODIFIED_COMMAND=true
    CONFIDENCE=$((CONFIDENCE + 25))  # Modified command = MEDIUM confidence
  fi
fi

# Check for MCP config changes
if echo "$CHANGED_FILES" | grep -q ".mcp.json"; then
  UPDATE_MCP=true
  CONFIDENCE=$((CONFIDENCE + 35))  # New MCP server = HIGH confidence
fi

# Check for package.json changes (new scripts)
if echo "$CHANGED_FILES" | grep -q "package.json"; then
  UPDATE_TECH_STACK=true
  # Check if commit message mentions "add" or "new"
  if echo "$COMMIT_MSG" | grep -iq "add\|new"; then
    CONFIDENCE=$((CONFIDENCE + 30))  # New script = HIGH confidence
  else
    CONFIDENCE=$((CONFIDENCE + 10))  # Modified script = LOW confidence
  fi
fi

# Check for structural changes
if echo "$CHANGED_FILES" | grep -q ".claude/agents/\|07-context/\|.serena/"; then
  UPDATE_STRUCTURE=true
  # Agent changes are usually important
  if echo "$CHANGED_FILES" | grep -q ".claude/agents/"; then
    CONFIDENCE=$((CONFIDENCE + 35))  # Agent changes = HIGH confidence
  else
    CONFIDENCE=$((CONFIDENCE + 20))  # Other structure = MEDIUM confidence
  fi
fi

# Check for experimental/temporary changes (reduce confidence)
if echo "$COMMIT_MSG" | grep -iq "wip\|temp\|test\|experiment"; then
  CONFIDENCE=$((CONFIDENCE - 20))
fi

# Check for docs-only changes (reduce confidence)
if echo "$COMMIT_MSG" | grep -iq "^docs:"; then
  if [ "$UPDATE_COMMANDS" = false ] && [ "$UPDATE_MCP" = false ]; then
    CONFIDENCE=$((CONFIDENCE - 15))  # Pure docs = less urgent
  fi
fi

# Ensure confidence is within bounds
if [ $CONFIDENCE -lt 0 ]; then CONFIDENCE=0; fi
if [ $CONFIDENCE -gt 100 ]; then CONFIDENCE=100; fi

# If nothing relevant changed, exit silently
if [ "$UPDATE_COMMANDS" = false ] && [ "$UPDATE_MCP" = false ] && [ "$UPDATE_STRUCTURE" = false ] && [ "$UPDATE_TECH_STACK" = false ]; then
  exit 0
fi

# Decision logic based on confidence
echo ""
echo -e "${BLUE}🔄 Serena Memory Sync Trigger${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Show what changed
if [ "$NEW_COMMAND" = true ]; then
  echo -e "${YELLOW}📝 New slash command(s) created${NC}"
  echo "   Files: $(echo "$NEW_COMMAND_FILES" | tr '\n' ' ')"
elif [ "$MODIFIED_COMMAND" = true ]; then
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

# Execute based on confidence level
if [ $CONFIDENCE -ge 80 ]; then
  # HIGH CONFIDENCE - Auto-update
  echo -e "${GREEN}🤖 Auto-updating Serena memory${NC} (confidence: ${CONFIDENCE}/100)"
  echo ""

  # Create trigger file for Claude Code to detect
  TRIGGER_FILE=".serena-auto-update-trigger.json"
  cat > "$TRIGGER_FILE" << EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "confidence": $CONFIDENCE,
  "changes": {
    "newCommand": $NEW_COMMAND,
    "modifiedCommand": $MODIFIED_COMMAND,
    "mcpConfig": $UPDATE_MCP,
    "techStack": $UPDATE_TECH_STACK,
    "structure": $UPDATE_STRUCTURE
  },
  "files": $(echo "$CHANGED_FILES" | jq -R -s -c 'split("\n") | map(select(length > 0))')
}
EOF

  echo -e "${GREEN}✅ Trigger created:${NC} ${TRIGGER_FILE}"
  echo -e "${BLUE}💡 Next Claude Code session will auto-update Serena's memory${NC}"

elif [ $CONFIDENCE -ge 50 ]; then
  # MEDIUM CONFIDENCE - Recommend
  echo -e "${YELLOW}⚠️  Memory update recommended${NC} (confidence: ${CONFIDENCE}/100)"
  echo ""
  echo -e "${GREEN}💡 Recommendation:${NC} Run ${BLUE}/update-serena-memory --auto${NC} to review and confirm"

else
  # LOW CONFIDENCE - Just mention
  echo -e "${BLUE}📌 Minor changes detected${NC} (confidence: ${CONFIDENCE}/100)"
  echo -e "${NC}   Skipping automatic memory sync${NC}"
  echo -e "${NC}   Run ${BLUE}/update-serena-memory${NC} manually if needed${NC}"
fi

echo ""
exit 0
