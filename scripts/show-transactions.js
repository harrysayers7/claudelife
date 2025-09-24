#!/usr/bin/env node

const { createClient } = require('@supabase/supabase-js');

const SUPABASE_URL = 'https://gshsshaodoyttdxippwx.supabase.co';
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY;

if (!SUPABASE_SERVICE_KEY) {
  console.error('❌ SUPABASE_SERVICE_KEY environment variable is required');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

async function showAllTransactions() {
  console.log('📊 COMPLETE TRANSACTION HISTORY\n');

  // Get account summary with transaction counts
  const { data: accounts, error: accountError } = await supabase
    .from('personal_accounts')
    .select(`
      display_name,
      balance_cents,
      personal_transactions (
        id,
        description,
        amount_cents,
        transaction_date,
        status
      )
    `)
    .order('display_name');

  if (accountError) {
    console.error('❌ Error fetching accounts:', accountError);
    return;
  }

  let totalTransactions = 0;
  let totalNetAmount = 0;

  accounts.forEach(account => {
    const transactions = account.personal_transactions;
    const transactionCount = transactions.length;
    const accountNetAmount = transactions.reduce((sum, t) => sum + t.amount_cents, 0);

    console.log(`🏦 ${account.display_name}`);
    console.log(`   Current Balance: $${(account.balance_cents / 100).toFixed(2)}`);
    console.log(`   Total Transactions: ${transactionCount}`);
    console.log(`   Net Transaction Amount: $${(accountNetAmount / 100).toFixed(2)}`);

    if (transactionCount > 0) {
      const dates = transactions.map(t => new Date(t.transaction_date));
      const earliest = new Date(Math.min(...dates));
      const latest = new Date(Math.max(...dates));
      console.log(`   Date Range: ${earliest.toLocaleDateString('en-AU')} to ${latest.toLocaleDateString('en-AU')}`);

      // Show recent transactions
      const recentTransactions = transactions
        .sort((a, b) => new Date(b.transaction_date) - new Date(a.transaction_date))
        .slice(0, 3);

      console.log(`   Recent Transactions:`);
      recentTransactions.forEach(t => {
        const amount = t.amount_cents / 100;
        const date = new Date(t.transaction_date).toLocaleDateString('en-AU');
        console.log(`     ${date}: ${amount >= 0 ? '+' : ''}$${amount.toFixed(2)} - ${t.description}`);
      });
    }
    console.log('');

    totalTransactions += transactionCount;
    totalNetAmount += accountNetAmount;
  });

  console.log('=' * 50);
  console.log(`🎯 SUMMARY ACROSS ALL ACCOUNTS:`);
  console.log(`   Total Transactions: ${totalTransactions}`);
  console.log(`   Total Net Amount: $${(totalNetAmount / 100).toFixed(2)}`);

  // Show transactions by type (income vs expenses)
  const { data: allTransactions } = await supabase
    .from('personal_transactions')
    .select('amount_cents')
    .order('transaction_date', { ascending: false });

  if (allTransactions) {
    const income = allTransactions.filter(t => t.amount_cents > 0).reduce((sum, t) => sum + t.amount_cents, 0);
    const expenses = allTransactions.filter(t => t.amount_cents < 0).reduce((sum, t) => sum + Math.abs(t.amount_cents), 0);

    console.log(`   Total Income: $${(income / 100).toFixed(2)}`);
    console.log(`   Total Expenses: $${(expenses / 100).toFixed(2)}`);
  }
}

showAllTransactions().catch(console.error);
