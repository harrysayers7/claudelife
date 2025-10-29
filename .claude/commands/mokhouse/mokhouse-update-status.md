---
created: "2025-10-16 11:52"
updated: "2025-10-28 16:45"
version: "1.2"
version_history:
  - version: "1.2"
    date: "2025-10-28 16:45"
    changes: "Added CRITICAL RULE: Always set demo fee to $0 when marking project as awarded (demo absorbed into award fee)"
  - version: "1.1"
    date: "2025-10-27 14:30"
    changes: "Updated valid status values to match Supabase constraint: 'submitted', 'awaiting PO', 'sent', 'paid'; Clarified Obsidian-only updates vs Supabase status management"
  - version: "1.0"
    date: "2025-10-16 11:52"
    changes: "Initial command creation"
description: |
  Updates MOK HOUSE project status in Obsidian throughout the project lifecycle. Handles status transitions
  from `'submitted'` → `'awaiting PO'` → `'sent'` → `'paid'`, plus award decisions and metadata updates.
  Uses Obsidian patch operations for fast, surgical updates. Note: Supabase status is managed by
  `/mokhouse-create-invoice` (sets to 'sent') and `/mokhouse-mark-paid` (sets to 'paid').

  Outputs:
    - Updated project frontmatter with new status
    - Updated dates (submitted date, date paid, etc.)
    - Updated award/fee information
    - Confirmation of changes made
examples:
  - /mokhouse-update-status "Mark Repco project as submitted"
  - /mokhouse-update-status "Update Nintendo campaign - mark as awaiting PO"
  - /mokhouse-update-status "Panda Candy project awarded with $1500 fee"
---

# Update MOK HOUSE Project Status

**Voice Transcription Note**: When Harry says "mock house" or "mok house", he means **MOK HOUSE** (all caps, two words).

This command handles all project status updates throughout the MOK HOUSE project lifecycle, from submission through completion and award decisions.

## Usage

```bash
/mokhouse-update-status "[project name] status update details"
```

## What This Command Does

**Phase 2: Project Status Management (Obsidian)**

Updates Obsidian project metadata as work progresses through stages:
- **Status: `'submitted'`** → When demo is delivered/project submitted
- **Status: `'awaiting PO'`** → When waiting for purchase order
- **Status: `'sent'`** → When invoice is sent (Supabase auto-updates this)
- **Status: `'paid'`** → When payment is received (Supabase auto-updates this)
- **Award decisions** → When award/no-award decision is made

## Interactive Process

When you run this command, I will:

1. **Identify the project:**
   - Which project needs updating?
   - Confirm project file exists in `/02-projects/mokhouse/`

2. **Determine update type:**
   - Status change (submitted, awaiting PO, sent, paid)?
   - Award decision (awarded: true/false)?
   - Fee information (demo fee, award fee)?
   - Date updates (submitted date, date paid)?

3. **Gather required information:**
   - For "submitted": submitted date, wav file name (if different)
   - For "awaiting PO": PO number
   - For "Awarded": award fee amount, APRA status
   - For "paid": date paid

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

#### Status: "submitted"
```yaml
status: "submitted"
submitted date: "YYYY-MM-DD"
wav name: "[filename if different from template]"
```

#### Status: "awaiting PO"
```yaml
status: "awaiting PO"
PO: "[PO number without prefix]"
```

#### Status: "sent"
```yaml
status: "sent"
"Invoice #": "[Stripe invoice number]"
```

#### Status: "paid"
```yaml
status: "paid"
paid: true
Date Paid: "YYYY-MM-DD"
```

#### Award Decision (can combine with any status)
```yaml
awarded: true
award fee: [amount]
demo fee: 0  # IMPORTANT: Always set to 0 when awarded (demo absorbed into award fee)
APRA: [true/false]
```

**CRITICAL RULE**: When marking a project as `awarded: true`, **ALWAYS** set `demo fee: 0` because the demo fee is absorbed into the award fee. The invoice should only include the award fee amount.

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
[Project created]
    ↓
  [Work on demo]
    ↓
submitted ← /mokhouse-update-status "mark as submitted"
    ↓
  [Client reviews]
    ↓
awaiting PO ← /mokhouse-update-status "awaiting PO"
    ↓
  [Create invoice]
    ↓
sent ← Automatically updated by /mokhouse-create-invoice
    ↓
  [Await payment]
    ↓
paid ← /mokhouse-mark-paid (or this command)
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
3. Read current state: status = "current"
4. Update frontmatter:
   - status: "submitted"
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
   - demo fee: 0 (absorbed into award fee)
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
   - status: "awaiting PO"
   - PO: "0166"
4. Next step: "Ready to create invoice with /mokhouse-create-invoice"

### Example 4: Multiple Updates

**User request:**
```
"Repco project: submitted yesterday, awarded with $1500 award fee, no APRA"
```

**Command execution:**

1. Find Repco project
2. Update multiple fields:
   - status: "submitted"
   - submitted date: "2025-10-15"
   - awarded: true
   - award fee: 1500
   - demo fee: 0 (absorbed into award fee)
   - APRA: false
3. Confirm all changes in summary

## Valid Status Values

Only use these exact status strings (must match Supabase constraint):

- `"current"` - Initial state when project created (not commonly used in Obsidian)
- `"submitted"` - Demo has been delivered to client
- `"awaiting PO"` - Purchase order awaited, ready to update after PO received
- `"sent"` - Invoice created and sent (auto-set by /mokhouse-create-invoice)
- `"paid"` - Payment received, project closed (auto-set by /mokhouse-mark-paid)

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
- For "submitted": Ask for submission date
- For "awaiting PO": Ask for PO number
- For "paid": Ask for payment date
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
