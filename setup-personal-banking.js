#!/usr/bin/env node

const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  process.env.SUPABASE_URL || 'https://gshsshaodoyttdxippwx.supabase.co',
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY
);

async function createTables() {
  console.log('🔧 Setting up personal banking tables...');

  // Create personal_accounts table
  const { error: error1 } = await supabase.rpc('exec_sql', {
    sql: `CREATE TABLE IF NOT EXISTS personal_accounts (
      id TEXT PRIMARY KEY,
      display_name TEXT NOT NULL,
      account_type TEXT NOT NULL,
      balance_cents INTEGER NOT NULL DEFAULT 0,
      balance_currency TEXT NOT NULL DEFAULT 'AUD',
      created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
      updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
    )`
  });

  if (error1) {
    console.error('❌ Error creating personal_accounts:', error1);
    return;
  }
  console.log('✅ personal_accounts table created');

  // Create personal_categories table
  const { error: error2 } = await supabase.rpc('exec_sql', {
    sql: `CREATE TABLE IF NOT EXISTS personal_categories (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      parent_id TEXT REFERENCES personal_categories(id),
      created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
    )`
  });

  if (error2) {
    console.error('❌ Error creating personal_categories:', error2);
    return;
  }
  console.log('✅ personal_categories table created');

  // Create personal_transactions table
  const { error: error3 } = await supabase.rpc('exec_sql', {
    sql: `CREATE TABLE IF NOT EXISTS personal_transactions (
      id TEXT PRIMARY KEY,
      account_id TEXT NOT NULL REFERENCES personal_accounts(id),
      status TEXT NOT NULL,
      description TEXT NOT NULL,
      message TEXT,
      amount_cents INTEGER NOT NULL,
      currency TEXT NOT NULL DEFAULT 'AUD',
      settled_at TIMESTAMP WITH TIME ZONE,
      created_at TIMESTAMP WITH TIME ZONE NOT NULL,
      updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
      category_id TEXT REFERENCES personal_categories(id),
      ai_category TEXT,
      ai_confidence DECIMAL(3,2),
      categorization_method TEXT DEFAULT 'manual',
      is_business_expense BOOLEAN DEFAULT FALSE,
      business_keywords TEXT[],
      raw_text TEXT,
      foreign_fee_cents INTEGER,
      round_up_cents INTEGER,
      cashback_cents INTEGER
    )`
  });

  if (error3) {
    console.error('❌ Error creating personal_transactions:', error3);
    return;
  }
  console.log('✅ personal_transactions table created');

  // Create indexes
  const indexes = [
    'CREATE INDEX IF NOT EXISTS idx_personal_transactions_account_id ON personal_transactions(account_id)',
    'CREATE INDEX IF NOT EXISTS idx_personal_transactions_created_at ON personal_transactions(created_at)',
    'CREATE INDEX IF NOT EXISTS idx_personal_transactions_settled_at ON personal_transactions(settled_at)',
    'CREATE INDEX IF NOT EXISTS idx_personal_transactions_is_business ON personal_transactions(is_business_expense)'
  ];

  for (const indexSql of indexes) {
    const { error } = await supabase.rpc('exec_sql', { sql: indexSql });
    if (error) {
      console.error('❌ Error creating index:', error);
    }
  }
  console.log('✅ Indexes created');

  console.log('🎉 Personal banking tables setup complete!');
}

// Check if exec_sql function exists, if not create simple tables directly
async function setupDatabase() {
  try {
    await createTables();
  } catch (error) {
    console.log('🔄 Trying direct table creation...');

    // Direct table creation
    const { error: directError } = await supabase
      .from('personal_accounts')
      .select('count')
      .limit(1);

    if (directError && directError.code === 'PGRST116') {
      console.log('Tables do not exist, creating them...');
      // Tables don't exist - we need different approach
      console.error('❌ Need database admin access to create tables');
      console.log('💡 Please create these tables manually in Supabase dashboard:');
      console.log('1. personal_accounts');
      console.log('2. personal_categories');
      console.log('3. personal_transactions');
      return;
    }

    console.log('✅ Tables appear to exist already');
  }
}

setupDatabase().catch(console.error);
