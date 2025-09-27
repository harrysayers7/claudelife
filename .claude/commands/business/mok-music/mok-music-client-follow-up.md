# MOK Music - Client Follow-up Management

Generate follow-up communications and track outstanding items with ESM and clients.

## Usage
```
/mok-music-client-follow-up [type] [project_name]
```

**Follow-up types:**
- `overdue` - Projects over 30 days in "Invoiced" status
- `po-missing` - Projects needing purchase orders
- `apra` - Projects with incomplete APRA registrations
- `status` - General project status check
- `all` - Comprehensive follow-up report

## Steps

1. **Identify follow-up targets**
   ```javascript
   // For overdue payments
   mcp__notion__API-post-database-query({
     database_id: "1e64a17b-b7f0-807d-b0f3-fe2cf5a6e3ac",
     filter: {
       and: [
         {property: "Status", status: {equals: "Invoiced"}},
         {property: "Days", formula: {number: {greater_than: 30}}}
       ]
     }
   })
   ```

2. **Generate appropriate communication**
   Based on follow-up type:

   **Overdue Payment:**
   ```
   Subject: Follow-up: Outstanding Invoice - [Project Name]

   Hi Kate,

   Hope you're well! Just following up on the invoice for [Project Name]
   (submitted [date], currently [X] days outstanding).

   Could you please check the status with accounts? Let me know if you
   need me to resend any documentation.

   Cheers,
   Harry
   ```

   **Missing PO:**
   ```
   Subject: PO Required - [Project Name]

   Hi Kate,

   [Project Name] is ready for invoicing but I don't have a PO number yet.
   Could you please send through when convenient?

   Project details:
   • Demo Fee: $[amount]
   • Award Fee: $[amount]
   • Completion: [date]

   Thanks!
   Harry
   ```

3. **Update tracking**
   ```javascript
   mcp__notion__API-patch-page({
     page_id: "[project_id]",
     properties: {
       "Text": {
         type: "rich_text",
         rich_text: [{
           type: "text",
           text: {content: "Follow-up sent [date]: [summary]"}
         }]
       }
   })
   ```

4. **Create action items**
   - Schedule follow-up reminder (7-14 days)
   - Update project notes with communication history
   - Escalate if necessary (Glenn for creative, Kate for business)

5. **Integration with email**
   If Gmail MCP is available:
   ```javascript
   mcp__gmail__draft_email({
     to: ["kate@electricsheepmusic.com"],
     subject: "[Generated subject]",
     body: "[Generated message]"
   })
   ```

6. **Generate summary report**
   ```
   📞 MOK MUSIC FOLLOW-UP SUMMARY - [Date]

   OVERDUE ITEMS:
   • [Project] - [Days] days, $[Amount]

   MISSING POs:
   • [Project] - Ready for invoicing

   APRA PENDING:
   • [Project] - Registration required

   ACTIONS TAKEN:
   • [Summary of communications]

   NEXT STEPS:
   • [Recommended actions]
   ```

## Context
This command helps Harry maintain professional client relationships by systematically tracking and following up on outstanding items, ensuring cash flow and project completion while maintaining the collaborative relationship with Electric Sheep Music.

IMPORTANT: Use Serena to search through the codebase. If you get any errors using Serena, retry with different
Serena tools.
