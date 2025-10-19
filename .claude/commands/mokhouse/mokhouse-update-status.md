---
created: "2025-10-16 11:52"
description: |
  Updates MOK HOUSE project status throughout the project lifecycle. Handles status transitions
  from "Brief Received" → "Submitted" → "PO Received" → "Invoiced" → "Complete", plus award
  decisions and metadata updates. Uses Obsidian patch operations for fast, surgical updates.

  Outputs:
    - Updated project frontmatter with new status
    - Updated dates (submitted date, date paid, etc.)
    - Updated award/fee information
    - Confirmation of changes made
examples:
  - /mokhouse-update-status "Mark Repco project as submitted"
  - /mokhouse-update-status "Update Nintendo campaign - awarded with $1500 fee"
  - /mokhouse-update-status "Set Panda Candy project status to PO Received with PO-1234"
---

# Update MOK HOUSE Project Status

**Voice Transcription Note**: When Harry says "mock house" or "mok house", he means **MOK HOUSE** (all caps, two words).

This command handles all project status updates throughout the MOK HOUSE project lifecycle, from submission through completion and award decisions.

## Usage

```bash
/mokhouse-update-status "[project name] status update details"
```

## What This Command Does

**Phase 2: Project Status Management**

Updates project metadata as work progresses through stages:
- **Submission tracking** → When demo is delivered
- **PO receipt** → When purchase order arrives
- **Invoice tracking** → When invoice is created
- **Payment completion** → When payment is received
- **Award decisions** → When award/no-award decision is made

## Interactive Process

When you run this command, I will:

1. **Identify the project:**
   - Which project needs updating?
   - Confirm project file exists in `/02-projects/mokhouse/`

2. **Determine update type:**
   - Status change (Submitted, PO Received, Invoiced, Complete)?
   - Award decision (awarded: true/false)?
   - Fee information (demo fee, award fee)?
   - Date updates (submitted date, date paid)?

3. **Gather required information:**
   - For "Submitted": submitted date, wav file name (if different)
   - For "PO Received": PO number
   - For "Awarded": award fee amount, APRA status
   - For "Complete": date paid

4. **Execute update:**
   - Use Obsidian patch to update specific frontmatter fields
   - Confirm changes made

5. **Provide confirmation:**
   - Show before/after values
   - Next steps in workflow

## Input Requirements

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

Before running, prepare:

1. **Project identification:**
   - Project name or file name
   - Customer name (helps narrow search)

2. **Update details:**
   - New status value OR
   - Award decision + fee OR
   - Date information

## Process

### Step 1: Find Project File

**Use:** `mcp__claudelife-obsidian__list_files` or `mcp__claudelife-obsidian__simple_search`

Search in: `/02-projects/mokhouse/`

Look for:
- Matching project name in filename
- Matching customer name
- Recent files if approximate match

**If multiple matches:**
- Present list with project name, customer, current status
- Ask user to select correct project

### Step 2: Read Current State

**Use:** `mcp__claudelife-obsidian__get_file_contents`

Extract current values:
- Current status
- Existing dates
- Award information
- PO and invoice details

### Step 3: Determine Updates Needed

Based on user request, identify which fields to update:

#### Status: "Submitted"
```yaml
status: "Submitted"
submitted date: "YYYY-MM-DD"
wav name: "[filename if different from template]"
```

#### Status: "PO Received"
```yaml
status: "PO Received"
PO: "[PO number without prefix]"
```

#### Status: "Invoiced"
```yaml
status: "Invoiced"
"Invoice #": "[Stripe invoice number]"
```

#### Status: "Complete"
```yaml
status: "Complete"
paid: true
Date Paid: "YYYY-MM-DD"
```

#### Award Decision (can combine with any status)
```yaml
awarded: true
award fee: [amount]
APRA: [true/false]
```

### Step 4: Apply Updates

**Use:** `mcp__claudelife-obsidian__patch_content`

Update only the specific frontmatter fields that changed.

**Important:**
- Preserve all other frontmatter values
- Use proper YAML formatting
- Dates in YYYY-MM-DD format
- Booleans as true/false (unquoted)
- Numbers unquoted

### Step 5: Confirm Changes

Provide summary:
```
✅ Project Status Updated
────────────────────────────
Project: [project name]
Customer: [customer]

CHANGES MADE:
────────────────────────────
Status: [old] → [new]
[Other fields changed]

CURRENT STATE:
────────────────────────────
Status: [current status]
Submitted: [date if applicable]
PO: [number if applicable]
Invoice: [number if applicable]
Paid: [true/false]
Awarded: [true/false]

NEXT STEPS:
────────────────────────────
[Suggested next action based on current status]
────────────────────────────
```

## Status Workflow

### Typical Project Lifecycle:

```
Brief Received
    ↓
  [Work on demo]
    ↓
Submitted ← /mokhouse-update-status "mark as submitted"
    ↓
  [Client reviews]
    ↓
PO Received ← /mokhouse-update-status "PO received PO-1234"
    ↓
  [Create invoice]
    ↓
Invoiced ← Automatically updated by /mokhouse-create-invoice
    ↓
  [Await payment]
    ↓
Complete ← /mokhouse-mark-paid (or this command)
```

### Award Decisions (can happen anytime):

```
[At any stage]
    ↓
Award Decision Made
    ↓
  [Update project]
    ↓
awarded: true + award fee
  OR
awarded: false
```

## Examples

### Example 1: Mark Project as Submitted

**User request:**
```
"Mark the Repco Q4 project as submitted"
```

**Command execution:**

1. Search for Repco Q4 project file
2. Find: `251016-repco-automotive-q4.md`
3. Read current state: status = "Brief Received"
4. Update frontmatter:
   - status: "Submitted"
   - submitted date: "2025-10-16"
5. Confirm changes
6. Next step: "Awaiting PO from Electric Sheep Music"

### Example 2: Update with Award Information

**User request:**
```
"Nintendo campaign was awarded with $2000 fee, APRA registered"
```

**Command execution:**

1. Search for Nintendo campaign
2. Find project file
3. Update frontmatter:
   - awarded: true
   - award fee: 2000
   - APRA: true
4. Keep existing status unchanged
5. Confirm award recorded

### Example 3: PO Received

**User request:**
```
"PO-0166 received for Panda Candy Provider Care project"
```

**Command execution:**

1. Search for "Panda Candy" + "Provider Care"
2. Find project file
3. Update frontmatter:
   - status: "PO Received"
   - PO: "0166"
4. Next step: "Ready to create invoice with /mokhouse-create-invoice"

### Example 4: Multiple Updates

**User request:**
```
"Repco project: submitted yesterday, awarded with $1500 demo fee, no APRA"
```

**Command execution:**

1. Find Repco project
2. Update multiple fields:
   - status: "Submitted"
   - submitted date: "2025-10-15"
   - awarded: true
   - demo fee: 1500
   - APRA: false
3. Confirm all changes in summary

## Valid Status Values

Only use these exact status strings:

- `"Brief Received"` - Initial state when project created
- `"Submitted"` - Demo has been delivered to client
- `"PO Received"` - Purchase order received, ready for invoicing
- `"Invoiced"` - Invoice created and sent (usually auto-set by invoice command)
- `"Complete"` - Payment received, project closed

## Field Reference

### Status-Related Fields

```yaml
status: "[Status value]"
submitted date: "YYYY-MM-DD"
Date Paid: "YYYY-MM-DD"
```

### PO & Invoice Fields

```yaml
PO: "[Number only, no 'PO-' prefix]"
"Invoice #": "[Stripe invoice number]"
```

### Payment Fields

```yaml
paid: [true/false]
Date Paid: "YYYY-MM-DD"
```

### Award Fields

```yaml
awarded: [true/false]
demo fee: [amount]
award fee: [amount]
APRA: [true/false]
```

### File Naming Field

```yaml
wav name: "[Actual filename if different from template]"
```

## Error Handling

**Project not found:**
- Try alternate search terms
- List recent projects for user selection
- Suggest creating project first if brief is new

**Invalid status value:**
- Show valid status options
- Ask user to clarify intended status

**Missing required information:**
- For "Submitted": Ask for submission date
- For "PO Received": Ask for PO number
- For "Complete": Ask for payment date
- For "Awarded": Ask for fee amount

**Patch operation failed:**
- Verify file still exists
- Check file permissions
- Retry with fresh file read

## Evaluation Criteria

A successful status update should:

1. ✅ **Correct project identified** from user description
2. ✅ **Appropriate fields updated** based on status change
3. ✅ **Valid YAML formatting** preserved in frontmatter
4. ✅ **Date format correct** (YYYY-MM-DD)
5. ✅ **Boolean values proper** (true/false, not quoted)
6. ✅ **Numbers unquoted** in YAML
7. ✅ **Clear confirmation** showing what changed
8. ✅ **Next steps provided** based on new status

## Related Commands

- `/mokhouse-create-project` - Create new project from brief
- `/mokhouse-create-invoice` - Create invoice when PO received (auto-updates status)
- `/mokhouse-mark-paid` - Mark invoice as paid and complete project

---

**Version:** 1.0
**Integration:** Obsidian
**File Location:** `/02-projects/mokhouse/`
