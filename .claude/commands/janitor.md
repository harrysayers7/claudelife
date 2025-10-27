---
created: "2025-10-15 04:12"
updated: "2025-10-23 06:45"
version_history:
  - version: "3.2"
    date: "2025-10-23 06:45"
    changes: "Added Phase 9.9: APRA payment auto-sync from personal_transactions to personal.apra_payments"
  - version: "3.1"
    date: "2025-10-22 06:30"
    changes: "Added Phase 9.8: INDEX.md file maintenance across 01-areas/, 00-inbox/, 02-projects/, 03-labs/, 04-resources/"
  - version: "3.0"
    date: "2025-10-21 16:00"
    changes: "Added frontmatter validation and intelligent tag inference for areas/projects/labs/resources"
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
    - Archives abandoned labs files (with `archive: true` frontmatter)
  **MOK HOUSE Operations:**
    - Syncs Supabase invoices with Obsidian project files (02-projects/mokhouse)
    - Flags invoices marked [paid] in Supabase but not in Stripe
    - Extracts delivery date updates from Kate/Glenn emails (Gmail MCP)
    - Creates inbox tasks for relevant non-project MOK HOUSE info with [[mokhouse]] relation
  **Frontmatter Validation:**
    - Scans 01-areas/, 02-projects/, 03-labs/, 04-resources/ for missing/wrong relations
    - Infers intelligent tags based on file content and existing tag library
    - Fixes malformed frontmatter and adds missing type fields (context files)
    - Only suggests new tags for genuinely new connections (no tag spam)
  **INDEX.md Maintenance:**
    - Recursively scans for INDEX.md files in 01-areas/, 00-inbox/, 02-projects/, 03-labs/, 04-resources/
    - Detects outdated indexes (structure changes, file count mismatches, missing descriptions)
    - Regenerates INDEX.md files with current directory structure and file counts
    - Preserves user-added custom sections while updating metadata
  **APRA Payment Sync:**
    - Auto-syncs APRA royalty transactions from personal_transactions to personal.apra_payments
    - Calculates financial year and cumulative totals
    - Only syncs new APRA payments (prevents duplicates)
performance: |
  Vault cleanup: <1 second (script-based scanning)
  Frontmatter validation: <1 second scanning + 5-10 seconds tag inference
  INDEX.md maintenance: 2-5 seconds (scanning + regeneration)
  Business operations: 15-30 seconds total (Supabase + Stripe + Gmail MCPs)
  Total runtime: ~30-50 seconds for full master cleanup
examples:
  - /janitor
  - npm run scan-archive  # Preview vault cleanup only
  - npm run scan-frontmatter  # Preview frontmatter issues only
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

## Phase 4: Labs Cleanup (03-labs/)

**Purpose**: Archive abandoned experiments and flag stale labs for review.

Scan `03-labs/` for files that need attention:

```bash
find "03-labs" -name "*.md" -type f -exec stat -f "%m %N" {} \;
```

For each file found:
1. **Check frontmatter** for `archive: true` → Move to `99-archive/`
2. **Check last modified** > 90 days without updates → Add to review list
3. Track archived/flagged files for summary report

**Labs Review List Format**:
```markdown
🧪 Stale Labs (>90 days inactive):
- [[03-labs/experiment-name.md]] - Last modified: YYYY-MM-DD
```

**Note**: Labs files do NOT auto-archive based on age alone (unlike other vault sections). Only explicit `archive: true` or manual review triggers archiving.

---

# PART B: MOK HOUSE BUSINESS OPERATIONS

**IMPORTANT**: Use Serena MCP to explore project structure before operations.

## Phase 5: Supabase-Obsidian Invoice Sync

**Purpose**: Ensure invoices in Supabase database are mirrored in Obsidian project files.

### 5.1: Get Active MOK HOUSE Projects

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

### 5.2: Get Supabase Invoices

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

### 5.3: Compare and Flag Discrepancies

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

## Phase 6: Payment Verification (Supabase vs Stripe)

**Purpose**: Flag invoices marked [paid] in Supabase but not reflected in Stripe.

### 6.1: Get Paid Invoices from Supabase

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

### 6.2: Check Stripe Payment Records

For each paid invoice:

```javascript
mcp__stripe__list_payment_intents({
  limit: 100
})

// Match by amount and date range
// Check if payment exists within ±7 days of paid_date
```

### 6.3: Flag Missing Stripe Payments

Create discrepancy report:
```
💳 Payment Verification (Supabase vs Stripe)

⚠️ Paid in Supabase, Missing in Stripe:
  - Invoice #789: "Covermore Campaign" ($15,000) - Marked paid 2025-10-10, no Stripe payment found
  - Invoice #234: "Nintendo Switch Ad" ($8,500) - Marked paid 2025-09-25, no matching Stripe payment

✅ Verified Payments: X invoices matched in both systems
```

## Phase 7: Gmail Extraction (Kate/Glenn Updates)

**Purpose**: Extract delivery date changes from Kate or Glenn's emails for active MOK HOUSE projects.

### 7.1: Search Gmail for Project Updates

```javascript
mcp__gmail__search_emails({
  query: "from:(kate OR glenn) subject:(delivery OR deadline OR date) after:2025/09/01",
  maxResults: 50
})
```

### 7.2: Parse Email Content for Date Changes

For each email:
1. **Read email body** with `mcp__gmail__read_email`
2. **Extract project references**: Look for project names matching `02-projects/mokhouse/` directories
3. **Identify date mentions**: Parse delivery dates, deadlines, or schedule changes
4. **Match to active projects**: Link email content to specific project files

### 7.3: Confirm Before Updating Project Dates

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

## Phase 8: Create Inbox Tasks from Non-Project Info

**Purpose**: Extract MOK HOUSE-related info from emails that doesn't match active projects.

### 8.1: Identify Non-Project Emails

From Phase 6 Gmail search results, identify emails that:
- Mention MOK HOUSE or music business
- Don't reference specific active projects
- Contain actionable information or important updates

### 8.2: Create Inbox Task Files

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

# PART C: FRONTMATTER VALIDATION

**IMPORTANT**: Use fast shell scripts for instant scanning (<1 second for entire vault).

## Phase 9: Frontmatter Validation & Tag Inference

**Purpose**: Ensure all files in 01-areas/, 02-projects/, 03-labs/, 04-resources/ have proper frontmatter with correct `relation` and intelligent tags.

### 9.1: Scan for Frontmatter Issues

**Performance**: Uses `scan-frontmatter-issues.sh` script for instant scanning.

Run the frontmatter scanner:
```bash
npm run scan-frontmatter:json
```

This returns JSON with:
- `missing_relation`: Files without `relation: [[entity]]` field
- `wrong_relation`: Files with incorrect relation for their directory
- `missing_type`: Context files without `type: context`
- `missing_tags`: Files without `tags:` field (even if empty)
- `malformed_frontmatter`: Files missing `---` frontmatter delimiters
- `summary`: Count of each issue type

Expected relation patterns:
- `01-areas/business/mokai/*.md` → `relation: [["[[mokai]]"]]`
- `01-areas/business/mokhouse/*.md` → `relation: [["[[mokhouse]]"]]`
- `01-areas/health-fitness/*.md` → `relation: [["[[health-fitness]]"]]`
- `02-projects/mokhouse/*.md` → `relation: [["[[mokhouse]]"]]` or project-specific
- `03-labs/*.md` → `relation: [["[[labs]]"]]`
- `04-resources/*.md` → `relation: [["[[resources]]"]]` or topic-specific

### 9.2: Build Tag Library (First Run Only)

Build tag library from existing vault tags:
```bash
npm run build-tag-library
```

This creates `.claude/.tag-library.json` with:
- All existing tags extracted from vault
- Context patterns (which directories use which tags)
- Suggested tags per entity (mokai, mokhouse, tech, etc.)

**Note**: Only rebuild when adding many new tags manually. Otherwise, use existing library.

### 9.3: Fix Missing Relations

For files in `missing_relation` array:

1. **Determine expected relation** from file path
2. **Read file** to check if frontmatter exists
3. **Add relation field**:

```yaml
---
relation:
  - "[[entity-name]]"
date created: "existing-date"
date modified: "$(date +"%Y-%m-%d %H:%M")"
---
```

If frontmatter missing entirely, create it:
```yaml
---
relation:
  - "[[entity-name]]"
date created: "$(date +"%Y-%m-%d %H:%M")"
date modified: "$(date +"%Y-%m-%d %H:%M")"
tags: []
---
```

### 9.4: Fix Wrong Relations

For files in `wrong_relation` array:

1. **Parse expected vs actual** from JSON entry
2. **Update relation field** to match directory context
3. **Preserve other frontmatter** fields

Example fix:
```diff
---
-relation: [[wrong-entity]]
+relation: [["[[mokai]]"]]
 date modified: "2025-10-21 15:30"
---
```

### 9.5: Intelligent Tag Inference

**Purpose**: Add relevant tags based on file content, location, and existing tag patterns. Only add new tags if genuine new connections found.

For each file with `missing_tags` or empty `tags: []`:

1. **Load tag library** from `.claude/.tag-library.json`
2. **Determine file context** from path (mokai, mokhouse, tech, etc.)
3. **Get context-appropriate tags** from library
4. **Analyze file content** for keywords matching existing tags
5. **Suggest 2-5 relevant tags** (don't over-tag)

**Tag Suggestion Logic**:
```javascript
// Example for mokai file
const contextTags = tagLibrary.context_patterns.mokai;
// ["cybersecurity", "compliance", "IRAP", "government", "consulting", "business"]

// Read file content
const content = readFile(filePath);

// Find matching tags
const suggestedTags = contextTags.filter(tag => {
  const pattern = new RegExp(`\\b${tag}\\b`, 'i');
  return pattern.test(content);
});

// Limit to 5 most relevant
const finalTags = suggestedTags.slice(0, 5);
```

**Only suggest new tags** if:
- File discusses a genuinely new topic not in tag library
- New tag would be reusable across multiple files
- New tag follows vault's existing tag naming conventions

Example additions:
```yaml
# MOKAI compliance doc
tags: [compliance, IRAP, cybersecurity, government]

# MOK HOUSE creative project
tags: [music, production, creative, client-work]

# Tech AI research
tags: [AI, automation, research, claude-code]

# Labs experiment
tags: [experiment, POC, testing]
```

### 9.6: Confirmation Before Bulk Updates

**USER CONFIRMATION REQUIRED** before applying fixes:

```
🔧 Frontmatter Validation Issues Found

Missing Relations: 42 files
  - 01-areas/business/mokai/: 15 files need relation: [["[[mokai]]"]]
  - 03-labs/: 12 files need relation: [["[[labs]]"]]
  - 04-resources/: 15 files need relation: [["[[resources]]"]]

Wrong Relations: 8 files
  - 01-areas/business/mokhouse/project.md: has [[mokai]], should be [[mokhouse]]

Missing Tags: 67 files
  - Will infer from content + context patterns
  - Example suggestions:
    • mokai files → [compliance, cybersecurity, government]
    • mokhouse files → [music, production, creative]
    • labs files → [experiment, POC, testing]

Apply fixes? (yes/no)
```

If approved:
- Update all frontmatter fields
- Add inferred tags (max 5 per file)
- Log changes to summary report

### 9.7: Summary Report

```
🏷️ FRONTMATTER VALIDATION COMPLETE

✅ Relations Fixed: X files
✅ Tags Added: Y files (Z total tags inferred)
✅ Type Fields Added: N context files
⚠️  Manual Review Needed: M files (malformed frontmatter)

Tag Distribution:
  - mokai: compliance (12), cybersecurity (8), IRAP (5)
  - mokhouse: music (15), production (12), creative (10)
  - tech: AI (20), automation (15), claude-code (8)
  - labs: experiment (10), POC (7), testing (5)

🆕 New Tags Suggested: 0 (all tags from existing library)
```

### 9.8: INDEX.md File Maintenance

**Purpose**: Ensure INDEX.md files are up-to-date with current directory structure across all PARA sections.

**Target Directories**:
- `01-areas/`
- `00-inbox/`
- `02-projects/`
- `03-labs/`
- `04-resources/`

#### 9.8.1: Scan for INDEX.md Files

Recursively find all INDEX.md files in target directories:

```bash
find "01-areas" "00-inbox" "02-projects" "03-labs" "04-resources" -name "INDEX.md" -type f
```

For each INDEX.md found, track its directory path for processing.

#### 9.8.2: Detect Outdated INDEX Files

For each INDEX.md file, check if it needs updating by comparing:

1. **File list changes**: Get current directory contents
   ```javascript
   mcp__serena__list_dir({
     relative_path: "[index-directory-path]",
     recursive: false,
     skip_ignored_files: true
   })
   ```

2. **Parse existing INDEX.md** to extract:
   - Listed subdirectories
   - Listed files
   - File counts mentioned

3. **Compare current vs documented**:
   - New subdirectories not in INDEX.md
   - Removed subdirectories still in INDEX.md
   - File count mismatches
   - Missing section descriptions

4. **Mark as outdated if**:
   - ≥3 new files/directories added
   - Any subdirectory added/removed
   - File counts off by >20%
   - Last updated >30 days ago

#### 9.8.3: Regenerate Outdated INDEX Files

For each outdated INDEX.md:

1. **Analyze directory structure**:
   - List all subdirectories
   - Count files per subdirectory
   - Identify CLAUDE.md files for descriptions
   - Detect special files (README.md, .gitignore, etc.)

2. **Read related context** for descriptions:
   ```javascript
   // If subdirectory has CLAUDE.md
   mcp__serena__find_file({
     file_mask: "CLAUDE.md",
     relative_path: "[subdirectory-path]"
   })
   // Extract description from frontmatter or first paragraph
   ```

3. **Generate INDEX.md structure**:

```markdown
---
date: "YYYY-MM-DD"
type: index
---

# [Directory Name] Index

[Brief description of this section's purpose]

---

## 📋 Directory Structure

### 📁 [Subdirectory Name] (`subdirectory/`)
[Description from CLAUDE.md or inferred from content]

**Files**: X total
**Key Resources**:
- [[file1.md]] - Brief description
- [[file2.md]] - Brief description

### 📁 [Another Subdirectory] (`another/`)
[Description]

**Files**: Y total
**Subdomains**:
- **[subdomain/](subdomain/CLAUDE.md)** - Description

---

## 📚 Navigation

- **Parent**: [[../INDEX.md]] or [[../CLAUDE.md]]
- **Related**: [[related-area/INDEX.md]]

---

**Last Updated:** YYYY-MM-DD
**Files Tracked:** [total-count]
```

4. **Update file**:
   - Preserve custom sections user may have added
   - Update counts and structure
   - Update "Last Updated" timestamp
   - Maintain frontmatter format

#### 9.8.4: Confirmation Before Updates

**USER CONFIRMATION REQUIRED** before regenerating:

```
📑 INDEX.md Files Need Updates

Outdated Indexes: X files

1. 01-areas/business/INDEX.md
   - 3 new subdirectories added (mokai/, mokhouse/, crypto/)
   - File count changed: 12 → 18
   - Last updated: 45 days ago

2. 02-projects/INDEX.md
   - 2 subdirectories removed (archived/)
   - 8 new project files added
   - Missing descriptions for 4 subdirectories

3. 03-labs/INDEX.md
   - 5 new experiments added
   - Last updated: 62 days ago

Regenerate INDEX files? (yes/no)
```

If approved:
- Regenerate INDEX.md files with current structure
- Preserve user-added custom sections
- Update timestamps
- Log changes to summary

#### 9.8.5: INDEX.md Update Summary

```
📑 INDEX.md MAINTENANCE COMPLETE

✅ Up-to-Date: X indexes (no changes needed)
🔄 Regenerated: Y indexes
  - 01-areas/business/INDEX.md (+3 subdirs, +6 files)
  - 02-projects/INDEX.md (-2 subdirs, +8 files)
  - 03-labs/INDEX.md (+5 experiments)

📊 Structure Changes Tracked:
  - New subdirectories: Z total
  - Removed subdirectories: W total
  - File count updates: V indexes

⏱️ Total indexes scanned: N files
```

### 9.9: APRA Payment Sync (Personal Schema)

**Purpose**: Automatically sync APRA royalty transactions from `personal_transactions` to `personal.apra_payments` when detected.

#### 9.9.1: Find New APRA Transactions

Query `personal_transactions` for APRA-related transactions not yet in `apra_payments`:

```javascript
mcp__supabase__execute_sql({
  query: `
    SELECT pt.*
    FROM personal.personal_transactions pt
    LEFT JOIN personal.apra_payments ap ON pt.id = ap.id
    WHERE (
      pt.description ILIKE '%apra%'
      OR pt.message ILIKE '%royalty%'
      OR pt.message ILIKE '%apra%'
    )
    AND ap.id IS NULL
    ORDER BY pt.transaction_date DESC
  `
})
```

This returns only APRA transactions that haven't been synced yet.

#### 9.9.2: Calculate Financial Year & Cumulative Totals

For each new APRA transaction:

1. **Determine financial year** (July 1 - June 30):
   ```javascript
   const transactionDate = new Date(transaction.transaction_date);
   const year = transactionDate.getFullYear();
   const month = transactionDate.getMonth(); // 0-indexed

   // If month is Jul-Dec (6-11), FY is current year to next year
   // If month is Jan-Jun (0-5), FY is previous year to current year
   const fyStart = month >= 6 ? year : year - 1;
   const fyEnd = fyStart + 1;
   const financialYear = `FY${fyStart}-${fyEnd}`;
   ```

2. **Calculate cumulative FY totals** (sum of all APRA payments in same FY up to this transaction):
   ```javascript
   mcp__supabase__execute_sql({
     query: `
       SELECT COALESCE(SUM(amount_cents), 0) as cumulative_cents
       FROM personal.apra_payments
       WHERE financial_year = '${financialYear}'
         AND transaction_date <= '${transaction.transaction_date}'
     `
   })

   const cumulativeCentsFy = previousTotal + transaction.amount_cents;
   const cumulativeAudFy = (cumulativeCentsFy / 100).toFixed(2);
   ```

#### 9.9.3: Insert into apra_payments

For each new APRA transaction:

```javascript
mcp__supabase__execute_sql({
  query: `
    INSERT INTO personal.apra_payments (
      id,
      description,
      message,
      amount_cents,
      amount_aud,
      transaction_date,
      settled_at,
      status,
      personal_category,
      business_category,
      ai_category,
      ai_confidence,
      tags,
      notes,
      financial_year,
      cumulative_cents_fy,
      cumulative_aud_fy,
      created_at
    ) VALUES (
      '${transaction.id}',
      '${transaction.description}',
      '${transaction.message}',
      ${transaction.amount_cents},
      ${transaction.amount_cents / 100},
      '${transaction.transaction_date}',
      '${transaction.settled_at}',
      '${transaction.status}',
      'Income',
      'Royalties',
      ${transaction.ai_category ? `'${transaction.ai_category}'` : 'NULL'},
      ${transaction.ai_confidence || 'NULL'},
      ARRAY['APRA royalty'],
      'Tagged as APRA royalty payment',
      '${financialYear}',
      ${cumulativeCentsFy},
      ${cumulativeAudFy},
      NOW()
    )
    ON CONFLICT (id) DO NOTHING
  `
})
```

**Safety**: `ON CONFLICT DO NOTHING` prevents duplicate inserts if transaction already exists.

#### 9.9.4: APRA Sync Summary

```
💰 APRA PAYMENT SYNC COMPLETE

✅ New APRA Payments Synced: X transactions
📊 Total APRA in personal.apra_payments: Y transactions

Financial Year Breakdown:
  - FY2025-2026: $X,XXX.XX (Y payments)
  - FY2024-2025: $X,XXX.XX (Y payments)

Recent Payments:
  - 2025-10-14: $451.97 (AU Royalty W784794)
  - 2025-09-15: $992.91 (APRA royalty)

⏱️ Next APRA payments will auto-sync when UpBank syncs
```

---

# Phase 10: Master Summary Report

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
PART C: FRONTMATTER VALIDATION
═══════════════════════════════════════════════

🏷️ Frontmatter Fixes:
  ✅ Relations fixed: X files
  ✅ Tags inferred: Y files (Z total tags)
  ✅ Type fields added: N context files
  🧪 Labs files updated: M files
  ⚠️ Manual review needed: P files (malformed frontmatter)

📊 Tag Distribution:
  - mokai: compliance (12), cybersecurity (8), IRAP (5)
  - mokhouse: music (15), production (12), creative (10)
  - tech: AI (20), automation (15), claude-code (8)
  - labs: experiment (10), POC (7), testing (5)

📑 INDEX.md Maintenance:
  ✅ Up-to-date: X indexes
  🔄 Regenerated: Y indexes
  📊 Structure changes: Z subdirectories updated

💰 APRA Payment Sync:
  ✅ New payments synced: X transactions
  📊 Total APRA tracked: Y payments ($Z,ZZZ.ZZ)
  💵 Current FY total: $X,XXX.XX

═══════════════════════════════════════════════
✨ System cleanup complete! Runtime: [X] seconds
```

# Execution Notes

## Performance
- **Vault cleanup**: <1 second (script-based scanning)
- **Frontmatter validation**: <1 second (script-based scanning)
- **Tag inference**: 5-10 seconds (content analysis per file)
- **INDEX.md maintenance**: 2-5 seconds (scanning + regeneration)
- **Business operations**: 15-30 seconds (MCP calls to Supabase, Stripe, Gmail)
- **Total runtime**: ~30-50 seconds for full master cleanup

## Safety
- **User confirmation required** for:
  - Delivery date changes from emails
  - Bulk frontmatter updates
  - Tag additions to multiple files
- Preserve file structure (no subdirectories in /99-archive)
- Handle filename conflicts gracefully (append timestamp if needed)
- Skip operations on error, continue processing
- Preserve existing frontmatter when adding missing fields

## Preview Mode
- User can run `npm run scan-archive` to preview vault cleanup only
- User can run `npm run scan-frontmatter` to preview frontmatter issues
- Gmail updates always show preview before applying
- Invoice sync shows discrepancies without modifying files
- Tag suggestions shown before applying

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
- `scripts/scan-frontmatter-issues.sh` (frontmatter validation scanning)
- `scripts/build-tag-library.sh` (tag library generation)

**Generated Files**:
- `.claude/.tag-library.json` (tag inference library, auto-generated)

**Project Structure Dependencies**:
- `01-areas/` - Areas with expected relations
- `02-projects/mokhouse/` - Active project directories
- `03-labs/` - Labs experiments
- `04-resources/` - Resources with expected relations
- `00-inbox/tasks/` - Task creation destination
- `99-archive/` - Archive destination
