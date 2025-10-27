---
Done: true
today: true
follow up: false
this week: false
back burner: false
ASAP: true
type: Task
status: completed
relation:
description: Provide business context for Supabase tables so /master-supabase command understands what each table is for
effort: 15 minutes
ai-assigned: true
ai-ignore: false
ai-ask: false
priority: high
agent: claude
slash-command: /master-supabase
---

# Supabase Table Business Context - Questionnaire

Claude needs to understand the business purpose of each Supabase table to provide better context when you run `/master-supabase`.

Currently, the documentation is outdated and doesn't explain which tables belong to which business entity (MOK HOUSE, MOKAI, Harrison personal).

## Questions to Answer

### 1. Entity Mapping

**Current entities in Supabase (from live query):**
We have 3 entities. Please confirm which is which:
I don't really know. Don't they have UUID numbers in the entities table? ________________

### 2. Core Financial Tables

**invoices** (31 rows):
- [ ] MOK HOUSE only
- [ ] MOKAI only
- [ ] Harrison personal only
- [x] Shared across all entities
- Notes: invoices before repco are Harrison or my sole trader abn and from repco until now are all mh

**transactions** (1 row):
I think this table could possibly be deleted.

**contacts** (3 rows):
- [ ] MOK HOUSE clients/vendors
- [ ] MOKAI clients/vendors
- [x] Shared across entities
- [ ] Personal contacts
- Notes: mok house and perosnal can share but mokai is separated________________________________________________________________

### 3. Personal Finance Tables

**personal_transactions** (261 rows):
- Purpose: trackong my personal transactions________________________________________________________________
- Source: UpBank personal account? Which account? ________________________
- Entity owner: Harrison Sayers and soletrader ABN___________________________________________________________
- Business vs Personal: ___________________________________________________MIX

**personal_accounts** (4 rows):
- Purpose: These are various spending accounts within my UpBank. The main account is called spending. The ones called Greece and crypto are just accounts, more savings accounts, not transactions.  ___________________________________________
- Are these all your UpBank accounts? ____________________________________
- Entity owner:

### 4. Tax & Compliance Tables

**trust_distributions** (0 rows):
- Purpose: I think we can ignore this one for now. I don't think it's set up properly. ________________________________________________________________
- Which trust entity? _____________________________________________________
- Used for: _______________________________________________________________

**crypto_assets** (0 rows):
- [ ] MOK HOUSE crypto
- [ ] MOKAI crypto
- [ ] Harrison personal crypto
- [ ] Not used yet
- Notes: NOT USED YET IGNORE________________________________________________________________

**crypto_transactions** (0 rows):
- Same as crypto_assets ownership? _______________________________________The same for this one. Haven't set up properly.

**gst_threshold_monitoring** (0 rows):
- Monitors which entities? ________________________________________________
- Purpose: Haven't set up properly. ________________________________________________________________

### 5. AI/ML Tables

**ml_models** (7 rows):
-I don't think this is set up yet. __________________________________________

**ai_predictions** (0 rows):
- Used for: _______________________________________________________________I believe these are intended for MindsDB, but we haven't got around to setting them up.

**categorization_rules** (3 rows):
- Purpose: ________________________________________________________________
I haven't set it up yet.

### 6. Sync Infrastructure Tables

**sync_sessions** (11 rows):
**personal_transactions** sync from UpBank:
- Purpose: ________________________________________________________________
- Sync frequency: __________________________________________________________

**recurring_transactions** (26 rows):
- Purpose: ________________________________________________________________
- Covers: [ ] Personal [ ] Business [ ] Both

### 7. Project Attribution

Several tables have a `project` column mentioning "DiDi, Repco, Nintendo":

These are mok house projects. _________________________________________________________________

### 8. High-Level Summary

In 2-3 sentences, describe what the Supabase database is for:

Supabase database is for tracking all financial data across my personal and my businesses as well as crypto, and we'll be building on it as we go, adding more features and data and tables.
___________________________________________________________________________
___________________________________________________________________________

## What Happens Next

Once you fill this out:

1. Claude will create/update `context/finance/database/supabase-table-business-map.md`
2. The `/master-supabase` command will automatically load this context
3. When you ask "Show me MOK HOUSE invoices", Claude will know which tables to query
4. AI categorization will understand business vs personal transactions

## Notes/Additional Context

Add any other context that would help Claude understand your Supabase structure:

___________________________________________________________________________
___________________________________________________________________________
___________________________________________________________________________
