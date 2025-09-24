-- Sync State Management Tables for Enhanced UpBank Sync
-- Provides error recovery, checkpoint management, and monitoring

-- Sync sessions table - tracks each sync attempt
CREATE TABLE IF NOT EXISTS sync_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status TEXT NOT NULL DEFAULT 'started', -- started, completed, failed, resumed
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    failed_at TIMESTAMP WITH TIME ZONE,

    -- Progress tracking
    progress JSONB DEFAULT '{}',

    -- Summary data
    summary JSONB DEFAULT '{}',

    -- Error information
    error JSONB,

    -- Metadata
    metadata JSONB DEFAULT '{}',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Sync checkpoints - allows resuming from last good state
CREATE TABLE IF NOT EXISTS sync_checkpoints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sync_id UUID NOT NULL REFERENCES sync_sessions(id) ON DELETE CASCADE,

    -- Progress counters
    accounts_synced INTEGER DEFAULT 0,
    categories_synced INTEGER DEFAULT 0,
    transactions_synced INTEGER DEFAULT 0,

    -- Resume points
    last_account_id TEXT,
    last_transaction_id TEXT,
    last_category_id TEXT,

    -- Full state for complex resumes
    state_data JSONB DEFAULT '{}',

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Sync errors log - detailed error tracking
CREATE TABLE IF NOT EXISTS sync_errors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sync_id UUID REFERENCES sync_sessions(id) ON DELETE CASCADE,

    -- Error classification
    error_type TEXT NOT NULL, -- AUTH_ERROR, RATE_LIMIT, NETWORK_ERROR, DATABASE_ERROR, etc.
    error_message TEXT NOT NULL,
    error_stack TEXT,

    -- Context for debugging
    context JSONB DEFAULT '{}',

    -- Recovery information
    retry_count INTEGER DEFAULT 0,
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Webhook locks - prevents duplicate webhook processing
CREATE TABLE IF NOT EXISTS webhook_locks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    webhook_id TEXT UNIQUE NOT NULL,
    transaction_id TEXT,
    locked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '5 minutes')
);

-- Transaction sync status - tracks individual transaction sync attempts
CREATE TABLE IF NOT EXISTS transaction_sync_status (
    upbank_transaction_id TEXT PRIMARY KEY,
    sync_id UUID REFERENCES sync_sessions(id) ON DELETE SET NULL,

    -- Status tracking
    status TEXT NOT NULL DEFAULT 'pending', -- pending, synced, failed, skipped
    attempt_count INTEGER DEFAULT 0,
    last_attempt_at TIMESTAMP WITH TIME ZONE,

    -- Error information
    last_error TEXT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Balance reconciliation history
CREATE TABLE IF NOT EXISTS balance_reconciliations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sync_id UUID REFERENCES sync_sessions(id) ON DELETE CASCADE,
    account_id UUID REFERENCES personal_accounts(id) ON DELETE CASCADE,

    -- Balance comparison
    upbank_balance_cents INTEGER NOT NULL,
    calculated_balance_cents INTEGER NOT NULL,
    difference_cents INTEGER NOT NULL,

    -- Reconciliation status
    status TEXT NOT NULL, -- matched, mismatch, error
    resolution TEXT, -- manual_adjustment, re_sync, ignored

    -- Additional data
    transaction_count INTEGER,
    date_range_start TIMESTAMP WITH TIME ZONE,
    date_range_end TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Rate limit tracking
CREATE TABLE IF NOT EXISTS rate_limit_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    api_name TEXT NOT NULL DEFAULT 'upbank',

    -- Rate limit info
    requests_remaining INTEGER,
    requests_limit INTEGER DEFAULT 1000,
    reset_at TIMESTAMP WITH TIME ZONE,

    -- Tracking
    last_request_at TIMESTAMP WITH TIME ZONE,
    requests_this_hour INTEGER DEFAULT 0,

    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_sync_sessions_status ON sync_sessions(status, completed_at DESC);
CREATE INDEX idx_sync_checkpoints_sync_id ON sync_checkpoints(sync_id, created_at DESC);
CREATE INDEX idx_sync_errors_sync_id ON sync_errors(sync_id, error_type);
CREATE INDEX idx_transaction_sync_status_status ON transaction_sync_status(status, last_attempt_at);
CREATE INDEX idx_balance_reconciliations_sync_id ON balance_reconciliations(sync_id);
CREATE INDEX idx_webhook_locks_expires ON webhook_locks(expires_at);

-- Cleanup old webhook locks
CREATE OR REPLACE FUNCTION cleanup_expired_webhook_locks()
RETURNS void AS $$
BEGIN
    DELETE FROM webhook_locks WHERE expires_at < NOW();
END;
$$ LANGUAGE plpgsql;

-- Function to get last successful sync time
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

-- Function to check for sync gaps
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

-- Function to get sync health metrics
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

-- Trigger to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_sync_sessions_updated_at BEFORE UPDATE ON sync_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_transaction_sync_status_updated_at BEFORE UPDATE ON transaction_sync_status
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_rate_limit_status_updated_at BEFORE UPDATE ON rate_limit_status
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO service_role;
