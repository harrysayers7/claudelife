#!/bin/bash

# Post-System-Completion Hook
# Suggests documentation when substantial features/systems are completed

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get commit details
CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD)
COMMIT_MSG=$(git log -1 --pretty=%B)
ADDED_FILES=$(git diff-tree --no-commit-id --name-status -r HEAD | grep "^A" | wc -l | tr -d ' ')

# Confidence scoring for documentation suggestion (0-100)
DOC_CONFIDENCE=0

# Check for feature completion indicators
if echo "$COMMIT_MSG" | grep -iq "feat:.*complete\|feat:.*implement\|feat:.*add.*system"; then
  DOC_CONFIDENCE=$((DOC_CONFIDENCE + 30))
fi

# Check for substantial code additions (5+ new files)
if [ "$ADDED_FILES" -ge 5 ]; then
  DOC_CONFIDENCE=$((DOC_CONFIDENCE + 40))
elif [ "$ADDED_FILES" -ge 3 ]; then
  DOC_CONFIDENCE=$((DOC_CONFIDENCE + 20))
fi

# Check for system-related files
if echo "$CHANGED_FILES" | grep -qE ".github/workflows|mcp.*server|automation|integration"; then
  DOC_CONFIDENCE=$((DOC_CONFIDENCE + 25))
fi

# Check for task completion
if echo "$COMMIT_MSG" | grep -iq "task.*complete\|mark.*done\|finished.*task"; then
  DOC_CONFIDENCE=$((DOC_CONFIDENCE + 15))
fi

# Check for configuration files (indicates new system)
if echo "$CHANGED_FILES" | grep -qE "\.mcp\.json|package\.json|requirements\.txt"; then
  DOC_CONFIDENCE=$((DOC_CONFIDENCE + 15))
fi

# Reduce confidence for minor changes
if echo "$COMMIT_MSG" | grep -iq "^fix:\|^refactor:\|^chore:"; then
  DOC_CONFIDENCE=$((DOC_CONFIDENCE - 30))
fi

# Ensure bounds
if [ $DOC_CONFIDENCE -lt 0 ]; then DOC_CONFIDENCE=0; fi
if [ $DOC_CONFIDENCE -gt 100 ]; then DOC_CONFIDENCE=100; fi

# Only suggest if confidence is meaningful
if [ $DOC_CONFIDENCE -lt 50 ]; then
  exit 0
fi

# Show documentation suggestion
echo ""
echo -e "${BLUE}📚 System Documentation Opportunity${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $DOC_CONFIDENCE -ge 80 ]; then
  echo -e "${GREEN}HIGH confidence${NC} (${DOC_CONFIDENCE}/100) - Substantial system completion detected"
elif [ $DOC_CONFIDENCE -ge 65 ]; then
  echo -e "${YELLOW}MEDIUM confidence${NC} (${DOC_CONFIDENCE}/100) - Feature addition detected"
else
  echo -e "${CYAN}LOW-MEDIUM confidence${NC} (${DOC_CONFIDENCE}/100) - Consider if documentation needed"
fi

echo ""
echo -e "${YELLOW}📊 Analysis:${NC}"
echo "   New files added: $ADDED_FILES"

if echo "$CHANGED_FILES" | grep -qE ".github/workflows"; then
  echo "   System type: GitHub Actions automation"
fi
if echo "$CHANGED_FILES" | grep -qE "mcp.*server|\.mcp\.json"; then
  echo "   System type: MCP server"
fi
if echo "$CHANGED_FILES" | grep -qE "scripts/.*\.js|scripts/.*\.py"; then
  echo "   System type: Utility scripts"
fi

echo ""
echo -e "${GREEN}💡 Suggested Action:${NC}"
echo -e "   ${BLUE}/document-system \"[system name]\"${NC}"
echo ""
echo -e "${CYAN}Why document now?${NC}"
echo "   ✓ Fresh in your mind - details are clear"
echo "   ✓ Future LLMs can understand what you built"
echo "   ✓ Easy handoff to collaborators or future you"
echo "   ✓ Maintains institutional knowledge"
echo ""
echo -e "${YELLOW}Auto-detection available:${NC} /document-system will analyze code and suggest appropriate location"
echo ""

exit 0
