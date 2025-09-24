#!/usr/bin/env node

/**
 * UpBank to Supabase Sync Script
 * Syncs personal banking data from UpBank API to Supabase
 */

const { createClient } = require('@supabase/supabase-js');

// Configuration
const SUPABASE_URL = process.env.SUPABASE_URL || 'https://gshsshaodoyttdxippwx.supabase.co';
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY;
const UPBANK_TOKEN = process.env.UPBANK_API_TOKEN;

if (!SUPABASE_SERVICE_KEY) {
  console.error('❌ SUPABASE_SERVICE_ROLE_KEY environment variable is required');
  process.exit(1);
}

if (!UPBANK_TOKEN) {
  console.error('❌ UPBANK_API_TOKEN environment variable is required');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

class UpBankAPI {
  constructor(token) {
    this.token = token;
    this.baseURL = 'https://api.up.com.au/api/v1';
  }

  async request(endpoint) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`UpBank API error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  }

  async getAccounts() {
    const data = await this.request('/accounts');
    return data.data;
  }

  async getTransactions(accountId = null, limit = 100, before = null) {
    let endpoint = '/transactions';
    const params = new URLSearchParams();

    if (accountId) {
      endpoint = `/accounts/${accountId}/transactions`;
    }

    params.append('page[size]', limit.toString());
    if (before) {
      params.append('page[before]', before);
    }

    const data = await this.request(`${endpoint}?${params}`);
    return data;
  }

  async getCategories() {
    const data = await this.request('/categories');
    return data.data;
  }
}

class UpBankSyncer {
  constructor() {
    this.upbank = new UpBankAPI(UPBANK_TOKEN);
  }

  async syncAccounts() {
    console.log('📦 Syncing accounts...');

    const accounts = await this.upbank.getAccounts();
    let syncedCount = 0;

    for (const account of accounts) {
      const accountData = {
        upbank_account_id: account.id,
        display_name: account.attributes.displayName,
        account_type: account.attributes.accountType,
        ownership_type: account.attributes.ownershipType,
        balance_cents: Math.round(parseFloat(account.attributes.balance.value) * 100),
        balance_currency_code: account.attributes.balance.currencyCode
      };

      const { error } = await supabase
        .from('personal_accounts')
        .upsert(accountData, {
          onConflict: 'upbank_account_id',
          ignoreDuplicates: false
        });

      if (error) {
        console.error(`❌ Error syncing account ${account.id}:`, error);
      } else {
        syncedCount++;
        console.log(`✅ Synced account: ${account.attributes.displayName}`);
      }
    }

    console.log(`📦 Synced ${syncedCount} accounts`);
    return accounts;
  }

  async syncCategories() {
    console.log('🏷️  Syncing categories...');

    const categories = await this.upbank.getCategories();
    let syncedCount = 0;

    for (const category of categories) {
      const categoryData = {
        id: category.id,
        name: category.attributes.name,
        parent_id: category.relationships?.parent?.data?.id || null
      };

      const { error } = await supabase
        .from('upbank_categories')
        .upsert(categoryData, {
          onConflict: 'id',
          ignoreDuplicates: false
        });

      if (error) {
        console.error(`❌ Error syncing category ${category.id}:`, error);
      } else {
        syncedCount++;
      }
    }

    console.log(`🏷️  Synced ${syncedCount} categories`);
  }

  async syncTransactions(accountId = null, daysBack = 90) {
    console.log(`💳 Syncing transactions${accountId ? ` for account ${accountId}` : ''}...`);

    let allTransactions = [];
    let hasMore = true;
    let before = null;

    // Get existing transaction IDs to avoid duplicates
    const { data: existingTransactions } = await supabase
      .from('personal_transactions')
      .select('upbank_transaction_id');

    const existingIds = new Set(existingTransactions?.map(t => t.upbank_transaction_id) || []);

    while (hasMore) {
      const response = await this.upbank.getTransactions(accountId, 100, before);
      const transactions = response.data;

      if (transactions.length === 0) {
        hasMore = false;
        break;
      }

      // Check if we're going too far back
      const oldestTransaction = new Date(transactions[transactions.length - 1].attributes.createdAt);
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - daysBack);

      if (oldestTransaction < cutoffDate) {
        // Filter transactions within the date range
        const recentTransactions = transactions.filter(t =>
          new Date(t.attributes.createdAt) >= cutoffDate
        );
        allTransactions.push(...recentTransactions);
        hasMore = false;
      } else {
        allTransactions.push(...transactions);
        // Get the next page
        before = response.links?.prev ? new URL(response.links.prev).searchParams.get('page[before]') : null;
        hasMore = before !== null;
      }
    }

    // Filter out existing transactions
    const newTransactions = allTransactions.filter(t => !existingIds.has(t.id));
    console.log(`Found ${newTransactions.length} new transactions to sync`);

    // Get account mapping
    const { data: accounts } = await supabase
      .from('personal_accounts')
      .select('id, upbank_account_id');

    const accountMapping = {};
    accounts?.forEach(acc => {
      accountMapping[acc.upbank_account_id] = acc.id;
    });

    let syncedCount = 0;

    for (const transaction of newTransactions) {
      const accountId = accountMapping[transaction.relationships.account.data.id];
      if (!accountId) {
        console.error(`❌ No local account found for UpBank account ${transaction.relationships.account.data.id}`);
        continue;
      }

      const transactionData = {
        upbank_transaction_id: transaction.id,
        account_id: accountId,
        description: transaction.attributes.description,
        message: transaction.attributes.message,
        amount_cents: Math.round(parseFloat(transaction.attributes.amount.value) * 100),
        currency_code: transaction.attributes.amount.currencyCode,
        transaction_date: transaction.attributes.createdAt,
        settled_at: transaction.attributes.settledAt,
        status: transaction.attributes.status,
        is_categorizable: transaction.attributes.isCategorizable,
        hold_info: transaction.attributes.holdInfo,
        round_up: transaction.attributes.roundUp,
        cashback: transaction.attributes.cashback,
        upbank_category_id: transaction.relationships?.category?.data?.id || null,
        upbank_parent_category_id: transaction.relationships?.parentCategory?.data?.id || null,
        raw_data: transaction
      };

      const { error } = await supabase
        .from('personal_transactions')
        .insert(transactionData);

      if (error) {
        console.error(`❌ Error syncing transaction ${transaction.id}:`, error);
      } else {
        syncedCount++;
        if (syncedCount % 50 === 0) {
          console.log(`✅ Synced ${syncedCount} transactions...`);
        }
      }
    }

    console.log(`💳 Synced ${syncedCount} new transactions`);
  }

  async fullSync(daysBack = 90) {
    console.log('🚀 Starting full UpBank sync...');

    try {
      // 1. Sync categories first
      await this.syncCategories();

      // 2. Sync accounts
      const accounts = await this.syncAccounts();

      // 3. Sync transactions for each account
      for (const account of accounts) {
        await this.syncTransactions(account.id, daysBack);
      }

      console.log('✅ Full sync completed successfully!');

    } catch (error) {
      console.error('❌ Sync failed:', error);
      process.exit(1);
    }
  }
}

// CLI Interface
async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'full';

  const syncer = new UpBankSyncer();

  switch (command) {
    case 'accounts':
      await syncer.syncAccounts();
      break;
    case 'categories':
      await syncer.syncCategories();
      break;
    case 'transactions':
      const accountId = args[1] || null;
      const daysBack = parseInt(args[2]) || 90;
      await syncer.syncTransactions(accountId, daysBack);
      break;
    case 'full':
      const fullDaysBack = parseInt(args[1]) || 90;
      await syncer.fullSync(fullDaysBack);
      break;
    default:
      console.log(`
Usage: node sync-upbank-data.js [command] [options]

Commands:
  full [days]              - Full sync (default: 90 days)
  accounts                 - Sync accounts only
  categories               - Sync categories only
  transactions [id] [days] - Sync transactions for account (optional)

Examples:
  node sync-upbank-data.js full 30
  node sync-upbank-data.js transactions account-123 7
      `);
  }
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { UpBankSyncer };
