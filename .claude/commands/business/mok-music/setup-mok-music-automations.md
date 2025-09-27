# Setup MOK Music Automation Workflows

Comprehensive automation setup connecting Notion ESM Projects database with existing n8n and Supabase infrastructure.

## Prerequisites Check

1. **Verify n8n Access**:
   ```bash
   curl -X GET "http://134.199.159.190:5678/api/v1/workflows" \
     -H "Accept: application/json"
   ```

2. **Verify Supabase Connection**:
   ```
   mcp__supabase__list_projects
   ```

3. **Test Notion MCP Integration**:
   ```
   mcp__notion__API-post-database-query({
     database_id: "1e64a17b-b7f0-807d-b0f3-fe2cf5a6e3ac",
     page_size: 1
   })
   ```

## Core Automation Workflows

### 1. Project Status Change Automation

**Trigger**: Notion database property changes
**Actions**: Update Supabase, send notifications, trigger follow-up tasks

n8n Workflow Structure:
- **Webhook Node**: Receive Notion database changes
- **Switch Node**: Route based on status change
- **Supabase Node**: Update project records
- **Gmail Node**: Send status notifications to ESM
- **Wait Node**: Schedule follow-up reminders

### 2. Invoice Generation Automation

**Trigger**: Status change to "Invoice Ready"
**Actions**: Generate invoice, update financial records, notify accounting

n8n Workflow:
- **Notion Trigger**: Status = "Invoice Ready"
- **Data Transformer**: Calculate fees (demo + award)
- **Invoice Generator**: Create MOK HOUSE invoice template
- **Supabase Insert**: Record in financial system
- **Email Node**: Send to ESM + copy to Xero/Dext

### 3. APRA Registration Tracking

**Trigger**: APRA status changes or project completion
**Actions**: Track registration requirements, send reminders

n8n Workflow:
- **Scheduled Trigger**: Daily APRA status check
- **Notion Query**: Filter projects with APRA = "Check" or "In Progress"
- **Conditional Node**: Check days since status change
- **Reminder Email**: Send follow-up if overdue

### 4. Financial Sync Automation

**Trigger**: New projects, status changes, or schedule
**Actions**: Sync project data with Supabase financial system

n8n Workflow:
- **Notion Trigger**: New project or status change
- **Data Mapping**: Transform Notion data to Supabase schema
- **Supabase Upsert**: Update financial records
- **Slack/Email**: Notify of sync completion

## Implementation Steps

1. **Create n8n Webhook Endpoints**:
   - Project status changes: `/webhook/mok-music/status`
   - New project created: `/webhook/mok-music/new`
   - Invoice ready: `/webhook/mok-music/invoice`

2. **Configure Notion Webhooks**:
   ```javascript
   // Add to Notion integration settings
   {
     "url": "http://134.199.159.190:5678/webhook/mok-music/status",
     "events": ["database.page.property_change"],
     "database_id": "1e64a17b-b7f0-807d-b0f3-fe2cf5a6e3ac"
   }
   ```

3. **Setup Supabase Tables** for MOK Music tracking:
   ```sql
   CREATE TABLE mok_music_projects (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     notion_id TEXT UNIQUE NOT NULL,
     project_name TEXT NOT NULL,
     client_name TEXT,
     status TEXT,
     demo_fee DECIMAL,
     award_fee DECIMAL,
     apra_status TEXT,
     date_received DATE,
     date_completed DATE,
     invoice_sent BOOLEAN DEFAULT false,
     created_at TIMESTAMP DEFAULT NOW(),
     updated_at TIMESTAMP DEFAULT NOW()
   );
   ```

4. **Test Automation Flow**:
   - Create test project in Notion
   - Verify webhook triggers n8n workflow
   - Check Supabase record creation
   - Confirm email notifications

## Next Steps

After setup completion:
1. Monitor automation logs for 1 week
2. Adjust timing and notification settings
3. Add advanced features (project templates, bulk operations)
4. Create dashboard for automation health monitoring

**Estimated Setup Time**: 2-3 hours
**ROI**: Save 5-10 minutes per project, 2-3 hours per week on administrative tasks
