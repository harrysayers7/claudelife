#!/bin/bash
# MOK HOUSE Project Creation Helper
# Creates a new project file with proper metadata structure

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}MOK HOUSE Project Creation${NC}\n"

# Get project details
read -p "Project Name: " project_name
read -p "Customer (ESM/Panda Candy): " customer
read -p "Demo Fee: " demo_fee
read -p "Due Date (YYYY-MM-DD): " due_date
read -p "Date Received (YYYY-MM-DD): " date_received

# Generate filename from project name
filename=$(echo "$project_name" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')
date_prefix=$(date +%y%m%d)
full_filename="${date_prefix}-${filename}.md"

# Determine project number by counting existing projects
project_dir="02-projects/mokhouse"
project_count=$(find "$project_dir" -maxdepth 1 -name "*.md" -type f ! -name "CLAUDE.md" | wc -l)
project_number=$(printf "%03d" $((project_count + 1)))

# Create project file
cat > "$project_dir/$full_filename" << EOF
---
date: "$(date '+%Y-%m-%d %H:%M')"
type: project
relation:
  - "[[mokhouse]]"
project name: "$project_name"
customer: "$customer"
status: "Brief Received"
demo fee: $demo_fee
award fee: 0
due date: "$due_date"
date received: "$date_received"
Date Paid: ""
Invoice #: ""
PO: ""
paid: false
awarded: false
APRA: false
---

# $project_name

**Project #:** $project_number
**Customer:** $customer via MOK Music
**Status:** Brief Received

---

## CREATIVE DIRECTION

### Brief Summary
[Paste brief summary here]

### Tone & Emotion
[Describe desired tone and emotional direction]

### Reference Tracks
[List any reference tracks or sonic inspiration]

### Technical Requirements
- Format: [WAV, MP3, etc.]
- Duration: [Length]
- Stems Required: [Yes/No]
- Deliverables: [Final mix, stems, project files, etc.]

---

## CREATIVE APPROACH

### Concept
[Your creative concept for this project]

### Instrumentation
[Planned instruments and sounds]

### Production Notes
[Technical approach, production techniques]

---

## TIMELINE

- **Brief Received:** $date_received
- **Due Date:** $due_date
- **Internal Review:** [Date before submission]
- **Submission Date:** [Actual submission date]

---

## CLIENT FEEDBACK

### Submission Notes
[Notes from when you submitted]

### Client Response
[Client feedback when received]

---

## FINANCIALS

- **Demo Fee:** \$$demo_fee
- **Award Fee:** \$[If won]
- **Total:** \$[Total amount]
- **Invoice #:** [Invoice number when sent]
- **PO #:** [PO if provided]
- **Payment Date:** [Date paid]

---

## LEARNINGS

### What Worked
[Note successful creative choices]

### What to Improve
[Note areas for improvement]

### Client Preferences
[Document client preferences for future projects]
EOF

echo -e "\n${GREEN}✓ Project created:${NC} $project_dir/$full_filename"
echo -e "${YELLOW}Don't forget to:${NC}"
echo "  1. Paste brief into CREATIVE DIRECTION section"
echo "  2. Update creative approach as you develop concept"
echo "  3. Update status when submitted/awarded/invoiced/paid"
