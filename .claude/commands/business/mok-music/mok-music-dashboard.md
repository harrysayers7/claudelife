Display MOK Music business dashboard with current projects and financial overview

## Usage
- `/mok-music-dashboard` - Show full dashboard
- `/mok-music-dashboard current` - Show only current projects
- `/mok-music-dashboard financial` - Show financial summary only

## Dashboard Sections

1. **Active Projects Summary**
   - Current status breakdown
   - Projects by stage (New, Current, Submitted, etc.)
   - Urgent deadlines and actions required

2. **Financial Overview**
   - Total outstanding demo fees
   - Total potential award fees
   - Monthly/quarterly revenue projections
   - Recent payments and invoices

3. **APRA Status Tracking**
   - Projects requiring APRA submission
   - Completed vs pending registrations
   - Deadline alerts

4. **Recent Activity**
   - Latest project updates
   - Status changes in last 7 days
   - Upcoming deadlines

## Steps

1. **Query ESM Projects database**
   - Get all projects with full properties
   - Sort by status and date received
   - Calculate financial totals

2. **Generate visual summary**
   - Create status distribution chart
   - Show financial breakdown
   - Highlight action items

3. **Provide actionable insights**
   - Projects needing attention
   - Revenue opportunities
   - Process bottlenecks

## Example Output
```
🎵 MOK MUSIC DASHBOARD - January 2025

📊 ACTIVE PROJECTS (12 total)
• New Project: 3
• Current: 4
• Submitted: 2
• Awaiting PO: 2
• Complete: 1

💰 FINANCIAL SUMMARY
• Outstanding Demo Fees: $2,250
• Potential Award Fees: $21,000
• This Month Revenue: $7,500
• Pipeline Value: $45,000

⚠️  ACTION REQUIRED
• 2 projects need APRA submission
• 1 invoice overdue (7 days)
• 3 projects approaching deadline

🔗 Quick Actions:
- /mok-music-new-project
- /mok-music-status-update
- /mok-music-apra-check
```
