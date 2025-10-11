#!/bin/bash
# MOKAI Agent Knowledge Staleness Checker
# Verifies if mokai-business-assistant agent knowledge is current with Operations Guide

set -e

# File paths
AGENT_FILE=".claude/agents/mokai-business-assistant.md"
OPS_GUIDE="01-areas/business/mokai/docs/research/📘 - OPERATIONS GUIDE.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if files exist
if [ ! -f "$AGENT_FILE" ]; then
    echo -e "${RED}❌ Error: Agent file not found: $AGENT_FILE${NC}"
    exit 1
fi

if [ ! -f "$OPS_GUIDE" ]; then
    echo -e "${RED}❌ Error: Operations Guide not found: $OPS_GUIDE${NC}"
    exit 1
fi

# Extract last synced date from agent file
AGENT_SYNC=$(grep "Last Synced" "$AGENT_FILE" | sed 's/.*: //' | tr -d '**')

# Get Operations Guide last modified date
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    OPS_MODIFIED=$(stat -f "%Sm" -t "%Y-%m-%d" "$OPS_GUIDE")
else
    # Linux
    OPS_MODIFIED=$(stat -c "%y" "$OPS_GUIDE" | cut -d' ' -f1)
fi

# Calculate days since last sync
CURRENT_DATE=$(date +%Y-%m-%d)
DAYS_OLD=$(( ( $(date -j -f "%Y-%m-%d" "$CURRENT_DATE" +%s) - $(date -j -f "%Y-%m-%d" "$AGENT_SYNC" +%s) ) / 86400 ))

echo "================================================"
echo "  MOKAI Agent Knowledge Staleness Check"
echo "================================================"
echo ""
echo "Agent Last Synced:     $AGENT_SYNC"
echo "Operations Guide Modified: $OPS_MODIFIED"
echo "Knowledge Age:         $DAYS_OLD days"
echo ""

# Check if Operations Guide modified after last sync
if [[ "$OPS_MODIFIED" > "$AGENT_SYNC" ]]; then
    echo -e "${RED}⚠️  WARNING: MOKAI Agent Knowledge is STALE!${NC}"
    echo ""
    echo "Operations Guide has been updated since agent's last sync."
    echo ""
    echo -e "${YELLOW}Recommended Action:${NC}"
    echo "  Run: /business:mokai:update-mokai-context"
    echo ""
    exit 1
elif [ "$DAYS_OLD" -gt 30 ]; then
    echo -e "${YELLOW}⚠️  NOTICE: Agent knowledge is >30 days old${NC}"
    echo ""
    echo "Consider refreshing agent knowledge even if Operations Guide hasn't changed."
    echo ""
    echo -e "${YELLOW}Recommended Action:${NC}"
    echo "  Run: /business:mokai:update-mokai-context"
    echo ""
    exit 2
else
    echo -e "${GREEN}✅ MOKAI Agent knowledge is CURRENT${NC}"
    echo ""
    echo "No action needed at this time."
    echo ""
    exit 0
fi
