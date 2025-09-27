-- MOK Music Project Management Database Schema
-- Run this in Supabase SQL Editor for project: gshsshaodoyttdxippwx

-- Create MOK Music projects tracking table
CREATE TABLE IF NOT EXISTS mok_music_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    notion_id TEXT UNIQUE NOT NULL,
    project_name TEXT NOT NULL,
    client_name TEXT DEFAULT 'Electric Sheep Music',
    status TEXT CHECK (status IN ('New Project', 'In Progress', 'Sent to ESM', 'Invoice Ready', 'Complete', 'On Hold')),
    demo_fee DECIMAL(10,2) DEFAULT 0.00,
    award_fee DECIMAL(10,2) DEFAULT 0.00,
    total_value DECIMAL(10,2) GENERATED ALWAYS AS (COALESCE(demo_fee, 0) + COALESCE(award_fee, 0)) STORED,
    apra_status TEXT CHECK (apra_status IN ('Not Required', 'Check', 'In Progress', 'Complete')),
    date_received DATE,
    date_submitted DATE,
    date_completed DATE,
    po_number TEXT,
    is_invoiceable BOOLEAN DEFAULT false,
    invoice_sent BOOLEAN DEFAULT false,
    payment_received BOOLEAN DEFAULT false,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create APRA tracking table
CREATE TABLE IF NOT EXISTS mok_music_apra_tracking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    check_date DATE NOT NULL,
    items_needing_attention INTEGER DEFAULT 0,
    overdue_count INTEGER DEFAULT 0,
    in_progress_count INTEGER DEFAULT 0,
    completed_today INTEGER DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(check_date)
);

-- Create financial snapshots table for regular reporting
CREATE TABLE IF NOT EXISTS financial_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type TEXT NOT NULL, -- 'mok_music', 'mokai', etc.
    snapshot_date DATE NOT NULL,
    total_projects INTEGER DEFAULT 0,
    invoiceable_count INTEGER DEFAULT 0,
    total_pipeline_value DECIMAL(10,2) DEFAULT 0.00,
    invoiceable_value DECIMAL(10,2) DEFAULT 0.00,
    apra_pending_count INTEGER DEFAULT 0,
    sync_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(entity_type, snapshot_date)
);

-- Create automation logs table
CREATE TABLE IF NOT EXISTS automation_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    automation_type TEXT NOT NULL,
    notion_page_id TEXT,
    action_performed TEXT NOT NULL,
    success BOOLEAN DEFAULT true,
    error_message TEXT,
    execution_time_ms INTEGER,
    data_processed JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create project collaboration tracking
CREATE TABLE IF NOT EXISTS project_collaborations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES mok_music_projects(id) ON DELETE CASCADE,
    collaborator_name TEXT NOT NULL,
    collaborator_email TEXT,
    role TEXT, -- 'artist', 'producer', 'engineer', 'manager'
    contribution_type TEXT, -- 'writing', 'production', 'mixing', 'mastering'
    payment_share DECIMAL(5,2), -- percentage
    contact_method TEXT, -- 'email', 'phone', 'manager'
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create project milestones tracking
CREATE TABLE IF NOT EXISTS project_milestones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES mok_music_projects(id) ON DELETE CASCADE,
    milestone_name TEXT NOT NULL,
    milestone_type TEXT CHECK (milestone_type IN ('demo_delivery', 'revisions', 'final_delivery', 'apra_registration', 'payment')),
    due_date DATE,
    completed_date DATE,
    completed BOOLEAN DEFAULT false,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_mok_music_projects_notion_id ON mok_music_projects(notion_id);
CREATE INDEX IF NOT EXISTS idx_mok_music_projects_status ON mok_music_projects(status);
CREATE INDEX IF NOT EXISTS idx_mok_music_projects_apra_status ON mok_music_projects(apra_status);
CREATE INDEX IF NOT EXISTS idx_mok_music_projects_date_received ON mok_music_projects(date_received);
CREATE INDEX IF NOT EXISTS idx_financial_snapshots_date ON financial_snapshots(snapshot_date, entity_type);
CREATE INDEX IF NOT EXISTS idx_automation_logs_type ON automation_logs(automation_type, created_at);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_mok_music_projects_updated_at BEFORE UPDATE ON mok_music_projects FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create RLS policies (Row Level Security)
ALTER TABLE mok_music_projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE mok_music_apra_tracking ENABLE ROW LEVEL SECURITY;
ALTER TABLE financial_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE automation_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_collaborations ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_milestones ENABLE ROW LEVEL SECURITY;

-- Create policies for authenticated users
CREATE POLICY "Allow all operations for authenticated users" ON mok_music_projects
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all operations for authenticated users" ON mok_music_apra_tracking
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all operations for authenticated users" ON financial_snapshots
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all operations for authenticated users" ON automation_logs
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all operations for authenticated users" ON project_collaborations
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all operations for authenticated users" ON project_milestones
    FOR ALL USING (auth.role() = 'authenticated');

-- Insert some initial data for testing
INSERT INTO mok_music_projects (notion_id, project_name, status, demo_fee, award_fee, apra_status, date_received)
VALUES
    ('test-project-1', 'Test Project 1', 'New Project', 500.00, 1500.00, 'Check', CURRENT_DATE)
ON CONFLICT (notion_id) DO NOTHING;

-- Create views for common queries
CREATE OR REPLACE VIEW mok_music_dashboard AS
SELECT
    COUNT(*) as total_projects,
    COUNT(CASE WHEN status IN ('Invoice Ready', 'Complete') THEN 1 END) as invoiceable_projects,
    SUM(total_value) as total_pipeline_value,
    SUM(CASE WHEN status IN ('Invoice Ready', 'Complete') THEN total_value ELSE 0 END) as invoiceable_value,
    COUNT(CASE WHEN apra_status = 'Check' THEN 1 END) as apra_items_pending,
    COUNT(CASE WHEN status = 'In Progress' THEN 1 END) as active_projects,
    AVG(EXTRACT(DAYS FROM (COALESCE(date_completed, CURRENT_DATE) - date_received))) as avg_project_duration_days
FROM mok_music_projects
WHERE date_received >= CURRENT_DATE - INTERVAL '12 months';

CREATE OR REPLACE VIEW recent_project_activity AS
SELECT
    p.*,
    EXTRACT(DAYS FROM (CURRENT_DATE - p.date_received)) as days_since_received,
    CASE
        WHEN p.apra_status = 'Check' AND EXTRACT(DAYS FROM (CURRENT_DATE - p.date_received)) > 14 THEN 'APRA_OVERDUE'
        WHEN p.status = 'In Progress' AND EXTRACT(DAYS FROM (CURRENT_DATE - p.date_received)) > 21 THEN 'PROJECT_OVERDUE'
        WHEN p.status = 'Invoice Ready' THEN 'READY_TO_INVOICE'
        ELSE 'NORMAL'
    END as alert_status
FROM mok_music_projects p
WHERE p.date_received >= CURRENT_DATE - INTERVAL '6 months'
ORDER BY p.date_received DESC;

-- Grant permissions to service role
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO service_role;

-- Success message
SELECT 'MOK Music database schema created successfully! 🎵' as status;
