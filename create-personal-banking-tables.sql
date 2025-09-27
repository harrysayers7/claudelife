-- Create personal banking tables for UpBank sync
-- Based on the sync script requirements

CREATE TABLE IF NOT EXISTS personal_accounts (
    id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    account_type TEXT NOT NULL,
    balance_cents INTEGER NOT NULL DEFAULT 0,
    balance_currency TEXT NOT NULL DEFAULT 'AUD',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

CREATE TABLE IF NOT EXISTS personal_categories (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    parent_id TEXT REFERENCES personal_categories(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

CREATE TABLE IF NOT EXISTS personal_transactions (
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

    -- ML and categorization fields
    category_id TEXT REFERENCES personal_categories(id),
    ai_category TEXT,
    ai_confidence DECIMAL(3,2),
    categorization_method TEXT DEFAULT 'manual',
    is_business_expense BOOLEAN DEFAULT FALSE,
    business_keywords TEXT[],

    -- Up Bank specific fields
    raw_text TEXT,
    foreign_fee_cents INTEGER,
    round_up_cents INTEGER,
    cashback_cents INTEGER
);

CREATE TABLE IF NOT EXISTS transaction_sync_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sync_session_id TEXT NOT NULL,
    account_id TEXT NOT NULL,
    last_transaction_id TEXT,
    last_sync_timestamp TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
    transactions_synced INTEGER DEFAULT 0,
    errors_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'in_progress',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_personal_transactions_account_id ON personal_transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_created_at ON personal_transactions(created_at);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_settled_at ON personal_transactions(settled_at);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_is_business ON personal_transactions(is_business_expense);
CREATE INDEX IF NOT EXISTS idx_transaction_sync_status_session ON transaction_sync_status(sync_session_id);

-- Update function for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc', now());
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers
CREATE TRIGGER update_personal_accounts_updated_at
    BEFORE UPDATE ON personal_accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_personal_transactions_updated_at
    BEFORE UPDATE ON personal_transactions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
