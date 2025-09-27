# MOK Music - Create New Project

Create a new project in the ESM Projects (1)database with proper structure and initial workflow setup.

## Usage
```
/mok-music-new-project [project_name] [demo_fee] [award_fee]
```

**Examples:**
- `/mok-music-new-project "Cabot's Winter Campaign" 500 4500`
- `/mok-music-new-project "Mercedes Digital" 750 5250`

## Steps

1. **Gather project details**
   If parameters not provided, prompt for:
   - Project name (brand/campaign)
   - Demo fee amount
   - Award fee amount (usage/license fee)
   - Due date (if known)
   - Agency/client information

2. **Create new project entry**
   ```javascript
   mcp__notion__API-post-page({
     parent: {page_id: "1e64a17b-b7f0-807d-b0f3-fe2cf5a6e3ac"},
     properties: {
       title: [{type: "text", text: {content: "[project_name]"}}],
       "Demo Fee": {type: "number", number: [demo_fee]},
       "Award Fee": {type: "number", number: [award_fee]},
       "Status": {type: "status", status: {name: "New Project"}},
       "Date Received": {type: "date", date: {start: [today]}},
       "APRA": {type: "select", select: {name: "Check"}}
     }
   })
   ```

3. **Set up project workflow**
   - Initialize status as "New Project"
   - Set received date to today
   - Mark APRA as "Check" for follow-up
   - Create placeholder for brief details

4. **Generate next actions**
   Provide immediate next steps:
   - Review creative brief and requirements
   - Confirm timeline and deliverables with ESM
   - Set up project folder in Dropbox/Google Drive
   - Schedule composition time in calendar

5. **Cross-system integration**
   - Create entry in Supabase financial tracking (if connected)
   - Add to n8n automation workflows (if configured)
   - Set up monitoring for status changes

## Context
This command streamlines the project initiation process, ensuring all new MOK Music projects start with consistent data structure and proper workflow setup for tracking through to completion and payment.
