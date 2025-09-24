#!/usr/bin/env node

/**
 * UpBank Sync Monitoring and Management Utilities
 * Provides health checks, error analysis, and recovery tools
 */

const { createClient } = require('@supabase/supabase-js');

// Configuration
const SUPABASE_URL = process.env.SUPABASE_URL || 'https://gshsshaodoyttdxippwx.supabase.co';
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY;

if (!SUPABASE_SERVICE_KEY) {
  console.error('❌ SUPABASE_SERVICE_ROLE_KEY environment variable is required');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

class SyncMonitor {
  constructor() {
    this.colors = {
      reset: '\x1b[0m',
      bright: '\x1b[1m',
      red: '\x1b[31m',
      green: '\x1b[32m',
      yellow: '\x1b[33m',
      blue: '\x1b[34m',
      magenta: '\x1b[35m',
      cyan: '\x1b[36m'
    };
  }

  formatTime(date) {
    if (!date) return 'Never';
    return new Date(date).toLocaleString();
  }

  formatDuration(seconds) {
    if (!seconds) return 'N/A';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}m ${secs}s`;
  }

  formatAmount(cents) {
    return `$${Math.abs(cents / 100).toFixed(2)}`;
  }

  log(level, message, data = null) {
    const colors = {
      info: this.colors.blue,
      success: this.colors.green,
      warning: this.colors.yellow,
      error: this.colors.red,
      header: this.colors.cyan + this.colors.bright
    };

    const icons = {
      info: 'ℹ️ ',
      success: '✅ ',
      warning: '⚠️ ',
      error: '❌ ',
      header: '📊 '
    };

    console.log(
      `${colors[level] || ''}${icons[level] || ''}${message}${this.colors.reset}`
    );

    if (data) {
      console.log(JSON.stringify(data, null, 2));
    }
  }

  async getHealthMetrics() {
    try {
      const { data: metrics, error } = await supabase.rpc('get_sync_health_metrics');

      if (error) throw error;

      return metrics;
    } catch (error) {
      console.error('Failed to get health metrics:', error);
      return null;
    }
  }

  async getLastSyncDetails() {
    try {
      const { data: session, error } = await supabase
        .from('sync_sessions')
        .select('*')
        .order('started_at', { ascending: false })
        .limit(1)
        .single();

      if (error && error.code !== 'PGRST116') throw error;

      return session;
    } catch (error) {
      console.error('Failed to get last sync details:', error);
      return null;
    }
  }

  async getRecentErrors(limit = 10) {
    try {
      const { data: errors, error } = await supabase
        .from('sync_errors')
        .select(`
          *,
          sync_sessions!inner(started_at, status)
        `)
        .order('created_at', { ascending: false })
        .limit(limit);

      if (error) throw error;

      return errors;
    } catch (error) {
      console.error('Failed to get recent errors:', error);
      return [];
    }
  }

  async getFailedTransactions() {
    try {
      const { data: failed, error } = await supabase
        .from('transaction_sync_status')
        .select('*')
        .eq('status', 'failed')
        .order('last_attempt_at', { ascending: false });

      if (error) throw error;

      return failed;
    } catch (error) {
      console.error('Failed to get failed transactions:', error);
      return [];
    }
  }

  async getBalanceMismatches() {
    try {
      const { data: mismatches, error } = await supabase
        .from('balance_reconciliations')
        .select(`
          *,
          personal_accounts!inner(display_name, account_type)
        `)
        .eq('status', 'mismatch')
        .order('created_at', { ascending: false })
        .limit(10);

      if (error) throw error;

      return mismatches;
    } catch (error) {
      console.error('Failed to get balance mismatches:', error);
      return [];
    }
  }

  async getTransactionGaps() {
    try {
      const { data: gaps, error } = await supabase.rpc('check_transaction_gaps');

      if (error) throw error;

      return gaps;
    } catch (error) {
      console.error('Failed to check transaction gaps:', error);
      return [];
    }
  }

  async showHealthDashboard() {
    this.log('header', 'UpBank Sync Health Dashboard');
    console.log('═'.repeat(60));

    // Health metrics
    const metrics = await this.getHealthMetrics();

    if (metrics) {
      this.log('info', `Last Sync: ${this.formatTime(metrics.last_sync_time)}`);
      this.log('info', `Total Sessions: ${metrics.total_sync_sessions}`);
      this.log('success', `Successful: ${metrics.successful_syncs}`);

      if (metrics.failed_syncs > 0) {
        this.log('error', `Failed: ${metrics.failed_syncs}`);
      }

      if (metrics.average_sync_duration_seconds) {
        this.log('info', `Avg Duration: ${this.formatDuration(metrics.average_sync_duration_seconds)}`);
      }

      this.log('info', `Total Transactions: ${metrics.total_transactions_synced}`);

      if (metrics.pending_retries > 0) {
        this.log('warning', `Pending Retries: ${metrics.pending_retries}`);
      }
    }

    console.log('─'.repeat(60));

    // Last sync details
    const lastSync = await this.getLastSyncDetails();

    if (lastSync) {
      this.log('header', 'Last Sync Session');

      const statusIcon = lastSync.status === 'completed' ? '✅' :
                        lastSync.status === 'failed' ? '❌' : '⏳';

      console.log(`${statusIcon} Status: ${lastSync.status.toUpperCase()}`);
      console.log(`📅 Started: ${this.formatTime(lastSync.started_at)}`);

      if (lastSync.completed_at) {
        console.log(`✅ Completed: ${this.formatTime(lastSync.completed_at)}`);

        const duration = (new Date(lastSync.completed_at) - new Date(lastSync.started_at)) / 1000;
        console.log(`⏱️  Duration: ${this.formatDuration(duration)}`);
      }

      if (lastSync.failed_at) {
        console.log(`❌ Failed: ${this.formatTime(lastSync.failed_at)}`);
      }

      if (lastSync.summary) {
        const summary = lastSync.summary.summary || lastSync.summary;
        console.log('\n📊 Results:');
        console.log(`  • Accounts: ${summary.accountsSynced || 0}`);
        console.log(`  • Categories: ${summary.categoriesSynced || 0}`);
        console.log(`  • Transactions: ${summary.transactionsSynced || 0}`);

        if (summary.transactionsFailed > 0) {
          console.log(`  • Failed: ${summary.transactionsFailed}`);
        }

        if (summary.duplicatesSkipped > 0) {
          console.log(`  • Skipped: ${summary.duplicatesSkipped} duplicates`);
        }
      }

      if (lastSync.error) {
        console.log(`\n❌ Error: ${lastSync.error.message}`);
      }
    }

    console.log('─'.repeat(60));

    // Recent errors
    const errors = await this.getRecentErrors(5);

    if (errors.length > 0) {
      this.log('header', 'Recent Errors');

      errors.forEach((error, index) => {
        console.log(`${index + 1}. [${error.error_type}] ${error.error_message}`);
        console.log(`   📅 ${this.formatTime(error.created_at)}`);

        if (error.context && Object.keys(error.context).length > 0) {
          console.log(`   📝 Context: ${JSON.stringify(error.context)}`);
        }
        console.log();
      });
    } else {
      this.log('success', 'No recent errors found');
    }

    console.log('─'.repeat(60));

    // Balance mismatches
    const mismatches = await this.getBalanceMismatches();

    if (mismatches.length > 0) {
      this.log('warning', 'Balance Mismatches Found');

      mismatches.forEach((mismatch, index) => {
        const account = mismatch.personal_accounts;
        console.log(`${index + 1}. ${account.display_name} (${account.account_type})`);
        console.log(`   UpBank: ${this.formatAmount(mismatch.upbank_balance_cents)}`);
        console.log(`   Database: ${this.formatAmount(mismatch.calculated_balance_cents)}`);
        console.log(`   Difference: ${this.formatAmount(mismatch.difference_cents)}`);
        console.log(`   📅 ${this.formatTime(mismatch.created_at)}`);
        console.log();
      });
    } else {
      this.log('success', 'All account balances match');
    }

    console.log('═'.repeat(60));
  }

  async showErrorAnalysis() {
    this.log('header', 'Error Analysis Report');
    console.log('═'.repeat(60));

    const errors = await this.getRecentErrors(20);

    if (errors.length === 0) {
      this.log('success', 'No errors found in recent syncs');
      return;
    }

    // Group by error type
    const errorsByType = {};
    errors.forEach(error => {
      const type = error.error_type;
      if (!errorsByType[type]) {
        errorsByType[type] = [];
      }
      errorsByType[type].push(error);
    });

    Object.entries(errorsByType).forEach(([type, typeErrors]) => {
      this.log('header', `${type} (${typeErrors.length} occurrences)`);

      // Get unique error messages
      const uniqueMessages = [...new Set(typeErrors.map(e => e.error_message))];

      uniqueMessages.forEach(message => {
        const count = typeErrors.filter(e => e.error_message === message).length;
        console.log(`  • ${message} (${count}x)`);
      });

      // Show most recent occurrence
      const latest = typeErrors[0];
      console.log(`  📅 Most recent: ${this.formatTime(latest.created_at)}`);

      if (latest.context && Object.keys(latest.context).length > 0) {
        console.log(`  📝 Context: ${JSON.stringify(latest.context)}`);
      }

      console.log();
    });

    console.log('─'.repeat(60));

    // Failed transactions
    const failedTxs = await this.getFailedTransactions();

    if (failedTxs.length > 0) {
      this.log('warning', `Failed Transactions (${failedTxs.length})`);

      failedTxs.slice(0, 10).forEach((tx, index) => {
        console.log(`${index + 1}. ${tx.upbank_transaction_id}`);
        console.log(`   Attempts: ${tx.attempt_count}`);
        console.log(`   Last attempt: ${this.formatTime(tx.last_attempt_at)}`);
        console.log(`   Error: ${tx.last_error}`);
        console.log();
      });

      if (failedTxs.length > 10) {
        console.log(`   ... and ${failedTxs.length - 10} more`);
      }
    }

    console.log('═'.repeat(60));
  }

  async retryFailedTransactions() {
    this.log('info', 'Checking for failed transactions to retry...');

    const failed = await this.getFailedTransactions();
    const retryable = failed.filter(tx => tx.attempt_count < 3);

    if (retryable.length === 0) {
      this.log('success', 'No failed transactions to retry');
      return;
    }

    this.log('info', `Found ${retryable.length} transactions to retry`);

    const { EnhancedUpBankSyncer } = require('./sync-upbank-enhanced.js');
    const syncer = new EnhancedUpBankSyncer();

    let retrySuccessCount = 0;
    let retryFailedCount = 0;

    for (const tx of retryable) {
      try {
        console.log(`Retrying transaction ${tx.upbank_transaction_id}...`);

        // Mark as attempting retry
        await supabase
          .from('transaction_sync_status')
          .update({
            attempt_count: tx.attempt_count + 1,
            last_attempt_at: new Date()
          })
          .eq('upbank_transaction_id', tx.upbank_transaction_id);

        // TODO: Implement individual transaction retry logic
        // For now, we'll mark as needing full sync
        console.log(`  Marked for retry attempt ${tx.attempt_count + 1}`);

        retrySuccessCount++;

      } catch (error) {
        console.error(`  Failed: ${error.message}`);

        await supabase
          .from('transaction_sync_status')
          .update({
            last_error: error.message,
            last_attempt_at: new Date()
          })
          .eq('upbank_transaction_id', tx.upbank_transaction_id);

        retryFailedCount++;
      }
    }

    this.log('success', `Retry completed: ${retrySuccessCount} queued, ${retryFailedCount} failed`);
  }

  async cleanupOldData(daysToKeep = 30) {
    this.log('info', `Cleaning up sync data older than ${daysToKeep} days...`);

    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - daysToKeep);

    try {
      // Cleanup old sync sessions (keep successful ones longer)
      const { data: cleanedSessions, error: sessionError } = await supabase
        .from('sync_sessions')
        .delete()
        .lt('started_at', cutoffDate.toISOString())
        .neq('status', 'completed');

      if (sessionError) throw sessionError;

      // Cleanup old error logs
      const { data: cleanedErrors, error: errorError } = await supabase
        .from('sync_errors')
        .delete()
        .lt('created_at', cutoffDate.toISOString());

      if (errorError) throw errorError;

      // Cleanup expired webhook locks
      await supabase.rpc('cleanup_expired_webhook_locks');

      this.log('success', 'Cleanup completed');

    } catch (error) {
      this.log('error', `Cleanup failed: ${error.message}`);
    }
  }

  async exportSyncReport(format = 'json') {
    this.log('info', 'Generating sync report...');

    const report = {
      generated_at: new Date(),
      health_metrics: await this.getHealthMetrics(),
      last_sync: await this.getLastSyncDetails(),
      recent_errors: await this.getRecentErrors(50),
      failed_transactions: await this.getFailedTransactions(),
      balance_mismatches: await this.getBalanceMismatches(),
      transaction_gaps: await this.getTransactionGaps()
    };

    const filename = `sync-report-${new Date().toISOString().slice(0, 10)}.${format}`;

    if (format === 'json') {
      const fs = require('fs');
      fs.writeFileSync(filename, JSON.stringify(report, null, 2));
    } else if (format === 'csv') {
      // Simple CSV export for errors
      const csv = [
        'Timestamp,Error Type,Message,Context',
        ...report.recent_errors.map(e =>
          `${e.created_at},${e.error_type},"${e.error_message}","${JSON.stringify(e.context)}"`
        )
      ].join('\n');

      const fs = require('fs');
      fs.writeFileSync(filename, csv);
    }

    this.log('success', `Report exported to ${filename}`);
  }
}

// CLI Interface
async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'dashboard';

  const monitor = new SyncMonitor();

  try {
    switch (command) {
      case 'dashboard':
      case 'health':
        await monitor.showHealthDashboard();
        break;

      case 'errors':
        await monitor.showErrorAnalysis();
        break;

      case 'retry':
        await monitor.retryFailedTransactions();
        break;

      case 'cleanup':
        const days = parseInt(args[1]) || 30;
        await monitor.cleanupOldData(days);
        break;

      case 'export':
        const format = args[1] || 'json';
        await monitor.exportSyncReport(format);
        break;

      default:
        console.log(`
Usage: node sync-monitor.js [command] [options]

Commands:
  dashboard            - Show health dashboard (default)
  health               - Same as dashboard
  errors               - Show detailed error analysis
  retry                - Retry failed transactions
  cleanup [days]       - Cleanup old sync data (default: 30 days)
  export [format]      - Export sync report (json|csv)

Examples:
  node sync-monitor.js dashboard
  node sync-monitor.js errors
  node sync-monitor.js cleanup 14
  node sync-monitor.js export csv
        `);
    }
  } catch (error) {
    console.error('Monitor error:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { SyncMonitor };
