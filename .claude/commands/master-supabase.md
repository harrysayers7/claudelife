---
created: "2025-10-20 06:15"
updated: "2025-10-20 06:30"
description: |
  Loads LIVE Supabase context for the SAYERS DATA project (gshsshaodoyttdxippwx).
  Verifies MCP connection, loads current database state, and identifies optimization opportunities.

  ALWAYS LOADS FRESH DATA - no caching to avoid staleness when schema changes.

  This command:
    - Validates Supabase MCP server connection (instant)
    - Loads database purpose from docs (instant)
    - Gets current table list and row counts (~2-3 seconds)
    - Runs health checks for security/performance issues (optional)
    - Provides full schema details on-demand when needed
examples:
  - /master-supabase (lightweight, 2-3 seconds)
  - /master-supabase --deep (full schema, 10-15 seconds)
  - /master-supabase --check-health (health analysis only, 5-10 seconds)
---

# Master Supabase Context

This command primes the complete context for your Supabase database, understanding its purpose, structure, and health status. After running this command, Claude will be ready to answer queries, make schema changes, and identify optimization opportunities without needing re-explanation.

## Usage

```bash
/master-supabase [--deep] [--check-health]
```

**Options:**
- `--deep`: Include full schema dump with column details, indexes, and constraints
- `--check-health`: Run optimization analysis only (bloat detection, inconsistencies)

## Process

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

I will execute the following steps to load Supabase context:

### 1. Verify MCP Connection & Tools

First, I'll check which Supabase MCP tools are available and verify connection status:

```javascript
// Check MCP server availability
ListMcpResourcesTool({ server: "supabase" })

// Verify project connection
mcp__supabase__get_project_url()
```

**Expected tools** (from .mcp.json):
- `mcp__supabase__list_tables` - List all tables
- `mcp__supabase__execute_sql` - Run SQL queries
- `mcp__supabase__apply_migration` - Apply schema changes
- `mcp__supabase__get_advisors` - Security/performance checks
- `mcp__supabase__get_logs` - Debug and monitoring
- `mcp__supabase__generate_typescript_types` - Type generation

If connection fails, I'll guide you through troubleshooting (restart Claude Code, verify `.mcp.json` config).

### 2. Load Database Purpose & Architecture

I'll read existing documentation to understand the **why** behind your Supabase structure:

```javascript
// Read purpose documentation
Read("context/finance/database/supabase-purpose.md")
Read("context/finance/database/supabase-schema.md")
Read("context/finance/database/supabase-ml-pipeline.md")
```

This tells me:
- What data domains are stored (financial, business entities, etc.)
- How data flows through the system (UpBank sync → Supabase → ML processing)
- Integration points (n8n workflows, FastAPI endpoints, Notion sync)

### 3. Get Database Overview (Lightweight)

Unless `--deep` is specified, I'll load a **minimal schema overview**:

```javascript
// Get table list with full schema (includes row counts via RLS-enabled tables)
const tables = await mcp__supabase__list_tables({ schemas: ["public"] })

// Extract table names and basic stats from the response
// Tables array contains: name, schema, rls_enabled, rls_forced
```

This gives me:
- Table names and their purposes (from documentation)
- RLS status (security indicator)
- Schema structure (from MCP response)

**I will NOT pull column details, indexes, or constraints** unless you ask a specific question that requires it or use `--deep` flag.

### 4. Run Health & Optimization Checks

I'll automatically check for:

**A. Security Advisors**
```javascript
mcp__supabase__get_advisors({ type: "security" })
```
- Missing RLS policies
- Publicly accessible tables
- Insecure configurations

**B. Performance Advisors**
```javascript
mcp__supabase__get_advisors({ type: "performance" })
```
- Missing indexes on foreign keys
- Slow query patterns
- Table bloat from dead tuples

**C. Data Inconsistencies** (via SQL)
```javascript
mcp__supabase__execute_sql({
  query: `
    -- Check for orphaned records (broken foreign keys)
    -- Check for duplicate entries in unique fields
    -- Identify tables with excessive NULL values
  `
})
```

### 5. Provide Context Summary

After loading LIVE data, I'll provide a **concise summary** that stays in conversation context:

```markdown
## Supabase Context Loaded ✅

**Project**: gshsshaodoyttdxippwx (SAYERS DATA)
**MCP Status**: Connected (9 tools available)

### Database Overview
| Table | Rows | Purpose | Status |
|-------|------|---------|--------|
| entities | 127 | Business entities (MOKAI, MOK HOUSE) | ✅ Healthy |
| contacts | 543 | Client and vendor contacts | ⚠️ 12 orphaned records |
| transactions | 8,234 | Financial transactions from UpBank | ✅ Healthy |
| invoices | 189 | Receivable/payable invoices | ⚠️ Missing index on entity_id |
| accounts | 15 | Bank accounts and financial accounts | ✅ Healthy |

### Health Summary
- ✅ All tables have RLS policies enabled
- ⚠️ Performance: 3 missing indexes detected (recommended for invoices, contacts)
- ⚠️ Data Quality: 12 orphaned contact records (no matching entity_id)
- ✅ Bloat: All tables <5% dead tuples (healthy)

### Common Operations Ready
I'm now prepared to:
- Answer questions about schema, relationships, data
- Run SQL queries and migrations
- Identify optimization opportunities
- Suggest schema improvements
- Debug data issues
```

This summary stays in context for the entire conversation.

### 6. On-Demand Deep Dives

When you ask specific questions, I'll **automatically pull fresh details** as needed:

**Examples:**
- "Show me the invoices schema" → Pull full column details, constraints, indexes for `invoices` table
- "Why are contacts slow?" → Run performance advisors, analyze missing indexes
- "What's linked to entities?" → Query foreign key relationships from schema
- "How do I add a new field to transactions?" → Guide migration with current schema context

I'll use the overview from steps 3-5 to provide fast, contextual answers, pulling deeper data only when required.

## Output Format

After running `/master-supabase`, you'll receive:

1. **Connection Status**: MCP tools available, project verified
2. **Purpose Summary**: What data lives here and why
3. **Schema Overview**: Tables, row counts, purposes (lightweight)
4. **Health Report**: Security advisors, performance issues, data quality
5. **Ready Confirmation**: "Context loaded. Ask me anything about Supabase."

## Examples

### Example 1: Standard Context Load

```
User: /master-supabase

Claude:
✅ Supabase MCP connected (9 tools available)
📊 Loading SAYERS DATA database context...

**Project**: gshsshaodoyttdxippwx
**Purpose**: Central financial data for MOKAI & MOK HOUSE
- UpBank transaction sync (automated via n8n)
- Invoice and contact management
- ML pipeline for tax categorization

**Tables**: 5 tables, 9,108 total rows
- entities (127): Business entities
- contacts (543): Clients/vendors
- transactions (8,234): Financial transactions
- invoices (189): AR/AP invoices
- accounts (15): Bank accounts

**Health**:
✅ Security: All RLS policies active
⚠️ Performance: 3 missing indexes (fix recommended)
⚠️ Data Quality: 12 orphaned contacts

Ready for queries! Ask me anything about schema, data, or optimizations.
```

### Example 2: Deep Schema Load

```
User: /master-supabase --deep

Claude:
[Standard context load from Example 1]

📋 Full Schema Details:

**entities**
- id: bigint (PK, auto-increment)
- business_name: text (NOT NULL)
- abn: text (UNIQUE)
- entity_type: text (CHECK: individual|company|trust)
- created_at: timestamptz (DEFAULT now())
Indexes: entities_pkey (id), entities_abn_key (abn)
RLS: Enabled, policy: allow_authenticated_users

**contacts**
- id: bigint (PK)
- entity_id: bigint (FK → entities.id)  ⚠️ Missing index!
- name: text (NOT NULL)
- email: text
- phone: text
- company: text
- contact_type: text (customer|vendor|partner)
- created_at: timestamptz
Indexes: contacts_pkey (id)
RLS: Enabled, policy: allow_authenticated_users

[... full details for all tables ...]

💡 Optimization Recommendations:
1. Add index on contacts(entity_id) - speeds up entity lookups
2. Add composite index on invoices(entity_id, status) - common query pattern
3. Clean up 12 orphaned contact records (entity_id doesn't exist)
```

### Example 3: Health Check Only

```
User: /master-supabase --check-health

Claude:
🏥 Supabase Health Analysis

**Security Advisors**: ✅ All clear
- RLS enabled on all tables
- No public access detected
- Credentials properly configured

**Performance Advisors**: ⚠️ 3 issues found

1. Missing Index: contacts(entity_id)
   Impact: Slow joins with entities table
   Fix: `CREATE INDEX idx_contacts_entity ON contacts(entity_id);`

2. Missing Index: invoices(entity_id, status)
   Impact: Slow invoice filtering queries
   Fix: `CREATE INDEX idx_invoices_entity_status ON invoices(entity_id, status);`

3. Table Bloat: transactions (4.2% dead tuples)
   Impact: Slightly increased storage and scan time
   Fix: `VACUUM ANALYZE transactions;`

**Data Quality Issues**: ⚠️ 1 issue found

1. Orphaned Records: 12 contacts have invalid entity_id
   Query to find: `SELECT id, name FROM contacts WHERE entity_id NOT IN (SELECT id FROM entities);`
   Fix Options:
   - Delete orphans: `DELETE FROM contacts WHERE entity_id NOT IN (...)`
   - Reassign to default entity
   - Manual review and correction

**Recommendations**:
- Run migrations to add missing indexes (estimated query speedup: 50-80%)
- Clean up orphaned data to maintain referential integrity
- Schedule weekly VACUUM ANALYZE for tables >1000 rows
```

## Evaluation Criteria

A successful Supabase context load should:

1. **✅ Verify MCP connectivity** and list all available tools
2. **✅ Load database purpose** from existing documentation
3. **✅ Provide schema overview** without excessive detail (unless --deep)
4. **✅ Identify health issues** via security/performance advisors
5. **✅ Detect data quality problems** (orphans, inconsistencies, bloat)
6. **✅ Load fresh data every time** - no stale cached context
7. **✅ Explain optimization opportunities** with concrete SQL fixes
8. **✅ Be ready to answer specific questions** with on-demand data fetching

After this command, you should be able to say:
- "Show me all invoices for entity 2" → I know the schema and can query
- "Add a notes field to contacts" → I can write the migration
- "Why is this query slow?" → I know the indexes and can optimize
- "Clean up orphaned data" → I can identify and fix data issues

## Related Resources

- Supabase documentation: `context/finance/database/supabase-purpose.md`
- Schema overview: `context/finance/database/supabase-schema.md`
- ML pipeline: `context/finance/database/supabase-ml-pipeline.md`
- MCP configuration: `.mcp.json` (server: supabase)
- Sync scripts: `scripts/sync-supabase-context.js`, `scripts/sync-supabase-notion.py`

## Technical Implementation Notes

### MCP Tools Usage Patterns

**For schema exploration:**
```javascript
// Lightweight table list
mcp__supabase__list_tables({ schemas: ["public"] })

// Get table stats (row counts, bloat)
mcp__supabase__execute_sql({
  query: "SELECT * FROM pg_stat_user_tables WHERE schemaname = 'public';"
})
```

**For health checks:**
```javascript
// Security check
mcp__supabase__get_advisors({ type: "security" })

// Performance check
mcp__supabase__get_advisors({ type: "performance" })

// Custom data quality checks
mcp__supabase__execute_sql({
  query: `
    SELECT
      c.id, c.name, c.entity_id
    FROM contacts c
    LEFT JOIN entities e ON c.entity_id = e.id
    WHERE e.id IS NULL;
  `
})
```

**For schema changes:**
```javascript
// Apply migration with proper naming
mcp__supabase__apply_migration({
  name: "add_contacts_entity_index",
  query: "CREATE INDEX idx_contacts_entity ON contacts(entity_id);"
})

// Generate TypeScript types after schema changes
mcp__supabase__generate_typescript_types()
```

### Performance Optimization Strategy

1. **Index Analysis**: Identify missing indexes on foreign keys and frequently filtered columns
2. **Bloat Detection**: Check `n_dead_tup` in `pg_stat_user_tables`
3. **Query Patterns**: Use `get_logs` to find slow queries
4. **Data Volume**: Monitor table growth and partition if needed

### Data Quality Checks

Run these queries to identify common issues:

```sql
-- Orphaned foreign keys
SELECT table_name, column_name, COUNT(*) as orphaned_count
FROM information_schema.columns
WHERE column_name LIKE '%_id'
GROUP BY table_name, column_name;

-- Excessive NULLs (>50% of rows)
SELECT
  tablename,
  attname,
  null_frac
FROM pg_stats
WHERE null_frac > 0.5
ORDER BY null_frac DESC;

-- Duplicate entries in unique fields
SELECT email, COUNT(*)
FROM contacts
GROUP BY email
HAVING COUNT(*) > 1;
```

### Live Data Strategy

**No caching** - always fetch fresh data when command runs to avoid staleness.

**Why live data instead of caching:**
- ✅ Always current - reflects latest schema changes, migrations, data updates
- ✅ Simple - no cache invalidation, no hooks, no sync complexity
- ✅ Fast enough - 2-3 seconds for overview is acceptable
- ✅ Reliable - no risk of showing outdated information

**Conversation context retention:**
After running this command, the loaded context (table names, purposes, health status) stays in the conversation. For follow-up queries:
- "What columns are in X?" → Pull fresh schema for table X only
- "Show me the data in X" → Run live SELECT query
- "How do I change X?" → Provide migration using current schema

This keeps responses fast and accurate without permanent caching.
