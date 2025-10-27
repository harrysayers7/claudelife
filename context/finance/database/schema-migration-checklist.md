---
date: "2025-10-23"
---

# Supabase Multi-Schema Migration Checklist

## 🎯 Goal
Migrate from single `public` schema to multi-schema architecture (mokhouse, mokai, personal, finance) with **zero downtime** and **zero breaking changes**.

---

## ⚠️ Pre-Migration Safety Checks

### [ ] 1. Backup Current Database
```bash
# Create full database backup
pg_dump $SUPABASE_URL > backup-pre-schema-migration-$(date +%Y%m%d).sql

# Verify backup file exists and has content
ls -lh backup-pre-schema-migration-*.sql
```

### [ ] 2. Document Current State
```bash
# Export current schema
pg_dump --schema-only $SUPABASE_URL > current-schema.sql

# Count rows in key tables
psql $SUPABASE_URL -c "SELECT 'entities' as table, COUNT(*) FROM public.entities
UNION ALL SELECT 'invoices', COUNT(*) FROM public.invoices
UNION ALL SELECT 'transactions', COUNT(*) FROM public.transactions;"
```

### [ ] 3. Test Scripts Work Pre-Migration
```bash
# Run all Python scripts to establish baseline
python .claude/skills/australian-tax-intelligence/scripts/validate_gst_threshold.py --all
python .claude/skills/australian-tax-intelligence/scripts/optimize_trust_distribution.py --trust-entity "HS Family Trust"
python .claude/skills/australian-tax-intelligence/scripts/calculate_tax_bracket.py --entity "Harrison Robert Sayers"

# All should complete without errors ✅
```

### [ ] 4. Verify Environment Variables
```bash
echo $SUPABASE_URL
echo $SUPABASE_KEY | head -c 20  # Just verify it's set, don't print full key
echo $SUPABASE_USE_NEW_SCHEMAS  # Should be empty or 'false'
```

---

## 🚀 Migration Execution

### [ ] 5. Run Migration SQL Script
```bash
# Execute migration (creates schemas, tables, triggers, views)
psql $SUPABASE_URL -f context/finance/database/migrate-to-schemas.sql

# Verify no errors in output
# Expected: CREATE SCHEMA, CREATE TABLE, CREATE TRIGGER messages
```

### [ ] 6. Verify Migration Success
```bash
# Check schemas exist
psql $SUPABASE_URL -c "\dn"
# Should show: mokhouse, mokai, personal, finance

# Check tables created in new schemas
psql $SUPABASE_URL -c "\dt mokhouse.*"
psql $SUPABASE_URL -c "\dt mokai.*"
psql $SUPABASE_URL -c "\dt personal.*"
psql $SUPABASE_URL -c "\dt finance.*"

# Verify row counts match
psql $SUPABASE_URL -c "
SELECT
    'public.invoices' as location, COUNT(*) as count FROM public.invoices
UNION ALL
SELECT 'mokhouse.invoices', COUNT(*) FROM mokhouse.invoices
UNION ALL
SELECT 'mokai.invoices', COUNT(*) FROM mokai.invoices;
"
```

### [ ] 7. Verify Sync Triggers Are Working
```bash
# Insert test row into public.invoices (should auto-sync to mokhouse.invoices)
psql $SUPABASE_URL -c "
INSERT INTO public.invoices (id, entity_id, invoice_date, total_amount, invoice_type)
SELECT
    gen_random_uuid(),
    id,
    CURRENT_DATE,
    999.99,
    'receivable'
FROM finance.entities
WHERE name = 'MOK HOUSE PTY LTD'
LIMIT 1
RETURNING id;
"

# Check if it appears in mokhouse.invoices (should exist)
# psql $SUPABASE_URL -c "SELECT * FROM mokhouse.invoices WHERE total_amount = 999.99;"

# Delete test row
# psql $SUPABASE_URL -c "DELETE FROM public.invoices WHERE total_amount = 999.99;"
```

---

## 🧪 Testing Phase (New Schemas Disabled)

### [ ] 8. Test All Scripts with SUPABASE_USE_NEW_SCHEMAS=false (Legacy Mode)
```bash
export SUPABASE_USE_NEW_SCHEMAS=false

# Test GST threshold check
python .claude/skills/australian-tax-intelligence/scripts/validate_gst_threshold.py --entity "MOK HOUSE"
# ✅ Should work unchanged

# Test trust optimization
python .claude/skills/australian-tax-intelligence/scripts/optimize_trust_distribution.py --trust-entity "HS Family Trust"
# ✅ Should work unchanged

# Test tax calculation
python .claude/skills/australian-tax-intelligence/scripts/calculate_tax_bracket.py --entity "Harrison Robert Sayers"
# ✅ Should work unchanged
```

### [ ] 9. Test Slash Commands (Use Public Schema)
```bash
# All slash commands use MCP, should work unchanged
# Test in Claude Code:
/mokhouse-sync-invoices
/accountant
/master-supabase
```

### [ ] 10. Monitor for 24 Hours
- [ ] No errors in application logs
- [ ] All queries returning expected data
- [ ] Sync triggers keeping schemas in sync

---

## 🎚️ Cutover to New Schemas

### [ ] 11. Enable New Schemas for Testing
```bash
# Enable new schemas
export SUPABASE_USE_NEW_SCHEMAS=true
echo "export SUPABASE_USE_NEW_SCHEMAS=true" >> ~/.zshrc

# Test ONE script first
python .claude/skills/australian-tax-intelligence/scripts/validate_gst_threshold.py --entity "MOK HOUSE"
# ✅ Should route to mokhouse schema
```

### [ ] 12. Verify Schema Routing is Working
```bash
# Enable debug mode to see which schema is used
SUPABASE_USE_NEW_SCHEMAS=true python -c "
from supabase_client import get_schema_aware_client

client = get_schema_aware_client()
print('Schema routing enabled:', client._use_new_schemas)
print('Fallback count:', client.get_fallback_stats())

# Test entity-based routing
result = client.table('invoices', entity_name='MOK HOUSE PTY LTD')
print('Table reference created successfully')
"
```

### [ ] 13. Test All Scripts with New Schemas
```bash
export SUPABASE_USE_NEW_SCHEMAS=true

# Test all Python scripts
python .claude/skills/australian-tax-intelligence/scripts/validate_gst_threshold.py --all
python .claude/skills/australian-tax-intelligence/scripts/optimize_trust_distribution.py --trust-entity "HS Family Trust"
python .claude/skills/australian-tax-intelligence/scripts/calculate_tax_bracket.py --compare 35000,45000,60000

# All should complete without errors ✅
```

### [ ] 14. Monitor for 1 Week
- [ ] No schema errors or fallbacks
- [ ] All data writes appearing in correct schemas
- [ ] Performance acceptable (should be same or better)

---

## 🧹 Cleanup (Optional - Only After Confidence)

### [ ] 15. Disable Sync Triggers
```sql
-- After 1 week of stable operation with new schemas
DROP TRIGGER IF EXISTS mokhouse_invoice_sync ON public.invoices;
DROP TRIGGER IF EXISTS public_invoice_sync_from_mokhouse ON mokhouse.invoices;
-- (Drop other triggers)
```

### [ ] 16. Archive Public Schema Tables
```sql
-- Rename public tables instead of dropping (safety)
ALTER TABLE public.invoices RENAME TO invoices_deprecated;
ALTER TABLE public.transactions RENAME TO transactions_deprecated;

-- Or export and drop
pg_dump --table=public.invoices $SUPABASE_URL > archived-public-invoices.sql
-- DROP TABLE public.invoices;  -- DANGER: Only if confident
```

### [ ] 17. Remove Feature Flag from Scripts
```python
# Update scripts to remove USE_NEW_SCHEMAS checks
# Hard-code use_new_schemas=True in get_schema_aware_client() calls
```

---

## 🔄 Rollback Plan (If Issues Occur)

### Emergency Rollback
```bash
# 1. Disable new schemas immediately
export SUPABASE_USE_NEW_SCHEMAS=false
echo "export SUPABASE_USE_NEW_SCHEMAS=false" >> ~/.zshrc

# 2. All scripts fall back to public schema automatically
# No code changes needed!

# 3. Verify rollback successful
python .claude/skills/australian-tax-intelligence/scripts/validate_gst_threshold.py --all
# ✅ Should work using public schema
```

### Full Rollback (Remove Migration)
```bash
# Run rollback SQL (uncomment rollback section in migration script)
psql $SUPABASE_URL -f context/finance/database/migrate-to-schemas-rollback.sql

# Verify schemas removed
psql $SUPABASE_URL -c "\dn"
# Should only show: public, extensions
```

---

## 📊 Success Metrics

### Migration is successful when:
- [ ] All schemas created with correct tables
- [ ] Row counts match between public and new schemas
- [ ] Sync triggers working bidirectionally
- [ ] All Python scripts work with `USE_NEW_SCHEMAS=false` (legacy mode)
- [ ] All Python scripts work with `USE_NEW_SCHEMAS=true` (new mode)
- [ ] All slash commands work unchanged
- [ ] No data loss or corruption
- [ ] Performance same or better than before

---

## 🆘 Troubleshooting

### Issue: "Schema does not exist" Error
```bash
# Check schema was created
psql $SUPABASE_URL -c "\dn"

# If missing, re-run migration
psql $SUPABASE_URL -f context/finance/database/migrate-to-schemas.sql
```

### Issue: Row Counts Don't Match
```bash
# Check sync triggers are enabled
psql $SUPABASE_URL -c "
SELECT
    trigger_name,
    event_object_table,
    action_statement
FROM information_schema.triggers
WHERE trigger_schema = 'public';
"

# Manually sync if needed
INSERT INTO mokhouse.invoices SELECT * FROM public.invoices WHERE entity_id = (SELECT id FROM finance.entities WHERE name = 'MOK HOUSE PTY LTD');
```

### Issue: Scripts Failing with New Schemas
```bash
# Check fallback stats
python -c "
from supabase_client import get_schema_aware_client
client = get_schema_aware_client()
# Run some queries...
print(client.get_fallback_stats())
"

# If high fallback count, check schema routing mappings
# Update ENTITY_SCHEMA_MAP or TABLE_SCHEMA_MAP in supabase_client.py
```

---

## 📝 Notes

- **Duration**: Full migration should take 2-4 weeks (including monitoring periods)
- **Risk Level**: Low (zero downtime, automatic fallback)
- **Reversible**: Yes (instant rollback via feature flag)
- **Impact**: Zero breaking changes to existing workflows

---

## ✅ Final Checklist

- [ ] Pre-migration backups created
- [ ] Migration SQL executed successfully
- [ ] All scripts tested in legacy mode (USE_NEW_SCHEMAS=false)
- [ ] All scripts tested in new mode (USE_NEW_SCHEMAS=true)
- [ ] Slash commands working unchanged
- [ ] Monitored for 1 week with no issues
- [ ] Ready for cleanup (optional)

**Migration Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete
