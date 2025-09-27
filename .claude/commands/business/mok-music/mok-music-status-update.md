Update MOK Music project status in ESM Projects database: $ARGUMENTS

## Usage
- `/mok-music-status-update "Project Name" "Status"`
- Valid statuses: "New Project", "Current", "Submitted", "PO Received", "Awaiting PO", "Invoiced", "Awarded", "Complete"

## Steps

1. **Find project by name**
   - Search ESM Projects database for matching project name
   - Handle partial matches and suggest alternatives

2. **Update project status**
   - Validate status value against allowed options
   - Update Status property in Notion
   - Log timestamp of status change

3. **Trigger workflow actions**
   - If "Submitted": Set Submitted On date
   - If "PO Received": Request PO number and file
   - If "Invoiced": Set Invoice Sent date
   - If "Complete": Update APRA status if needed

4. **Generate status report**
   - Show current project overview
   - Display recent status history
   - Highlight any required actions

## Example
```
✅ Updated "Agency X Track": New Project → Submitted
📅 Submitted On: 2025-01-15
⏳ Next: Await client feedback and PO

Project Overview:
• Demo Fee: $750 (pending)
• Award Fee: $5,250 (if awarded)
• APRA: Check required
```
