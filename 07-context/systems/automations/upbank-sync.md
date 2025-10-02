---
created: 2025-10-02 12:45
updated: 2025-10-02 12:45
system_type: automation
status: active
relation:
  - "[[Automation]]"
---

# UpBank GitHub Actions Automation

## Overview

**Purpose**: Automated financial data synchronization system that syncs UpBank banking transactions to Supabase database for personal finance tracking, analysis, and ML-powered categorization.

**Type**: GitHub Actions Automation (scheduled workflows + Node.js scripts)

**Status**: Active (daily automated syncs running)

**Business Context**: Part of claudelife's personal finance automation system. Enables automatic transaction tracking, spending analysis, and integration with MindsDB for intelligent categorization of business expenses (MOKAI/MOK HOUSE).

## Location

### GitHub Actions Workflows

**Primary Files**:
- [.github/workflows/sync-upbank-daily.yml:1](/.github/workflows/sync-upbank-daily.yml) - Daily automated sync (8 AM Sydney time)
- [.github/workflows/sync-upbank-monitor.yml:1](/.github/workflows/sync-upbank-monitor.yml) - Health monitoring (every 6 hours)
- [.github/workflows/sync-upbank-manual.yml:1](/.github/workflows/sync-upbank-manual.yml) - On-demand manual sync

### Node.js Scripts

**Core Scripts**:
- [scripts/sync-upbank-data.js:1](scripts/sync-upbank-data.js) - Main sync script (accounts, categories, transactions)
- [scripts/sync-upbank-enhanced.js:1](scripts/sync-upbank-enhanced.js) - Enhanced version with error recovery
- [scripts/sync-monitor.js:1](scripts/sync-monitor.js) - Health monitoring and gap detection

### Database Schemas

**Supabase Migrations**:
- [migrations/personal_banking_schema.sql:1](migrations/personal_banking_schema.sql) - Core tables (accounts, transactions, categories)
- [migrations/sync-state-management.sql:1](migrations/sync-state-management.sql) - Sync tracking (sessions, checkpoints, errors)

### Related Files

**Documentation**:
- [.claude/commands/sync-upbank.md:1](.claude/commands/sync-upbank.md) - Command documentation for manual sync
- [scripts/show-transactions.js:1](scripts/show-transactions.js) - Transaction analysis utility

## Architecture

### Components

1. **Daily Sync Workflow** ([.github/workflows/sync-upbank-daily.yml](/.github/workflows/sync-upbank-daily.yml))
   - **Trigger**: Cron schedule (10 PM UTC / 8 AM Sydney)
   - **Action**: Syncs last 7 days of transactions
   - **Output**: Transaction counts, error logs, sync summary
   - **Integration**: UpBank API → Node.js script → Supabase

2. **Health Monitor Workflow** ([.github/workflows/sync-upbank-monitor.yml](/.github/workflows/sync-upbank-monitor.yml))
   - **Trigger**: Every 6 hours + manual dispatch
   - **Action**: Checks sync health, detects gaps, validates data integrity
   - **Alert**: Creates GitHub issue on critical failures
   - **Monitoring**: sync_sessions, sync_errors, transaction gaps

3. **Manual Sync Workflow** ([.github/workflows/sync-upbank-manual.yml](/.github/workflows/sync-upbank-manual.yml))
   - **Trigger**: Manual GitHub Actions UI
   - **Options**: Full/accounts/categories/transactions modes
   - **Parameters**: Configurable days, account-specific sync
   - **Artifacts**: Uploads sync logs for debugging

4. **Sync Script** ([scripts/sync-upbank-data.js](scripts/sync-upbank-data.js))
   - **Functions**: Account sync, category sync, transaction sync
   - **API**: UpBank REST API integration
   - **Database**: Supabase PostgreSQL via service role key
   - **Error Handling**: Rate limiting, duplicate detection, retry logic

5. **Monitor Script** ([scripts/sync-monitor.js](scripts/sync-monitor.js))
   - **Capabilities**: Error detection, gap analysis, health reporting
   - **Tables**: Queries sync_sessions, sync_errors, sync_checkpoints
   - **Outputs**: Health status, failed transaction counts, missing date ranges

### Data Flow

```
UpBank API
    ↓
[GitHub Actions Runner]
    ↓
sync-upbank-data.js
    ↓
Supabase PostgreSQL
    ├── personal_accounts (balances, account info)
    ├── personal_transactions (transaction data)
    ├── upbank_categories (category mappings)
    ├── sync_sessions (sync tracking)
    ├── sync_checkpoints (resume points)
    └── sync_errors (error logs)
    ↓
MindsDB ML Categorization (downstream)
    ↓
Business Expense Detection (MOKAI/MOK HOUSE)
```

### Integration Points

- **UpBank API**: Banking data source (transactions, accounts, categories)
  - Authentication: Bearer token (`UPBANK_API_TOKEN`)
  - Rate limiting: Respected with automatic backoff
  - Data format: JSON API responses

- **Supabase Database**: Data storage and querying
  - Project: `gshsshaodoyttdxippwx` (SAYERS DATA)
  - Authentication: Service role key for full access
  - Tables: 8 tables for banking data and sync state

- **GitHub Actions**: Execution environment
  - Secrets: `UPBANK_API_TOKEN`, `SUPABASE_SERVICE_ROLE_KEY`
  - Runner: ubuntu-latest with Node.js 20
  - Artifacts: Sync logs retained for 30 days

- **MindsDB ML Pipeline**: Downstream categorization
  - Input: New transactions from personal_transactions
  - Output: Predicted categories with confidence scores
  - Business rules: Auto-detect MOKAI/MOK HOUSE expenses

## Configuration

### Environment Variables

```bash
# Required for sync execution
UPBANK_API_TOKEN="up:yeah:..."  # UpBank API bearer token
SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIs..."  # Full database access
SUPABASE_URL="https://gshsshaodoyttdxippwx.supabase.co"  # Database endpoint
```

### GitHub Secrets

Add these in [GitHub repo settings → Secrets](https://github.com/harrysayers7/claudelife/settings/secrets/actions):
- `UPBANK_API_TOKEN`: UpBank API authentication token
- `SUPABASE_SERVICE_ROLE_KEY`: Supabase service role key for database access

### Workflow Schedules

- **Daily Sync**: `0 22 * * *` (10 PM UTC = 8 AM Sydney next day)
- **Health Monitor**: `0 */6 * * *` (Every 6 hours)
- **Manual Sync**: On-demand via GitHub Actions UI

### Database Requirements

**Tables** (auto-created via migrations):
- `personal_accounts` - UpBank accounts
- `personal_transactions` - Transaction history
- `upbank_categories` - Category mappings
- `sync_sessions` - Sync tracking
- `sync_checkpoints` - Resume points
- `sync_errors` - Error logs

**Indexes**: Auto-created on foreign keys and frequently queried columns

## Usage

### Automatic Daily Sync

**No action required** - runs automatically every day at 8 AM Sydney time.

**What it does**:
1. Syncs last 7 days of transactions
2. Updates account balances
3. Refreshes category mappings
4. Logs sync status to database

**View results**: Check [GitHub Actions runs](https://github.com/harrysayers7/claudelife/actions/workflows/sync-upbank-daily.yml)

### Manual Sync

**Via GitHub UI**:
1. Go to [Actions → Manual UpBank Sync](https://github.com/harrysayers7/claudelife/actions/workflows/sync-upbank-manual.yml)
2. Click "Run workflow"
3. Select options:
   - **Sync type**: full/accounts/categories/transactions
   - **Days**: Number of days to sync (default: 30)
   - **Account ID**: Optional, for transaction-specific sync
4. Click "Run workflow"

**Via Command** (if using Claude Code):
```bash
/sync-upbank full 30  # Sync last 30 days
/sync-upbank recent   # Sync last 24 hours
/sync-upbank check    # Health check only
```

### Health Monitoring

**Automatic monitoring** runs every 6 hours:
- Checks last successful sync timestamp
- Detects missing date ranges (gaps)
- Validates data integrity
- Creates GitHub issue if critical failures detected

**Manual health check**:
```bash
# Via GitHub Actions
Actions → UpBank Sync Monitor → Run workflow

# Via script (local)
node scripts/sync-monitor.js errors
node scripts/sync-monitor.js dashboard
```

## Examples

### Example 1: Daily Automated Sync

**Scenario**: Automatic sync runs at 8 AM Sydney time

**Process**:
1. GitHub Actions triggers workflow at 10 PM UTC
2. Checks out repository, installs Node.js 20
3. Runs `node scripts/sync-upbank-data.js full 7`
4. Script fetches last 7 days of transactions from UpBank
5. Inserts new transactions, skips duplicates
6. Updates account balances
7. Logs sync session to database
8. Outputs summary to workflow logs

**Result**:
```
✅ Daily UpBank sync completed
📅 Synced last 7 days of transactions
📊 New transactions: 23
💰 Total amount: -$543.21
⏱️ Duration: 8.3 seconds
```

### Example 2: Manual Full Sync

**Scenario**: Need to sync last 30 days for monthly reconciliation

**Process**:
1. Navigate to GitHub Actions → Manual UpBank Sync
2. Select "full" sync type, "30" days
3. Workflow executes `node scripts/sync-upbank-data.js full 30`
4. Syncs all accounts, categories, and 30 days of transactions
5. Uploads sync logs as artifact

**Result**: 30 days of transactions synced, logs available for download

### Example 3: Health Monitor Detects Gap

**Scenario**: Sync failed yesterday, monitor detects missing data

**Process**:
1. Monitor workflow runs every 6 hours
2. Queries database for last sync timestamp
3. Detects 24-hour gap in transaction data
4. Health check script exits with error code
5. GitHub issue automatically created: "⚠️ UpBank Sync Health Issue Detected"
6. Issue links to failed workflow run for investigation

**Action**: Manually run full sync to fill gap, or wait for next auto-sync

### Example 4: Account-Specific Transaction Sync

**Scenario**: Only sync transactions for specific UpBank account

**Process**:
1. Get account ID from UpBank (or database)
2. Manual sync → "transactions" type
3. Enter account ID: `acc_xxxxxxxxxxxx`
4. Enter days: `7`
5. Executes `node scripts/sync-upbank-data.js transactions acc_xxxxxxxxxxxx 7`

**Result**: Only syncs 7 days of transactions for specified account

## Dependencies

### External Services

- **UpBank API** (v1): Banking data source
  - Endpoint: `https://api.up.com.au/api/v1`
  - Authentication: Bearer token
  - Rate limits: Respected with exponential backoff

- **Supabase** (PostgreSQL): Data storage
  - Project: gshsshaodoyttdxippwx
  - Region: Sydney (low latency)
  - Service: PostgreSQL with REST API

### NPM Packages

- `@supabase/supabase-js`: Supabase client library
- `node-fetch` or built-in fetch: HTTP requests to UpBank API
- Standard Node.js libraries (no heavy dependencies)

### GitHub Actions

- `actions/checkout@v4`: Repository checkout
- `actions/setup-node@v4`: Node.js 20 runtime
- `actions/upload-artifact@v4`: Log artifact upload
- `actions/github-script@v7`: Issue creation on failures

### Internal Dependencies

- **MindsDB ML Pipeline**: Uses synced transaction data for categorization
- **Financial Analysis Scripts**: Query personal_transactions for insights
- **Business Expense Detection**: Keywords match for MOKAI/MOK HOUSE

## Troubleshooting

### Common Issues

**Issue 1: Sync fails with "Rate limit exceeded"**
- **Cause**: Too many API requests to UpBank in short time
- **Solution**: Wait 60 seconds, UpBank rate limits reset. Script has automatic retry logic.
- **Prevention**: Daily sync (7 days) stays well under limits

**Issue 2: "Invalid token" error**
- **Cause**: `UPBANK_API_TOKEN` expired or incorrect
- **Solution**:
  1. Get new token from UpBank dashboard
  2. Update GitHub secret: Settings → Secrets → `UPBANK_API_TOKEN`
  3. Re-run workflow
- **Check**: Token format should be `up:yeah:...`

**Issue 3: Duplicate transactions detected**
- **Cause**: Same transaction synced twice (shouldn't happen with unique constraint)
- **Solution**: Script automatically skips duplicates based on `upbank_transaction_id`
- **Verify**: Check database for duplicate entries (should be none)

**Issue 4: Health monitor creates issue but sync looks fine**
- **Cause**: False positive or edge case in gap detection
- **Solution**:
  1. Check workflow logs for actual errors
  2. Run manual health check: `node scripts/sync-monitor.js errors`
  3. Review sync_errors table for details
- **Close issue** if no real problems found

**Issue 5: Transactions missing for specific date**
- **Cause**: Sync gap due to failed run or pending transactions
- **Solution**:
  1. Run manual full sync for affected period
  2. Check UpBank for pending/held transactions (not synced until settled)
  3. Verify sync_checkpoints for resume points

### Debugging

**Check workflow logs**:
```bash
# Via GitHub UI
Actions → [workflow name] → Latest run → View logs

# Download logs artifact
Actions → [workflow run] → Artifacts → sync-logs-*
```

**Query sync status in database**:
```sql
-- Last 10 sync sessions
SELECT * FROM sync_sessions
ORDER BY started_at DESC
LIMIT 10;

-- Recent errors
SELECT * FROM sync_errors
WHERE created_at > NOW() - INTERVAL '24 hours'
ORDER BY created_at DESC;

-- Check for transaction gaps
SELECT DATE(transaction_date) as date, COUNT(*)
FROM personal_transactions
GROUP BY DATE(transaction_date)
ORDER BY date DESC;
```

**Manual script execution (local)**:
```bash
# Set environment variables
export UPBANK_API_TOKEN="your_token"
export SUPABASE_SERVICE_ROLE_KEY="your_key"
export SUPABASE_URL="https://gshsshaodoyttdxippwx.supabase.co"

# Run sync script
node scripts/sync-upbank-data.js full 7

# Run health check
node scripts/sync-monitor.js errors
```

## Monitoring & Maintenance

### Logs

- **GitHub Actions**: Workflow run logs (retained indefinitely)
- **Sync Artifacts**: Uploaded logs (30-day retention)
- **Database Logs**: sync_sessions and sync_errors tables

### Monitoring

**Automated**:
- Health monitor runs every 6 hours
- GitHub issue created on critical failures
- Slack/email notifications (if configured)

**Manual Checks**:
```bash
# View last sync status
node scripts/sync-monitor.js dashboard

# Check for errors
node scripts/sync-monitor.js errors

# Retry failed transactions
node scripts/sync-monitor.js retry
```

**Key Metrics**:
- Last successful sync timestamp
- Transaction sync rate (transactions/day)
- Error rate (errors/sync session)
- Sync duration (should be <30 seconds for daily)

### Maintenance Tasks

**Weekly**:
- Review GitHub Actions runs for patterns
- Check for any persistent errors in sync_errors table

**Monthly**:
- Verify account balances match UpBank dashboard
- Review categorization accuracy (MindsDB predictions)
- Clean up old sync_errors entries (>90 days)

**Quarterly**:
- Audit UpBank API token expiration
- Review and optimize sync script performance
- Update dependencies (npm packages, GitHub Actions)

### Update Frequency

- **Code**: As needed for bug fixes or feature additions
- **Workflows**: Stable, minimal changes required
- **Database schema**: Rarely (migrations for new features)
- **Dependencies**: Monthly security updates

## Related Systems

- **MindsDB ML Categorization** (07-context/systems/ml-pipelines/transaction-categorization.md) - Uses synced transactions for ML predictions
- **Business Financial API** (07-context/systems/mcp-servers/business-api.md) - Queries transaction data for business metrics
- **UpBank MCP Server** (.mcp.json) - Alternative MCP-based access to UpBank data
- **Financial Analysis Scripts** (scripts/show-transactions.js) - Analyzes synced transaction data

## Future Enhancements

- **Real-time webhooks**: UpBank webhook support for instant transaction sync (when available)
- **Spending alerts**: Notify on unusual spending patterns or large transactions
- **Budget tracking**: Compare actual vs. budgeted spending by category
- **Tax reporting**: Generate tax-ready reports for business expenses
- **Multi-account support**: Extend to other banking APIs (if needed)
- **Dashboard integration**: Visualize spending trends in web UI

## Change Log

- **2025-10-02**: Initial documentation created
- **2025-10-02**: Replaced Claude Code workflow with direct script execution (cost optimization)
- **2025-10-02**: Added health monitoring with auto-issue creation
- **2025-10-02**: Implemented manual sync with configurable parameters
