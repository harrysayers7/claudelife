---
Done: false
today: true
follow up: false
this week: false
back burner: false
ASAP: true
type: Task
status: pending
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

- Entity 1: ________________ (MOK HOUSE / MOKAI / Harrison?)
- Entity 2: ________________
- Entity 3: ________________

### 2. Core Financial Tables

**invoices** (31 rows):
- [ ] MOK HOUSE only
- [ ] MOKAI only
- [ ] Harrison personal only
- [x] Shared across all entities
- Notes: invoices before repco are Harrison or my sole trader abn and from repco until now are all mh

**transactions** (1 row):
- [ ] MOK HOUSE business transactions
- [ ] MOKAI business transactions
- [ ] Harrison personal business
- [ ] Shared across entities
- Notes: i dont think this is in use at the moment. Ignore

**contacts** (3 rows):
- [ ] MOK HOUSE clients/vendors
- [ ] MOKAI clients/vendors
- [ ] Shared across entities
- [ ] Personal contacts
- Notes: mok house and perosnal can share but mokai is separated________________________________________________________________

### 3. Personal Finance Tables

**personal_transactions** (261 rows):
- Purpose: trackong my personal transactions________________________________________________________________
- Source: UpBank personal account? Which account? ________________________
- Entity owner: Harrison Sayers and soletrader ABN___________________________________________________________
- Business vs Personal: ___________________________________________________MIX

**personal_accounts** (4 rows):
- Purpose: ________________________________________________________________
- Are these all your UpBank accounts? ____________________________________
- Entity owner: ❓️___________________________________________________________

### 4. Tax & Compliance Tables

**trust_distributions** (0 rows):
- Purpose: ________________________________________________________________
- Which trust entity? _____________________________________________________
- Used for: _______________________________________________________________

**crypto_assets** (0 rows):
- [ ] MOK HOUSE crypto
- [ ] MOKAI crypto
- [ ] Harrison personal crypto
- [ ] Not used yet
- Notes: NOT USED YET IGNORE________________________________________________________________

**crypto_transactions** (0 rows):
- Same as crypto_assets ownership? _______________________________________

**gst_threshold_monitoring** (0 rows):
- Monitors which entities? ________________________________________________
- Purpose: ________________________________________________________________

### 5. AI/ML Tables

**ml_models** (7 rows):
- Purpose: ________________________________________________________________
- What do these models predict? __________________________________________

**ai_predictions** (0 rows):
- Used for: _______________________________________________________________

**categorization_rules** (3 rows):
- Purpose: ________________________________________________________________
- Which entities do these apply to? ______________________________________

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

- Are these MOK HOUSE projects? __________________________________________
- Are these MOKAI projects? ______________________________________________
- Other? _________________________________________________________________

### 8. High-Level Summary

In 2-3 sentences, describe what the Supabase database is for:

___________________________________________________________________________
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
