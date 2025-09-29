# n8n UpBank Sync Setup - Step by Step

## Overview
Set up automated UpBank sync using n8n with minimal nodes, leveraging existing Node.js script.

## Prerequisites
- n8n running on server (134.199.159.190)
- Existing sync script at `/Users/harrysayers/Developer/claudelife/scripts/sync-upbank-data.js`
- Environment variables configured (UPBANK_API_TOKEN, SUPABASE_SERVICE_KEY)
- **IMPORTANT**: Script must be copied to server first (see Setup section)

## Step 0: Copy Script to Server (Required First)

Since n8n runs on your server but the script is on your local machine, you need to copy it first:

```bash
# Copy the sync script to server
scp /Users/harrysayers/Developer/claudelife/scripts/sync-upbank-data.js root@134.199.159.190:/root/

# Copy package.json for dependencies
scp /Users/harrysayers/Developer/claudelife/package.json root@134.199.159.190:/root/

# SSH to server and install dependencies
ssh root@134.199.159.190
cd /root
npm install
exit
```

**Verify the script works on server:**
```bash
ssh root@134.199.159.190 "cd /root && node sync-upbank-data.js full"
```

## Step 1: Access n8n Interface
1. Open browser to your n8n instance
2. Navigate to workflows section
3. Click "Create New Workflow"

## Step 2: Add Schedule Trigger Node
1. **Add Node** → **Trigger** → **Schedule Trigger**
2. **Settings**:
   - **Trigger Interval**: Custom (Cron)
   - **Cron Expression**: `0 2 * * *` (daily at 2 AM)
   - **Timezone**: Australia/Sydney
3. **Save** the node

## Step 3: Add Execute Command Node
1. **Add Node** → **Regular** → **Execute Command**
2. **Settings**:
   - **Command**: `cd /root && node sync-upbank-data.js full`
   - **Timeout**: `300000` (5 minutes)
3. **Note**: Since the Execute Command node doesn't have separate Parameters/Working Directory fields, we use the full command with `cd`
4. **Environment Variables** (if needed):
   - Add any missing env vars that n8n doesn't inherit
5. **Save** the node

## Step 4: Connect Nodes
1. Click and drag from Schedule Trigger output to Execute Command input
2. Green line should connect them

## Step 5: Add Error Handling (Optional)
1. **Add Node** → **Regular** → **HTTP Request** (for webhook notification)
2. **Connect** Execute Command **error output** to HTTP Request
3. **Configure webhook** for Slack/email notifications

## Step 6: Test the Workflow
1. Click **Execute Workflow** button
2. Check **Executions** tab for results
3. Verify sync output matches local execution

## Step 7: Activate Workflow
1. Toggle **Active** switch in top right
2. Workflow will now run on schedule

## Alternative: Function Node Approach (NOT RECOMMENDED)

**Note**: This approach doesn't work because n8n's Function node sandbox blocks `child_process` module. Use Execute Command instead.

~~If you prefer everything in one node:~~

### ~~Step 1: Schedule Trigger (same as above)~~

### ~~Step 2: Function Node~~
**❌ This approach fails with "Cannot find module 'child_process'" error**

n8n Function nodes run in a restricted sandbox that doesn't allow executing external commands. Use the Execute Command approach above instead.

## Monitoring & Troubleshooting

### Check Execution History
1. **Workflows** → **Your Workflow** → **Executions**
2. Click on any execution to see logs
3. Green = success, Red = failed

### Common Issues
- **Permission errors**: Check file permissions on script
- **Environment variables**: Ensure n8n has access to required env vars
- **Path issues**: Use absolute paths for reliability
- **Timeout**: Increase timeout if sync takes longer than 5 minutes

### Manual Test
Before activating, test manually:
1. SSH to server: `ssh root@134.199.159.190`
2. Run script directly: `cd /root && node sync-upbank-data.js full`
3. Verify it works, then set up n8n

### Server Environment Setup
Ensure these environment variables are set on the server:
```bash
# SSH to server and add to ~/.bashrc or /etc/environment
ssh root@134.199.159.190
echo 'export UPBANK_API_TOKEN="your_token_here"' >> ~/.bashrc
echo 'export SUPABASE_SERVICE_KEY="your_key_here"' >> ~/.bashrc
echo 'export SUPABASE_URL="https://gshsshaodoyttdxippwx.supabase.co"' >> ~/.bashrc
source ~/.bashrc
```

## Workflow Settings
- **Name**: "UpBank Daily Sync"
- **Tags**: banking, automation, daily
- **Description**: "Automated daily sync of UpBank transactions to Supabase"

## Success Criteria
- ✅ Workflow executes daily at 2 AM
- ✅ Sync completes without errors
- ✅ New transactions appear in Supabase
- ✅ Execution history shows green status
- ✅ No manual intervention required

## Future Enhancements
- Add Slack notifications on success/failure
- Multiple sync frequencies (hourly incremental)
- Monitoring dashboard with sync metrics
- Error recovery workflows
