# Deploy MOK Music Automations

Complete deployment guide for MOK Music project management automations.

## Quick Deployment Checklist

### 1. Database Setup (5 minutes)
```bash
# Run the database schema creation
mcp__supabase__execute_sql({
  project_id: "gshsshaodoyttdxippwx",
  query: [paste content from create-mok-music-tables.sql]
})
```

### 2. Import n8n Workflows (10 minutes)

**Access n8n**: http://134.199.159.190:5678

Import these workflow files:
- `n8n-workflows/mok-music-project-sync.json` - Real-time Notion sync
- `n8n-workflows/mok-music-apra-tracker.json` - Daily APRA monitoring
- `n8n-workflows/mok-music-financial-sync.json` - Financial reporting

For each workflow:
1. Go to n8n → Workflows → Import from File
2. Upload the JSON file
3. Configure credentials (Notion, Supabase, Gmail)
4. Test and activate

### 3. Configure Notion Integration (3 minutes)

**Add webhook to ESM Projects database**:
1. Open Notion → ESM Projects → Settings → Integrations
2. Add webhook URL: `http://134.199.159.190:5678/webhook/mok-music/project-sync`
3. Select events: `page.property_changed`, `page.created`

### 4. Test Automations (5 minutes)

**Quick test sequence**:
1. Create test project in Notion ESM Projects
2. Change status to "Invoice Ready"
3. Check n8n execution logs
4. Verify Supabase record created
5. Check email notifications sent

## Slash Commands Available

After deployment, these commands are ready to use:

- `/mok-music-project-status` - Dashboard view of all projects
- `/mok-music-new-project` - Create new project with proper structure
- `/mok-music-invoice-ready` - Mark project ready and generate invoice
- `/mok-music-client-follow-up` - Send status updates to ESM
- `/mok-music-financial-summary` - Generate financial reports
- `/setup-mok-music-automations` - Comprehensive automation setup

## What Gets Automated

### Real-time Project Sync
- **Trigger**: Any property change in Notion ESM Projects
- **Actions**:
  - Update Supabase database
  - Send invoice emails when status = "Invoice Ready"
  - Send completion notifications
  - Log all changes for audit

### Daily APRA Monitoring
- **Schedule**: Every 24 hours at 9:00 AM
- **Actions**:
  - Check projects with APRA = "Check" status
  - Send reminders for overdue items (>7 days)
  - Escalate urgent items (>21 days)
  - Log tracking metrics

### Financial Reporting
- **Schedule**: Every 6 hours
- **Actions**:
  - Sync all project data to Supabase
  - Create invoice records for eligible projects
  - Generate financial snapshots
  - Send daily summary reports

### Key Metrics Tracked
- Total projects and pipeline value
- Invoiceable projects and revenue
- APRA registration status and overdue items
- Project duration and completion rates
- Client communication history

## Expected Time Savings

**Per Project (estimated)**:
- Status updates: 3 minutes → automated
- Invoice creation: 15 minutes → automated
- APRA tracking: 5 minutes → automated
- Financial reporting: 10 minutes → automated

**Weekly Savings**: ~3-4 hours of administrative work

## Monitoring & Maintenance

### Health Checks
1. **n8n Dashboard**: Monitor execution success rates
2. **Supabase Logs**: Check database sync status
3. **Gmail Activity**: Verify notifications are sending
4. **Notion Integration**: Confirm webhook connectivity

### Monthly Reviews
- Review automation execution logs
- Update workflow timing if needed
- Check for new project workflow patterns
- Optimize notification timing and content

## Troubleshooting

### Common Issues
1. **Webhook not triggering**: Check Notion integration settings
2. **Email not sending**: Verify Gmail OAuth credentials in n8n
3. **Database errors**: Check Supabase connection and table schema
4. **Missing data**: Review data transformation mappings

### Support Resources
- n8n Documentation: https://docs.n8n.io
- Notion API Docs: https://developers.notion.com
- Supabase Dashboard: https://supabase.com/dashboard/project/gshsshaodoyttdxippwx

## Success Metrics

After 1 month of deployment, expect:
- 95%+ automation success rate
- 80% reduction in manual administrative tasks
- Real-time project visibility for ESM
- Consistent invoice and payment tracking
- Proactive APRA registration management

**Total Setup Time**: ~25 minutes
**Ongoing Maintenance**: ~30 minutes per month
