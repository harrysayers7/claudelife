#!/bin/bash

# Setup weekly memory maintenance cron job
# Runs every Sunday at 2 AM

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Cron job command
CRON_CMD="0 2 * * 0 cd $PROJECT_DIR && npm run memory-maintenance >> $PROJECT_DIR/logs/memory-maintenance.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "memory-maintenance"; then
  echo "✅ Memory maintenance cron job already exists"
  echo "Current schedule: Every Sunday at 2 AM"
  exit 0
fi

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_DIR/logs"

# Add cron job
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

echo "✅ Memory maintenance cron job installed"
echo "Schedule: Every Sunday at 2 AM"
echo "Logs: $PROJECT_DIR/logs/memory-maintenance.log"
echo ""
echo "To verify: crontab -l"
echo "To remove: crontab -e (then delete the memory-maintenance line)"
