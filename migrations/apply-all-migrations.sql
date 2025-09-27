-- ========================================
-- CONSOLIDATED UPBANK SYNC MIGRATIONS
-- Apply this entire file in Supabase SQL Editor
-- ========================================

-- ========================================
-- PART 1: SYNC STATE MANAGEMENT
-- ========================================

-- Sync sessions table - tracks each sync attempt
CREATE TABLE IF NOT EXISTS sync_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status TEXT NOT NULL DEFAULT 'started',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    failed_at TIMESTAMP WITH TIME ZONE,
    progress JSONB DEFAULT '{}',
    summary JSONB DEFAULT '{}',
    error JSONB,
    metadata JSONB DEFAULT '{}',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Sync checkpoints
CREATE TABLE IF NOT EXISTS sync_checkpoints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sync_id UUID NOT NULL REFERENCES sync_sessions(id) ON DELETE CASCADE,
    accounts_synced INTEGER DEFAULT 0,
    categories_synced INTEGER DEFAULT 0,
    transactions_synced INTEGER DEFAULT 0,
    last_account_id TEXT,
    last_transaction_id TEXT,
    last_category_id TEXT,
    state_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Sync errors log
CREATE TABLE IF NOT EXISTS sync_errors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sync_id UUID REFERENCES sync_sessions(id) ON DELETE CASCADE,
    error_type TEXT NOT NULL,
    error_message TEXT NOT NULL,
    error_stack TEXT,
    context JSONB DEFAULT '{}',
    retry_count INTEGER DEFAULT 0,
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Webhook locks
CREATE TABLE IF NOT EXISTS webhook_locks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    webhook_id TEXT UNIQUE NOT NULL,
    transaction_id TEXT,
    locked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '5 minutes')
);

-- Transaction sync status
CREATE TABLE IF NOT EXISTS transaction_sync_status (
    upbank_transaction_id TEXT PRIMARY KEY,
    sync_id UUID REFERENCES sync_sessions(id) ON DELETE SET NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    attempt_count INTEGER DEFAULT 0,
    last_attempt_at TIMESTAMP WITH TIME ZONE,
    last_error TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Balance reconciliation history
CREATE TABLE IF NOT EXISTS balance_reconciliations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sync_id UUID REFERENCES sync_sessions(id) ON DELETE CASCADE,
    account_id UUID REFERENCES personal_accounts(id) ON DELETE CASCADE,
    upbank_balance_cents INTEGER NOT NULL,
    calculated_balance_cents INTEGER NOT NULL,
    difference_cents INTEGER NOT NULL,
    status TEXT NOT NULL,
    resolution TEXT,
    transaction_count INTEGER,
    date_range_start TIMESTAMP WITH TIME ZONE,
    date_range_end TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Rate limit tracking
CREATE TABLE IF NOT EXISTS rate_limit_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    api_name TEXT NOT NULL DEFAULT 'upbank',
    requests_remaining INTEGER,
    requests_limit INTEGER DEFAULT 1000,
    reset_at TIMESTAMP WITH TIME ZONE,
    last_request_at TIMESTAMP WITH TIME ZONE,
    requests_this_hour INTEGER DEFAULT 0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_sync_sessions_status ON sync_sessions(status, completed_at DESC);
CREATE INDEX IF NOT EXISTS idx_sync_checkpoints_sync_id ON sync_checkpoints(sync_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_sync_errors_sync_id ON sync_errors(sync_id, error_type);
CREATE INDEX IF NOT EXISTS idx_transaction_sync_status_status ON transaction_sync_status(status, last_attempt_at);
CREATE INDEX IF NOT EXISTS idx_balance_reconciliations_sync_id ON balance_reconciliations(sync_id);
CREATE INDEX IF NOT EXISTS idx_webhook_locks_expires ON webhook_locks(expires_at);

-- Functions
CREATE OR REPLACE FUNCTION cleanup_expired_webhook_locks()
RETURNS void AS $$
BEGIN
    DELETE FROM webhook_locks WHERE expires_at < NOW();
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_last_sync_time()
RETURNS TIMESTAMP WITH TIME ZONE AS $$
BEGIN
    RETURN (
        SELECT completed_at
        FROM sync_sessions
        WHERE status = 'completed'
        ORDER BY completed_at DESC
        LIMIT 1
    );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_transaction_gaps()
RETURNS TABLE(
    date_gap_start DATE,
    date_gap_end DATE,
    days_missing INTEGER
) AS $$
BEGIN
    RETURN QUERY
    WITH date_series AS (
        SELECT generate_series(
            (SELECT MIN(transaction_date::date) FROM personal_transactions),
            CURRENT_DATE,
            '1 day'::interval
        )::date AS transaction_date
    ),
    existing_dates AS (
        SELECT DISTINCT transaction_date::date AS transaction_date
        FROM personal_transactions
    )
    SELECT
        MIN(ds.transaction_date) AS date_gap_start,
        MAX(ds.transaction_date) AS date_gap_end,
        COUNT(*)::INTEGER AS days_missing
    FROM date_series ds
    LEFT JOIN existing_dates ed ON ds.transaction_date = ed.transaction_date
    WHERE ed.transaction_date IS NULL
    GROUP BY (ds.transaction_date - ROW_NUMBER() OVER (ORDER BY ds.transaction_date))
    ORDER BY date_gap_start;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_sync_health_metrics()
RETURNS JSONB AS $$
DECLARE
    metrics JSONB;
BEGIN
    metrics := jsonb_build_object(
        'last_sync_time', get_last_sync_time(),
        'total_sync_sessions', (SELECT COUNT(*) FROM sync_sessions),
        'successful_syncs', (SELECT COUNT(*) FROM sync_sessions WHERE status = 'completed'),
        'failed_syncs', (SELECT COUNT(*) FROM sync_sessions WHERE status = 'failed'),
        'average_sync_duration_seconds', (
            SELECT AVG(EXTRACT(EPOCH FROM (completed_at - started_at)))
            FROM sync_sessions
            WHERE status = 'completed'
        ),
        'total_transactions_synced', (SELECT COUNT(*) FROM personal_transactions),
        'recent_errors', (
            SELECT jsonb_agg(jsonb_build_object(
                'type', error_type,
                'message', error_message,
                'time', created_at
            ))
            FROM (
                SELECT error_type, error_message, created_at
                FROM sync_errors
                ORDER BY created_at DESC
                LIMIT 5
            ) recent
        ),
        'pending_retries', (
            SELECT COUNT(*)
            FROM transaction_sync_status
            WHERE status = 'failed' AND attempt_count < 3
        )
    );

    RETURN metrics;
END;
$$ LANGUAGE plpgsql;

-- Triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_sync_sessions_updated_at ON sync_sessions;
CREATE TRIGGER update_sync_sessions_updated_at BEFORE UPDATE ON sync_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_transaction_sync_status_updated_at ON transaction_sync_status;
CREATE TRIGGER update_transaction_sync_status_updated_at BEFORE UPDATE ON transaction_sync_status
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_rate_limit_status_updated_at ON rate_limit_status;
CREATE TRIGGER update_rate_limit_status_updated_at BEFORE UPDATE ON rate_limit_status
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- PART 2: ML INTEGRATION
-- ========================================

-- Add ML columns to personal_transactions
ALTER TABLE personal_transactions
ADD COLUMN IF NOT EXISTS ai_category TEXT,
ADD COLUMN IF NOT EXISTS ai_confidence DECIMAL(3,2),
ADD COLUMN IF NOT EXISTS ml_features JSONB;

-- Business keyword matching table
CREATE TABLE IF NOT EXISTS business_keywords (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    keyword TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    is_tax_deductible BOOLEAN DEFAULT TRUE,
    confidence_boost DECIMAL(3,2) DEFAULT 0.1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default business keywords
INSERT INTO business_keywords (keyword, category, is_tax_deductible) VALUES
('Setapp', 'Business Subscription', TRUE),
('Adobe', 'Business Software', TRUE),
('AWS', 'Cloud Services', TRUE),
('Google Cloud', 'Cloud Services', TRUE),
('Digital Ocean', 'Cloud Services', TRUE),
('Heroku', 'Cloud Services', TRUE),
('GitHub', 'Development Tools', TRUE),
('Linear', 'Project Management', TRUE),
('Notion', 'Productivity Software', TRUE),
('Slack', 'Business Communication', TRUE),
('Zoom', 'Business Communication', TRUE),
('Office 365', 'Business Software', TRUE),
('Microsoft 365', 'Business Software', TRUE),
('Xero', 'Accounting Software', TRUE),
('QuickBooks', 'Accounting Software', TRUE),
('Canva Pro', 'Design Tools', TRUE),
('Figma', 'Design Tools', TRUE)
ON CONFLICT (keyword) DO NOTHING;

-- ML prediction function
CREATE OR REPLACE FUNCTION predict_transaction_category(
    p_amount INTEGER,
    p_description TEXT,
    p_vendor_name TEXT DEFAULT NULL
)
RETURNS TABLE (
    category TEXT,
    confidence DECIMAL(3,2),
    is_business BOOLEAN
) AS $$
BEGIN
    -- Check for business keywords first
    IF EXISTS (
        SELECT 1 FROM business_keywords
        WHERE LOWER(p_description) LIKE '%' || LOWER(keyword) || '%'
    ) THEN
        RETURN QUERY
        SELECT
            bk.category,
            0.95::DECIMAL(3,2) as confidence,
            TRUE as is_business
        FROM business_keywords bk
        WHERE LOWER(p_description) LIKE '%' || LOWER(bk.keyword) || '%'
        LIMIT 1;
        RETURN;
    END IF;

    -- Fallback rules
    IF p_amount < 0 THEN
        IF LOWER(p_description) LIKE '%uber%' OR LOWER(p_description) LIKE '%taxi%' THEN
            RETURN QUERY SELECT 'Transport'::TEXT, 0.7::DECIMAL(3,2), FALSE::BOOLEAN;
        ELSIF LOWER(p_description) LIKE '%woolworths%' OR LOWER(p_description) LIKE '%coles%' THEN
            RETURN QUERY SELECT 'Groceries'::TEXT, 0.7::DECIMAL(3,2), FALSE::BOOLEAN;
        ELSIF LOWER(p_description) LIKE '%spotify%' OR LOWER(p_description) LIKE '%netflix%' THEN
            RETURN QUERY SELECT 'Entertainment'::TEXT, 0.7::DECIMAL(3,2), FALSE::BOOLEAN;
        ELSE
            RETURN QUERY SELECT 'Uncategorized'::TEXT, 0.3::DECIMAL(3,2), FALSE::BOOLEAN;
        END IF;
    ELSE
        RETURN QUERY SELECT 'Income'::TEXT, 0.7::DECIMAL(3,2), FALSE::BOOLEAN;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Auto-categorization trigger function
CREATE OR REPLACE FUNCTION auto_categorize_transaction()
RETURNS TRIGGER AS $$
DECLARE
    prediction RECORD;
BEGIN
    SELECT * INTO prediction
    FROM predict_transaction_category(
        NEW.amount_cents,
        NEW.description,
        NULL
    )
    LIMIT 1;

    IF prediction IS NOT NULL THEN
        NEW.ai_category := prediction.category;
        NEW.ai_confidence := prediction.confidence;
        NEW.is_business_related := prediction.is_business;

        IF prediction.is_business AND prediction.confidence >= 0.8 THEN
            NEW.is_tax_deductible := TRUE;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
DROP TRIGGER IF EXISTS auto_categorize_on_insert ON personal_transactions;
CREATE TRIGGER auto_categorize_on_insert
    BEFORE INSERT ON personal_transactions
    FOR EACH ROW
    EXECUTE FUNCTION auto_categorize_transaction();

-- Recategorize existing transactions
CREATE OR REPLACE FUNCTION recategorize_all_transactions()
RETURNS INTEGER AS $$
DECLARE
    updated_count INTEGER := 0;
    tx RECORD;
    prediction RECORD;
BEGIN
    FOR tx IN SELECT * FROM personal_transactions WHERE ai_category IS NULL
    LOOP
        SELECT * INTO prediction
        FROM predict_transaction_category(
            tx.amount_cents,
            tx.description,
            NULL
        )
        LIMIT 1;

        IF prediction IS NOT NULL THEN
            UPDATE personal_transactions
            SET
                ai_category = prediction.category,
                ai_confidence = prediction.confidence,
                is_business_related = prediction.is_business,
                is_tax_deductible = CASE
                    WHEN prediction.is_business AND prediction.confidence >= 0.8 THEN TRUE
                    ELSE is_tax_deductible
                END
            WHERE id = tx.id;

            updated_count := updated_count + 1;
        END IF;
    END LOOP;

    RETURN updated_count;
END;
$$ LANGUAGE plpgsql;

-- Indexes for ML features
CREATE INDEX IF NOT EXISTS idx_personal_transactions_ai_category ON personal_transactions(ai_category);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_ai_confidence ON personal_transactions(ai_confidence);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_is_business ON personal_transactions(is_business_related);

-- Comments
COMMENT ON COLUMN personal_transactions.ai_category IS 'ML-predicted transaction category';
COMMENT ON COLUMN personal_transactions.ai_confidence IS 'Confidence score for AI prediction (0.00-1.00)';
COMMENT ON COLUMN personal_transactions.ml_features IS 'Feature vector used for ML prediction';
COMMENT ON FUNCTION predict_transaction_category IS 'Predicts transaction category using ML or rule-based logic';
COMMENT ON FUNCTION auto_categorize_transaction IS 'Trigger function to automatically categorize new transactions';
COMMENT ON FUNCTION recategorize_all_transactions IS 'Batch recategorize all uncategorized transactions';

-- Grant permissions
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO service_role;

-- ========================================
-- PART 3: BUSINESS CATEGORIZATION
-- ========================================

-- Add business categorization columns to personal_transactions
ALTER TABLE personal_transactions
ADD COLUMN IF NOT EXISTS business_category TEXT,
ADD COLUMN IF NOT EXISTS business_subcategory TEXT;

-- Add index for business category queries
CREATE INDEX IF NOT EXISTS idx_personal_transactions_business_category
ON personal_transactions(business_category);

-- Comments for documentation
COMMENT ON COLUMN personal_transactions.business_category IS 'Business expense category (e.g., Software & Tools, Professional Services)';
COMMENT ON COLUMN personal_transactions.business_subcategory IS 'Business expense subcategory for detailed tracking';

-- ========================================
-- MIGRATION COMPLETE
-- ========================================
SELECT 'All migrations applied successfully!' as status;
