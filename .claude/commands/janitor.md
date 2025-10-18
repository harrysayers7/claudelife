---
created: "2025-10-15 04:12"
updated: "2025-10-18 07:45"
version_history:
  - version: "2.0"
    date: "2025-10-18 07:45"
    changes: "Added MOK HOUSE business operations: Supabase sync, payment verification, Gmail extraction, inbox task creation"
  - version: "1.0"
    date: "2025-10-15 04:18"
    changes: "Initial vault cleanup implementation"
description: |
  Master maintenance command that cleans up the entire claudelife system:
  **Vault Cleanup:**
    - Uses scan-archive-candidates.sh script for instant scanning (<1 second)
    - Moves files with `done: true` or `archive: true` to /99-archive directory
    - Deletes files in /99-archive older than 30 days
  **MOK HOUSE Operations:**
    - Syncs Supabase invoices with Obsidian project files (02-projects/mokhouse)
    - Flags invoices marked [paid] in Supabase but not in Stripe
    - Extracts delivery date updates from Kate/Glenn emails (Gmail MCP)
    - Creates inbox tasks for relevant non-project MOK HOUSE info with [[mokhouse]] relation
performance: |
  Vault cleanup: 30-60x faster than Serena MCP (processes 100+ files in <1 second)
  Business operations: 15-30 seconds total (Supabase + Stripe + Gmail MCPs)
examples:
  - /janitor
  - npm run scan-archive  # Preview vault cleanup only
---

# Master Janitor: Claudelife System Cleanup

This command performs comprehensive cleanup across vault files and MOK HOUSE business operations.

---

# PART A: VAULT CLEANUP

## Phase 1: Scan for Archivable Files

**Performance**: Uses `scan-archive-candidates.sh` script for instant scanning (<1 second vs 30+ seconds).

Run the archive candidate scanner:
```bash
npm run scan-archive:json
```

This returns JSON with:
- `archive_candidates`: All files to move to `/99-archive`
- `done_files`: Files with `done: true` or `Done: true`
- `archive_marked`: Files with `archive: true`
- `old_archive_files`: Files in `/99-archive` older than 30 days with modification dates
- `summary`: Count of each category

Parse the JSON output to get the list of files to process.

**Preview before executing**: User can run `npm run scan-archive` to see human-readable output before running `/janitor`.

## Phase 2: Move Files to Archive

For each file identified:
1. Verify frontmatter contains `done: true` or `archive: true`
2. Create `/99-archive/` directory if it doesn't exist
3. Move file to `/99-archive/` preserving filename
4. If file already exists in archive, append timestamp to filename

Track moved files for summary report.

## Phase 3: Clean Old Archives

The `old_archive_files` array from Phase 1 JSON output already contains files older than 30 days.

For each file in `old_archive_files`:
1. Delete the file
2. Track deleted files with their modification dates for summary report

---

# PART B: MOK HOUSE BUSINESS OPERATIONS

**IMPORTANT**: Use Serena MCP to explore project structure before operations.

## Phase 4: Supabase-Obsidian Invoice Sync

**Purpose**: Ensure invoices in Supabase database are mirrored in Obsidian project files.

### 4.1: Get Active MOK HOUSE Projects

Scan `02-projects/mokhouse/` for active projects:

```javascript
mcp__serena__list_dir({
  relative_path: "02-projects/mokhouse",
  recursive: false
})
```

Filter for:
- Directories with numeric prefixes (e.g., `035-Covermore/`, `036-nintendo/`)
- Exclude `archive/` subdirectories

### 4.2: Get Supabase Invoices

Query Supabase for all MOK HOUSE invoices:

```javascript
mcp__supabase__execute_sql({
  query: `
    SELECT
      invoice_id,
      project_name,
      client_name,
      amount,
      status,
      paid_date,
      created_at
    FROM invoices
    WHERE business = 'MOK HOUSE'
    ORDER BY created_at DESC
  `
})
```

### 4.3: Compare and Flag Discrepancies

For each Supabase invoice:
1. **Check if project exists** in `02-projects/mokhouse/`
2. **Read project file** frontmatter for invoice data
3. **Flag missing projects**: Invoices without corresponding Obsidian projects
4. **Flag status mismatches**: Invoices marked different status in Supabase vs Obsidian

Create summary:
```
📊 Supabase-Obsidian Invoice Sync

✅ Synced Invoices: X
⚠️ Missing Projects (in Supabase, not in Obsidian):
  - Invoice #123: "Covermore Campaign" ($15,000) - No project found

❌ Status Mismatches:
  - Invoice #456 (Nintendo DK): Supabase says "paid", Obsidian says "pending"
```

## Phase 5: Payment Verification (Supabase vs Stripe)

**Purpose**: Flag invoices marked [paid] in Supabase but not reflected in Stripe.

### 5.1: Get Paid Invoices from Supabase

```javascript
mcp__supabase__execute_sql({
  query: `
    SELECT invoice_id, project_name, amount, paid_date
    FROM invoices
    WHERE business = 'MOK HOUSE'
      AND status = 'paid'
    ORDER BY paid_date DESC
  `
})
```

### 5.2: Check Stripe Payment Records

For each paid invoice:

```javascript
mcp__stripe__list_payment_intents({
  limit: 100
})

// Match by amount and date range
// Check if payment exists within ±7 days of paid_date
```

### 5.3: Flag Missing Stripe Payments

Create discrepancy report:
```
💳 Payment Verification (Supabase vs Stripe)

⚠️ Paid in Supabase, Missing in Stripe:
  - Invoice #789: "Covermore Campaign" ($15,000) - Marked paid 2025-10-10, no Stripe payment found
  - Invoice #234: "Nintendo Switch Ad" ($8,500) - Marked paid 2025-09-25, no matching Stripe payment

✅ Verified Payments: X invoices matched in both systems
```

## Phase 6: Gmail Extraction (Kate/Glenn Updates)

**Purpose**: Extract delivery date changes from Kate or Glenn's emails for active MOK HOUSE projects.

### 6.1: Search Gmail for Project Updates

```javascript
mcp__gmail__search_emails({
  query: "from:(kate OR glenn) subject:(delivery OR deadline OR date) after:2025/09/01",
  maxResults: 50
})
```

### 6.2: Parse Email Content for Date Changes

For each email:
1. **Read email body** with `mcp__gmail__read_email`
2. **Extract project references**: Look for project names matching `02-projects/mokhouse/` directories
3. **Identify date mentions**: Parse delivery dates, deadlines, or schedule changes
4. **Match to active projects**: Link email content to specific project files

### 6.3: Confirm Before Updating Project Dates

**USER CONFIRMATION REQUIRED**: Show preview of date changes before applying:

```
📧 Gmail: Delivery Date Updates Found

Proposed Changes (requires confirmation):
1. **035-Covermore**: Update delivery from 2025-11-15 → 2025-11-22
   Source: Email from Kate (2025-10-15) - "Campaign delivery pushed to Nov 22"

2. **036-nintendo**: Update delivery from 2025-10-30 → 2025-11-05
   Source: Email from Glenn (2025-10-16) - "Nintendo wants early delivery by Nov 5"

Apply these changes? (yes/no)
```

If approved:
- Update project file frontmatter with new delivery dates
- Add note: `updated_from_email: "[sender] - [date] - [subject]"`

## Phase 7: Create Inbox Tasks from Non-Project Info

**Purpose**: Extract MOK HOUSE-related info from emails that doesn't match active projects.

### 7.1: Identify Non-Project Emails

From Phase 6 Gmail search results, identify emails that:
- Mention MOK HOUSE or music business
- Don't reference specific active projects
- Contain actionable information or important updates

### 7.2: Create Inbox Task Files

For each relevant email:

```markdown
---
Done: false
type: Task
relation:
  - "[[mokhouse]]"
source: gmail
email_from: "[sender name]"
email_date: "YYYY-MM-DD"
email_subject: "[subject]"
---

# [Task Title from Email Subject]

[Extracted relevant information from email body]

**Action Required**: [What needs to be done based on email content]

**Source**: Email from [sender] on [date]
```

Save to `00-inbox/tasks/[sanitized-subject].md`

Track created tasks for summary.

---

# Phase 8: Master Summary Report

Provide comprehensive cleanup summary:

```
🧹 MASTER JANITOR: Claudelife Cleanup Complete

═══════════════════════════════════════════════
PART A: VAULT CLEANUP
═══════════════════════════════════════════════

📦 Archived Files (moved to /99-archive):
  - task-1.md
  - old-note.md
  Total: X files

🗑️ Deleted Old Archives (>30 days):
  - ancient-file.md (created: 2024-09-10)
  Total: Y files

═══════════════════════════════════════════════
PART B: MOK HOUSE OPERATIONS
═══════════════════════════════════════════════

📊 Supabase-Obsidian Sync:
  ✅ Synced: X invoices
  ⚠️ Missing projects: Y invoices
  ❌ Status mismatches: Z invoices

💳 Payment Verification (Supabase vs Stripe):
  ✅ Verified: X payments
  ⚠️ Missing in Stripe: Y invoices

📧 Gmail Delivery Updates:
  ✅ Date changes applied: X projects
  ℹ️ User declined: Y updates

📝 Inbox Tasks Created:
  ✅ New tasks: X files in 00-inbox/tasks/

═══════════════════════════════════════════════
✨ System cleanup complete! Runtime: [X] seconds
```

# Execution Notes

## Performance
- **Vault cleanup**: <1 second (script-based scanning)
- **Business operations**: 15-30 seconds (MCP calls to Supabase, Stripe, Gmail)
- **Total runtime**: ~20-35 seconds for full master cleanup

## Safety
- **User confirmation required** for delivery date changes from emails
- Preserve file structure (no subdirectories in /99-archive)
- Handle filename conflicts gracefully (append timestamp if needed)
- Skip operations on error, continue processing

## Preview Mode
- User can run `npm run scan-archive` to preview vault cleanup only
- Gmail updates always show preview before applying
- Invoice sync shows discrepancies without modifying files

# Error Handling

- Skip files without proper frontmatter
- Handle permission errors gracefully
- Warn if /99-archive can't be created
- Continue processing even if individual file operations fail
- **MCP connection errors**: Skip phase and note in summary
- **Supabase query failures**: Report error, continue to next phase
- **Gmail API rate limits**: Respect limits, process available results
- **Stripe API errors**: Flag for manual review, continue cleanup

# Dependencies

**Required MCPs**:
- Supabase MCP (`mcp__supabase__*`)
- Stripe MCP (`mcp__stripe__*`)
- Gmail MCP (`mcp__gmail__*`)
- Serena MCP (`mcp__serena__*`)

**Required Scripts**:
- `scripts/scan-archive-candidates.sh` (vault cleanup scanning)

**Project Structure Dependencies**:
- `02-projects/mokhouse/` - Active project directories
- `00-inbox/tasks/` - Task creation destination
- `99-archive/` - Archive destination
