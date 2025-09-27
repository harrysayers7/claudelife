Check and update APRA status for MOK Music projects: $ARGUMENTS

## Usage
- `/mok-music-apra-check` - Show all projects needing APRA action
- `/mok-music-apra-check "Project Name"` - Check specific project
- `/mok-music-apra-check update "Project Name" "Done"` - Update status

## APRA Status Options
- **Check**: Needs review for APRA requirements
- **Done**: APRA submission completed
- **Not Done**: APRA not required for this project

## Steps

1. **Query projects with APRA status**
   - Find all projects with "Check" status
   - Show projects completed but not registered
   - Highlight overdue registrations

2. **APRA requirement assessment**
   - Check if project meets APRA criteria
   - Verify completion status
   - Calculate registration deadlines

3. **Update tracking**
   - Update APRA status in database
   - Log completion dates
   - Set reminders for future submissions

4. **Generate compliance report**
   - Show APRA compliance overview
   - List pending actions
   - Track submission history

## Example Output
```
🎵 APRA COMPLIANCE CHECK

⚠️  REQUIRES ATTENTION (3 projects)
• "Agency X Track" - Completed Dec 2024, needs registration
• "Brand Y Jingle" - Status: Check (submitted 15 days ago)
• "Commercial Z" - Deadline: Jan 30, 2025

✅ COMPLETED (8 projects)
• All registered and compliant

📋 NEXT ACTIONS:
1. Register "Agency X Track" - overdue 15 days
2. Check completion status for "Brand Y Jingle"
3. Prepare "Commercial Z" for submission

Quick Update:
/mok-music-apra-check update "Agency X Track" "Done"
```

## Automation Integration
- Links to n8n workflow for APRA deadline tracking
- Automatic email reminders for pending registrations
- Integration with MOK Music calendar for deadlines
