# Sync UpBank Transactions

This command helps you sync your UpBank banking data with Supabase for the claudelife project, ensuring all transactions, accounts, and categories are properly imported and categorized for financial tracking and analysis.

## Usage

```bash
/sync-upbank [full|recent|check]
```

## Interactive Process

When you run this command, I will:
1. Check the last sync timestamp to prevent duplicate syncs
2. Verify environment variables are configured (UPBANK_API_TOKEN, SUPABASE_SERVICE_ROLE_KEY)
3. Ask about sync preferences:
   - Time period (last 7/30/90 days or custom)
   - Specific accounts only or all accounts
   - Whether to update categories and account balances
4. Monitor sync progress and handle any errors
5. Provide a comprehensive summary with spending insights

## Input Requirements

Before running this command, ensure:
1. **Environment variables are set**:
   - `UPBANK_API_TOKEN` - Your UpBank API token
   - `SUPABASE_SERVICE_ROLE_KEY` - Supabase service role key
   - `SUPABASE_URL` - Should be `https://gshsshaodoyttdxippwx.supabase.co`

2. **Database tables exist**:
   - `personal_accounts` - For UpBank accounts
   - `personal_transactions` - For transaction data
   - `upbank_categories` - For UpBank category mappings

3. **Script is accessible**:
   - Location: `/Users/harrysayers/Developer/claudelife/scripts/sync-upbank-data.js`

## Process

I'll help you sync UpBank data by:

1. **Pre-sync Validation**
   - Check last sync time from database
   - Verify API credentials are working
   - Confirm database connectivity
   - Identify any accounts with pending transactions

2. **Category Sync**
   - Fetch latest UpBank categories
   - Upsert to `upbank_categories` table
   - Map parent-child category relationships

3. **Account Sync**
   - Retrieve all UpBank accounts
   - Update account balances in cents
   - Track account types (SAVER, TRANSACTIONAL)
   - Log any new accounts discovered

4. **Transaction Sync**
   - Determine sync period based on last sync or user preference
   - Fetch transactions per account (respecting rate limits)
   - Filter out existing transactions to prevent duplicates
   - Convert amounts to cents for consistency
   - Preserve UpBank categorization
   - Store complete transaction metadata

5. **Post-sync Analysis**
   - Calculate spending by category
   - Identify unusual transactions
   - Update account balance reconciliation
   - Generate sync summary report

## Technical Implementation Guide

### Running the Sync Script

```bash
# Full sync (last 90 days by default)
node /Users/harrysayers/Developer/claudelife/scripts/sync-upbank-data.js full

# Sync specific period
node /Users/harrysayers/Developer/claudelife/scripts/sync-upbank-data.js full 30

# Sync only accounts
node /Users/harrysayers/Developer/claudelife/scripts/sync-upbank-data.js accounts

# Sync only categories
node /Users/harrysayers/Developer/claudelife/scripts/sync-upbank-data.js categories

# Sync transactions for specific account
node /Users/harrysayers/Developer/claudelife/scripts/sync-upbank-data.js transactions [account-id] [days]
```

### Checking Sync Status

```javascript
// Check last sync time
const { data: lastSync } = await supabase
  .from('personal_transactions')
  .select('created_at')
  .order('created_at', { ascending: false })
  .limit(1);

// Check for sync gaps
const { data: syncGaps } = await supabase.rpc('check_transaction_gaps');
```

### Error Recovery

```javascript
// Retry failed transactions
const retryFailedSync = async (failedTransactionIds) => {
  for (const txId of failedTransactionIds) {
    await syncSingleTransaction(txId);
  }
};

// Validate account balances
const validateBalances = async () => {
  const upbankBalances = await upbank.getAccounts();
  const dbBalances = await supabase.from('personal_accounts').select('*');
  // Compare and reconcile
};
```

## Output Format

I'll provide:
1. **Sync Summary**:
   ```
   📊 UpBank Sync Complete
   ✅ Categories: 42 synced
   ✅ Accounts: 3 synced (2 SAVER, 1 TRANSACTIONAL)
   ✅ Transactions: 156 new, 0 failed
   💰 Total synced: -$2,345.67 (spending)
   📅 Period: Last 30 days
   ⏱️ Duration: 12.3 seconds
   ```

2. **Account Balance Update**:
   ```
   💳 Account Balances:
   • Spending: $1,234.56
   • Savings: $10,000.00
   • Emergency: $5,000.00
   ```

3. **Spending Analysis** (if requested):
   ```
   📈 Top Categories (Last 30 days):
   • Groceries: $450.23 (15 transactions)
   • Transport: $234.56 (8 transactions)
   • Entertainment: $123.45 (5 transactions)
   ```

4. **Error Report** (if any):
   ```
   ⚠️ Sync Issues:
   • 2 transactions failed (will retry)
   • Rate limit reached at transaction 500
   ```

## Examples

### Example 1: Daily Morning Sync

```bash
# Run every morning to catch overnight transactions
/sync-upbank recent

# I'll automatically:
# - Sync last 24 hours of transactions
# - Update account balances
# - Alert on any large/unusual transactions
# - Provide daily spending summary
```

### Example 2: Monthly Financial Review

```bash
# Full sync for monthly reconciliation
/sync-upbank full

# I'll:
# - Sync all data from last 90 days
# - Generate spending report by category
# - Identify spending trends
# - Validate all balances match UpBank
```

### Example 3: Check Sync Health

```bash
# Verify sync is working correctly
/sync-upbank check

# I'll:
# - Show last successful sync time
# - Identify any missing date ranges
# - Check for failed transactions
# - Validate database integrity
```

## Evaluation Criteria

A successful sync should:
1. **Complete without errors** - All accounts and transactions processed
2. **Maintain data integrity** - No duplicate transactions, accurate balances
3. **Respect rate limits** - Handle UpBank API limits gracefully
4. **Provide useful feedback** - Clear progress indicators and summaries
5. **Enable financial insights** - Categorized data ready for analysis
6. **Run efficiently** - Complete within 30 seconds for daily syncs
7. **Handle edge cases** - Pending transactions, refunds, round-ups
8. **Support incremental syncs** - Only fetch new data when possible

## Error Handling

Common issues and solutions:
- **Missing API Token**: Check ~/.zshrc for UPBANK_API_TOKEN
- **Database Connection Failed**: Verify SUPABASE_URL and service key
- **Rate Limit Exceeded**: Script will pause and retry automatically
- **Duplicate Transaction**: Script checks existing IDs before insert
- **Invalid Category**: Falls back to parent category or null

## Integration Points

- **MCP Integration**: Can trigger via `mcp__upbank__get_recent_transactions`
- **Database**: Uses Supabase project `gshsshaodoyttdxippwx` (SAYERS DATA)
- **Financial API**: Can trigger MindsDB predictions after sync
- **Automation**: Can be scheduled via cron or n8n workflows

## Related Resources

- **Enhanced Sync Script**: `/Users/harrysayers/Developer/claudelife/scripts/sync-upbank-enhanced.js`
- **Original Sync Script**: `/Users/harrysayers/Developer/claudelife/scripts/sync-upbank-data.js`
- **Sync Monitor**: `/Users/harrysayers/Developer/claudelife/scripts/sync-monitor.js`
- **Database Schema**: `/Users/harrysayers/Developer/claudelife/migrations/personal_banking_schema.sql`
- **Sync State Management**: `/Users/harrysayers/Developer/claudelife/migrations/sync-state-management.sql`
- **UpBank MCP tools**: `mcp__upbank__*` commands
- **Financial analysis**: `/Users/harrysayers/Developer/claudelife/scripts/show-transactions.js`

## Testing & Validation

The enhanced sync system includes comprehensive error handling and monitoring:

```bash
# Test script syntax
node -c scripts/sync-upbank-enhanced.js
node -c scripts/sync-monitor.js

# View sync health dashboard (requires environment setup)
node scripts/sync-monitor.js dashboard

# Check for errors and failed transactions
node scripts/sync-monitor.js errors

# Retry failed transactions
node scripts/sync-monitor.js retry
```

## Advanced Options

For specific sync scenarios:
- **Business expense tracking**: Add `--tag=business` to mark transactions
- **Parallel sync**: Use `--parallel` for faster multi-account sync
- **Dry run**: Add `--dry-run` to preview without database changes
- **Force refresh**: Use `--force` to ignore duplicate checks

Remember: The sync respects UpBank's rate limits and will automatically pause if needed. For best results, run daily syncs during off-peak hours (early morning) to capture overnight transactions.
